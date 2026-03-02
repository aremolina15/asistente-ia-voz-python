"""
Router para procesamiento de voz
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
import logging
from datetime import datetime

from src.services.gcp_service import get_gcp_service
from src.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
_rag_pipeline = None


def _get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is not None:
        return _rag_pipeline

    try:
        from src.rag import RagPipeline

        _rag_pipeline = RagPipeline()
        logger.info("✅ RAG pipeline inicializado")
        return _rag_pipeline
    except Exception as rag_error:
        logger.warning(f"⚠️ No se pudo inicializar RAG, usando fallback base: {str(rag_error)}")
        return None


class VoiceQuery(BaseModel):
    """Modelo para consulta de voz"""
    query: str
    language_code: str = settings.voice_default_language_code


class SynthesizeRequest(BaseModel):
    """Solicitud para síntesis de voz"""
    text: str
    language_code: str = settings.voice_default_language_code


class AudioTranscriptionResponse(BaseModel):
    """Respuesta de transcripción de audio"""
    transcript: str
    confidence: float = 0.95


@router.post("/transcribe", response_model=AudioTranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...), language_code: str = Form(settings.voice_default_language_code)):
    """
    Transcribir archivo de audio a texto
    
    - Soporta formatos: WAV, OGG, WEBM, FLAC, MP3
    """
    try:
        # Leer contenido del archivo
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="Archivo vacío")
        
        gcp_service = get_gcp_service()
        
        # Guardar audio de entrada en Storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_path = f"audios/input/{timestamp}_input.wav"
        gcp_service.upload_to_storage(settings.storage_bucket, input_path, content)
        logger.info(f"📦 Audio guardado: {input_path}")
        
        # Transcribir usando GCP
        transcription = gcp_service.transcribe_audio(content, language_code=language_code)
        transcript = transcription.get("transcript", "")
        confidence = transcription.get("confidence", 0.0)

        if not transcript:
            raise HTTPException(status_code=422, detail="No se pudo extraer texto del audio. Intenta hablar más claro o reducir ruido.")
        
        return AudioTranscriptionResponse(
            transcript=transcript,
            confidence=confidence,
        )
    except Exception as e:
        logger.error(f"Error en transcripción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synthesize")
async def synthesize_speech(request: SynthesizeRequest):
    """
    Sintetizar texto a voz
    
    Retorna audio MP3
    """
    try:
        if not request.text or len(request.text) == 0:
            raise HTTPException(status_code=400, detail="Texto vacío")
        
        if len(request.text) > 5000:
            raise HTTPException(status_code=400, detail="Texto muy largo (máximo 5000 caracteres)")
        
        gcp_service = get_gcp_service()
        
        # Sintetizar usando GCP
        audio_content = gcp_service.synthesize_speech(request.text, request.language_code)
        
        # Guardar audio sintetizado en Storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"audios/synthesized/{timestamp}_output.mp3"
        gcp_service.upload_to_storage(settings.storage_bucket, output_path, audio_content)
        logger.info(f"📦 Audio sintetizado guardado: {output_path}")
        
        return {
            "audio_base64": __import__("base64").b64encode(audio_content).decode("utf-8"),
            "format": "mp3",
            "text": request.text,
            "storage_path": f"gs://{settings.storage_bucket}/{output_path}",
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        sources = []
        response = ""

        if settings.rag_enabled:
            rag_pipeline = _get_rag_pipeline()
            if rag_pipeline is not None:
                rag_result = rag_pipeline.answer(query.query)
                response = rag_result.get("response", "")
                sources = rag_result.get("sources", [])

        if not response:
            response = gcp_service.get_ai_recommendation(query.query)
        
        # Sintetizar respuesta a voz
        audio_content = gcp_service.synthesize_speech(response, query.language_code)
        
        # Guardar respuesta de audio en Storage
        response_path = f"audios/responses/{timestamp}_response.mp3"
        gcp_service.upload_to_storage(settings.storage_bucket, response_path, audio_content)
        logger.info(f"📦 Respuesta guardada: {response_path}")
        
        return {
            "query": query.query,
            "response": response,
            "sources": sources,
            "rag_enabled": settings.rag_enabled,
            "audio_base64": __import__("base64").b64encode(audio_content).decode("utf-8"),
            "format": "mp3",
            "storage_path": f"gs://{settings.storage_bucket}/{response_path}",
        }
    except Exception as e:
        logger.error(f"Error en consulta de voz: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
