from typing import Any, Dict, List, Optional
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

from core.agents.llm_agent import LLMAgent

class LLMAgentMistral(LLMAgent):
    """Mistral test agent for simulating decision making."""

    def __init__(self):
        """Initialize the Mistral agent."""
        super().__init__()
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.3"
        self.hf_token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_HUB_TOKEN environment variable is not set. Please set it in your .env file or environment.")

        # Load tokenizer and model with token
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_auth_token=self.hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,       # use float16 if on GPU
            device_map="auto",                # automatically places model on GPU/CPU
            use_auth_token=self.hf_token
        )
        self.model.bfloat16()
        self.temperature = 1.0
    
    def ask(self, prompt: str) -> str:
        """Send prompt to Mistral model and return the generated output as a string."""
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
