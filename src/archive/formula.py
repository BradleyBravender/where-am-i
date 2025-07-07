'''
import numpy as np
from scipy.optimize import root

def equations(vars):
    x1, y1, x2, y2, x3, y3, x4, y4 = vars	
    # Replace these with your actual equations
    eq1 = (x2 - x1)**2 + (y2 - y1)**2 - a**2 
    eq2 = (x3 - x1)**2 + (y3 - y1)**2 - b**2 
    eq3 = (x4 - x1)**2 + (y4 - y1)**2 - c**2  
    eq4 = (x3 - x2)**2 + (y3 - y2)**2 - d**2
    eq5 = (x4 - x2)**2 + (y4 - y2)**2 - e**2
    eq6 = (x4 - x3)**2 + (y4 - y3)**2 - f**2
    print(x1, y1)
    
    return [eq1, eq2, eq3, eq4, eq5, eq6]

a, b, c, d, e, f = 5, 5, 3.16227766017, 4.472135955, 2.2360679775, 5
initial_guess = [0, 0, 1, 1, 1, 0, 1, 1]
sol = root(equations, initial_guess)

print(sol.x) 
''' 


import numpy as np
from scipy.optimize import differential_evolution

# Define the equation residuals (objective function to minimize)
def objective(vars):
    x1, y1, y3 = 0, 0, 0
    x2, y2, x3, x4, y4 = vars	
    eq1 = (x2 - x1)**2 + (y2 - y1)**2 - a**2 
    eq2 = (x3 - x1)**2 + (y3 - y1)**2 - b**2 
    eq3 = (x4 - x1)**2 + (y4 - y1)**2 - c**2  
    eq4 = (x3 - x2)**2 + (y3 - y2)**2 - d**2
    eq5 = (x4 - x2)**2 + (y4 - y2)**2 - e**2
    eq6 = (x4 - x3)**2 + (y4 - y3)**2 - f**2
    # Minimize the sum of squares of residuals
    return eq1**2 + eq2**2 + eq3**2 + eq4**2 + eq5**2 + eq6**2

# Distance constraints
a, b, c, d, e, f = 5, 5, 3.16227766017, 4.472135955, 2.2360679775, 5

# Define bounds for each variable (x1, y1, ..., y4)
bounds = [(0, 10)] * 5

# Perform global optimization
result = differential_evolution(objective, bounds)

# Output
x1, y1, y3 = 0, 0, 0
if result.success:
    print(result.x)
    x2, y2, x3, x4, y4 = result.x
    print("Solution found:")
    print(f"({x1:.3f}, {y1:.3f}), ({x2:.3f}, {y2:.3f}), ({x3:.3f}, {y3:.3f}), ({x4:.3f}, {y4:.3f})")
else:
    print("No solution found.")
