"""=============================================================================
Authors:        Alex Alves, Bradley Bravender, Noah Johnson
Organization:   SnowScape
Date Created:   July 2, 2025
Purpose:        Simulates a novel avalanche-victim localization technology.
Usage:          python3 simulation.py
============================================================================="""

import random
from typing import Tuple


class Device():
    """Used to simulate anchors and tags.
    """

    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        # The amount of noise to add to the coordinates. Not sure if noise should
        # be implemented in this class or elsewhere.
        self.error_percentage = 5


    def get_coordinates(self) -> Tuple[float, float]:
        """Returns the coordinates of the device.

        Returns:
            Tuple[float, float]: the x and y coordinates of the device.
        """
        return self.x_coordinate, self.y_coordinate


    def get_noisy_coordinates(self) -> Tuple[float, float]:
        """An experimental method that needs to be revised. Not sure where to 
        put the functionality for noisy measurements.

        Returns:
            Tuple[float, float]: _description_
        """
        x_delta = self.x_coordinate * (self.error_percentage / 100)
        x_noise = random.uniform(-x_delta, x_delta)
        noisy_x_coord = self.x_coordinate + x_noise
        
        y_delta = self.y_coordinate * (self.error_percentage / 100)
        y_noise = random.uniform(-y_delta, y_delta)
        noisy_y_coord = self.y_coordinate + y_noise
        
        return noisy_x_coord, noisy_y_coord
    

    def set_coordinates(self, new_x: float, new_y: float) -> None:
        """Used to set updated coordinates for the device. 

        Args:
            new_x (float): The x coordinate.
            new_y (float): The y coordinate.
        """
        self.x_coordinate = new_x
        self.y_coordinate = new_y


class MainClass():
     
    def __init__(self):
        # TODO: in the future, we need to add functionality to normalize a given
        # anchor coordinate as (0,0). For now, we will trivially set one at (0,0).
        self.anchor0 = Device(0,0)
        self.anchor1 = Device(3,0)
        self.anchor2 = Device(0,3)
        self.tag0 = Device(1,1)
        self.tag1 = Device(2,2)


    def display_points(self, points: list[tuple[float, float]]) -> None:
        """@Alex, this function is your baby. My thought is that it takes in a 
        list of x and y coodinates, and updates a 2D plot in real time based on 
        whenever new points are passed to the method.

        Args:
            points (list[tuple[float, float]]): A list of the x and y coordinates
            of the anchors and tags.
        """
        pass


    def calibration(self):
        """Develop the self-calibration algorithm here
        """


    def trilateration(self):
        """Develop the trilateration algorithm here
        """


if __name__=="__main__":
    # Just some filler code for now
    obj = Device(5,7.6)
    print(obj.get_noisy_coordinates())
    print(obj.get_noisy_coordinates())
    obj.set_coordinates(10,20)
    print(obj.get_noisy_coordinates())