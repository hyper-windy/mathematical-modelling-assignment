from cau5 import *
import csv
   
def cal_saturation_pressure(t):
    return 610.78 * exp( t / ( t + 238.3 ) * 17.2694)
    
def cal_VP(rhAir, t):
    return rhAir * cal_saturation_pressure(t) / 100.0
      
data = []
with open("Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        data.append(row)

solver = Solver()

for i in range(300):
    VP_air = cal_VP(float(data[i]["RHair"]), float(data[i]["Tair"]))
    T_air = float(data[i]["Tair"])  #air temperature
    T_out = T_air + 1               #temperature of the air outside
    T_thscr = T_air + 1             #temperature of the thermal screen
    T_top = T_air                   #temperature in the top room
    VP_out = VP_air
    VP_top = VP_air
    VP_thscr = cal_saturation_pressure(T_thscr)
    U_roof = (float(data[i]["VentLee"]) + float(data[i]["Ventwind"])) / 2 / 100.0
    U_thscr = float(data[i]["EnScr"]) / 100
    d = solver.dx(VP_air = VP_air, T_air = T_air, VP_out = VP_out, T_out = T_out, T_top = T_top, T_thscr = T_thscr, U_roof = U_roof, U_thscr = U_thscr, VP_top = VP_top, VP_thscr = VP_thscr)
    print("VP_air' = %f \t\t VP_top' = %f" %(d[0], d[1]))
