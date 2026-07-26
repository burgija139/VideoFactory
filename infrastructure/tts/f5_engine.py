import subprocess
import os

class F5Engine:

    def __init__(
        self,
        model="F5TTS_v1_Base",
        device="cpu"
    ):
        self.model = model
        self.device = device

    def generate(
        self,
        ref_audio,
        ref_text,
        text,
        output_file
    ):

        command = [
            "f5-tts_infer-cli",
            "-m", self.model,
            "-r", str(ref_audio),
            "-s", ref_text,
            "-t", text,
            "-w", str(output_file),
            "--device", self.device
        ]

        print("Running F5:")
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"F5 generation failed:\n{result.stderr}"
            )

        # =================================================================
        # 🔊 OVDE SMANJUJEMO ZVUK GOVORA LIKOVA PREKO FFMPEG-a
        # =================================================================
        # Pravimo privremeno ime za izmenjeni fajl
        temp_volume_file = str(output_file).replace(".wav", "_volume.wav")
        
        # volume=0.30 smanjuje jačinu govora na 30%. Potezi će sada biti glasniji.
        # Ako hoćeš još tiši glas, stavi 0.15. Ako hoćeš skroz da ugasiš, stavi 0.0
        ffmpeg_command = [
            "ffmpeg", "-y",
            "-i", str(output_file),
            "-filter:a", "volume=0.70",
            temp_volume_file
        ]

        print(f"[🔊 Volume Control] Utišavam generisani glas na 30% jačine...")
        ffmpeg_result = subprocess.run(ffmpeg_command, capture_output=True, text=True)

        if ffmpeg_result.returncode == 0:
            # Ako je ffmpeg uspešno odradio posao, zamenimo originalni fajl utišanim
            os.replace(temp_volume_file, str(output_file))
        else:
            print(f"[⚠️ Volume Control] Greška pri utišavanju: {ffmpeg_result.stderr}")
            if os.path.exists(temp_volume_file):
                os.remove(temp_volume_file)
        # =================================================================

        return output_file