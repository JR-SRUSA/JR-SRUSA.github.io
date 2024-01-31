"""
2024-01-25
John Robinson

Will run a speed simulation and return a Plotly graph for displaying on the GitHub pages site
"""
import numpy as np
from plotly import graph_objects as go
from scipy.integrate import solve_ivp

# Conversions
KW2W = 1000  # Converting from kW to W
MS2KPH = 3.6  # Converting from m/s to km/h
# Constants
RHO = 1.3  # Hardcoded air density [kg/m^3]


def acceleration(time: float, state: list, args: dict) -> list:
    """
    Acceleration equations of motion

    state = [
        position [m],
        velocity [m/s],
    ]

    >>> vehicle_params = {'mass_kg': 200, 'cda_m2': 0.5, 'power_kw': 100}
    >>> acceleration(0, [0, 10], vehicle_params)
    [10, 49.8375]

    """
    sum_forces = args["power_kw"] * KW2W / state[1] - 0.5 * RHO * args["cda_m2"] * state[1] ** 2
    acc = sum_forces / args["mass_kg"]
    return [state[1], acc]


def calc_topspeed(vehicle):
    """
    Calculate the top speed based on drag area and power

    >>> vehicle_params = {'mass_kg': 200, 'cda_m2': 0.5, 'power_kw': 100}
    >>> calc_topspeed(vehicle_params)
    243.0382972244989
    """
    return MS2KPH * (vehicle["power_kw"] * KW2W / (0.5 * vehicle["cda_m2"] * RHO)) ** (1 / 3)


def solve_accel(vehicle_params: dict) -> dict:
    """
    Wrapper for solving the acceleration problem

    >>> vehicle_params = {'mass_kg': 200, 'cda_m2': 0.5, 'power_kw': 100}
    >>> sim_data = solve_accel(vehicle_params)

    """
    tf = 20  # Final time [s]
    v0 = 10  # Initial velocity [m/s]

    sol = solve_ivp(acceleration, [0, tf], [0, v0], args=(vehicle_params,))
    return sol


def accel_graph(vehicle_params: dict, show_plot: bool = False):
    """
    Get the graph of acceleration based on the vehicle parameters.

    >>> vehicle_params = {'mass_kg': 200, 'cda_m2': 0.5, 'power_kw': 100}
    >>> sim_data = accel_graph(vehicle_params)
    """
    sol = solve_accel(vehicle_params)
    fig = go.Figure()
    fig.add_scatter(
        x=sol.t,
        y=sol.y[1] * MS2KPH,
        name="Speed",
    )
    fig.add_hline(
        y=calc_topspeed(vehicle_params),
        name="Calculated Topspeed",
    )
    if show_plot:
        fig.show()

    return fig.to_html()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    vehicle_params = {'mass_kg': 200, 'cda_m2': 0.5, 'power_kw': 100}
    fig_html = solve_accel(vehicle_params, True)
