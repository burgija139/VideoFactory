# plugins/chess/video/chess_video_builder.py

import os
import subprocess

import chess

from plugins.chess.audio.move_audio_builder import MoveAudioBuilder
from plugins.chess.dto.audio_item import AudioItem
from plugins.chess.video.board_renderer import BoardRenderer
from plugins.chess.video.overlay_renderer import OverlayRenderer


class ChessVideoBuilder:

    def __init__(self, sounds_path="assets/sounds"):
        self.board_renderer = BoardRenderer()
        self.overlay_renderer = OverlayRenderer()
        self.move_audio_builder = MoveAudioBuilder(sounds_path)

    def create(
        self,
        context,
        audio_plan: list[AudioItem],
        output_file="final.mp4"
    ):
        puzzle = context.puzzle
        video_plan = context.video_plan

        current_dir = os.path.dirname(os.path.abspath(__file__))

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(current_dir)
            )
        )

        output_dir = os.path.join(
            base_dir,
            "shorts",
            "chess"
        )

        os.makedirs(output_dir, exist_ok=True)

        if not os.path.isabs(output_file):
            output_file = os.path.join(
                output_dir,
                output_file
            )

        move_list = puzzle.moves.split()

        fps = 30

        video_title = (
            video_plan.title
            if video_plan.title
            else "Chess Puzzle"
        )

        intro_duration = float(
            video_plan.intro_seconds
        )

        timer_duration = (
            float(video_plan.timer_duration)
            if video_plan.timer_enabled
            else 0.0
        )

        current_speech_pointer = (
            intro_duration + timer_duration
        )

        for index, item in enumerate(audio_plan):
            original_duration = (
                item.end - item.start
            )

            if index == 0:
                item.start = 0.5
                item.end = (
                    item.start + original_duration
                )
            else:
                item.start = (
                    current_speech_pointer + 0.2
                )

                item.end = (
                    item.start + original_duration
                )

                current_speech_pointer = item.end

        events = []

        simulated_board = chess.Board(
            puzzle.fen
        )

        move_timestamps = []

        if not video_plan.show_moves:
            move_list = []

            print(
                "[🎮 ChessVideoBuilder] "
                "Format detektovan: "
                "Statični izazov (show_moves=False)."
            )

        chess_start_time = (
            intro_duration + timer_duration
        )

        audio_nudge = -0.15

        for i, move in enumerate(move_list):
            visual_move_time = (
                chess_start_time + (i * 2.0)
            )

            audio_move_time = (
                visual_move_time + audio_nudge
            )

            move_obj = chess.Move.from_uci(move)

            is_capture = (
                simulated_board.is_capture(move_obj)
            )

            is_castle = (
                simulated_board.is_castling(move_obj)
            )

            simulated_board.push(move_obj)

            if is_castle:
                event_type = "castle"
            elif simulated_board.is_check():
                event_type = "check"
            elif is_capture:
                event_type = "capture"
            else:
                event_type = "move"

            events.append({
                "time": audio_move_time,
                "type": event_type
            })

            move_timestamps.append({
                "trigger_time": visual_move_time,
                "move_obj": move_obj,
                "board_state": simulated_board.copy()
            })

        last_move_end = (
            chess_start_time
            + (len(move_list) * 2.0)
            + 1.5
        )

        total_duration = max(
            current_speech_pointer + 1.5,
            last_move_end
        )

        total_frames = int(
            total_duration * fps
        )

        temp_video = "temp_video.mp4"
        temp_audio = "temp_audio.wav"

        video_proc = subprocess.Popen(
            [
                "ffmpeg",
                "-y",
                "-f",
                "image2pipe",
                "-vcodec",
                "png",
                "-r",
                str(fps),
                "-i",
                "-",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "22",
                temp_video
            ],
            stdin=subprocess.PIPE
        )

        try:
            for frame_idx in range(total_frames):
                current_time = frame_idx / fps

                state = "intro"
                timer_text = ""
                dinamicki_tekst = ""

                active_speech = next(
                    (
                        x
                        for x in audio_plan
                        if x.start
                        <= current_time
                        <= x.end
                    ),
                    None
                )

                if active_speech:
                    dinamicki_tekst = (
                        f"{active_speech.character.upper()}: "
                        f"{active_speech.text}"
                    )
                else:
                    dinamicki_tekst = video_title

                if current_time < intro_duration:
                    state = "intro"

                elif (
                    video_plan.timer_enabled
                    and current_time
                    < intro_duration + timer_duration
                ):
                    state = "timer"

                    time_passed_in_timer = (
                        current_time - intro_duration
                    )

                    timer_text = str(
                        int(
                            timer_duration
                            - time_passed_in_timer
                        )
                    )

                else:
                    state = "moves"

                active_board = chess.Board(
                    puzzle.fen
                )

                last_move_obj = None

                for m_idx, m_data in enumerate(
                    move_timestamps
                ):
                    if (
                        current_time
                        >= m_data["trigger_time"]
                    ):
                        active_board = (
                            m_data["board_state"]
                        )

                        last_move_obj = (
                            m_data["move_obj"]
                        )

                        if (
                            m_idx
                            == len(move_timestamps) - 1
                            and not active_speech
                        ):
                            ending_item = next(
                                (
                                    x
                                    for x in video_plan.timeline
                                    if x.type == "ending"
                                ),
                                None
                            )

                            if ending_item:
                                dinamicki_tekst = (
                                    ending_item.text
                                )

                board_image = (
                    self.board_renderer.render(
                        active_board,
                        last_move_obj
                    )
                )

                timer_current = None
                timer_total = None

                if state == "timer":
                    timer_total = timer_duration

                    timer_current = (
                        timer_duration
                        - (
                            current_time
                            - intro_duration
                        )
                    )

                frame_bytes = (
                    self.overlay_renderer.render(
                        board_image=board_image,
                        title=video_title,
                        rating=puzzle.rating,
                        context_text=dinamicki_tekst,
                        video_type=context.video_type,
                        state=state,
                        timer_text=timer_text,
                        timer_current=timer_current,
                        timer_total=timer_total
                    )
                )

                video_proc.stdin.write(frame_bytes)

        finally:
            if video_proc.stdin:
                video_proc.stdin.close()

            video_proc.wait()

        self.move_audio_builder.build(
            events=events,
            audio_plan=audio_plan,
            total_duration=total_duration,
            output_file=temp_audio
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                temp_video,
                "-i",
                temp_audio,
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                output_file
            ],
            check=True
        )

        if os.path.exists(temp_video):
            os.remove(temp_video)

        if os.path.exists(temp_audio):
            os.remove(temp_audio)

        print(
            f"🎬 Video uspešno kreiran: {output_file}"
        )

        return output_file