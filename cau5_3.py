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
result = open("ex5_3.csv", "w+")
fieldnames = ["GHtime", "Current VP_air", "VP_air'", "VP_top'"]

writer = csv.DictWriter(result, fieldnames=fieldnames)
writer.writeheader()

for i in range(10):
    VP_air = cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"]))
    VP_top = VP_air #Gia dinh

    T_air = float(climate[i]["Tair"])  # air temperature
    T_out = float(meteo[i]["Tout"])  # temperature of the air outside

    T_thscr = T_air     # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    T_can = T_air   #Gia dinh chenh lech nhiet do khong doi
    T_covin = T_air #Gia dinh lech nhiet do khong doi

    ########### TINH TOAN BANG CONG THUC TUONG UNG
    v_wind = float(meteo[i]["Windsp"])
    VP_can = cal_saturation_pressure(T_can)
    VP_out = cal_VP(float(meteo[i]["Rhout"]), float(meteo[i]["Tout"]))
    VP_thscr = cal_saturation_pressure(T_thscr)
    U_roof = (float(climate[i]["VentLee"]) + float(climate[i]["Ventwind"])) / 2 / 100.0
    U_thscr = float(climate[i]["EnScr"]) / 100
    # print(str(i) + ": "),
    
    (a, b) = solver.dx(VP_air=VP_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top, VP_top=VP_air,T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin)
    writer.writerow({"GHtime": climate[i]["GHtime"],"Current VP_air": VP_air,
                           "VP_air'": a, "VP_top'": b})
