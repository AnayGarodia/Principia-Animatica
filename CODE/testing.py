from manim import *
import itertools
import numpy as np
import random
from manim.utils import rate_functions

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

FONT_PATH = "../assets/fonts/NotoSans-Bold.ttf"
FONT_NAME = "Noto Sans"
CHANNEL_NAME = "PRINCIPIA ANIMATICA"

N_POINTS = 10
N_BG_DOTS = 600
DOT_SPEED = 0.25

class MovingDot(Dot):
    """A tiny background dot that moves in straight random motion."""
    def __init__(self, **kwargs):
        color = random.choice(DOT_CHORD_COLORS)
        radius = random.uniform(0.02, 0.05)
        super().__init__(radius=radius, color=color, **kwargs)
        self.set_opacity(0.3)
        vx, vy = np.random.uniform(-DOT_SPEED, DOT_SPEED, 2)
        self.velocity = np.array([vx, vy, 0.0]) * 1.5 # 150% speed
        self.add_updater(self.move_dot)

    def move_dot(self, m, dt):
        m.shift(self.velocity * dt)

def SCENE_intro(scene_self):
    # --- Helper functions unchanged ---
    def get_points_on_circle(n_points, circle):
        points = []
        center = circle.get_center()
        for i in range(n_points):
            angle = 2 * PI * i / n_points
            points.append(
                center + 2.5 * np.array([
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

    # --- Add background moving dots ---
    bg_dots = VGroup(*[
        MovingDot().move_to([
            np.random.uniform(-config.frame_width/2, config.frame_width/2),
            np.random.uniform(-config.frame_height/2, config.frame_height/2),
            0
        ]) for _ in range(N_BG_DOTS)
    ])
    scene_self.add(bg_dots)

    # --- Main Scene Logic ---
    circle = Circle(radius=2.5, stroke_width=4)
    circle.set_stroke(color=PRIMARY_COLOR)
    circle.shift(UP * 0.7)

    try:
        with register_font(FONT_PATH):
            channel_name = Text(CHANNEL_NAME, font=FONT_NAME, font_size=70)
    except:
        channel_name = Text(CHANNEL_NAME, font_size=70)
        print("Warning: Noto Sans font not found. Using default font.")

    channel_name.set_color(PRIMARY_COLOR)
    channel_name.next_to(circle, DOWN, buff=0.6)

    scene_self.play(
        GrowFromCenter(circle, run_time=0.75),
        Write(channel_name, run_time=1.75),
    )

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

    # --- Zoom in on circle after chords ---
    scene_self.play(
        scene_self.camera.frame.animate.move_to(circle.get_center()).set(height=circle.radius*2*1.1),
        run_time=2.0,
        rate_func=rate_functions.ease_in_out_sine
    )

    chords = get_chords(points_pos, dots)

    scene_self.play(
        LaggedStart(*chords, lag_ratio=0.1, run_time=2.5)
    )

# Change Scene to MovingCameraScene to fix the error
class IntroScene(MovingCameraScene):
    def construct(self):
        SCENE_intro(self)

if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 30
    config.background_color = "#000000"
    scene = IntroScene()
    scene.render()