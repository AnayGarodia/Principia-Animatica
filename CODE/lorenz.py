from manim import *
from scipy.integrate import solve_ivp
import numpy as np


# Function to define the Lorenz system equations
def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    """
    Defines the Lorenz system of differential equations.

    Parameters:
    - t: Time variable (ignored in autonomous systems like Lorenz).
    - state: Current [x, y, z] coordinates.
    - sigma, rho, beta: Parameters controlling the system's behavior.

    Returns:
    - List of derivatives [dx/dt, dy/dt, dz/dt].
    """
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


# Function to solve the Lorenz system using scipy's solve_ivp
def ode_solution_points(function, state0, time, dt=0.075):
    """
    Solves the Lorenz system over a specified time range and returns the solution points.

    Parameters:
    - function: The system of equations to solve.
    - state0: Initial state [x, y, z].
    - time: The total duration of the solution.
    - dt: Time step between evaluation points.

    Returns:
    - solution.y.T: Transposed array of solution points [x, y, z] over time.
    """
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T


# Main Manim scene class combining intro and Lorenz animation
class LorenzIntroToAttractor(ThreeDScene):
    def construct(self):
        # ------------------------------------------------------------
        # TEXT INTRO ANIMATION
        # ------------------------------------------------------------
        title = MarkupText('<span fgcolor="#00FFFF">The Lorenz Attractor</span>', font_size=80)
        title.set_opacity(0.9)
        glow_circle = Circle(radius=2.8, color=BLUE, stroke_opacity=0.2).scale(0.9)
        glow_circle.set_fill(BLUE, opacity=0.2)
        glow_circle.move_to(title)

        line1 = MarkupText('How <span fgcolor="#FFFF00">Tiny Changes</span>', font_size=44)
        line2 = MarkupText('Cause <span fgcolor="#FF2222">Massive Chaos</span>', font_size=44)

        text_group = VGroup(title, line1, line2).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(
            LaggedStart(
                GrowFromCenter(title),
                FadeIn(glow_circle, scale=2),
                lag_ratio=0.1
            ),
            run_time=1.5
        )
        self.wait(0.4)
        self.play(Write(line1), run_time=1)
        self.wait(0.2)
        self.play(Write(line2), run_time=1)
        self.wait(0.8)
        self.play(
            ApplyMethod(text_group.shift, UP * 0.05),
            ApplyMethod(text_group.shift, DOWN * 0.1),
            ApplyMethod(text_group.shift, UP * 0.05),
            run_time=0.3
        )
        self.play(
            text_group.animate.shift(UP * 3).scale(0.9).set_opacity(0),
            glow_circle.animate.scale(1.5).set_opacity(0),
            run_time=1.6
        )
        self.wait()

        # ------------------------------------------------------------
        # LORENZ ATTRACTOR BEGINS HERE
        # ------------------------------------------------------------
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(0, 50, 5),
            x_length=16,
            y_length=16,
            z_length=8
        )
        axes.center()

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=10 * DEGREES,
            zoom=0.75
        )
        self.add(axes)

        # Multiple initial conditions
        epsilon = 0.001
        states = [[10, 10, 10 + n * epsilon] for n in range(4)]
        colors = color_gradient([BLUE, YELLOW], len(states))
        evolution_time = 10
        curves = VGroup()

        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            manim_points = [axes.c2p(x, y, z) for x, y, z in points]
            curve = VMobject()
            curve.set_points_smoothly(manim_points)
            curve.set_color(color)
            curve.set_stroke(width=1.2)
            curves.add(curve)

        # Add spheres that follow the attractor
        spheres = VGroup(*[
            Sphere(radius=0.05).set_color(color).set_opacity(0.8)
            for color in colors
        ])

        def update_spheres(spheres):
            for sphere, curve in zip(spheres.submobjects, curves):
                sphere.move_to(curve.get_end())

        spheres.add_updater(update_spheres)
        self.add(spheres)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=10 * DEGREES,
            zoom=0.75
        )
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(
            *[Create(curve, run_time=evolution_time, rate_func=linear) for curve in curves]
        )
        self.wait(2)
        self.stop_ambient_camera_rotation()
