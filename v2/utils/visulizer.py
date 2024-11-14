import matplotlib.pyplot as plt
import numpy
from typing import List, Union


def visualize_energy(y: Union[numpy.ndarray, List]):
    plt.figure(figsize=(10, 4))
    plt.plot(y)
    plt.title("Energy of Audio Signal")
    plt.xlabel("Frame")
    plt.ylabel("Energy")
    plt.show()

def visualize_energy_with_details(times: Union[numpy.ndarray, List], energy: Union[numpy.ndarray, List], energy_threshold_min: float, energy_threshold_max: float):
    plt.figure(figsize=(10, 4))
    plt.plot(times, energy, label="Energy")
    plt.axhline(y = energy_threshold_min, color='r', linestyle='--', label="Min Threshold")
    plt.axhline(y = energy_threshold_max, color='g', linestyle='--', label="Max Threshold")
    plt.fill_between(times, energy_threshold_min, energy_threshold_max, where=((energy > energy_threshold_min) & (energy < energy_threshold_max)), color="b", alpha=0.3)
    plt.title("Energy of Audio Signal Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Energy")
    plt.legend()
    plt.show()