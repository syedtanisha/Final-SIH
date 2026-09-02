from pydantic import BaseModel, Field
from typing import Optional, List
from .chat import ChatMessageOut

class TranscriptionResponse(BaseModel):
    text: str = Field(..., description="Transcribed text from input spoken audio")
    language: str = Field("en", description="Language code detected or requested (e.g. 'en', 'hi')")
    confidence: float = Field(0.95, description="Transcription confidence score (0.0 - 1.0)")
    duration_seconds: float = Field(0.0, description="Audio duration in seconds")
    stt_provider: str = Field(..., description="Provider used for Speech-to-Text (Groq, OpenAI, Gemini, Fallback)")

class TTSSynthesisRequest(BaseModel):
    text: str = Field(..., description="Text content to synthesize into spoken audio")
    language: Optional[str] = Field("en", description="Target language ('en', 'hi')")
    voice_gender: Optional[str] = Field("neutral", description="Voice characteristics ('male', 'female', 'neutral')")
    speed: Optional[float] = Field(1.0, description="Playback speed multiplier (0.5 - 2.0)")

class TTSSynthesisResponse(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio string")
    audio_format: str = Field("mp3", description="Audio format ('mp3', 'wav', 'ogg')")
    sample_rate: int = Field(24000, description="Audio sample rate in Hz")
    tts_provider: str = Field(..., description="Provider used for Text-to-Speech (gTTS, OpenAI, Fallback)")

class VoiceChatSubmitReq(BaseModel):
    session_id: str = Field(..., description="Chat session ID to submit voice message into")
    language: Optional[str] = Field("en", description="Target language ('en', 'hi')")

class VoiceChatResponse(BaseModel):
    transcription: TranscriptionResponse
    chat_message: ChatMessageOut
    audio_base64: Optional[str] = None
    audio_format: Optional[str] = "mp3"
