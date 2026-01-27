"""
Servicios para integración con Google Cloud Platform
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from google.cloud import storage, speech_v1, texttospeech_v1
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from io import BytesIO

from src.config import settings

logger = logging.getLogger(__name__)


class GCPService:
    """Servicio para operaciones con GCP"""

    def __init__(self):
        """Inicializar servicio GCP"""
        self.project_id = settings.gcp_project_id
        self.region = settings.gcp_region
        
        # Inicializar VertexAI
        vertexai.init(project=self.project_id, location=self.region)
        
        # Inicializar clientes
        self.storage_client = storage.Client()
        self.speech_client = speech_v1.SpeechClient()
        self.tts_client = texttospeech_v1.TextToSpeechClient()

    def upload_to_storage(self, bucket_name: str, file_path: str, data: bytes) -> str:
        """
        Subir archivo a Cloud Storage
        
        Args:
            bucket_name: Nombre del bucket
            file_path: Ruta del archivo en el bucket
            data: Contenido del archivo
            
        Returns:
            URL pública del archivo
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            blob.upload_from_string(data)
            logger.info(f"✅ Archivo subido: gs://{bucket_name}/{file_path}")
            return f"gs://{bucket_name}/{file_path}"
        except Exception as e:
            logger.error(f"❌ Error al subir archivo: {str(e)}")
            raise

    def download_from_storage(self, bucket_name: str, file_path: str) -> bytes:
        """
        Descargar archivo de Cloud Storage
        
        Args:
            bucket_name: Nombre del bucket
            file_path: Ruta del archivo en el bucket
            
        Returns:
            Contenido del archivo
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            return blob.download_as_bytes()
        except Exception as e:
            logger.error(f"❌ Error al descargar archivo: {str(e)}")
            raise

    def transcribe_audio(self, audio_data: bytes, language_code: str = "es-ES") -> str:
        """
        Transcribir audio a texto usando Speech-to-Text
        
        Args:
            audio_data: Datos de audio en bytes
            language_code: Código de idioma
            
        Returns:
            Texto transcrito
        """
        try:
            audio = speech_v1.RecognitionAudio(content=audio_data)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            # Extraer texto de la respuesta
            transcript = ""
            for result in response.results:
                for alternative in result.alternatives:
                    transcript += alternative.transcript
                    
            logger.info(f"✅ Audio transcrito: {transcript[:100]}...")
            return transcript
        except Exception as e:
            logger.error(f"❌ Error al transcribir audio: {str(e)}")
            raise

    def synthesize_speech(self, text: str, language_code: str = "es-ES") -> bytes:
        """
        Sintetizar texto a voz usando Text-to-Speech
        
        Args:
            text: Texto a sintetizar
            language_code: Código de idioma
            
        Returns:
            Audio sintetizado en bytes
        """
        try:
            synthesis_input = texttospeech_v1.SynthesisInput(text=text)
            
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code=language_code,
                name=f"{language_code}-Neural2-A",
            )
            
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                pitch=0.0,
                speaking_rate=1.0,
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
            
            logger.info(f"✅ Texto sintetizado: {text[:50]}...")
            return response.audio_content
        except Exception as e:
            logger.error(f"❌ Error al sintetizar voz: {str(e)}")
            raise

    def get_ai_recommendation(self, prompt: str) -> str:
        """
        Obtener recomendación usando VertexAI Gemini
        
        Args:
            prompt: Prompt para el modelo
            
        Returns:
            Respuesta del modelo IA
        """
        try:
            model = GenerativeModel(
                settings.vertex_ai_model,
                system_instruction="""
Eres un asistente experto en DevOps y Cloud Engineering conversacional.
Trabajas con ingenieros que preguntan de forma natural y casual.

TEMAS QUE DOMINAS:
- Google Cloud Platform (GCP, Compute, Storage, Databases, etc.)
- CI/CD (pipelines, GitHub Actions, Cloud Build)
- Kubernetes, Docker, contenedores
- Infrastructure as Code (Terraform, Ansible)
- Seguridad cloud y gobernanza
- Monitoreo, logging y observabilidad
- Best practices DevOps
- Troubleshooting de infraestructura

CÓMO RESPONDER:
✓ Interpreta preguntas naturales sin necesidad de formato perfecto
✓ Si alguien pregunta "¿cómo despliego?", entiende que pide pasos prácticos
✓ Si preguntan "¿qué es?", explica de forma clara y concisa
✓ Si piden "ejemplos", incluye comandos o código relevante
✓ Sé conversacional pero profesional
✓ Responde en español siempre
✓ Si el usuario no termina la frase perfectamente, interpreta la intención
✓ Reconoce variaciones: "¿Cómo haço?", "¿Me ayudas con?", "Necesito..."

ESTRUCTURA DE RESPUESTA:
1. Responde directamente lo que preguntan
2. Sé conciso pero completo
3. Solo agrega ejemplos si es útil para la pregunta
4. Ofrece alternativas si hay varias opciones
5. Sugiere próximos pasos si es relevante

SI LA PREGUNTA NO ES DE DEVOPS:
Responde amablemente: "No tengo expertise en eso, pero si tienes preguntas sobre DevOps, GCP, CI/CD o infraestructura, ¡te ayudo!"

RECUERDA: El usuario habla por voz, así que puede haber pequeños errores en la transcripción. Interpreta la intención.
                """
            )
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": settings.vertex_ai_temperature,
                    "max_output_tokens": settings.vertex_ai_max_tokens,
                },
            )
            
            logger.info(f"✅ Respuesta IA generada")
            return response.text
        except Exception as e:
            logger.error(f"❌ Error al obtener recomendación IA: {str(e)}")
            raise

    def get_governance_analysis(self, resource_type: str, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar gobernanza de un recurso
        
        Args:
            resource_type: Tipo de recurso (iam, storage, compute, etc)
            resource_data: Datos del recurso
            
        Returns:
            Análisis de gobernanza
        """
        try:
            prompt = f"""
            Analiza los siguientes datos de gobernanza de {resource_type} y proporciona:
            1. Problemas de seguridad identificados
            2. Recomendaciones de mejora
            3. Cumplimiento de estándares de DevOps
            4. Nivel de riesgo (Alto/Medio/Bajo)
            
            Datos: {json.dumps(resource_data, indent=2)}
            
            Responde en formato JSON estructurado.
            """
            
            response_text = self.get_ai_recommendation(prompt)
            
            # Parsear respuesta JSON
            try:
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                analysis = {"raw_response": response_text}
            
            return analysis
        except Exception as e:
            logger.error(f"❌ Error en análisis de gobernanza: {str(e)}")
            raise


# Instancia global del servicio
_gcp_service: Optional[GCPService] = None


def get_gcp_service() -> GCPService:
    """Obtener instancia del servicio GCP (patrón Singleton)"""
    global _gcp_service
    if _gcp_service is None:
        _gcp_service = GCPService()
    return _gcp_service
