import io

import chess.svg
from cairosvg import svg2png
from PIL import Image, ImageDraw, ImageFont


class BoardRenderer:

    def __init__(self):

        try:
            self.font = ImageFont.truetype("DejaVuSans.ttf", 28)
        except OSError:
            self.font = ImageFont.load_default()

    def render(self, board, last_move=None):

        svg_data = chess.svg.board(
            board=board,
            size=1080,
            coordinates=False,
            lastmove=last_move
        )

        png_data = svg2png(bytestring=svg_data)

        img = Image.open(io.BytesIO(png_data)).convert("RGB")

        draw = ImageDraw.Draw(img)

        width, _ = img.size
        square = width // 8

        letters = "abcdefgh"
        numbers = "87654321"

        for row in range(8):
            for col in range(8):

                x0 = col * square
                y0 = row * square

                if (row + col) % 2 == 0:
                    text_color = (110, 80, 50)
                else:
                    text_color = (245, 225, 200)

                # letters
                if row == 7:
                    draw.text(
                        (x0 + square - 20, y0 + square - 30),
                        letters[col],
                        fill=text_color,
                        font=self.font
                    )

                # numbers
                if col == 0:
                    draw.text(
                        (x0 + 2, y0 + 2),
                        numbers[row],
                        fill=text_color,
                        font=self.font
                    )

        return img