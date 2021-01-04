# import cau2

    # def dx(cap_CO2air, cap_CO2top, MC_blow_air, MC_ext_air, MC_pad_air, MC_air_can, MC_air_top, MC_air_out):
    #     vCO2_air = (MC_blow_air + MC_ext_air + MC_pad_air - MC_air_can - MC_air_top - MC_air_out)/cap_CO2air
    #     vCO2_top = (MC_air_top - MC_top_out)/cap_CO2top
    #     return (vCO2_air, vCO2_top)


#   X = Co2_top
#   Y = Co2_air
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

y_true = [11,20,19,17,10]
y_approximate = [12,18,19.5,18,9]
summation = 0  
n = len(y) 
for i in range (0,n):
  difference = y_true[i] - y_approximate[i]  
  squared_difference = difference**2  
  summation = summation + squared_difference  
MSE = summation/n  
print "The Mean Square Error is: " , MSE
