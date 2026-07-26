class PuzzleClassifier:

    def classify(self, puzzle):

        themes = (puzzle.themes or "").lower()

        # MATES
        if "matein2" in themes:
            return "mate_in_2"

        if "matein3" in themes:
            return "mate_in_3"

        # OPENINGS
        if "opening" in themes:
            return "opening_guess"

        # SPECIFIC TACTICS
        if "fork" in themes:
            return "fork_tactic"

        if "pin" in themes:
            return "pin_tactic"

        if "skewer" in themes:
            return "skewer_tactic"

        # SACRIFICES
        if "sacrifice" in themes:
            return "sacrifice"

        # ENDGAMES
        if "endgame" in themes:
            return "endgame"

        # CRUSHING POSITIONS
        if "crushing" in themes:
            return "crushing_attack"

        # DEFENSE
        if "defensive" in themes:
            return "defensive_move"

        # GENERAL TACTICS
        if (
            "hangingpiece" in themes or
            "discoveredattack" in themes or
            "doublecheck" in themes
        ):
            return "tactic"

        # FALLBACK
        return "best_move"