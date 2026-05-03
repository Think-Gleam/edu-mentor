# TTS fallback logic - intelligently routes between different TTS providers

import os
import io
from typing import Optional, Tuple
from utils.logger import setup_logger
from config.settings import TTS_FALLBACK_ORDER, ELEVENLABS_VOICE_ID

logger = setup_logger(__name__)


class TTSClient:
    """Unified TTS client with automatic fallback."""
    
    def __init__(self):
        """Initialize TTS client with all available providers."""
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.azure_speech_key_1 = os.getenv("AZURE_SPEECH_KEY_1")
        self.azure_speech_key_2 = os.getenv("AZURE_SPEECH_KEY_2")
        self.azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
    
    def synthesize(
        self,
        text: str,
        language: str = "en",
        voice_name: Optional[str] = None,
    ) -> Tuple[Optional[bytes], str]:
        """
        Synthesize speech from text.
        Automatically falls back if primary fails.
        
        Args:
            text: Text to convert to speech
            language: Language code (en, ur for Urdu, etc.)
            voice_name: Optional specific voice name
        
        Returns:
            Tuple of (audio_bytes, provider) or (None, 'error') if all fail
        """
        for provider in TTS_FALLBACK_ORDER:
            try:
                logger.info(f"Attempting TTS via {provider}...")
                
                if provider == "elevenlabs":
                    result = self._use_elevenlabs(text, voice_name)
                    if result:
                        return result, "elevenlabs"
                
                elif provider == "azure":
                    result = self._use_azure_tts(text, language, voice_name)
                    if result:
                        return result, "azure"
                
                elif provider == "browser":
                    logger.info("Falling back to browser-based TTS (client-side)")
                    return None, "browser"
            
            except Exception as e:
                logger.warning(f"{provider} TTS failed: {str(e)}. Trying next provider...")
                continue
        
        logger.error("All TTS providers failed!")
        return None, "error"
    
    def _use_elevenlabs(self, text: str, voice_id: Optional[str] = None) -> Optional[bytes]:
        """Use ElevenLabs API."""
        if not self.elevenlabs_key:
            raise ValueError("ELEVENLABS_API_KEY not found")
        
        try:
            import httpx
            
            voice_id = voice_id or ELEVENLABS_VOICE_ID
            
            headers = {"xi-api-key": self.elevenlabs_key}
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                },
            }
            
            response = httpx.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json=data,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            
            logger.info("✅ ElevenLabs TTS succeeded")
            return response.content
        except Exception as e:
            logger.warning(f"ElevenLabs error: {e}")
            raise
    
    def _use_azure_tts(self, text: str, language: str = "en", voice_name: Optional[str] = None) -> Optional[bytes]:
        """Use Azure Speech Services."""
        if not self.azure_speech_key_1 or not self.azure_speech_region:
            raise ValueError("AZURE_SPEECH_KEY_1 and AZURE_SPEECH_REGION not found")
        
        try:
            import azure.cognitiveservices.speech as speechsdk
            
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key_1,
                region=self.azure_speech_region,
            )
            
            # Set voice based on language
            if language == "ur":
                speech_config.speech_synthesis_voice_name = voice_name or "ur-PK-UzmaNeural"
            else:
                speech_config.speech_synthesis_voice_name = voice_name or "en-US-AriaNeural"
            
            # Synthesize to memory
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config,
            )
            
            # Use pull audio stream to get bytes
            stream = speechsdk.AudioDataStream(
                speech_synthesizer.speak_text_async(text).get()
            )
            
            # Read to bytes
            audio_bytes = io.BytesIO()
            stream.save_to_stream(audio_bytes)
            audio_bytes.seek(0)
            
            logger.info("✅ Azure TTS succeeded")
            return audio_bytes.getvalue()
        except Exception as e:
            logger.warning(f"Azure TTS error: {e}")
            raise
    
    def get_browser_tts_html(self, text: str, language: str = "en") -> str:
        """
        Generate HTML/JavaScript for browser-based TTS fallback.
        Uses Web Speech API (works in most browsers).
        """
        safe_text = text.replace('"', '\\"').replace("\n", " ")
        
        html = f"""
        <script>
            const utterance = new SpeechSynthesisUtterance('{safe_text}');
            utterance.lang = '{language}';
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            window.speechSynthesis.speak(utterance);
        </script>
        """
        return html


# Global instance
_tts_client = None


def get_tts_client() -> TTSClient:
    """Get or create the TTS client singleton."""
    global _tts_client
    if _tts_client is None:
        _tts_client = TTSClient()
    return _tts_client


def synthesize_speech(
    text: str,
    language: str = "en",
    voice_name: Optional[str] = None,
) -> Tuple[Optional[bytes], str]:
    """Convenience function to synthesize speech."""
    client = get_tts_client()
    return client.synthesize(text, language, voice_name)
