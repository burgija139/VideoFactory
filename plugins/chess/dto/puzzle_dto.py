class PuzzleDTO:

    def __init__(self, puzzle_id, fen, moves, rating, themes):
        self.puzzle_id = puzzle_id
        self.fen = fen
        self.moves = moves
        self.rating = rating
        self.themes = themes

    def __repr__(self):
        return f"PuzzleDTO(id={self.puzzle_id}, rating={self.rating})"