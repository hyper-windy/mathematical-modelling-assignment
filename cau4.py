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

def rk4(dx, x_init, func_val, step, x_fini, CO2_out, CO2_top, T_air, T_top, T_out, T_can, v_wind):
    while x_init < x_fini:
        (k1_air, k1_top) = (step * k1 for k1 in
                            dx(CO2_out=CO2_out, CO2_air=func_val, CO2_top=CO2_top, T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind))
        (k2_air, k2_top) = (step * k2 for k2 in
                            dx(CO2_out=CO2_out, CO2_air=func_val+0.5*k1_air, CO2_top=CO2_top+0.5*k1_top, T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind))
        (k3_air, k3_top) = (step * k3 for k3 in
                            dx(CO2_out=CO2_out, CO2_air=func_val+0.5*k2_air, CO2_top=CO2_top+0.5*k2_top, T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind))
        (k4_air, k4_top) = (step * k4 for k4 in
                            dx(CO2_out=CO2_out, CO2_air=func_val+0.5*k3_air, CO2_top=CO2_top+0.5*k3_top, T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind))
        func_val = func_val + (1.0 / 6.0) * (k1_air + 2 * k2_air + 2 * k3_air + k4_air)
        CO2_top += (1.0 / 6.0) * (k1_top + 2 * k2_top + 2 * k3_top + k4_top)
        x_init += step
    return func_val, CO2_top


# Function for euler formula
def euler(dx, x_init, func_val, step, x_fini, CO2_out, CO2_top, T_air, T_top, T_out, T_can, v_wind):
    #print(CO2_top)
    while x_init < x_fini:
        # (a, b) = dx(CO2_out=CO2_out, CO2_air=func_val, CO2_top=CO2_top, T_air=T_air, T_top=T_top, T_out=T_out, T_can=T_can, v_wind=v_wind)
        (a, b) = (step * k1 for k1 in
                            dx(CO2_out=CO2_out, CO2_air=func_val, CO2_top=CO2_top, T_air=T_air, T_top=T_top,
                               T_out=T_out, T_can=T_can, v_wind=v_wind))
        #print("dx a: " + str(a))
        #print("dx b: " + str(b))
        func_val = func_val + a
        CO2_top += b
        x_init += step
    return func_val, CO2_top

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
CO2_air_euler = convertPPM(float(climate[start]["CO2air"]))     #divide by 1000 to convert ppm to mg/m^3
CO2_top_euler = CO2_air_euler
CO2_air_rk4 = CO2_air_euler
CO2_top_rk4 = CO2_air_rk4
solver = Dynamic()
time = 0  # measure the time in minute
eulerData = []
rk4Data = []
expectedData = []
timeline = []

mse_euler = 0
mse_rk4 = 0
CO2_mean = 0

timeLength = 24*60*7  # perform the prediction in 2 days (time measured in minute)
end = calEndRow(timeLength, start)  # the last row that we'll use in the dataset
result_euler = open("ex4_euler.csv", "w+")
result_rk4 = open("ex4_rk4.csv", "w+")
fieldnames = ["GHtime", "Current CO2_air", "Next CO2_air", "Predicted CO2_air", "Predicted CO2_top"]

writer_euler = csv.DictWriter(result_euler, fieldnames=fieldnames)
writer_rk4 = csv.DictWriter(result_rk4, fieldnames=fieldnames)
writer_euler.writeheader()
writer_rk4.writeheader()

for i in range(start, end):
    expectedData.append(convertPPM(float(climate[i]["CO2air"])))
    timeline.append(time)
    eulerData.append(CO2_air_euler)
    rk4Data.append(CO2_air_rk4)

    T_air = float(climate[i]["Tair"])  # air temperature
    T_out = float(meteo[i]["Tout"])  # temperature of the air outside
    T_thscr = T_air - 1  # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    T_can = T_air - 1
    T_covin = T_air
    v_wind = float(meteo[i]["Windsp"])
    solver.URoof = (float(climate[i]["VentLee"]) + float(climate[i]["Ventwind"])) / 2 / 100.0
    solver.U_Thscr = float(climate[i]["EnScr"]) / 100.0

    CO2_out = convertPPM(409.8)   #from van11

    (CO2_air_euler, CO2_top_euler) = euler(solver.dx, time, CO2_air_euler, 0.5, (time + 5), CO2_out, CO2_top_euler, T_air, T_top, T_out, T_can, v_wind)


    (CO2_air_rk4, CO2_top_rk4) = rk4(solver.dx, time, CO2_air_rk4, 0.5, (time + 5), CO2_out, CO2_top_rk4, T_air, T_top, T_out, T_can, v_wind)

    CO2_expected = convertPPM(float(climate[i + 1]["CO2air"]))
    mse_euler += (CO2_expected - CO2_air_euler) ** 2
    mse_rk4 += (CO2_expected - CO2_air_rk4) ** 2
    CO2_mean += convertPPM(float(climate[i]["CO2air"]))

    writer_euler.writerow({"GHtime": climate[i]["GHtime"],"Current CO2_air": convertPPM(float(climate[i]["CO2air"])),
                           "Next CO2_air": CO2_expected, "Predicted CO2_air": CO2_air_euler,
                           "Predicted CO2_top": CO2_top_euler})
    writer_rk4.writerow({"GHtime": climate[i]["GHtime"],
                           "Current CO2_air": convertPPM(float(climate[i]["CO2air"])),
                           "Next CO2_air": CO2_expected, "Predicted CO2_air": CO2_air_rk4,
                           "Predicted CO2_top": CO2_top_rk4})

    time += 5

CO2_mean = CO2_mean / (end - start)
rrmse_euler = sqrt(mse_euler) / CO2_mean * 100.0
rrmse_rk4 = sqrt(mse_rk4)/ CO2_mean * 100.0

print("RRMSE of Euler method: %f"%(mse_euler) + "%")
print("RRMSE of RK4 method: %f"%(mse_rk4) + "%")


plt.plot(timeline, expectedData, label="Expected")
plt.plot(timeline, eulerData, label="Euler")
plt.plot(timeline, rk4Data, label="RK4")
plt.legend()
plt.show()