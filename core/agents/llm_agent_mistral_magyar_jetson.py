from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from core.agents.llm_agent import LLMAgent

class LLMAgentMistralMagyarJetson(LLMAgent):
    """Agent for ikerion/mistral-magyar-jetson-ready."""
    def __init__(self):
        super().__init__()
        self.model_name = "ikerion/mistral-magyar-jetson-ready"
        self.hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_HUB_TOKEN environment variable is not set. Please set it in your .env file or environment.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            use_auth_token=self.hf_token
        )
        self.model.bfloat16()
        self.temperature = 1.0

    def ask(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=True,
                temperature=self.temperature
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
