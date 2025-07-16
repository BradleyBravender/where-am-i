import numpy as np
from scipy.optimize import differential_evolution



a0x, a0y, a1x = 0, 0, 0

class Test():
    def __init__(self):
        self.calculate_coordinates()


    def objective(self, vars) -> float:
        a0x, a0y, a1x = 0, 0, 0
        a1y, a2x, a2y, vtx, vty = vars
        
        eq1 = (a1x - a0x)**2 + (a1y - a0y)**2 - self.a0a1**2 
        eq2 = (a2x - a0x)**2 + (a2y - a0y)**2 - self.a0a2**2 
        eq3 = (vtx - a0x)**2 + (vty - a0y)**2 - self.a0vt**2  
        eq4 = (a2x - a1x)**2 + (a2y - a1y)**2 - self.a1a2**2
        eq5 = (vtx - a1x)**2 + (vty - a1y)**2 - self.a1vt**2
        eq6 = (vtx - a2x)**2 + (vty - a2y)**2 - self.a2vt**2
        
        return eq1**2 + eq2**2 + eq3**2 + eq4**2 + eq5**2 + eq6**2


    def calculate_coordinates(self):
        # Distance constraints
        self.a0a1 = 3.0734396317134607
        self.a0a2 = 4.997924975368032
        self.a0vt = 2.342934456946655
        self.a1a2 = 7.767700984912579
        self.a1vt = 2.805802078272575
        self.a2vt = 4.939391758591277

        # Define bounds for each variable (x1, y1, ..., y4)
        bounds = [(-100, 100)] * 5

        # Perform global optimization using differential evolution
        result = differential_evolution(self.objective, bounds)

        # Output result
        if result.success:
            print(result.x)
            a1y, a2x, a2y, vtx, vty = result.x
            print("Solution found:")
            print(f"({a0x:.3f}, {a0y:.3f}), ({a1x:.3f}, {a1y:.3f}), ({a2x:.3f}, {a2y:.3f}), ({vtx:.3f}, {vty:.3f})")
        else:
            print("No solution found.")

# Run the calculation
calculate_coordinates()
