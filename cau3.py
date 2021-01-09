from ex2 import *
import csv
import matplotlib.pyplot as plt
from math import sqrt

climate = []
with open("data\\Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        climate.append(row)
vip = []
with open("data\\vip.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        vip.append(row)

meteo = []
with open("data\\meteo.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        meteo.append(row)

def toMin(timestamp):
    return round((timestamp * 24 * 3600) % 3600 / 60)

def convertPPM(num):
    return 0.0409 * num * 44.01

def calEndRow(timeLen, startRow):
    return startRow + timeLen // 5 + 1

# determine the start of the dataset
start = 0
startData = "NaN"
while startData == "NaN":
    startData = climate[start]["CO2air"]
    start += 1
start -= 1

# initialize some values
solver = Dynamic()
time = 0  # measure the time in minute


timeLength = 24*60*7  # perform the prediction in 2 days (time measured in minute)
end = calEndRow(timeLength, start)  # the last row that we'll use in the dataset
result = open("ex3.csv", "w+")
fieldnames = ["GHtime", "Current CO2_air", "CO2_air'", "CO2_top'"]

writer = csv.DictWriter(result, fieldnames=fieldnames)
writer.writeheader()
for i in range(start, end):
    T_air = float(climate[i]["Tair"])  # air temperature
    T_out = float(meteo[i]["Tout"])  # temperature of the air outside
    T_thscr = T_air + 1  # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    T_can = T_air + 1

    T_covin = T_air
    v_wind = float(meteo[i]["Windsp"])

    CO2_out = 668   #from van11

    solver.URoof = (float(climate[i]["VentLee"]) + float(climate[i]["Ventwind"])) / 2 / 100.0
    solver.U_Thscr = float(climate[i]["EnScr"]) / 100.0


    (a, b) = solver.dx(CO2_out=CO2_out, CO2_air=convertPPM(float(climate[i]["CO2air"])), CO2_top=convertPPM(float(climate[i]["CO2air"])), T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind)
    writer.writerow({"GHtime": climate[i]["GHtime"],"Current CO2_air": convertPPM(float(climate[i]["CO2air"])),
                           "CO2_air'": a, "CO2_top'": b})


    time += 5
