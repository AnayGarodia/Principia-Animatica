# helper_scene_intro.py

from manim import *
import itertools
import numpy as np


# --- INTRO ANIMATION ---
PRIMARY_COLOR = "#F1C40F"
ACCENT_COLOR = "#00CED1"
NEUTRAL_COLOR = "#AAAAAA"

DOT_CHORD_COLORS = [
    PRIMARY_COLOR,
    ACCENT_COLOR,
    "#E74C3C",
    "#9B59B6"
]

FONT_PATH = "../Fonts/Audiowide-Regular.ttf"
FONT_NAME = "Audiowide"
CHANNEL_NAME = "PRINCIPIA ANIMATICA"

N_POINTS = 10

def SCENE_intro(scene_self):
    # --- Internal Helper Functions ---
    def get_points_on_circle(n_points, circle):
        points = []
        center = circle.get_center()
        for i in range(n_points):
            angle = 2 * PI * i / n_points
            points.append(
                center + 2.5 * np.array([  # 2.5 is radius
                    np.cos(angle),
                    np.sin(angle),
                    0
                ])
            )
        return points

    def get_chords(points_pos, dots):
        chord_colors = itertools.cycle(DOT_CHORD_COLORS)
        chords_with_start_index = []
        all_chord_mobjects = []

        for i in range(len(points_pos)):
            for j in range(i + 1, len(points_pos)):
                chord = Line(points_pos[i], points_pos[j], color=next(chord_colors), stroke_width=3)
                chords_with_start_index.append((chord, i))
                all_chord_mobjects.append(chord)

        chords_with_start_index.sort(key=lambda item: item[1])

        chord_creation_anims = []
        current_start_index = -1

        for chord, start_index in chords_with_start_index:
            if start_index != current_start_index:
                indicate_color_index = start_index % len(DOT_CHORD_COLORS)
                chord_creation_anims.append(
                    Indicate(
                        dots[start_index],
                        color=DOT_CHORD_COLORS[indicate_color_index],
                        scale=1.2,
                        run_time=0.2,
                    )
                )
                current_start_index = start_index

            dot_copy = dots[start_index].copy().scale(1.5)
            chord_creation_anims.append(
                AnimationGroup(
                    FadeIn(dot_copy, run_time=0.02),
                    Transform(dot_copy, chord, run_time=0.15, rate_func=rate_functions.smooth),
                    lag_ratio=0.05,
                )
            )

        return chord_creation_anims

    # --- Main Scene Logic ---
    scene_self.play(FadeIn(
        Rectangle(
            width=config.frame_width * 2,
            height=config.frame_height * 2,
            fill_color="#000000",
            fill_opacity=1
        ), 
        run_time=0.5
    ))

    circle = Circle(radius=2.5, stroke_width=4)
    circle.set_stroke(color=PRIMARY_COLOR)
    circle.shift(UP * 0.7)

    try:
        with register_font(FONT_PATH):
            channel_name = Text(CHANNEL_NAME, font=FONT_NAME, font_size=70)
    except:
        channel_name = Text(CHANNEL_NAME, font_size=55)
        print("Warning: Audiowide font not found. Using default font.")

    channel_name.set_color(PRIMARY_COLOR)
    channel_name.next_to(circle, DOWN, buff=0.6)

    cursor = Rectangle(
        color=NEUTRAL_COLOR,
        fill_color=NEUTRAL_COLOR,
        fill_opacity=1.0,
        height=channel_name.get_height(),
        width=0.05,
    )
    cursor.next_to(channel_name, LEFT, buff=0.1)

    scene_self.add(channel_name, cursor)

    scene_self.play(
        GrowFromCenter(circle, run_time=0.45),
        TypeWithCursor(channel_name, cursor, run_time=0.75),
    )

    scene_self.play(
        Blink(cursor, blinks=2, run_time=0.25),
        FadeOut(cursor, run_time=0.25),
    )

    scene_self.remove(cursor)

    points_pos = get_points_on_circle(N_POINTS, circle)

    dot_colors = itertools.cycle(DOT_CHORD_COLORS)
    dots = VGroup(*[Dot(pos, color=next(dot_colors), radius=0.15) for pos in points_pos])

    dot_anims = []
    for dot in dots:
        dot_anims.append(
            AnimationGroup(
                FadeIn(dot, scale=3.0, run_time=0.25, rate_func=rate_functions.ease_in_out_bounce),
                Flash(
                    dot,
                    color="#FFFFFF",
                    flash_radius=0.3,
                    line_length=0.25,
                    num_lines=8,
                    run_time=0.25,
                ),
                lag_ratio=0.075,
            )
        )

    scene_self.play(LaggedStart(*dot_anims, lag_ratio=0.25, run_time=1.6))

    chords = get_chords(points_pos, dots)

    scene_self.play(
        LaggedStart(*chords, lag_ratio=0.1, run_time=2.5)
    )
