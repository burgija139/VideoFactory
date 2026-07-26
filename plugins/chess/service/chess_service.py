from plugins.chess.repository.puzzle_repository import PuzzleRepository
from plugins.chess.dto.puzzle_dto import PuzzleDTO
from plugins.chess.service.puzzle_classifier import PuzzleClassifier
from plugins.chess.dto.video_conteext import VideoContext
from plugins.chess.content_generation.ai_context_generator import AIContextGenerator


class ChessService:

    def __init__(self):

        self.repo = PuzzleRepository()

        self.classifier = PuzzleClassifier()

        self.ai_context_generator = (
            AIContextGenerator()
        )

    def get_content(self):

        row = self.repo.get_random_puzzle()

        if not row:
            return None

        puzzle_dto = PuzzleDTO(
            puzzle_id=row[0],
            fen=row[1],
            moves=row[2],
            rating=row[3],
            themes=row[4]
        )

        video_type = self.classifier.classify(
            puzzle_dto
        )

        print("---------themes----------")
        print(
            f"puzzle theme: {puzzle_dto.themes}"
        )

        video_context = VideoContext(
            puzzle=puzzle_dto,
            video_type=video_type
        )

        video_context.video_plan = (
            self.ai_context_generator.generate(
                video_context
            )
        )

        return video_context