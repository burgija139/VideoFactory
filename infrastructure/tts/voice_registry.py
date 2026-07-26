from pathlib import Path


class VoiceRegistry:

    def __init__(self):

        self.base_path = Path(__file__).parent / "samples"

        self.voices = {

            ("naruto", "excited"):
            {
                "audio": self.base_path / "naruto_excited.wav",
                "text": self.base_path / "naruto_excited.txt"
            },

            ("naruto", "natural"):
            {
                "audio": self.base_path / "naruto_natural.wav",
                "text": self.base_path / "naruto_natural.txt"
            },

            ("sasuke", "excited"):
            {
                "audio": self.base_path / "sasuke_excited.wav",
                "text": self.base_path / "sasuke_excited.txt"
            },

            ("sasuke", "natural"):
            {
                "audio": self.base_path / "sasuke_natural.wav",
                "text": self.base_path / "sasuke_natural.txt"
            }
        }


    def get_voice(self, character, emotion):

        key = (character, emotion)

        if key not in self.voices:
            raise ValueError(
                f"Voice sample not found: {character}/{emotion}"
            )

        return self.voices[key]