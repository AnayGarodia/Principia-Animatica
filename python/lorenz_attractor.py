"""
Manim Animation of the Lorenz Attractor

Description:
- This script visualizes the Lorenz attractor in 3D using Manim.
- The Lorenz system is a set of three coupled, nonlinear differential equations that exhibit chaotic behavior.
- The animation includes:
    - 3D axes for visualization.
    - Multiple Lorenz curves with slight variations in initial conditions.
    - Animated spheres that follow the curves.
    - Smooth camera movement with ambient rotation.
- The script uses `scipy.solve_ivp` for solving the differential equations over time.

Dependencies:
- Manim
- SciPy
- NumPy
"""

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
    dxdt = sigma * (y - x)  # Rate of change of x
    dydt = x * (rho - z) - y  # Rate of change of y
    dzdt = x * y - beta * z  # Rate of change of z

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
        function,  # Lorenz system function
        t_span=(0, time),  # Time range (start, end)
        y0=state0,  # Initial state
        t_eval=np.arange(0, time, dt)  # Time points at which to evaluate
    )

    return solution.y.T


# Main Manim scene class
class LorenzAttractor(ThreeDScene):
    """
    Manim scene to visualize the Lorenz attractor with animated curves and spheres.
    """

    def construct(self):
        # ------------------------------------------------------------
        # 1. Setting up the 3D coordinate system
        # ------------------------------------------------------------
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),  # X-axis range and tick spacing
            y_range=(-50, 50, 5),  # Y-axis range and tick spacing
            z_range=(0, 50, 5),  # Z-axis range and tick spacing
            x_length=16,  # Physical length of the X-axis in scene
            y_length=16,  # Physical length of the Y-axis
            z_length=8  # Physical length of the Z-axis
        )

        # Center the axes in the scene
        axes.center()

        # Set the initial camera orientation
        self.set_camera_orientation(
            phi=80 * DEGREES,  # Slight downward tilt
            theta=10 * DEGREES,  # Side angle for depth
            gamma=0 * DEGREES,  # No unnatural twist
            zoom=0.75  # Zoomed out for better visibility
        )

        # Add the axes to the scene
        self.add(axes)

        # ------------------------------------------------------------
        # 2. Configuring the Lorenz attractor curves
        # ------------------------------------------------------------

        # Slightly varied initial conditions for multiple trajectories
        epsilon = 0.001
        states = [
            [10, 10, 10 + n * epsilon]  # Starting at slightly different Z-values
            for n in range(4)
        ]

        # Color gradient for the curves
        colors = color_gradient([BLUE, YELLOW], len(states))

        # Animation duration
        evolution_time = 30

        # Group to hold all Lorenz curves
        curves = VGroup()

        # Iterate over initial states and colors to create multiple curves
        for state, color in zip(states, colors):
            # Solve the Lorenz system and convert the points to Manim coordinates
            points = ode_solution_points(lorenz_system, state, evolution_time)
            manim_points = [axes.c2p(x, y, z) for x, y, z in points]

            # Create the curve
            curve = VMobject()
            curve.set_points_smoothly(manim_points)  # Smooth the curve
            curve.set_color(color)
            curve.set_stroke(width=1.2)

            # Add the curve to the group
            curves.add(curve)

        # ------------------------------------------------------------
        # 3. Adding spheres to follow the attractor curves
        # ------------------------------------------------------------

        # Create small spheres for visual interest
        spheres = VGroup(*[
            Sphere(radius=0.12).set_color(color).set_opacity(0.8)
            for color in colors
        ])

        # Updater function to make spheres follow the curve ends
        def update_spheres(spheres):
            """
            Updater to position spheres at the end of each curve.

            Parameters:
            - spheres: Group of sphere objects.
            """
            for sphere, curve in zip(spheres.submobjects, curves):
                sphere.move_to(curve.get_end())

        # Add the updater to continuously update sphere positions
        spheres.add_updater(update_spheres)
        self.add(spheres)

        # ------------------------------------------------------------
        # 4. Animating the scene
        # ------------------------------------------------------------

        # Set the camera position again before animation
        self.set_camera_orientation(
            phi=80 * DEGREES,  # Slight downward tilt
            theta=10 * DEGREES,  # Side angle for depth
            gamma=0 * DEGREES,  # No unnatural twist
            zoom=0.75  # Initial zoom
        )

        # Start ambient camera rotation for a dynamic effect
        self.begin_ambient_camera_rotation(rate=0.2)  # Slow and smooth rotation

        # Simultaneously play the curve animations while the camera rotates
        self.play(
            *[Create(curve, run_time=evolution_time, rate_func=linear) for curve in curves]
        )

        # Allow the camera to continue moving briefly
        self.wait(2)

        # Stop the ambient camera motion
        self.stop_ambient_camera_rotation()
