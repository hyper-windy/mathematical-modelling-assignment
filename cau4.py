import ex2_old

def euler(dx, x0, y0, h, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out):
    k,l = h*dx(x0, y0, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)
    x0 += k
    y0 += l
    return x0, y0


def rk4(dx, x0, y0, h, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out):
    k1, l1 = h*dx(x0, y0, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)
    k2, l2 = h*dx(x0+k1/2,y0+l1/2, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)
    k3, l3 = h*dx(x0+k2/2,y0+l2/2, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)
    k4, l4 = h*dx(x0+k3,y0+l3, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)
    x0 += (k1 + 2* k2 + 2*k3 + k4)/6
    y0 += (l1 + 2* l2 + 2*l3 + l4)/6
    return x0 , y0


def rk4_main(dx, x0, y0, h, t_finish, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out):
    # 5 minute  = 300 s
    # step = 10s
    loop = t_finish/h
    a ,b = x0 , y0
    for i in range(loop):
        a,b  = rk4(dx, a, b, h, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)

    return a,b

def euler_main(dx, x0, y0, h, t_finish, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out):
    loop = t_finish/h
    a ,b = x0 , y0
    for i in range(loop):
        a,b  = euler(dx, a, b, h, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out)

    return a,b

### mean squared error
data = []
with open("Greenhouse_climate.csv", "r") as f:
    csv_file = csv.DictReader(f)
    for row in csv_file:
        data.append(row)
VP_air = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))
VP_top = VP_air
VP_air_compare = VP_air
solver = Solver()
Vp_air_compare = cal_VP(float(data[0]["RHair"]), float(data[0]["Tair"]))  # extract VP_air value from the dataset
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

'''y_true = [11,20,19,17,10]
y_approximate = [12,18,19.5,18,9]
summation = 0  
n = len(y) 
for i in range (0,n):
  difference = y_true[i] - y_approximate[i]  
  squared_difference = difference**2  
  summation = summation + squared_difference  
MSE = summation/n  
print "The Mean Square Error is: " , MSE'''
