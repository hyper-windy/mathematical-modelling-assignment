def rk4(dx, x0, y0, h): 

    y = y0 

    k1 = h * dx(x0, y) 
    k2 = h * dx(x0 + 0.5 * h, y + 0.5 * k1) 
    k3 = h * dx(x0 + 0.5 * h, y + 0.5 * k2) 
    k4 = h * dx(x0 + h, y + k3) 

    return y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 

####################
def euler(dx, x0, y, h): 
  
    return y + h * dx(x0, y)

def dydx(x, y): 
    return ((x - y)/2)  
def rungeKutta(x0, y0, x, h): 
    # Count number of iterations using step size or 
    # step height h 
    n = (int)((x - x0)/h)  
    # Iterate for number of iterations 
    y = y0 
    for i in range(1, n + 1): 
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * dydx(x0, y) 
        k2 = h * dydx(x0 + 0.5 * h, y + 0.5 * k1) 
        k3 = h * dydx(x0 + 0.5 * h, y + 0.5 * k2) 
        k4 = h * dydx(x0 + h, y + k3) 
  
        # Update next value of y 
        y = y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 
  
        # Update next value of x 
        x0 = x0 + h 
    return y 
    ######################
def func( x, y ): 
    return (x + y + x * y) 
      
# Function for euler formula 
def euler( x0, y, h, x ): 
    temp = -0
  
    # Iterating till the point at which we 
    # need approximation 
    while x0 < x: 
        temp = y 
        y = y + h * func(x0, y) 
        x0 = x0 + h 
  
    # Printing approximation 
    print("Approximate solution at x = ", x, " is ", "%.6f"% y) 
