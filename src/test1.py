import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# Global variable to track mouse position
cursor_pos = (0, 0)

class UserInterface:
    
    def __init__(self, fig, ax):
        self.ax = ax
        self.fig = fig
        self.points = {}
        

    def update_data(self, points_dict):
        print("update_data: ",self.points)
        self.points = points_dict


    def animate(self, frame):
        print("ANIMATE: ",self.points)
        """Animation function called at each frame."""
        #ADD LINES BETWEEN ALL POINTS AND RESCUER WITH DISTANCES.
            #Start with just lines
            #Move to distances after (have to pull from basestation)
        self.ax.clear()
        # Set axis limits (could dynamically calculate from points if needed)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)

        updated_artists = []

        for label, (x, y) in self.points.items():
            if x is not None and y is not None:
                print(x,y)
                scatter = self.ax.scatter(x, y, label=label)
                text = self.ax.text(x + 0.1, y + 0.1, label, fontsize=9)
                #Append the artists
                updated_artists.append(scatter)
                updated_artists.append(text)
                
        legend = self.ax.legend(loc="upper right")
        updated_artists.append(legend)

        return updated_artists
    
    def start_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)


class BaseStation:

    def __init__(self, anchor_dict):
        self.points = anchor_dict
        self.main()


    def mouse_move(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.rescuer_tuple = (float(event.xdata), float(event.ydata))
            self.on_mouse_move(self.rescuer_tuple)


    def on_mouse_move(self, coordinates):
        # This function will eventually measure the distances to the rescuer,
        # calculate the rescuer's position, and update the points dictionary for 
        # the new rescuers position.
        self.points["rescuer"] = coordinates
        self.visual_obj.update_data(self.points)


    def main(self):
        # Create figure and axes
        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

        self.visual_obj = UserInterface(fig, ax)
        self.visual_obj.update_data(self.points)
        self.visual_obj.start_animation()
        
        # Mouse motion event handler
        fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)

        plt.show()
        


if __name__=="__main__":
    anchor_dict = {
        "anchor0": (0,0),
        "anchor1": (5,8),
        "anchor2": (9,2)
    }

    obj = BaseStation(anchor_dict)
