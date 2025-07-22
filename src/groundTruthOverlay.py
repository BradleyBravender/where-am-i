"""=============================================================================
Authors:        Alex Alves, Bradley Bravender, Noah Johnson
Organization:   SnowScape
Date Created:   July 2, 2025
Purpose:        Simulates a novel avalanche-victim localization technology.
Usage:          python3 simulation.py
============================================================================="""

import random
from math import sqrt
import time
from typing import Tuple
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Device():
    """Used to simulate anchors and tags. Manages ground truth (gt) coordinates,
    and calculated (calc) coordinates.

    BaseStation() uses the distances between ground truth coordinates to 
    calculate the calculated coordinates. 
    """

    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.gt_x_coordinate = x_coordinate
        self.calc_x_coordinate = x_coordinate
        
        self.gt_y_coordinate = y_coordinate
        self.calc_y_coordinate = y_coordinate


    def get_gt_coordinates(self) -> Tuple[float, float]:
        """Returns the ground truth coordinates of the device.

        Returns:
            Tuple[float, float]: the x and y coordinates of the device.
        """
        return self.gt_x_coordinate, self.gt_y_coordinate
    
    
    def get_calc_coordinates(self) -> Tuple[float, float]:
        """Returns the calculated coordinates of the device.

        Returns:
            Tuple[float, float]: the x and y coordinates of the device.
        """
        return self.calc_x_coordinate, self.calc_y_coordinate
    

    def set_gt_coordinates(self, new_x: float, new_y: float) -> None:
        """Used to set updated ground truth coordinates for the device. 

        Args:
            new_x (float): The x coordinate.
            new_y (float): The y coordinate.
        """
        self.gt_x_coordinate = new_x
        self.gt_y_coordinate = new_y


    def set_calc_coordinates(self, new_x: float, new_y: float) -> None:
        """Used to set updated calculated coordinates for the device. 

        Args:
            new_x (float): The x coordinate.
            new_y (float): The y coordinate.
        """
        self.calc_x_coordinate = new_x
        self.calc_y_coordinate = new_y


class UserInterface:
    
    def __init__(self, fig, ax):
        self.ax = ax
        self.fig = fig
        self.points_to_draw = {}
        

    def update_data(self, points_dict):
        # If I do not make a copy, UserInterface will access the same self.points
        # data structure managed in BaseStation, which isn't bad in this 
        # configuration but renders this function useless after its first call
        # and poses challenges down the road.
        self.points_to_draw = points_dict.copy()


    def animate(self, frame):
        """Animation function called at each frame."""
        #ADD LINES BETWEEN ALL POINTS AND RESCUER WITH DISTANCES.
            #Start with just lines
            #Move to distances after (have to pull from basestation)
        #Look further into line artists and how to properly initialize and update them
        self.ax.clear()
        # TODO: Set axis limits (could dynamically calculate from points if needed)
        self.ax.set_xlim(-50, 80)
        self.ax.set_ylim(-80, 50)
        self.ax.grid(True)

        updatedArtists = []

        # place points on graph
        for label, (x, y) in self.points_to_draw.items():
            if x is not None and y is not None:
                #Scatter is better for multiple points
                scatter = self.ax.scatter(x, y, label=label)
                text = self.ax.text(x + 0.2, y + 0.2, label, fontsize=8)
                #Append the artists
                updatedArtists.extend([scatter,text])
        
        #place lines between victim/beacon and rescuer point
        rescuerCoords = self.points_to_draw.get("rescuer", None)
        if rescuerCoords is not None:
            rx, ry = rescuerCoords
            for label, (x,y) in self.points_to_draw.items():
                if label != "rescuer" and x is not None and y is not None:
                    #grabs the element from the returned list to use as an artist in animation
                    if label == 'victim':
                        line = self.ax.plot([x, rx], [y, ry], color='red', linestyle='--')[0]
                    else:
                        line = self.ax.plot([x, rx], [y, ry], color='gray', linestyle='--')[0]
                    updatedArtists.append(line)

        for label, device in [("anchor0", anchor0), ("anchor1", anchor1), ("anchor2", anchor2), ("victim", victim_tag), ("rescuer", rescuer_tag)]:
            gt_x, gt_y = device.get_gt_coordinates()
            if label != "rescuer":
                scatter = self.ax.scatter(gt_x, gt_y, color='black', marker='x', label=f"{label}GT")
                text = self.ax.text(gt_x + 0.2, gt_y + 0.2, f"{label}GT", fontsize=8, color='black')
            else:
                scatter = self.ax.scatter(gt_x, gt_y, color='black', label=f"{label}GT")
                text = self.ax.text(gt_x + 0.2, gt_y + 0.2, f"{label}GT", fontsize=8, color='black')

            updatedArtists.extend([scatter,text])


        #gt_rx, gt_ry = rescuer_tag.get_gt_coordinates()
        #scatter = self.ax.scatter(gt_rx, gt_ry, color='black', label='rescuerGT')

        legend = self.ax.legend(loc="lower left")
        updatedArtists.extend([legend,scatter])

        return updatedArtists
    

    def start_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100, cache_frame_data=False)

        
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
    error_percentage = 0
    
    device1_coords = device1.get_gt_coordinates()
    device2_coords = device2.get_gt_coordinates()
    x_delta = device1_coords[x] - device2_coords[x]
    y_delta = device1_coords[y] - device2_coords[y]
    magnitude = sqrt(x_delta**2 + y_delta**2)

    maximum_noise = magnitude * (error_percentage / 100)
    noisy_magnitude = magnitude + random.uniform(-maximum_noise, maximum_noise)
    
    return noisy_magnitude


