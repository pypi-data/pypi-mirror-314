from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv

@dataclass
class Config:
    """Configuration settings for the README generator."""
    gemini_api_key: str
    model_name: str = "gemini-pro"
    default_output: str = "repopack-output.txt"
    default_readme: str = "README.md"
    generation_temperature: float = 0.7
    max_output_tokens: int = 8192

    @classmethod
    def from_env(cls) -> "Config":
        """Create a Config instance from environment variables."""
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        return cls(
            gemini_api_key=api_key,
            model_name=os.getenv("GEMINI_MODEL", cls.model_name),
            default_output=os.getenv("DEFAULT_OUTPUT", cls.default_output),
            default_readme=os.getenv("DEFAULT_README", cls.default_readme),
            generation_temperature=float(os.getenv("GENERATION_TEMPERATURE", cls.generation_temperature)),
            max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", cls.max_output_tokens))
        )
