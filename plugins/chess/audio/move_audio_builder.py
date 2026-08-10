import os
import wave

import numpy as np


class MoveAudioBuilder:
    def __init__(self, sounds_path="assets/sounds"):
        self.sample_rate = 24000
        # Učitavamo šahovske zvukove unapred u memoriju
        self.sounds = {
            "move": self._load_wav_as_np(f"{sounds_path}/move.wav"),
            "capture": self._load_wav_as_np(f"{sounds_path}/capture.wav"),
            "check": self._load_wav_as_np(f"{sounds_path}/check.wav"),
            "castle": self._load_wav_as_np(f"{sounds_path}/castle.wav"),
        }

    def _load_wav_as_np(self, path):
        if not os.path.exists(path):
            print(f"[⚠️ MoveAudioBuilder] Upozorenje: Zvuk {path} nije pronađen! Koristim tišinu.")
            return np.zeros(1000, dtype=np.float32)
        
        with wave.open(path, "rb") as f:
            file_channels = f.getnchannels()
            file_sample_width = f.getsampwidth()
            file_frame_rate = f.getframerate()
            
            data = f.readframes(f.getnframes())
            
            # Detektujemo bitsku dubinu fajla
            if file_sample_width == 2:
                raw_sound = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            elif file_sample_width == 1:
                raw_sound = (np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 128) * 256
            else:
                # Za 32-bit ili 24-bit koristimo fallback
                raw_sound = np.frombuffer(data, dtype=np.int32).astype(np.float32) / 65536.0

            # Ako je stereo, spajamo u mono (uzimamo samo prvi kanal)
            if file_channels > 1:
                raw_sound = raw_sound[::file_channels]

            # 🚀 DINAMIČKI RESAMPLING: Ako se brzina semplovanja ne poklapa sa naših 24000 Hz,
            # radimo brzu i čistu linearnu interpolaciju kako bi se nizovi poklopili po dužini
            if file_frame_rate != self.sample_rate:
                duration = len(raw_sound) / file_frame_rate
                new_num_samples = int(duration * self.sample_rate)
                
                # Kreiramo indeksne mape za interpolaciju
                old_indices = np.linspace(0, len(raw_sound) - 1, len(raw_sound))
                new_indices = np.linspace(0, len(raw_sound) - 1, new_num_samples)
                
                raw_sound = np.interp(new_indices, old_indices, raw_sound)

            return raw_sound

    def build(self, events, audio_plan, total_duration, output_file):
        total_samples = int(self.sample_rate * total_duration)
        timeline = np.zeros(total_samples, dtype=np.float32)

        # 1. Miksuj zvukove šahovskih poteza (move, capture, check...) - SA POJAČANJEM (2.5x)
        for event in events:
            start_sample = int(event["time"] * self.sample_rate)
            # Sigurnosna provera granica
            start_sample = max(start_sample, 0)
                
            sound = self.sounds.get(event["type"])
            if sound is None: 
                continue
            
            # Pojačavamo šahovske udarce da lepo odjeknu preko glasa
            boosted_sound = sound * 2.5
            
            end_sample = start_sample + len(boosted_sound)
            if end_sample > total_samples:
                boosted_sound = boosted_sound[:total_samples - start_sample]
                end_sample = total_samples
                
            timeline[start_sample:end_sample] += boosted_sound

        # 2. Miksuj TTS glasove likova iz audio_plan-a
        for item in audio_plan:
            if not os.path.exists(item.audio):
                print(f"[⚠️ MoveAudioBuilder] Nedostaje generisani TTS fajl: {item.audio}")
                continue
                
            with wave.open(item.audio, "rb") as f:
                # F5-TTS podrazumevano izbacuje 24000Hz mono 16-bit
                data = f.readframes(f.getnframes())
                sound = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
            start_sample = int(item.start * self.sample_rate)
            start_sample = max(start_sample, 0)
                
            end_sample = start_sample + len(sound)
            
            if end_sample > total_samples:
                sound = sound[:total_samples - start_sample]
                end_sample = total_samples
                
            # Miksujemo glas sa punom jačinom (1.0) jer smo šah već pojačali
            timeline[start_sample:end_sample] += sound

        # Sigurno odsecanje vrhova amplituda (Peak Clipping) i konverzija nazad u PCM 16-bit
        final_audio = np.clip(timeline, -32768, 32767).astype(np.int16)

        with wave.open(output_file, "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(self.sample_rate)
            out.writeframes(final_audio.tobytes())
        print(f"[✅ MoveAudioBuilder] Audio traka kompletno smiksana i sačuvana u: {output_file}")