from cau5 import *
import csv
   
def cal_saturation_pressure(t):
    return 610.78 * exp( t / ( t + 238.3 ) * 17.2694)
    
def cal_VP(rhAir, t):
    return rhAir * cal_saturation_pressure(t) / 100.0
      
data = []
with open("data//Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        data.append(row)

vip = []
with open("data\\vip.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        vip.append(row)

climate = []
with open("data\\Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        climate.append(row)

meteo = []
with open("data//meteo.csv", "r") as k:
    csv_file = csv.DictReader(k)
    for row in csv_file:
        meteo.append(row)

solver = Solver()

for i in range(100):
    VP_air = cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"]))
    VP_top = VP_air

    T_air = float(climate[i]["Tair"])  # air temperature
    T_out = float(meteo[i]["Tout"])  # temperature of the air outside
    T_thscr = T_air + 1     # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    T_can = T_air + 1
    T_covin = T_air
    v_wind = float(meteo[i]["Windsp"])

    VP_can = cal_saturation_pressure(T_can)
    VP_out = cal_VP(float(meteo[i]["Rhout"]), float(meteo[i]["Tout"]))
    VP_thscr = cal_saturation_pressure(T_thscr)

    U_roof = (float(climate[i]["VentLee"]) + float(climate[i]["Ventwind"])) / 2 / 100.0
    U_thscr = float(climate[i]["EnScr"]) / 100
    # print(str(i) + ": ")
    
    d = solver.dx(VP_air=VP_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top, VP_top=VP_top,T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin)
    print("VP_air' = %f \t\t VP_top' = %f" %(d[0], d[1]))
