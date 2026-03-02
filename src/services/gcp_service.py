"""
Servicios para integración con Google Cloud
"""
import json
import logging
import wave
import re
from typing import Optional, Dict, Any
from google.cloud import storage, speech_v1, texttospeech_v1
import vertexai
from vertexai.generative_models import GenerativeModel

from src.config import settings
from src.prompts import DEVOPS_SYSTEM_PROMPT, build_governance_analysis_prompt

logger = logging.getLogger(__name__)


class GCPService:
    """Servicio para operaciones con GCP"""

    _TERM_NORMALIZATION_PATTERNS = [
        (r"\b(cube\s*ernetes|kubernete[s]?|ku\s*bernetes)\b", "Kubernetes"),
        (r"\b(terra\s*form|terrafo[rm])\b", "Terraform"),
        (r"\b(cloud\s*ran|clou\s*run)\b", "Cloud Run"),
        (r"\b(cloud\s*bild|cloud\s*build)\b", "Cloud Build"),
        (r"\b(i\s*a\s*m|iam)\b", "IAM"),
        (r"\b(c\s*i\s*/?\s*c\s*d|ci\s*cd)\b", "CI/CD"),
        (r"\b(g\s*k\s*e|j\s*k\s*e)\b", "GKE"),
        (r"\b(vertes\s*ai|vertex\s*ai)\b", "Vertex AI"),
    ]

    @staticmethod
    def _to_plain_natural_text(text: str) -> str:
        if not text:
            return ""

        cleaned = text.replace("**", "").replace("__", "")
        cleaned = cleaned.replace("`", "")
        cleaned = re.sub(r"^\s*#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*[-*•]+\s*", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"^\s*\d+[\)\.:-]\s*", "", cleaned, flags=re.MULTILINE)
        cleaned = cleaned.replace("*", "")

        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        if not lines:
            return ""

        merged = " ".join(lines)
        merged = re.sub(r"\s+", " ", merged).strip()
        merged = re.sub(r"\s+,", ",", merged)
        merged = re.sub(r",\s*,+", ", ", merged)
        merged = re.sub(r",\s*\.", ".", merged)
        merged = re.sub(
            r",?\s*teniendo\s+en\s+cuenta\s+que[^:]{0,180}:\s*",
            ". ",
            merged,
            flags=re.IGNORECASE,
        )
        merged = re.sub(
            r"\b(Crear|Configurar|Asignar|Validar|Definir|Aplicar|Ejecutar)\b[^:]{0,70}:\s*",
            "",
            merged,
            flags=re.IGNORECASE,
        )
        merged = re.sub(
            r",?\s*te\s+recomiendo\s+(este\s+)?(flujo|pasos)\s*:\s*",
            ". ",
            merged,
            flags=re.IGNORECASE,
        )
        merged = re.sub(
            r",?\s*te\s+recomiendo\s+seguir\s+estos\s+pasos\s*:\s*",
            ". ",
            merged,
            flags=re.IGNORECASE,
        )

        intro_patterns = [
            r"^para\s+[^.]{0,120}?,\s*estos\s+son\s+los\s+pasos\s+a\s+seguir:\s*",
            r"^para\s+[^.]{0,180}?,\s*sigue\s+estos\s+pasos:\s*",
            r"^sigue\s+estos\s+pasos:\s*",
            r"^a\s+continuacion,?\s*",
            r"^en\s+resumen,?\s*",
            r"^pasos\s+recomendados:\s*",
            r"^estos\s+son\s+los\s+pasos:\s*",
        ]
        for pattern in intro_patterns:
            merged = re.sub(pattern, "", merged, flags=re.IGNORECASE)

        merged = re.sub(
            r"\bsigue\s+estos\s+pasos(?:,\s*basados\s+en\s+[^:]{0,80})?:?\s*",
            "",
            merged,
            count=1,
            flags=re.IGNORECASE,
        )
        merged = re.sub(
            r"\b(seguimos|seguiremos|seguiria|seguiria|seguirás|seguiras|seguirian|seguirían)\s+estos\s+pasos:?\s*",
            "",
            merged,
            count=1,
            flags=re.IGNORECASE,
        )
        merged = re.sub(r"\bsigue\s+estos\s+pasos\s*:?\s*", "", merged, flags=re.IGNORECASE)
        merged = re.sub(r",\s+(?=[A-ZÁÉÍÓÚÑ])", ". ", merged, count=1)
        merged = re.sub(r"(?<=[:;]\s)\d+[\.)]\s+", "", merged)

        sentence_like = [segment.strip(" ;") for segment in re.split(r"[\n\.]+", merged) if segment.strip()]
        if 3 <= len(sentence_like) <= 6 and all(len(item.split()) < 20 for item in sentence_like[:4]):
            connectors = ["Primero", "Después", "Luego", "Al final"]
            rebuilt = []
            step_index = 0
            for index, sentence in enumerate(sentence_like):
                normalized_sentence = re.sub(
                    r"^(primero|segundo|tercero|luego|despues|después|finalmente|ademas|además)[:,]?\s*",
                    "",
                    sentence,
                    flags=re.IGNORECASE,
                )
                normalized_sentence = re.sub(
                    r"^[A-ZÁÉÍÓÚÑ][^:]{3,80}:\s*",
                    "",
                    normalized_sentence,
                )

                is_context_intro = index == 0 and re.match(
                    r"^(para|si|cuando|en\s+caso\s+de|con)\b",
                    normalized_sentence,
                    flags=re.IGNORECASE,
                )

                if is_context_intro:
                    rebuilt.append(normalized_sentence)
                    continue

                prefix = connectors[step_index] if step_index < len(connectors) else "Además"
                step_index += 1

                if step_index == 1:
                    rebuilt.append(f"{prefix}, {normalized_sentence}")
                elif prefix == "Al final":
                    rebuilt.append(f"{prefix}, {normalized_sentence}")
                else:
                    lowered_sentence = (
                        normalized_sentence[:1].lower() + normalized_sentence[1:]
                        if len(normalized_sentence) > 1
                        else normalized_sentence.lower()
                    )
                    rebuilt.append(f"{prefix}, {lowered_sentence}")
            return ". ".join(rebuilt).strip() + "."

        return merged

    def __init__(self):
        """Inicializar servicio GCP"""
        self.project_id = settings.gcp_project_id
        self.region = settings.gcp_region

        configured_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not configured_credentials and settings.google_application_credentials:
            raw_path = settings.google_application_credentials
            candidate_paths = [
                raw_path,
                os.path.abspath(raw_path),
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", raw_path)),
            ]

            for path in candidate_paths:
                if os.path.exists(path):
                    configured_credentials = path
                    break

        if not configured_credentials:
            fallback_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "appengine-sa-key.json")
            )
            if os.path.exists(fallback_path):
                configured_credentials = fallback_path

        if configured_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = configured_credentials
            logger.info("✅ Credenciales GCP configuradas desde archivo local")
        else:
            logger.warning(
                "⚠️ GOOGLE_APPLICATION_CREDENTIALS no configurado. Se intentará usar ADC del sistema."
            )
        
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

    def _detect_audio_format(self, audio_data: bytes) -> Dict[str, Any]:
        """Detectar formato básico de audio para configurar STT."""
        if audio_data.startswith(b"RIFF") and audio_data[8:12] == b"WAVE":
            try:
                with wave.open(BytesIO(audio_data), "rb") as wav_file:
                    sample_rate = wav_file.getframerate()
                    sample_width = wav_file.getsampwidth()
                detected = {
                    "format": "wav",
                    "sample_rate_hz": sample_rate,
                    "encoding": None,
                }
                if sample_width == 2:
                    detected["encoding"] = speech_v1.RecognitionConfig.AudioEncoding.LINEAR16
                return detected
            except Exception:
                return {"format": "wav", "sample_rate_hz": None, "encoding": None}

        if audio_data.startswith(b"fLaC"):
            return {
                "format": "flac",
                "sample_rate_hz": None,
                "encoding": speech_v1.RecognitionConfig.AudioEncoding.FLAC,
            }

        if audio_data.startswith(b"OggS"):
            return {
                "format": "ogg",
                "sample_rate_hz": None,
                "encoding": speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS,
            }

        if audio_data.startswith(b"\x1a\x45\xdf\xa3"):
            return {
                "format": "webm",
                "sample_rate_hz": None,
                "encoding": speech_v1.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            }

        if audio_data.startswith(b"ID3") or (len(audio_data) > 1 and audio_data[0] == 0xFF and (audio_data[1] & 0xE0) == 0xE0):
            return {
                "format": "mp3",
                "sample_rate_hz": None,
                "encoding": speech_v1.RecognitionConfig.AudioEncoding.MP3,
            }

        return {"format": "unknown", "sample_rate_hz": None, "encoding": None}

    def _build_recognition_config(self, audio_data: bytes, language_code: str) -> speech_v1.RecognitionConfig:
        """Crear configuración STT robusta para español técnico DevOps."""
        detected = self._detect_audio_format(audio_data)

        config_kwargs = {
            "language_code": language_code,
            "alternative_language_codes": ["es-419", "es-ES", "es-US"],
            "enable_automatic_punctuation": True,
            "enable_spoken_punctuation": True,
            "enable_word_confidence": True,
            "max_alternatives": 5,
            "profanity_filter": False,
            "model": "latest_long",
            "use_enhanced": True,
            "speech_contexts": [
                speech_v1.SpeechContext(
                    phrases=[
                        "Kubernetes",
                        "kubectl",
                        "Terraform",
                        "Cloud Run",
                        "Cloud Build",
                        "Cloud Storage",
                        "IAM",
                        "CI/CD",
                        "DevOps",
                        "pipeline",
                        "GKE",
                        "Vertex AI",
                        "Gemini",
                    ],
                    boost=20.0,
                )
            ],
        }

        if detected["encoding"] is not None:
            config_kwargs["encoding"] = detected["encoding"]
        if detected["sample_rate_hz"] is not None:
            config_kwargs["sample_rate_hertz"] = detected["sample_rate_hz"]

        return speech_v1.RecognitionConfig(**config_kwargs)

    @staticmethod
    def _map_voice_gender(gender_value: str):
        value = (gender_value or "").strip().upper()
        if value == "MALE":
            return texttospeech_v1.SsmlVoiceGender.MALE
        if value == "NEUTRAL":
            return texttospeech_v1.SsmlVoiceGender.NEUTRAL
        return texttospeech_v1.SsmlVoiceGender.FEMALE

    def _normalize_technical_terms(self, text: str) -> str:
        """Corregir errores típicos de STT en términos técnicos."""
        normalized = text
        for pattern, replacement in self._TERM_NORMALIZATION_PATTERNS:
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _technical_term_score(self, text: str) -> int:
        """Puntuar alternativa por presencia de términos DevOps esperados."""
        terms = [
            "kubernetes", "terraform", "cloud", "iam", "ci/cd", "gke", "vertex ai", "gemini", "devops",
        ]
        text_lower = text.lower()
        return sum(1 for term in terms if term in text_lower)

    def transcribe_audio(self, audio_data: bytes, language_code: str | None = None) -> Dict[str, Any]:
        """
        Transcribir audio a texto usando Speech-to-Text
        
        Args:
            audio_data: Datos de audio en bytes
            language_code: Código de idioma
            
        Returns:
            Resultado de transcripción con texto y confianza
        """
        try:
            language_code = language_code or settings.voice_default_language_code
            audio = speech_v1.RecognitionAudio(content=audio_data)

            config = self._build_recognition_config(audio_data, language_code)

            try:
                response = self.speech_client.recognize(config=config, audio=audio)
            except Exception as first_error:
                logger.warning(f"⚠️ Reintento STT con configuración básica: {str(first_error)}")
                fallback_config = speech_v1.RecognitionConfig(
                    language_code=language_code,
                    enable_automatic_punctuation=True,
                )
                response = self.speech_client.recognize(config=fallback_config, audio=audio)

            transcript_parts = []
            confidences = []

            for result in response.results:
                if result.alternatives:
                    ranked = sorted(
                        result.alternatives,
                        key=lambda alt: ((alt.confidence or 0.0), self._technical_term_score(alt.transcript)),
                        reverse=True,
                    )
                    best = ranked[0]
                    transcript_parts.append(best.transcript.strip())
                    if best.confidence:
                        confidences.append(best.confidence)

            transcript = " ".join(part for part in transcript_parts if part).strip()
            transcript = self._normalize_technical_terms(transcript)
            confidence = round(sum(confidences) / len(confidences), 3) if confidences else 0.0

            logger.info(f"✅ Audio transcrito: {transcript[:100]}...")
            return {
                "transcript": transcript,
                "confidence": confidence,
            }
        except Exception as e:
            logger.error(f"❌ Error al transcribir audio: {str(e)}")
            raise

    def synthesize_speech(self, text: str, language_code: str | None = None) -> bytes:
        """
        Sintetizar texto a voz usando Text-to-Speech
        
        Args:
            text: Texto a sintetizar
            language_code: Código de idioma
            
        Returns:
            Audio sintetizado en bytes
        """
        try:
            language_code = language_code or settings.voice_default_language_code
            synthesis_input = texttospeech_v1.SynthesisInput(text=text)

            voice_kwargs = {
                "language_code": language_code,
                "ssml_gender": self._map_voice_gender(settings.voice_tts_gender),
            }
            if settings.voice_tts_name:
                voice_kwargs["name"] = settings.voice_tts_name

            voice = texttospeech_v1.VoiceSelectionParams(**voice_kwargs)
            
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding=texttospeech_v1.AudioEncoding.MP3,
                pitch=settings.voice_tts_pitch,
                speaking_rate=settings.voice_tts_speaking_rate,
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

    def get_ai_recommendation(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Obtener recomendación usando VertexAI Gemini
        
        Args:
            prompt: Prompt para el modelo
            system_instruction: Prompt de sistema opcional
            
        Returns:
            Respuesta del modelo IA
        """
        try:
            model = GenerativeModel(
                settings.vertex_ai_model,
                system_instruction=system_instruction or DEVOPS_SYSTEM_PROMPT,
            )
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": settings.vertex_ai_temperature,
                    "max_output_tokens": settings.vertex_ai_max_tokens,
                },
            )
            
            logger.info(f"✅ Respuesta IA generada")
            return self._to_plain_natural_text(response.text)
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
            prompt = build_governance_analysis_prompt(resource_type, resource_data)
            
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
