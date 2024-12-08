import asyncio
from typing import List, Dict, Set, Optional, TYPE_CHECKING
import time
from threading import Timer
from llama_cpp import Llama
from llama_cpp.llama_chat_format import (
    MoondreamChatHandler,
    MiniCPMv26ChatHandler,
    Llava15ChatHandler,
    Llava16ChatHandler,
)

from llama_assistant import config
from llama_assistant.agent import RAGAgent

if TYPE_CHECKING:
    from llama_assistant.processing_thread import ProcessingThread


class Model:
    def __init__(
        self,
        model_type: str,
        model_id: str,
        model_name: str,
        model_path: Optional[str] = None,
        repo_id: Optional[str] = None,
        filename: Optional[str] = None,
    ):
        self.model_type = model_type
        self.model_id = model_id
        self.model_name = model_name
        self.model_path = model_path
        self.repo_id = repo_id
        self.filename = filename

    def is_online(self) -> bool:
        return self.repo_id is not None and self.filename is not None


class ModelHandler:
    def __init__(self):
        self.supported_models: List[Model] = []
        self.loaded_agent: Optional[Dict] = None
        self.current_model_id: Optional[str] = None
        self.unload_timer: Optional[Timer] = None

    def refresh_supported_models(self):
        self.supported_models = [Model(**model_data) for model_data in config.models]

    def list_supported_models(self) -> List[Model]:
        return self.supported_models

    def add_supported_model(self, model: Model):
        self.supported_models.append(model)

    def remove_supported_model(self, model_id: str):
        self.supported_models = [m for m in self.supported_models if m.model_id != model_id]
        if self.current_model_id == model_id:
            self.unload_agent()

    def load_agent(
        self,
        model_id: str,
        generation_setting,
        rag_setting: Dict,
        processing_thread: "ProcessingThread",
    ) -> Optional[Dict]:
        self.refresh_supported_models()
        if self.current_model_id == model_id and self.loaded_agent:
            if generation_setting["context_len"] == self.loaded_agent["model"].context_params.n_ctx:
                self.loaded_agent["agent"].update_rag_setting(rag_setting)
                self.loaded_agent["agent"].update_generation_setting(generation_setting)
                return self.loaded_agent

        processing_thread.set_preloading(True, "Loading model ....")

        # if no model is loaded or different model is loaded, or context_len is different, reinitialize the agent
        self.unload_agent()  # Unload the current model if any

        model = next((m for m in self.supported_models if m.model_id == model_id), None)
        if not model:
            print(f"Model with ID {model_id} not found.")
            return None

        if model.is_online():
            if model.model_type == "text":
                print("load online model")
                loaded_model = Llama.from_pretrained(
                    repo_id=model.repo_id,
                    filename=model.filename,
                    n_ctx=generation_setting["context_len"],
                )
            elif model.model_type == "image":
                if "moondream2" in model.model_id:
                    chat_handler = MoondreamChatHandler.from_pretrained(
                        repo_id="vikhyatk/moondream2",
                        filename="*mmproj*",
                    )
                    loaded_model = Llama.from_pretrained(
                        repo_id=model.repo_id,
                        filename=model.filename,
                        chat_handler=chat_handler,
                        n_ctx=generation_setting["context_len"],
                    )
                elif "MiniCPM" in model.model_id:
                    chat_handler = MiniCPMv26ChatHandler.from_pretrained(
                        repo_id=model.repo_id,
                        filename="*mmproj*",
                    )
                    loaded_model = Llama.from_pretrained(
                        repo_id=model.repo_id,
                        filename=model.filename,
                        chat_handler=chat_handler,
                        n_ctx=generation_setting["context_len"],
                    )
                elif "llava-v1.5" in model.model_id:
                    chat_handler = Llava15ChatHandler.from_pretrained(
                        repo_id=model.repo_id,
                        filename="*mmproj*",
                    )
                    loaded_model = Llama.from_pretrained(
                        repo_id=model.repo_id,
                        filename=model.filename,
                        chat_handler=chat_handler,
                        n_ctx=generation_setting["context_len"],
                    )
                elif "llava-v1.6" in model.model_id:
                    chat_handler = Llava16ChatHandler.from_pretrained(
                        repo_id=model.repo_id,
                        filename="*mmproj*",
                    )
                    loaded_model = Llama.from_pretrained(
                        repo_id=model.repo_id,
                        filename=model.filename,
                        chat_handler=chat_handler,
                        n_ctx=generation_setting["context_len"],
                    )
            else:
                print(f"Unsupported model type: {model.model_type}")
                return None
        else:
            # Load model from local path
            print("load local model")
            loaded_model = Llama(model_path=model.model_path)

        print("Initializing agent ...")

        agent = RAGAgent(
            generation_setting,
            rag_setting,
            llm=loaded_model,
        )

        self.loaded_agent = {
            "model": loaded_model,
            "agent": agent,
            "generation_setting": generation_setting,
            "rag_setting": rag_setting,
            "last_used": time.time(),
        }
        self.current_model_id = model_id
        self._schedule_unload()

        return self.loaded_agent

    def unload_agent(self):
        if self.loaded_agent:
            print(f"Unloading model: {self.current_model_id}")
            self.loaded_agent = None
            self.current_model_id = None
        if self.unload_timer:
            self.unload_timer.cancel()
            self.unload_timer = None

    async def run_agent(
        self, agent: RAGAgent, message: str, lookup_files: Set, image: str, stream: bool
    ):
        response = await agent.run(
            query_str=message, lookup_files=lookup_files, image=image, streaming=stream
        )
        return response

    def chat_completion(
        self,
        model_id: str,
        generation_setting: Dict,
        rag_setting: Dict,
        message: str,
        image: Optional[str] = None,
        lookup_files: Optional[Set[str]] = None,
        stream: bool = False,
        processing_thread: "ProcessingThread" = None,
    ) -> str:
        agent_data = self.load_agent(model_id, generation_setting, rag_setting, processing_thread)
        agent = agent_data.get("agent")
        if not agent_data:
            return "Failed to load model"

        agent_data["last_used"] = time.time()
        self._schedule_unload()

        processing_thread.set_preloading(True, "Thinking ....")
        try:
            loop = asyncio.get_running_loop()
            response = loop.run_until_complete(
                self.run_agent(agent, message, lookup_files, image, stream)
            )
        except RuntimeError:  # no running event loop
            response = asyncio.run(self.run_agent(agent, message, lookup_files, image, stream))

        processing_thread.set_preloading(False, "Thinking done.")

        return response

    def update_chat_history(self, message: str, role: str):
        agent = self.loaded_agent.get("agent")
        if agent:
            agent.chat_history.add_message({"role": role, "content": message})

    def clear_chat_history(self):
        agent = self.loaded_agent.get("agent")
        if agent:
            agent.chat_history.clear()

    def _schedule_unload(self):
        if self.unload_timer:
            self.unload_timer.cancel()

        self.unload_timer = Timer(3600, self.unload_agent)
        self.unload_timer.start()


# Example usage
handler = ModelHandler()
