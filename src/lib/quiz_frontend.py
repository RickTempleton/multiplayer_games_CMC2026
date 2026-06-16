"""Basic frontend screen for the Quiz game."""

from __future__ import annotations

from typing import Callable, Optional

import arcade

try:
    from .localization import tr
    from .menu import CYAN, PURPLE, NeonBaseView
except ImportError:
    from localization import tr
    from menu import CYAN, PURPLE, NeonBaseView


QUESTION_PLACEHOLDER = "Вопрос появится здесь"
ANSWER_PLACEHOLDERS = (
    "A. Вариант ответа",
    "B. Вариант ответа",
    "C. Вариант ответа",
    "D. Вариант ответа",
)


class QuizView(NeonBaseView):
    """Static visual base for the quiz screen."""

    def __init__(
        self,
        player_name: str = "",
        on_back: Optional[Callable[[], None]] = None,
    ):
        super().__init__()
        self.player_name = player_name
        self.on_back = on_back

        self.title_label = arcade.Text(
            tr("game.quiz.title").upper(),
            x=0,
            y=0,
            color=(228, 243, 255),
            font_size=56,
            font_name=("Bahnschrift", "Calibri", "Arial"),
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.question_label = arcade.Text(
            QUESTION_PLACEHOLDER,
            x=0,
            y=0,
            color=(236, 247, 255),
            font_size=28,
            font_name=("Bahnschrift", "Calibri", "Arial"),
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )
        self.hint_label = arcade.Text(
            "Базовый экран викторины без интерактивности",
            x=0,
            y=0,
            color=(165, 188, 214),
            font_size=18,
            font_name=("Calibri", "Arial"),
            anchor_x="center",
            anchor_y="center",
        )

        self.answer_labels = [
            arcade.Text(
                text,
                x=0,
                y=0,
                color=(222, 238, 255),
                font_size=22,
                font_name=("Bahnschrift", "Calibri", "Arial"),
                anchor_x="center",
                anchor_y="center",
            )
            for text in ANSWER_PLACEHOLDERS
        ]

        self._register_responsive_text(self.title_label, 56, 20, 0.42)
        self._register_responsive_text(self.question_label, 28, 14, 0.54)
        self._register_responsive_text(self.hint_label, 18, 10, 0.58)
        for label in self.answer_labels:
            self._register_responsive_text(label, 22, 12, 0.24)

    def on_draw(self) -> None:
        """Draw the static quiz layout."""

        self.clear()
        self._draw_neon_background()
        self._draw_shell()
        self._draw_question_card()
        self._draw_answer_cards()
        self._draw_text_layer()

    def _draw_shell(self) -> None:
        width = self.window.width
        height = self.window.height

        self._draw_filled_rect(
            width * 0.16,
            width * 0.84,
            height * 0.14,
            height * 0.78,
            (5, 12, 30, 105),
        )
        self._draw_outlined_rect(
            width * 0.16,
            width * 0.84,
            height * 0.14,
            height * 0.78,
            (66, 188, 255, 80),
            border_width=2,
        )

    def _draw_question_card(self) -> None:
        left, right, bottom, top = self._question_bounds()
        self._draw_filled_rect(left, right, bottom, top, (4, 14, 34, 220))
        self._draw_outlined_rect(
            left,
            right,
            bottom,
            top,
            (88, 212, 255, 170),
            border_width=3,
        )

    def _draw_answer_cards(self) -> None:
        for index, bounds in enumerate(self._answer_bounds()):
            left, right, bottom, top = bounds
            accent = CYAN if index % 2 == 0 else PURPLE
            self._draw_filled_rect(left, right, bottom, top, (8, 20, 48, 210))
            self._draw_outlined_rect(
                left,
                right,
                bottom,
                top,
                accent + (170,),
                border_width=2,
            )

    def _draw_text_layer(self) -> None:
        self._refresh_texts()
        self._update_responsive_layout()

        width = self.window.width
        height = self.window.height
        q_left, q_right, q_bottom, q_top = self._question_bounds()

        self.title_label.x = width / 2
        self.title_label.y = height * 0.86
        self.title_label.draw()

        self.question_label.x = (q_left + q_right) / 2
        self.question_label.y = (q_bottom + q_top) / 2
        self.question_label.draw()

        for label, bounds in zip(self.answer_labels, self._answer_bounds()):
            left, right, bottom, top = bounds
            label.x = (left + right) / 2
            label.y = (bottom + top) / 2
            label.draw()

        self.hint_label.x = width / 2
        self.hint_label.y = height * 0.18
        self.hint_label.draw()

    def _refresh_texts(self) -> None:
        super()._refresh_texts()
        self.title_label.text = tr("game.quiz.title").upper()

    def _question_bounds(self) -> tuple[float, float, float, float]:
        width = self.window.width
        height = self.window.height

        return (
            width * 0.25,
            width * 0.75,
            height * 0.52,
            height * 0.68,
        )

    def _answer_bounds(self) -> list[tuple[float, float, float, float]]:
        width = self.window.width
        height = self.window.height
        left = width * 0.25
        right = width * 0.75
        gap_x = max(12, width * 0.018)
        gap_y = max(10, height * 0.022)
        card_width = (right - left - gap_x) / 2
        card_height = height * 0.09
        top = height * 0.44

        return [
            (left, left + card_width, top - card_height, top),
            (left + card_width + gap_x, right, top - card_height, top),
            (
                left,
                left + card_width,
                top - card_height * 2 - gap_y,
                top - card_height - gap_y,
            ),
            (
                left + card_width + gap_x,
                right,
                top - card_height * 2 - gap_y,
                top - card_height - gap_y,
            ),
        ]
