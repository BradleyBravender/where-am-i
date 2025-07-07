import numpy as np
from scipy.optimize import minimize

# Distance constraints
a, b, c, d, e, f = 2.972779248055132, 3.0106849632221797, 1.4386494330444406, 4.069333246555455, 2.2319091570060703, 2.180491500216066

a0x, a0y, a1x = 0, 0, 0

# Define the equation residuals (objective function to minimize)
def objective(vars):
    a0x, a0y, a1x = 0, 0, 0
    a1y, a2x, a2y, vtx, vty = vars
    eq1 = (a1x - a0x)**2 + (a1y - a0y)**2 - a**2 
    eq2 = (a2x - a0x)**2 + (a2y - a0y)**2 - b**2 
    eq3 = (vtx - a0x)**2 + (vty - a0y)**2 - c**2  
    eq4 = (a2x - a1x)**2 + (a2y - a1y)**2 - d**2
    eq5 = (vtx - a1x)**2 + (vty - a1y)**2 - e**2
    eq6 = (vtx - a2x)**2 + (vty - a2y)**2 - f**2
    # Minimize the sum of squares of residuals
    return eq1**2 + eq2**2 + eq3**2 + eq4**2 + eq5**2 + eq6**2

def calculate_coordinates():
    # Initial guess for the unknowns
    initial_guess = [0, 0, 1, 1, 1]  # [a1y, a2x, a2y, vtx, vty]
    
    # Perform local optimization using 'BFGS' method
    result = minimize(objective, initial_guess, method='BFGS')

    # Output result
    if result.success:
        print("Solution found:")
        a1y, a2x, a2y, vtx, vty = result.x
        print(f"({a0x:.3f}, {a0y:.3f}), ({a1x:.3f}, {a1y:.3f}), ({a2x:.3f}, {a2y:.3f}), ({vtx:.3f}, {vty:.3f})")
    else:
        print("No solution found.")

# Run the calculation
calculate_coordinates()
