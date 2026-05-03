# STT fallback logic - intelligently routes between different STT providers

import os
from typing import Optional, Tuple
from utils.logger import setup_logger
from config.settings import STT_FALLBACK_ORDER

logger = setup_logger(__name__)


class STTClient:
    """Unified STT client with automatic fallback."""
    
    def __init__(self):
        """Initialize STT client with all available providers."""
        self.deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        self.assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.azure_speech_key_1 = os.getenv("AZURE_SPEECH_KEY_1")
        self.azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
    
    def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "en",
    ) -> Tuple[Optional[str], str]:
        """
        Transcribe audio to text.
        Automatically falls back if primary fails.
        
        Args:
            audio_bytes: Audio data in bytes
            language: Language code (en, ur for Urdu, etc.)
        
        Returns:
            Tuple of (transcription, provider) or (None, 'error') if all fail
        """
        for provider in STT_FALLBACK_ORDER:
            try:
                logger.info(f"Attempting STT via {provider}...")
                
                if provider == "deepgram":
                    result = self._use_deepgram(audio_bytes, language)
                    if result:
                        return result, "deepgram"
                
                elif provider == "assemblyai":
                    result = self._use_assemblyai(audio_bytes, language)
                    if result:
                        return result, "assemblyai"
                
                elif provider == "azure":
                    result = self._use_azure_stt(audio_bytes, language)
                    if result:
                        return result, "azure"
            
            except Exception as e:
                logger.warning(f"{provider} STT failed: {str(e)}. Trying next provider...")
                continue
        
        logger.error("All STT providers failed!")
        return None, "error"
    
    def _use_deepgram(self, audio_bytes: bytes, language: str = "en") -> Optional[str]:
        """Use Deepgram API."""
        if not self.deepgram_key:
            raise ValueError("DEEPGRAM_API_KEY not found")
        
        try:
            import httpx
            
            headers = {"Authorization": f"Token {self.deepgram_key}"}
            
            # Map language codes
            lang_map = {
                "en": "en",
                "ur": "hi",  # Hindi is closest to Urdu in most STT services
                "pashto": "ps",
            }
            language = lang_map.get(language, "en")
            
            params = {
                "model": "nova-2",
                "language": language,
                "punctuate": True,
            }
            
            response = httpx.post(
                "https://api.deepgram.com/v1/listen",
                content=audio_bytes,
                headers=headers,
                params=params,
                timeout=60,
            )
            response.raise_for_status()
            
            result = response.json()
            transcript = result.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
            
            logger.info("✅ Deepgram STT succeeded")
            return transcript
        except Exception as e:
            logger.warning(f"Deepgram error: {e}")
            raise
    
    def _use_assemblyai(self, audio_bytes: bytes, language: str = "en") -> Optional[str]:
        """Use AssemblyAI API."""
        if not self.assemblyai_key:
            raise ValueError("ASSEMBLYAI_API_KEY not found")
        
        try:
            import httpx
            
            headers = {"Authorization": self.assemblyai_key}
            
            # Upload audio
            upload_response = httpx.post(
                "https://api.assemblyai.com/v1/upload",
                content=audio_bytes,
                headers=headers,
                timeout=60,
            )
            upload_response.raise_for_status()
            upload_url = upload_response.json()["upload_url"]
            
            # Transcribe
            language_map = {
                "en": "en",
                "ur": "ur",  # AssemblyAI supports Urdu!
                "pashto": "ps",
            }
            
            transcribe_response = httpx.post(
                "https://api.assemblyai.com/v1/transcript",
                json={
                    "audio_url": upload_url,
                    "language_code": language_map.get(language, "en"),
                },
                headers=headers,
                timeout=60,
            )
            transcribe_response.raise_for_status()
            
            transcript_id = transcribe_response.json()["id"]
            
            # Poll for result
            import time
            for _ in range(30):  # Wait up to 5 minutes
                result_response = httpx.get(
                    f"https://api.assemblyai.com/v1/transcript/{transcript_id}",
                    headers=headers,
                    timeout=30,
                )
                result_response.raise_for_status()
                result = result_response.json()
                
                if result["status"] == "completed":
                    transcript = result.get("text", "")
                    logger.info("✅ AssemblyAI STT succeeded")
                    return transcript
                elif result["status"] == "error":
                    raise Exception(f"AssemblyAI error: {result.get('error')}")
                
                time.sleep(10)
            
            raise Exception("AssemblyAI transcription timeout")
        except Exception as e:
            logger.warning(f"AssemblyAI error: {e}")
            raise
    
    def _use_azure_stt(self, audio_bytes: bytes, language: str = "en") -> Optional[str]:
        """Use Azure Speech Services."""
        if not self.azure_speech_key_1 or not self.azure_speech_region:
            raise ValueError("AZURE_SPEECH_KEY_1 and AZURE_SPEECH_REGION not found")
        
        try:
            import azure.cognitiveservices.speech as speechsdk
            import io
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key_1,
                region=self.azure_speech_region,
            )
            
            # Set language
            lang_map = {
                "en": "en-US",
                "ur": "ur-PK",  # Azure supports Urdu (Pakistan)
                "pashto": "ps-AF",
            }
            speech_config.speech_recognition_language = lang_map.get(language, "en-US")
            
            # Create stream from audio bytes
            stream = speechsdk.AudioDataStream(
                speechsdk.audio.AudioData(audio_bytes)
            )
            audio_config = speechsdk.audio.AudioConfig(stream=stream)
            
            # Recognize
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config,
            )
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcript = result.text
                logger.info("✅ Azure STT succeeded")
                return transcript
            else:
                raise Exception(f"Azure STT failed: {result.reason}")
        except Exception as e:
            logger.warning(f"Azure STT error: {e}")
            raise


# Global instance
_stt_client = None


def get_stt_client() -> STTClient:
    """Get or create the STT client singleton."""
    global _stt_client
    if _stt_client is None:
        _stt_client = STTClient()
    return _stt_client


def transcribe_audio(audio_bytes: bytes, language: str = "en") -> Tuple[Optional[str], str]:
    """Convenience function to transcribe audio."""
    client = get_stt_client()
    return client.transcribe(audio_bytes, language)
