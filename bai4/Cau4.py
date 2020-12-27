import csv
def rk4(dx, x0, y0, x, h): 
    # Count number of iterations using step size or 
    # step height h 
    n = (int)((x - x0)/h)  
    # Iterate for number of iterations 
    y = y0 
    for i in range(1, n + 1): 
        k1 = h * dx(x0, y) 
        k2 = h * dx(x0 + 0.5 * h, y + 0.5 * k1) 
        k3 = h * dx(x0 + 0.5 * h, y + 0.5 * k2) 
        k4 = h * dx(x0 + h, y + k3) 
  
        # Update next value of y 
        y = y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 
  
        # Update next value of x 
        x0 = x0 + h 
    return y 

# Function for euler formula 
def euler(dx, x0, y, h, x ): 
    temp = -0
  
    # Iterating till the point at which we 
    # need approximation 
    while x0 < x: 
        temp = y 
        y = y + h * dx(x0, y) 
        x0 = x0 + h
  
    return y
    
