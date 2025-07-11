"""=============================================================================
Authors:        Alex Alves, Bradley Bravender, Noah Johnson
Organization:   SnowScape
Date Created:   July 2, 2025
Purpose:        Simulates a novel avalanche-victim localization technology.
Usage:          python3 simulation.py
============================================================================="""

import random
from math import sqrt
from typing import Tuple
import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt


class Device():
    """Used to simulate anchors and tags.
    """

    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate


    def get_coordinates(self) -> Tuple[float, float]:
        """Returns the coordinates of the device.

        Returns:
            Tuple[float, float]: the x and y coordinates of the device.
        """
        return self.x_coordinate, self.y_coordinate
    

    def set_coordinates(self, new_x: float, new_y: float) -> None:
        """Used to set updated coordinates for the device. 

        Args:
            new_x (float): The x coordinate.
            new_y (float): The y coordinate.
        """
        self.x_coordinate = new_x
        self.y_coordinate = new_y


def get_distance(device1: Device, device2: Device) -> float:
    """Returns the distance between two devices, with simulated noise up to 
    'error_percentage'% from the actual value. Kept separate from the base station
    class for a more accurate representation of the blindness of the base station
    to the ground-truth coordinates of the devices.

    Args:
        device1 (Device): The first device.
        device2 (Device): The second device.

    Returns:
        float: The magnitude of distance (in 2d) between devices, with noise.
    """
    x = 0
    y = 1
    error_percentage = 5
    
    device1_coords = device1.get_coordinates()
    device2_coords = device2.get_coordinates()
    x_delta = device1_coords[x] - device2_coords[x]
    y_delta = device1_coords[y] - device2_coords[y]
    magnitude = sqrt(x_delta**2 + y_delta**2)

    maximum_noise = magnitude * (error_percentage / 100)
    noisy_magnitude = magnitude + random.uniform(-maximum_noise, maximum_noise)
    
    return noisy_magnitude


class BaseStation():
     
    def __init__(self):
        self.main()


    def display_points(self, points: list[tuple[float, float]]) -> None:
        """@Alex, this function is your baby. My thought is that it takes in a 
        list of x and y coordinates, and updates a 2D plot in real time based on 
        whenever new points are passed to the method.

        First make it so there are lines between every point from rescue point with distances, also normalize graph to go to the edge of points
        Also include degrees from north of optimal path.
        Potentially use mouse as rescue tag, calculate distances and represent the cursor as a point.

        Args:
            points (list[tuple[float, float]]): A list of the x and y coordinates
            of the anchors and tags.
        """
        pass


    def temporary_display_method(self, points: dict):
        """
        Plots named points on a 2D graph using matplotlib.
        
        Parameters:
            coord_dict (dict): Dictionary with names as keys and (x, y) tuples as values.
        """
        for name, (x, y) in points.items():
            plt.scatter(x, y, label=name)
            plt.text(x, y, name, fontsize=9, ha='right', va='bottom')

        plt.axhline(0, color='black', linewidth=1)  # y=0 line (horizontal)
        plt.axvline(0, color='black', linewidth=1)  # x=0 line (vertical)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Named Coordinates')
        plt.grid(True)
        plt.legend()
        plt.axis('equal')  # optional: equal scaling for x and y
        plt.show()


    def calibration_equation(self, unknowns: list[float]) -> float:
        """A callback function used to approximate the relative coordinates of
        each device.

        Args:
            unknowns (list[float]): A list of approximate values for each unknown
                x and y coordinate.

        Returns:
            float: The equation to minimize for.
        """
        self.a1y, self.a2x, self.a2y, self.vtx, self.vty = unknowns
        eq1 = (self.a1x - self.a0x)**2 + (self.a1y - self.a0y)**2 - self.a0a1**2 
        eq2 = (self.a2x - self.a0x)**2 + (self.a2y - self.a0y)**2 - self.a0a2**2 
        eq3 = (self.vtx - self.a0x)**2 + (self.vty - self.a0y)**2 - self.a0vt**2  
        eq4 = (self.a2x - self.a1x)**2 + (self.a2y - self.a1y)**2 - self.a1a2**2
        eq5 = (self.vtx - self.a1x)**2 + (self.vty - self.a1y)**2 - self.a1vt**2
        eq6 = (self.vtx - self.a2x)**2 + (self.vty - self.a2y)**2 - self.a2vt**2
        # Minimize the sum of squares of residuals

        #Look into this and upload documentation on why we send in this format.
        return eq1**2 + eq2**2 + eq3**2 + eq4**2 + eq5**2 + eq6**2


    def calibration(self) -> None:
        """Uses the relative distances between devices to calculate relative
        coordinates for each device.
        """
        self.a0x, self.a0y, self.a1x = 0, 0, 0
        
        # Retrieve the distances between each device
        self.a0a1 = get_distance(anchor0, anchor1)
        self.a0a2 = get_distance(anchor0, anchor2)
        self.a0vt = get_distance(anchor0, victim_tag)
        self.a1a2 = get_distance(anchor1, anchor2)
        self.a1vt = get_distance(anchor1, victim_tag)
        self.a2vt = get_distance(anchor2, victim_tag)

        # Define bounds for each variable
        bounds = [(-100, 100)] * 5

        # Perform global optimization using differential evolution
        result = differential_evolution(self.calibration_equation, bounds)

        # Output result
        if result.success:
            a1y, a2x, a2y, vtx, vty = result.x
            print("Solution found:")
            print(f"({self.a0x:.3f}, {self.a0y:.3f}), ({self.a1x:.3f}, {a1y:.3f}), ({a2x:.3f}, {a2y:.3f}), ({vtx:.3f}, {vty:.3f})")
        else:
            print("No solution found.")

    
    def set_device_locations(self) -> dict:
        anchor0.set_coordinates(self.a0x, self.a0y)
        anchor1.set_coordinates(self.a1x, self.a1y)
        anchor2.set_coordinates(self.a2x, self.a2y)
        victim_tag.set_coordinates(self.vtx, self.vty)

        points = {
            "anchor0": (self.a0x, self.a0y),
            "anchor1": (self.a1x, self.a1y),
            "anchor2": (self.a2x, self.a2y),
            "victim": (self.vtx, self.vty)
        }
        
        return points


    def trilateration(self):
        """Develop the trilateration algorithm here
        """
        pass


    def main(self):
        self.calibration()

        points = self.set_device_locations()

        self.temporary_display_method(points)

        self.trilateration()



if __name__=="__main__":
    # Establish the ground truth for each device (5 total)
    anchor0 = Device(-5,4)
    anchor1 = Device(3,2)
    anchor2 = Device(6,-10)
    victim_tag = Device(4,4)
    rescuer_tag = Device(2,2)

    # Run the main program
    obj = BaseStation()

# TODO: calibrate should be used for trilateration too

print(variable2)