def rk4(dx, x0, y0, h): 

    y = y0 

    k1 = h * dx(x0, y) 
    k2 = h * dx(x0 + 0.5 * h, y + 0.5 * k1) 
    k3 = h * dx(x0 + 0.5 * h, y + 0.5 * k2) 
    k4 = h * dx(x0 + h, y + k3) 

    return y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 

####################
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
      
# Driver Code 
# Initial Values 
x0 = 0
y0 = 1
h = 0.025
  
# Value of x at which we need approximation 
x = 0.1
  
euler(x0, y0, h, x) 
