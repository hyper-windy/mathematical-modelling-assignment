def rk4(dx, x0, y0, h): 

    y = y0 

    k1 = h * dx(x0, y) 
    k2 = h * dx(x0 + 0.5 * h, y + 0.5 * k1) 
    k3 = h * dx(x0 + 0.5 * h, y + 0.5 * k2) 
    k4 = h * dx(x0 + h, y + k3) 

    return y + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4) 

####################
def euler(dx, x0, y, h): 

    y = y + h * dx(x0, y) 
  
    return y
