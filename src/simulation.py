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
        # TODO: in the future, we need to add functionality to normalize a given
        # anchor coordinate as (0,0). For now, we will trivially set one at (0,0).
        self.anchor0 = Device(0,0)
        self.anchor1 = Device(3,0)
        self.anchor2 = Device(0,3)
        # Let tag0 represent the tag of the buried skier (i.e. its position is static)
        self.victim_tag = Device(1,1)
        self.rescuer_tag = Device(2,2)

        self.calibration()

        self.trilateration()


    def display_points(self, points: list[tuple[float, float]]) -> None:
        """@Alex, this function is your baby. My thought is that it takes in a 
        list of x and y coordinates, and updates a 2D plot in real time based on 
        whenever new points are passed to the method.

        Args:
            points (list[tuple[float, float]]): A list of the x and y coordinates
            of the anchors and tags.
        """
        pass


    def calibration(self):
        """Develop the self-calibration algorithm here
        """
        # TODO:
        # Get distances between all anchors and the victim tag
        # Put these distances in a predefined equation
        # Use a non-linear library to solve the equation and establish the 
        # coordinates of each anchor and the victim tag
        # Future work includes a more robust solution instead of just hardcoding
        # the equations and distance function calls
        self.a0a1 = get_distance(self.anchor0, self.anchor1)
        self.a0a2 = get_distance(self.anchor0, self.anchor2)
        self.a0vt = get_distance(self.anchor0, self.victim_tag)
        self.a1a2 = get_distance(self.anchor1, self.anchor2)
        self.a1vt = get_distance(self.anchor1, self.victim_tag)
        self.a2vt = get_distance(self.anchor2, self.victim_tag)

        print(self.a0a1, self.a0a2, self.a0vt, self.a1a2, self.a1vt, self.a2vt)


    def trilateration(self):
        """Develop the trilateration algorithm here
        """
        pass



if __name__=="__main__":
    # A basic test for now:
    anchor0 = Device(0,0)
    tag0 = Device(0,5)
    for i in range(10):
        print(get_distance(anchor0, tag0))
    
    tag0.set_coordinates(0,7)
    for i in range(10):
        print(get_distance(anchor0, tag0))

    obj = BaseStation()
