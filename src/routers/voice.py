"""
Router para procesamiento de voz
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import logging

from src.services.gcp_service import get_gcp_service

logger = logging.getLogger(__name__)
router = APIRouter()


class VoiceQuery(BaseModel):
    """Modelo para consulta de voz"""
    query: str
    language_code: str = "es-ES"


class AudioTranscriptionResponse(BaseModel):
    """Respuesta de transcripción de audio"""
    transcript: str
    confidence: float = 0.95


@router.post("/transcribe", response_model=AudioTranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribir archivo de audio a texto
    
    - Soporta formatos: WAV, OGG, FLAC, MP3
    """
    try:
        # Leer contenido del archivo
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        
        # Transcribir usando GCP
        gcp_service = get_gcp_service()
        transcript = gcp_service.transcribe_audio(content)
        
        return AudioTranscriptionResponse(
            transcript=transcript,
            confidence=0.95,
        )
    except Exception as e:
        logger.error(f"Error en transcripción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize")
async def synthesize_speech(text: str, language_code: str = "es-ES"):
    """
    Sintetizar texto a voz
    
    Retorna audio MP3
    """
    try:
        if not text or len(text) == 0:
            raise HTTPException(status_code=400, detail="Texto vacío")
        
        if len(text) > 5000:
            raise HTTPException(status_code=400, detail="Texto muy largo (máximo 5000 caracteres)")
        
        # Sintetizar usando GCP
        gcp_service = get_gcp_service()
        audio_content = gcp_service.synthesize_speech(text, language_code)
        
        return {
            "audio_base64": __import__("base64").b64encode(audio_content).decode("utf-8"),
            "format": "mp3",
            "text": text,
        }
    except Exception as e:
        logger.error(f"Error en síntesis de voz: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def voice_query(query: VoiceQuery):
    """
    Realizar consulta de voz y obtener respuesta de IA
    """
    try:
        gcp_service = get_gcp_service()
        
        # Generar recomendación IA
        response = gcp_service.get_ai_recommendation(query.query)
        
        # Sintetizar respuesta a voz
        audio_content = gcp_service.synthesize_speech(response, query.language_code)
        
        return {
            "query": query.query,
            "response": response,
            "audio_base64": __import__("base64").b64encode(audio_content).decode("utf-8"),
            "format": "mp3",
        }
    except Exception as e:
        logger.error(f"Error en consulta de voz: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