class BaseStation():
     
    def __init__(self):
        self.points = {}
        self.main()


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


    def calculate_coordinates(self, calibration=False, trilateration=False):
        """ 'Converts' ground truth coordinates into calculated coordinates.

        This function might be redundant, but it neatly encapsulates methods
        which essentially solve the same problem from different angles, and which
        may be called separately or together.
        """

        if calibration:
            self.calibration()

        if trilateration:
            self.trilateration()


    def calibration(self) -> None:
        """Uses the relative distances between devices to calculate relative
        coordinates for each device.
        """
        a0x, a0y, a1x = 0, 0, 0
        
        # Retrieve the distances between each device
        a0a1 = get_distance(anchor0, anchor1)
        a0a2 = get_distance(anchor0, anchor2)
        a0vt = get_distance(anchor0, victim_tag)
        a1a2 = get_distance(anchor1, anchor2)
        a1vt = get_distance(anchor1, victim_tag)
        a2vt = get_distance(anchor2, victim_tag)

        def calibration_callback(unknowns):
            a1y, a2x, a2y, vtx, vty = unknowns
            eq1 = (a1x - a0x)**2 + (a1y - a0y)**2 - a0a1**2 
            eq2 = (a2x - a0x)**2 + (a2y - a0y)**2 - a0a2**2 
            eq3 = (vtx - a0x)**2 + (vty - a0y)**2 - a0vt**2  
            eq4 = (a2x - a1x)**2 + (a2y - a1y)**2 - a1a2**2
            eq5 = (vtx - a1x)**2 + (vty - a1y)**2 - a1vt**2
            eq6 = (vtx - a2x)**2 + (vty - a2y)**2 - a2vt**2
            return eq1**2 + eq2**2 + eq3**2 + eq4**2 + eq5**2 + eq6**2

        # Define bounds for each variable
        bounds = [(-100, 100)] * 5

        # Perform global optimization using differential evolution
        result = differential_evolution(calibration_callback, bounds)

        # Output result
        if result.success:
            a1y, a2x, a2y, vtx, vty = result.x
            
            # Update each devices calculated coordinates
            anchor0.set_calc_coordinates(a0x, a0y)
            anchor1.set_calc_coordinates(a1x, a1y)
            anchor2.set_calc_coordinates(a2x, a2y)
            victim_tag.set_calc_coordinates(vtx, vty)

            # Update the internal points object
            self.points = {
                "anchor0": (a0x, a0y),
                "anchor1": (a1x, a1y),
                "anchor2": (a2x, a2y),
                "victim": (vtx, vty)
            }
            
            print("Solution found:")

            for device in self.points:
                print(f"{device}: \t({self.points[device][0]:.3f}, {self.points[device][1]:.3f})")
        else:
            print("No solution found.")

    
    def trilateration(self):
        """Develop the trilateration algorithm here

        - uses get_distance to find the difference between the ground truths of
            each point with noise
        - uses a series of equations to calculate the coordinates of the rescuer
        - updates the rescuer's calculated points and adds/updates those 
            points in self.points
        """
        # self.points["rescuer"] = rescuer_tag.get_gt_coordinates()
        
        a0rt = get_distance(anchor0, rescuer_tag) 
        a1rt = get_distance(anchor1, rescuer_tag) 
        a2rt = get_distance(anchor2, rescuer_tag) 

        a0x, a0y = anchor0.get_calc_coordinates()
        a1x, a1y = anchor1.get_calc_coordinates()
        a2x, a2y = anchor2.get_calc_coordinates()

        def trilateration_callback(unknowns):
            rtx, rty = unknowns
            eq1 = (a0x - rtx)**2 + (a0y - rty)**2 - a0rt**2 
            eq2 = (a1x - rtx)**2 + (a1y - rty)**2 - a1rt**2 
            eq3 = (a2x - rtx)**2 + (a2y - rty)**2 - a2rt**2  
            return abs(eq1) + abs(eq2) + abs(eq3)

        # Define bounds for each variable
        bounds = [(-100, 100)] * 2

        # Perform global optimization using differential evolution
        result = differential_evolution(trilateration_callback, bounds)

        # Output result
        if result.success:
            rtx, rty = result.x

            rescuer_tag.set_calc_coordinates(rtx, rty)

            # Update the internal points object
            self.points["rescuer"] = (rtx, rty)
            
            print("Solution found:")

            for device in self.points:
                print(f"{device}: \t({self.points[device][0]:.3f}, {self.points[device][1]:.3f})")
        else:
            print("No solution found.")


    def mouse_move(self, event):
        # Every time the mouse is moved, it means that the rescuer's ground truth
        # has changed.
        
        if event.xdata is not None and event.ydata is not None:
            # Update the ground truth of the rescuer tag
            rescuer_tag.set_gt_coordinates(float(event.xdata), float(event.ydata))
            
            # Calculate the new coordinates of the rescue tag
            self.calculate_coordinates(calibration=False, trilateration=True)

        self.visual_obj.update_data(self.points)


    def main(self):
        # Establish the plot objects
        fig, ax = plt.subplots()
        self.visual_obj = UserInterface(fig, ax)

        # Determine where each static device is (the anchors and victim)
        self.calculate_coordinates(calibration=True, trilateration=False)

        self.visual_obj.update_data(self.points)
        self.visual_obj.start_animation()

        # Run the main program:
        fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)


        plt.show()
    


if __name__=="__main__":
    # Establish the initial ground truth coordinates for each device (5 total)
    anchor0 = Device(-20,20)
    anchor1 = Device(18, 15)
    anchor2 = Device(0,-19)
    victim_tag = Device(4,4)
    rescuer_tag = Device(2,2)

    # Run the main program
    obj = BaseStation()


# TODO:
# - consider shifting all coordinates so that the victim is at 0,0
# - introduce dynamic bounds for the graph
# - finish the trilateration algorithm
