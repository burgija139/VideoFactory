import os
import time
import random
from google import genai
from plugins.chess.dto.video_plan import VideoPlan 

class AIContextGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=api_key)

    def generate(self, video_context):
        puzzle = video_context.puzzle
        num_moves = len(puzzle.moves.split())
        
        # Dinamički biramo da li će video prikazivati poteze ili biti statični izazov
        # Možeš i sam da kontrolišeš procente (trenutno je 70% šansa da pokazuje poteze, 30% da je statični puzzle)
        show_moves_decision = random.random() < 0.70
        
        if show_moves_decision:
            # Ako prikazujemo poteze, nasumično biramo 1 ili 2 naratora za analizu/banter
            forced_speakers = random.choice(["1", "2"])
            force_timer_decision = random.choice([True, False])
            timer_duration_val = 5
        else:
            # Ako NE prikazujemo poteze (statična tabla), MORA biti samo 1 narator, a tajmer MORA biti upaljen
            forced_speakers = "1"
            force_timer_decision = True
            timer_duration_val = random.choice([5, 7])

        prompt = f"""
        You are a viral chess shorts director. Your job is to orchestrate the video timeline and character dialog scripts.

        DYNAMIC FORMAT RULES (SHOW_MOVES TRUE VS FALSE):
        - Current 'show_moves' decision for this video is: {str(show_moves_decision).upper()}

        1. IF 'show_moves' IS TRUE:
           - The video will actively render and play out all the puzzle solution moves on the screen.
           - For this format, you MUST set the 'speakers_count' field to "{forced_speakers}".
           - Dialogue should be about the active chess moves, lines, and banter between characters.

        2. IF 'show_moves' IS FALSE:
           - The chess board stays completely STATIC at the initial puzzle position for the whole video. No moves are played.
           - For this format, you MUST set 'speakers_count' to "1" (Solo Narrator).
           - This narrator can be any character (e.g., Naruto or Sasuke), but they MUST address the audience directly.
           - The script format is an interactive puzzle challenge for the viewers. Use hype phrases like: "Can you find the best move here?", "Can you solve this puzzle?", "White to play and win! What is the winning line?".
           - You MUST keep 'timer_enabled' as true and set 'timer_duration' to {timer_duration_val} so the audience has time to stare at the static board while the narrator loops.

        STRICT EMOTION BALANCING RULE (90% NATURAL, 10% EXCITED):
        - Around 90% of the timeline items MUST use the 'emotion': "natural".
        - Use 'emotion': "excited" ONLY for critical high-retention moments (e.g., severe blunders, smart checkmates, crazy trash-talk, or the initial hype hook at the start/end).
        - Keep the base tone cool and natural by default.

        CHARACTER PRONUNCIATION & CHESS TEXT FORMATTING RULES:
        1. NEVER use standard chess notation (like Bxe7, Nf3, d4, exd5, O-O, +) in the 'text' fields! The voice engine cannot read it.
        2. Instead, you MUST spell out every chess move and action in plain English words:
           - Convert figure letters to full words (e.g., N -> Knight, B -> Bishop, R -> Rook, Q -> Queen, K -> King).
           - Convert captures (x) to the word "takes" (e.g., instead of "Bxe7", write "Bishop takes e 7").
           - Always put spaces between the square letter and number so it pronounces correctly (e.g., "g 5", "h 6", "e 4").
           - Instead of "Nf3", write "Knight to f 3".
           - Instead of "+", write "check". Instead of "#", write "checkmate".
        3. If characters say the name Sasuke in their text, they MUST spell it as "Saskey" or "Sasky" so the voice engine pronounces it correctly.

        CRITICAL SHORTS DURATION RULES (TARGET: 30-45 SECONDS):
        1. Total video duration MUST BE BETWEEN 30 AND 45 SECONDS.
        2. To achieve this, create a richer, longer dialogue with more back-and-forth banter or thoughts.
        3. Make sure intro_seconds is around 4-6 seconds, and generate a solid 7 to 10 timeline items in total.

        TIMELINE PACING RULES:
        - timeline must be 7-10 items to fill the 30-45s duration.
        - max 8 words per text string.
        - intro always starts at time 0.
        - last item must be a high-retention hook/ending.

        Video type: {video_context.video_type}
        Rating: {puzzle.rating}
        Themes: {puzzle.themes}
        FEN: {puzzle.fen}
        Moves: {puzzle.moves} (Total moves: {num_moves})
        """

        max_retries = 3
        attempt = 0

        while True:
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": VideoPlan,
                        "temperature": 0.82
                    }
                )

                # Parsiramo i validiramo nazad u Pydantic model
                plan = VideoPlan.model_validate_json(response.text)
                
                # Dodatna softverska garancija da se poklapaju pre-generisane odluke sa JSON-om
                plan.show_moves = show_moves_decision
                plan.timer_enabled = force_timer_decision
                plan.timer_duration = timer_duration_val
                plan.speakers_count = forced_speakers

                return plan

            except Exception as e:
                status_code = getattr(e, "status_code", None)
                error_msg = str(e).lower()
                if status_code == 503 or "high demand" in error_msg or "unavailable" in error_msg:
                    attempt += 1
                    wait_time = attempt * 5
                    print(f"[Gemini 503] Server busy... Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise e