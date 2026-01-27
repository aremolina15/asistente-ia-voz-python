#!/usr/bin/env python
"""
Cliente de voz para interactuar con el asistente DevOps
Con escucha continua y respuesta en paralelo
"""
import sounddevice as sd
import soundfile as sf
import requests
import json
import base64
import os
import sys
import threading
import queue
import numpy as np
import time

API = "http://localhost:8000/api/v1/voice"
response_queue = queue.Queue()
processing_done = threading.Event()  # Señal para esperar fin de procesamiento

def record_audio_continuous(sample_rate=16000, silence_threshold=0.012, silence_duration=2.5):
    """Grabar audio continuamente con detección inteligente de silencio"""
    frames = []
    silence_count = 0
    max_silence_count = int(silence_duration * sample_rate / 2048)
    has_audio = False
    sustained_sound = 0  # Detectar si hay sonido sostenido
    
    def callback(indata, frames_count, time_info, status):
        nonlocal silence_count, has_audio, sustained_sound
        frames.append(indata.copy())
        
        # Detectar volumen promedio
        volume = np.abs(indata).mean()
        
        if volume < silence_threshold:
            silence_count += 1
        else:
            silence_count = 0
            has_audio = True
            sustained_sound += 1  # Contar frames con sonido
    
    try:
        print("🎤 Grabando... habla ahora")
        stream = sd.InputStream(samplerate=sample_rate, channels=1, callback=callback, dtype='float32', blocksize=2048)
        with stream:
            start_time = time.time()
            # Escuchar hasta 20 segundos máximo
            while time.time() - start_time < 20:
                time.sleep(0.05)
                
                # Necesita al menos 0.5s de sonido sostenido
                if sustained_sound > 10:
                    # Detectó sonido, ahora espera silencio
                    if silence_count > max_silence_count:
                        print("✋ Fin de solicitud detectado")
                        audio = np.concatenate(frames, axis=0)
                        sf.write("temp.wav", audio, sample_rate)
                        return "temp.wav"
        
        # Si pasó el tiempo máximo con audio, guarda
        if has_audio and frames and sustained_sound > 10:
            print("⏱️ Tiempo máximo alcanzado")
            audio = np.concatenate(frames, axis=0)
            sf.write("temp.wav", audio, sample_rate)
            return "temp.wav"
        
        return None
    except Exception as e:
        print(f"❌ Error al grabar: {e}")
        return None

def transcribe(wav_file):
    """Transcribir audio"""
    try:
        with open(wav_file, "rb") as f:
            res = requests.post(f"{API}/transcribe", files={"file": f}, timeout=15)
        if res.status_code == 200:
            return res.json()["transcript"]
        else:
            return None
    except Exception as e:
        print(f"❌ Error transcripción: {e}")
        return None

def clean_transcription(text):
    """Limpiar y normalizar transcripción con detección inteligente de intención"""
    text = text.strip()
    if not text:
        return ""
    
    # Palabras clave DevOps para mejor contexto
    question_starters = [
        'qué', 'como', 'cómo', 'cuándo', 'cuando', 'dónde', 'donde', 
        'cuál', 'cual', 'por qué', 'por que', 'quién', 'quien',
        'puedo', 'podés', 'podemos', 'necesito', 'necesitamos',
        'cómo se', 'como se', 'cuál es', 'cual es'
    ]
    
    # Palabras que indican comandos/acciones
    command_verbs = [
        'instala', 'instalar', 'crea', 'crear', 'despliega', 'desplegar',
        'configura', 'configurar', 'ejecuta', 'ejecutar', 'elimina', 'eliminar',
        'monitorea', 'monitorear', 'actualiza', 'actualizar'
    ]
    
    # Capitalizar primera letra
    text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
    
    # Detectar tipo de frase
    text_lower = text.lower()
    first_word = text_lower.split()[0] if text_lower.split() else ""
    
    is_question = (
        any(text_lower.startswith(q) for q in question_starters) or
        "?" in text or
        text_lower.startswith("ayuda") or
        text_lower.startswith("help")
    )
    
    is_command = any(v in text_lower for v in command_verbs)
    
    # Agregar puntuación inteligente si no la tiene
    if not text.endswith(('.', '?', '!', ',')):
        if is_question:
            text += '?'
        elif is_command:
            text += '.'
        else:
            text += '.'
    
    return text

def query_ai(text):
    """Consultar IA + obtener respuesta de voz"""
    # Limpiar transcripción
    text = clean_transcription(text)
    try:
        res = requests.post(f"{API}/query", json={
            "query": text,
            "language_code": "es-ES"
        }, timeout=30)
        if res.status_code == 200:
            data = res.json()
            audio_bytes = base64.b64decode(data["audio_base64"])
            with open("response.mp3", "wb") as f:
                f.write(audio_bytes)
            return data["response"]
        else:
            return None
    except Exception as e:
        print(f"❌ Error IA: {e}")
        return None

def process_audio_thread():
    """Thread que procesa audio en background"""
    global processing_done
    while True:
        wav_file = response_queue.get()
        if wav_file is None:
            break
        
        print("\n📝 Transcribiendo...")
        text = transcribe(wav_file)
        if not text or len(text.strip()) < 2:
            print("🎧 Escuchando...\n")
            processing_done.set()  # Señalizar que terminó
            continue
        
        print(f"👤 Tú: {text}\n")
        print("🤖 Procesando...")
        response = query_ai(text)
        if not response:
            print("🎧 Escuchando...\n")
            processing_done.set()  # Señalizar que terminó
            continue
        
        print(f"🗣️ Asistente: {response}\n")
        print("🔊 Reproduciendo audio...")
        os.system("ffplay -nodisp -autoexit response.mp3 2>/dev/null")  # Sin & para esperar
        print("✅ Respuesta completada\n")
        processing_done.set()  # Señalizar que terminó la respuesta

def main():
    """Loop principal con escucha continua y respuesta inteligente"""
    global processing_done
    print("=" * 60)
    print("✅ Cliente de voz DevOps - v2.0")
    print("Instrucciones:")
    print("1. Habla tu pregunta/solicitud")
    print("2. La IA espera 2.5s de silencio para entender que terminaste")
    print("3. Responde automáticamente con voz")
    print("4. ESPERA a que termine la respuesta")
    print("5. Automáticamente vuelve a escuchar")
    print("6. Ctrl+C para salir")
    print("=" * 60)
    
    # Iniciar thread de procesamiento
    processor = threading.Thread(target=process_audio_thread, daemon=True)
    processor.start()
    
    print("\n🎤 Sistema listo. Habla ahora...\n")
    
    try:
        while True:
            wav = record_audio_continuous()
            if wav:
                print("⏳ Enviando a procesar...")
                processing_done.clear()  # Resetear señal
                response_queue.put(wav)
                print("⏸️  Esperando respuesta de la IA...")
                processing_done.wait()  # ESPERAR A QUE TERMINE
                print("\n🎤 Sistema listo. Habla ahora...\n")
            else:
                print("⚠️ No se detectó audio claro\n")
    except KeyboardInterrupt:
        print("\n👋 Cerrando asistente...")
        response_queue.put(None)
        processor.join(timeout=2)
        sys.exit(0)

if __name__ == "__main__":
    main()
