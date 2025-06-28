import math

# Given distances
AB = 8
AC = 19.4
AD = 25.6
BC = 25.5
BD = 21
CD = 45

# Fix A and B
Ax, Ay = 0.0, 0.0
Bx, By = AB, 0.0

# Step 1: Calculate coordinates of C
# Using:
# x_C = (AB^2 + AC^2 - BC^2) / (2 * AB)
# y_C = sqrt(AC^2 - x_C^2)

xC = (AB**2 + AC**2 - BC**2) / (2 * AB)
yC_squared = AC**2 - xC**2

if yC_squared < 0:
    raise ValueError("Invalid distances: Cannot compute yC (imaginary result)")
yC = math.sqrt(yC_squared)  # Choose the upper half-plane

# Step 2: Brute-force search for point D = (xD, yD)
best_guess = None
min_error = float('inf')

step = 0.01  # Resolution of search

for xD in [i * step for i in range(0, int(AB * 2 / step))]:
    for yD in [j * step for j in range(-int(AB * 2 / step), int(AB * 2 / step))]:
        # Distances from D to other points
        dAD = math.hypot(xD - Ax, yD - Ay)
        dBD = math.hypot(xD - Bx, yD - By)
        dCD = math.hypot(xD - xC, yD - yC)

        # Compute squared error from desired distances
        error = (dAD - AD)**2 + (dBD - BD)**2 + (dCD - CD)**2

        if error < min_error:
            min_error = error
            best_guess = (xD, yD)

xD, yD = best_guess

# Output results
print(f"A = (0.00, 0.00)")
print(f"B = ({Bx:.2f}, 0.00)")
print(f"C = ({xC:.2f}, {yC:.2f})")
print(f"D ≈ ({xD:.2f}, {yD:.2f}) with error {min_error:.6f}")
