from cau5 import *
import csv


def rk4(dx, x_init, func_val, step, x_fini, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr):
    while x_init < x_fini:
        (k1_air, k1_top) = (step * k1 for k1 in dx(VP_air=func_val, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                                     VP_top=VP_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr))
        (k2_air, k2_top) = (step * k2 for k2 in dx(VP_air=func_val + 0.5 * k1_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                                  VP_top=VP_top + 0.5 * k1_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                                  VP_thscr=VP_thscr))
        (k3_air, k3_top) = (step * k3 for k3 in dx(VP_air=func_val + 0.5 * k2_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                                  VP_top=VP_top + 0.5 * k2_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                                  VP_thscr=VP_thscr))
        (k4_air, k4_top) = (step * k4 for k4 in dx(VP_air=func_val + 0.5 * k3_air, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top,
                                  VP_top=VP_top + 0.5 * k3_top, T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr,
                                  VP_thscr=VP_thscr))
        func_val = func_val + (1.0 / 6.0) * (k1_air + 2 * k2_air + 2 * k3_air + k4_air)
        VP_top += (1.0 / 6.0) * (k1_top + 2 * k2_top + 2 * k3_top + k4_top)
        x_init += step
    return func_val, VP_top


# Function for euler formula
def euler(dx, x_init, func_val, step, x_fini, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof, U_thscr, VP_thscr):
    while x_init < x_fini:
        (a, b) = dx(VP_air=func_val, T_air=T_air, VP_out=VP_out, T_out=T_out, T_top=T_top, VP_top=VP_top,
                    T_thscr=T_thscr, U_roof=U_roof, U_thscr=U_thscr, VP_thscr=VP_thscr)
        func_val = func_val + step * a
        VP_top += step * b
        x_init += step
    return func_val, VP_top


def cal_saturation_pressure(t):
    return 610.78 * exp(t / (t + 238.3) * 17.2694)


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
solver = Solver()
# print(VP_air)
Vp_air_compare = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))  # extract VP_air value from the dataset
# print(VP_air_compare)
VP_top = VP_air

for i in range(15):
    T_air = float(data[i]["Tair"])  # air temperature
    T_out = T_air + 1  # temperature of the air outside
    T_thscr = T_air + 1  # temperature of the thermal screen
    T_top = T_air  # temperature in the top room
    VP_out = VP_air
    VP_thscr = cal_saturation_pressure(T_thscr)
    U_roof = (float(data[i]["VentLee"]) + float(data[i]["Ventwind"])) / 2 / 100.0
    U_thscr = float(data[i]["EnScr"]) / 100
    # d = solver.dx(VP_air = VP_air, T_air = T_air, VP_out = VP_out, T_out = T_out, T_top = T_top, T_thscr = T_thscr, U_roof = U_roof, U_thscr = U_thscr, VP_top = VP_top, VP_thscr = VP_thscr)[0]
    (VP_air, VP_top) = rk4(solver.dx, 0, VP_air, 2.5, 5, T_air, VP_out, T_out, T_top, VP_top, T_thscr, U_roof,
                             U_thscr, VP_thscr)
    print("Current VP: %f\t\tNext VP:%f\t RK4: %f" % (cal_VP(float(data[i]["RHair"]), float(data[i]["Tair"])),
                                                        cal_VP(float(data[i + 1]["RHair"]), float(data[i + 1]["Tair"])),
                                                        VP_air))
