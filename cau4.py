from cau5 import *
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
   
def cal_saturation_pressure(t):
    return 610.78 * exp( t / ( t + 238.3 ) * 17.2694)
    
def cal_VP(rhAir, t):
    return rhAir * cal_saturation_pressure(t) / 100.0
      
data = []
with open("Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        data.append(row)
VP_air = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))
VP_top = VP_air
VP_air_compare = VP_air
VP_out = VP_air
solver = Solver()
for i in range(24):
    Vp_air_compare = cal_VP(float(data[i]["RHair"]), float(data[i]["Tair"]))
    T_air = float(data[i]["Tair"])
    T_out = T_air + 1
    T_thscr = T_air + 1
    T_top = T_air
    U_roof = (float(data[i]["VentLee"]) + float(data[i]["Ventwind"])) / 2 / 100
    U_thscr = float(data[i]["EnScr"]) / 100
    #(Vp_air, VP_top) = rk4()
    d = solver.dx(VP_air = VP_air, T_air = T_air, VP_out = VP_out , T_out = T_out, T_top = T_top, T_thscr = T_thscr, U_roof = U_roof, U_thscr = U_thscr)
    print(d)