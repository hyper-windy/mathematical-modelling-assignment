from cau5 import *
import csv
import matplotlib.pyplot as plt
from math import sqrt


def rk4(dx, x_init, func_val, step, x_fini, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr,
        VP_can, v_wind,T_covin):
    while x_init < x_fini:
        (k1_air, k1_top) = (step * k1 for k1 in
                            dx(VP_air=func_val, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                               VP_top=VP_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr,
                               VP_can=VP_can, v_wind=v_wind,T_covin=T_covin))
        (k2_air, k2_top) = (step * k2 for k2 in
                            dx(VP_air=func_val + 0.5 * k1_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                               VP_top=VP_top + 0.5 * k1_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                               VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin))
        (k3_air, k3_top) = (step * k3 for k3 in
                            dx(VP_air=func_val + 0.5 * k2_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                               VP_top=VP_top + 0.5 * k2_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                               VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin))
        (k4_air, k4_top) = (step * k4 for k4 in
                            dx(VP_air=func_val + k3_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                               VP_top=VP_top + k3_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                               VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin))
        func_val = func_val + (1.0 / 6.0) * (k1_air + 2 * k2_air + 2 * k3_air + k4_air)
        VP_top += (1.0 / 6.0) * (k1_top + 2 * k2_top + 2 * k3_top + k4_top)
        x_init += step
    return func_val, VP_top


# Function for euler formula
def euler(dx, x_init, func_val, step, x_fini, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr,
          VP_can, v_wind, T_covin):
    while x_init < x_fini:
        (a, b) = dx(VP_air=func_val, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top, VP_top=VP_top,
                    T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr, VP_can=VP_can, v_wind=v_wind,T_covin=T_covin)
        func_val = func_val + step * a
        VP_top += step * b
        x_init += step
    return func_val, VP_top


def cal_saturation_pressure(t):
    return 610.78 * exp(t / (t + 238.3) * 17.2694)


def cal_VP(rhAir, t):
    return rhAir * cal_saturation_pressure(t) / 100.0


def toMin(timestamp):
    return round((timestamp * 24 * 3600) % 3600 / 60)


def calEndRow(timeLen, startRow):
    return startRow + timeLen // 5 + 1


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

# determine the start of the dataset
start = 0
startData = "NaN"
while startData == "NaN":
    startData = climate[start]["CO2air"]
    start += 1
start -= 1

# initialize some values
VP_air_euler = cal_VP(float(climate[start]["RHair"]), float(climate[start]["Tair"]))
VP_top_euler = VP_air_euler
VP_air_rk4 = VP_air_euler
VP_top_rk4 = VP_air_rk4
solver = Solver()
time = 0  # measure the time in minute
eulerData = []
rk4Data = []
expectedData = []
timeline = []

mse_euler = 0
mse_rk4 = 0
VP_mean = 0

timeLength = 60 * 24 * 7  # perform the prediction in 2 days (time measured in minute)
end = calEndRow(timeLength, start)  # the last row that we'll use in the dataset
result_euler = open("ex5_4_euler.csv", "w+")
result_rk4 = open("ex5_4_rk4.csv", "w+")
fieldnames = ["GHtime", "Current VP_air", "Next VP_air", "Predicted VP_air", "Predicted VP_top"]

writer_euler = csv.DictWriter(result_euler, fieldnames=fieldnames)
writer_rk4 = csv.DictWriter(result_rk4, fieldnames=fieldnames)
writer_euler.writeheader()
writer_rk4.writeheader()
for i in range(start, end):
    expectedData.append(cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"])))
    timeline.append(time)
    eulerData.append(VP_air_euler)
    rk4Data.append(VP_air_rk4)

    T_air = float(climate[i]["Tair"])  # air temperature
    T_out = float(meteo[i]["Tout"])  # temperature of the air outside
    T_thscr = T_air + 1  # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    T_can = T_air + 1
    T_covin = T_air
    v_wind = float(meteo[i]["Windsp"])

    VP_can = cal_saturation_pressure(T_can)
    VP_out = cal_VP(float(meteo[i]["Rhout"]), float(meteo[i]["Tout"]))
    VP_thscr = cal_saturation_pressure(T_thscr)

    U_roof = (float(climate[i]["VentLee"]) + float(climate[i]["Ventwind"])) / 2 / 100.0
    U_thscr = float(climate[i]["EnScr"]) / 100
    # print(str(i) + ": "),
    (VP_air_euler, VP_top_euler) = euler(solver.dx, time*60, VP_air_euler, 10, (time + 5)*60, T_air, VP_out, T_out, T_top, VP_top_euler,
                                         T_thscr, U_roof,
                                         U_thscr, VP_thscr, VP_can, v_wind, T_covin)
    VP_air_expected = cal_VP(float(climate[i + 1]["RHair"]), float(climate[i + 1]["Tair"]))

    (VP_air_rk4, VP_top_rk4) = rk4(solver.dx, time*60, VP_air_rk4, 10, (time + 5)*60, T_air, VP_out, T_out, T_top, VP_top_rk4,
                                   T_thscr, U_roof,
                                   U_thscr, VP_thscr, VP_can, v_wind, T_covin)
    mse_euler += (VP_air_expected - VP_air_euler) ** 2
    mse_rk4 += (VP_air_expected - VP_air_rk4) ** 2
    VP_mean += cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"]))
    writer_euler.writerow({"GHtime": climate[i]["GHtime"],"Current VP_air": cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"])),
                           "Next VP_air": VP_air_expected, "Predicted VP_air": VP_air_euler,
                           "Predicted VP_top": VP_top_euler})
    writer_rk4.writerow({"GHtime": climate[i]["GHtime"],
                           "Current VP_air": cal_VP(float(climate[i]["RHair"]), float(climate[i]["Tair"])),
                           "Next VP_air": VP_air_expected, "Predicted VP_air": VP_air_rk4,
                           "Predicted VP_top": VP_top_rk4})

    time += 5

mse_euler = mse_euler / (end - start)
mse_rk4 = mse_rk4 / (end - start)
VP_mean = VP_mean / (end - start)

rrmse_euler = sqrt(mse_euler) / VP_mean * 100.0
rrmse_rk4 = sqrt(mse_rk4)/ VP_mean * 100.0

print("RRMSE of Euler method: %f"%(rrmse_euler) + "%")
print("RRMSE of RK4 method: %f"%(rrmse_rk4) + "%")

plt.plot(timeline, expectedData, label="Expected")
plt.plot(timeline, eulerData, label="Euler")
plt.plot(timeline, rk4Data, label="RK4")
plt.legend()
plt.show()
