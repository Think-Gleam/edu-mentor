# LLM fallback logic - intelligently routes between different LLM providers

import os
import time
from typing import Optional, Dict, Any, List
from utils.logger import setup_logger
from config.settings import LLM_FALLBACK_ORDER, MODEL_CONFIGS, LLM_TIMEOUT_SECONDS

logger = setup_logger(__name__)


class LLMClient:
    """Unified LLM client with automatic fallback."""
    
    def __init__(self):
        """Initialize LLM client with all available providers."""
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.huggingface_token = os.getenv("HUGGINGFACE_TOKEN")
        
        self.retry_count = 0
        self.max_retries = 3
        self.current_provider = None
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """
        Generate text using the best available LLM provider.
        Automatically falls back if primary fails.
        
        Args:
            prompt: The user/task prompt
            system_prompt: Optional system prompt
            temperature: Creativity level
            max_tokens: Max tokens to generate
        
        Returns:
            Dict with 'response', 'provider', 'tokens_used'
        """
        for provider in LLM_FALLBACK_ORDER:
            try:
                logger.info(f"Attempting {provider}...")
                
                if provider == "gemini":
                    return self._use_gemini(prompt, system_prompt, temperature, max_tokens)
                
                elif provider == "groq":
                    return self._use_groq(prompt, system_prompt, temperature, max_tokens)
                
                elif provider == "openrouter":
                    return self._use_openrouter(prompt, system_prompt, temperature, max_tokens)
                
                elif provider == "huggingface":
                    return self._use_huggingface(prompt, system_prompt, temperature, max_tokens)
            
            except Exception as e:
                logger.warning(f"{provider} failed: {str(e)}. Trying next provider...")
                continue
        
        # If all providers fail
        logger.error("All LLM providers failed!")
        return {
            "response": "I'm unable to process your request right now. Please try again later.",
            "provider": "error",
            "tokens_used": 0,
            "error": True,
        }
    
    def _use_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        """Use Google Gemini."""
        if not self.gemini_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            
            logger.info("✅ Gemini succeeded")
            return {
                "response": response.text,
                "provider": "gemini",
                "tokens_used": 0,  # Gemini doesn't expose token count in free tier
            }
        except Exception as e:
            logger.warning(f"Gemini error: {e}")
            raise
    
    def _use_groq(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        """Use Groq API (fast inference)."""
        if not self.groq_key:
            raise ValueError("GROQ_API_KEY not found")
        
        try:
            from groq import Groq
            
            client = Groq(api_key=self.groq_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=LLM_TIMEOUT_SECONDS,
            )
            
            logger.info("✅ Groq succeeded")
            return {
                "response": response.choices[0].message.content,
                "provider": "groq",
                "tokens_used": response.usage.total_tokens,
            }
        except Exception as e:
            logger.warning(f"Groq error: {e}")
            raise
    
    def _use_openrouter(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        """Use OpenRouter API (supports many models)."""
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY not found")
        
        try:
            import httpx
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "HTTP-Referer": "https://edumentor.app",
                "X-Title": "EduMentor",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": "meta-llama/llama-2-70b-chat",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            response = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=LLM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info("✅ OpenRouter succeeded")
            return {
                "response": result["choices"][0]["message"]["content"],
                "provider": "openrouter",
                "tokens_used": result.get("usage", {}).get("total_tokens", 0),
            }
        except Exception as e:
            logger.warning(f"OpenRouter error: {e}")
            raise
    
    def _use_huggingface(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> Dict[str, Any]:
        """Use HuggingFace Inference API."""
        if not self.huggingface_token:
            raise ValueError("HUGGINGFACE_TOKEN not found")
        
        try:
            import httpx
            
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": max_tokens,
                },
            }
            
            response = httpx.post(
                "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf",
                json=payload,
                headers=headers,
                timeout=LLM_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info("✅ HuggingFace succeeded")
            return {
                "response": result[0]["generated_text"],
                "provider": "huggingface",
                "tokens_used": 0,
            }
        except Exception as e:
            logger.warning(f"HuggingFace error: {e}")
            raise


# Global instance
_llm_client = None


def get_llm_client() -> LLMClient:
    """Get or create the LLM client singleton."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def generate_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    """Convenience function to generate text and return just the response."""
    client = get_llm_client()
    result = client.generate(prompt, system_prompt, temperature, max_tokens)
    return result.get("response", "Error generating response")
