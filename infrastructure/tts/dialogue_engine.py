import os
from typing import List
from plugins.chess.dto.audio_item import AudioItem
from plugins.chess.dto.video_plan import VideoPlan

class DialogueEngine:
    def __init__(self, tts_engine):
        self.tts = tts_engine

    def build_dialogue(self, video_plan: VideoPlan, output_dir: str = "temp_audio") -> List[AudioItem]:
        os.makedirs(output_dir, exist_ok=True)
        audio_plan = []

        print(f"[🎬 DialogueEngine] Proleđujem čist tekst iz Gemini-ja u TTS za {len(video_plan.timeline)} replika.")

        for index, item in enumerate(video_plan.timeline):
            # Prosto uzimamo tekst kakav je Gemini napravio jer je već napisan rečima
            print(f"[🗣️ TTS Line {index}] Lik: {item.character} ({item.emotion}) -> Tekst: '{item.text}'")

            output_file = os.path.join(output_dir, f"line_{index}.wav")
            
            try:
                # Šaljemo direktno u F5 preko tvog TTSEngine-a
                result = self.tts.synthesize(
                    item.character,
                    item.emotion,
                    item.text,
                    output_file
                )
                
                duration = result.get("duration", 0.0)
                
                audio_item = AudioItem(
                    start=item.time,
                    end=item.time + duration,
                    character=item.character,
                    emotion=item.emotion,
                    text=item.text,
                    audio=output_file
                )
                audio_plan.append(audio_item)
                
            except Exception as e:
                print(f"[❌ DialogueEngine] Greška prilikom generisanja linije {index}: {e}")
                raise e

        return audio_plan