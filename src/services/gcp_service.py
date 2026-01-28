"""
Servicios para integración con Google Cloud Platform
"""
import json
import logging
from typing import Optional, Dict, Any
from google.cloud import storage, speech_v1, texttospeech_v1
import vertexai
from vertexai.generative_models import GenerativeModel

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
                name=f"{language_code}-Neural2-B",  # Voz masculina clara
            )
            
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                pitch=0.0,  # Ajusta entre -20.0 (grave) y 20.0 (agudo)
                speaking_rate=1.0,  # Velocidad: 0.25 (lento) a 4.0 (rápido)
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
Eres un asistente experto en DevOps y Cloud Engineering. Respondes de forma directa y concisa.

ESPECIALIDADES:
Google Cloud Platform, CI/CD, Kubernetes, Docker, Terraform, Ansible, seguridad cloud, monitoreo e infraestructura.

REGLAS ESTRICTAS:
1. Responde en español, máximo 3-4 oraciones
2. NUNCA uses asteriscos, guiones, viñetas o símbolos especiales
3. NO uses markdown ni formato (sin *, -, #, etc)
4. Escribe en texto plano natural
5. Ve directo al punto, sin introducciones largas
6. Si piden pasos, enumera con palabras: "Primero", "Segundo", "Tercero"
7. Si piden definiciones, explica en 1-2 oraciones
8. Para comandos, di "ejecuta" seguido del comando

EJEMPLOS DE RESPUESTAS CORRECTAS:
Pregunta: "Qué es Kubernetes?"
Respuesta: "Kubernetes es un orquestador de contenedores que automatiza el despliegue, escalado y gestión de aplicaciones en contenedores. Lo usa principalmente para clusters de producción."

Pregunta: "Cómo despliego en GCP?"
Respuesta: "Primero, autentica con gcloud auth login. Segundo, configura tu proyecto. Tercero, usa gcloud app deploy o kubectl apply según el servicio. Necesitas tener configurado el archivo de configuración correspondiente."

SI LA PREGUNTA NO ES DE DEVOPS:
Responde: "No tengo información sobre eso. Puedo ayudarte con DevOps, GCP, Kubernetes, CI/CD e infraestructura."

IMPORTANTE: El usuario habla por voz. Interpreta transcripciones imperfectas. Sé breve y claro.
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
