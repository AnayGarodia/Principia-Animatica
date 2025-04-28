from tkinter.font import ITALIC
from manim import *
from manim.opengl import *
import numpy as np
import itertools
import animatica
import random


class Testing(Scene):

    config.background_color = "#001B2E"

    PRIMARY_COLOR = "#DEB841"  # Gold
    ACCENT_COLOR = "#957FEF"  # Tropical Indigo
    NEUTRAL_COLOR = "#FFFCFF"  # Snow
    QUOTE_COLOR = RED


    def construct(self):
        # Create and add the background

        self.SCENE_equations()
        self.transition(1.5, DOWN)

        animatica.SCENE_intro(self)

        self.transition(1.5)

        self.SCENE_opening_quote()

        self.interactive_embed()


    def transition(self, run, moving=None):
        animations = [FadeOut(*self.mobjects, run_time=run, shift=moving)]
        self.play(*animations)

    def SCENE_equations(self):

        text = MathTex(
            "\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)", "+",
            "g(x)\\frac{d}{dx}f(x)", color=self.NEUTRAL_COLOR
        )
        self.play(Write(text))
        framebox1 = SurroundingRectangle(text[1], buff=.1, color=self.PRIMARY_COLOR)
        framebox2 = SurroundingRectangle(text[3], buff=.1, color=self.PRIMARY_COLOR)
        self.play(
            Create(framebox1),
        )
        self.wait()
        self.play(
            ReplacementTransform(framebox1, framebox2),
        )
        self.wait()

    def SCENE_opening_quote(self):

        quote_line_1 = Text(
            "\"The infinite! No other question has ever moved so profoundly",
            slant=ITALIC,
            font_size=34,
            color= self.NEUTRAL_COLOR,
            t2c={'The infinite!': self.QUOTE_COLOR} # Using QUOTE_COLOR (now PRIMARY_COLOR)
        ).move_to(UP * 2.25)

        quote_line_2 = Text(
            "the spirit of man.\"",
            slant=ITALIC,
            font_size=34,
            color=self.NEUTRAL_COLOR,
        ).move_to(UP * 1.7)

        author = Text(
            "~ David Hilbert, Über das Unendliche",
            color=self.NEUTRAL_COLOR,
            t2c={'~ David Hilbert,': self.PRIMARY_COLOR},
            font_size=30,
        )
        author.to_edge(UP, buff=3)

        try:
            with register_font("../Fonts/Spectral-SemiBoldItalic.ttf"):
                quote_line_1.font = "Spectral-SemiBoldItalic"
                quote_line_2.font = "Spectral-SemiBoldItalic"
        except:
            print("Warning: Spectral font not found. Using default font.")

        try:
            with register_font("../Fonts/Spectral-SemiBold.ttf"):
                author.font = "Spectral-SemiBold"
        except:
            print("Warning: Spectral font not found. Using default font.")

        self.play(
            FadeIn(quote_line_1, quote_line_2, run_time=0.5)
        )
        self.play(Write(author), run_time=2.5)
        self.wait(1)
