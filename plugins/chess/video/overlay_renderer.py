import io
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont


class OverlayRenderer:

    def __init__(self):

        try:
            self.title_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                90
            )

            self.rating_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                38
            )

            self.timer_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                50
            )

            self.pause_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                80
            )

        except OSError:

            self.title_font = ImageFont.load_default()
            self.rating_font = ImageFont.load_default()
            self.timer_font = ImageFont.load_default()
            self.pause_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                110
            )

    def _get_theme_color(self, video_type):

        return {
            "mate_in_2": (255, 80, 80),
            "mate_in_3": (180, 80, 255),
            "opening_guess": (80, 120, 255),
            "tactic": (255, 170, 60),
            "only_move": (80, 255, 160),
            "best_move": (200, 200, 200),
            "fork_tactic": (255, 140, 80),
            "pin_tactic": (255, 80, 180),
            "skewer_tactic": (120, 180, 255),
            "sacrifice": (255, 60, 60),
            "endgame": (120, 255, 200),
            "crushing_attack": (255, 120, 120),
            "defensive_move": (120, 200, 255)
        }.get(video_type, (40, 40, 40))

    def render(
        self,
        board_image,
        title,
        rating,
        context_text="",
        video_type="",
        state="intro",
        timer_text="",
        timer_current=None,
        timer_total=None
    ):

        W, H = 1080, 1920

        # =========================================
        # BACKGROUND
        # =========================================

        bg = board_image.resize((W, W))

        bg = bg.filter(
            ImageFilter.GaussianBlur(35)
        )

        theme = self._get_theme_color(video_type)

        color_layer = Image.new(
            "RGB",
            (W, W),
            theme
        )

        bg = Image.blend(
            bg,
            color_layer,
            0.12
        )

        bg = bg.resize((W, H)).convert("RGBA")

        dark_overlay = Image.new(
            "RGBA",
            (W, H),
            (0, 0, 0, 165)
        )

        bg = Image.alpha_composite(
            bg,
            dark_overlay
        )

        canvas = bg

        draw = ImageDraw.Draw(canvas)

        # =========================================
        # TITLE
        # =========================================

        wrapped_title = textwrap.wrap(
            title,
            width=18
        )

        current_y = 160

        for line in wrapped_title:

            draw.text(
                (W // 2, current_y),
                line,
                fill=(255, 255, 255),
                font=self.title_font,
                anchor="mm"
            )

            current_y += 95

        # =========================================
        # BOARD
        # =========================================

        board_x = (W - board_image.width) // 2

        board_y = 420

        canvas.paste(
            board_image,
            (board_x, board_y)
        )

        # =========================================
        # TIMER DARK OVERLAY OVER BOARD
        # =========================================

        if state == "timer":

            dark_board = Image.new(
                "RGBA",
                (board_image.width, board_image.height),
                (0, 0, 0, 170)
            )

            board_region = canvas.crop((
                board_x,
                board_y,
                board_x + board_image.width,
                board_y + board_image.height
            )).convert("RGBA")

            board_region = Image.alpha_composite(
                board_region,
                dark_board
            )

            canvas.paste(
                board_region.convert("RGB"),
                (board_x, board_y)
            )

        # =========================================
        # RATING
        # =========================================

        rating_text = f"Rating: {rating}"

        rating_x = board_x + board_image.width - 20

        rating_y = board_y + board_image.height + 50

        draw.text(
            (rating_x, rating_y),
            rating_text,
            fill=(200, 200, 200),
            font=self.rating_font,
            anchor="ra"
        )

        # =========================================
        # TIMER OVERLAY
        # =========================================

        if state == "timer":

            center_x = W // 2
            center_y = board_y + board_image.height + 320

            radius = 70

            thickness = 15

            solution_font = ImageFont.truetype(
                "DejaVuSans-Bold.ttf",
                50
            )

            draw.text(
                (center_x, center_y - 100),
                "Solution In",
                fill=(255, 255, 255),
                font=solution_font,
                anchor="mm"
            )

            # OUTER CIRCLE
            draw.ellipse(
                (
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius
                ),
                outline=(255, 255, 255, 60),
                width=thickness
            )

            # PROGRESS ARC
            if timer_current is not None and timer_total is not None:

                progress = timer_current / timer_total

                end_angle = -90 + (360 * progress)

                draw.arc(
                    (
                        center_x - radius,
                        center_y - radius,
                        center_x + radius,
                        center_y + radius
                    ),
                    start=-90,
                    end=end_angle,
                    fill=(255, 255, 255),
                    width=thickness
                )

            # TIMER NUMBER
            draw.text(
                (center_x, center_y),
                str(timer_text),
                fill=(255, 255, 255),
                font=self.timer_font,
                anchor="mm"
            )

        # =========================================
        # PAUSE OVERLAY
        # =========================================

        if state == "pause":

            # DARKEN BOARD
            dark_board = Image.new(
                "RGBA",
                (board_image.width, board_image.height),
                (0, 0, 0, 170)
            )

            board_region = canvas.crop((
                board_x,
                board_y,
                board_x + board_image.width,
                board_y + board_image.height
            )).convert("RGBA")

            board_region = Image.alpha_composite(
                board_region,
                dark_board
            )

            canvas.paste(
                board_region.convert("RGB"),
                (board_x, board_y)
            )

            center_x = W // 2
            center_y = H // 2

            # TEXT
            draw.text(
                (center_x, center_y),
                "Did You Find It?",
                fill=(255, 255, 255),
                font=self.pause_font,
                anchor="mm",
                align="center"
            )

        # =========================================
        # OUTPUT
        # =========================================

        output = io.BytesIO()

        canvas.convert("RGB").save(
            output,
            format="PNG"
        )

        return output.getvalue()