from math import exp
##Du lieu lay o Netherland

n_heatCO2 = 0.057
n_heatVap = 4.43 * (10 ** (-8))
n_insScr = 1
n_side = 0
n_sideThr = -1
n_pad =-1
h_elevation = 0 #do cao nha kinh o netherland

###########

C_maxBuf = -1
C_buf = -1
C_d = -1
C_w = -1
###########
h_roof = 0
h_sideRoof = 0
h_vent = 0.68
h_air = 3.8
h_Gh = 4.2
h_flr = 0.02
h_Cbuf = -1
h_blowAir = -1

###########
A_flr = 1.4 * (10 ** 4)
A_roof = 0.1 * A_flr
A_side = -1
###########
o_fog = 0
o_pad = 16.7
o_ventForce = 0
o_exitCO2 = 7.2 * (10 ** 4)

###########
s_insScr = 1

###########
p_water = 1000
p_thrScr = 0.2 * (10**3)
p_flr = 2300
p_air = -1
p_blow = -1
p_top = -1
p_air_mean = -1
###########
r_b = 275
rs_min = 82
r_s = -1
s_r_s = -1

###########
e_flr = 1
e_can = 1
e_sky = 1

###########
M_water = 18
M_air = 28.96
M_ch2o = 30

###########
c_leakage = 10**-4
c_pFlr = 0.88 * (10 ** 3)
c_pThr = 1.8 * (10 ** 3)
c_pAir = 10**3

###########
y = 65.8
w = 1.99 * (10 **-7)
R = 8314
o = 5.670 * (10 ** -8)
P = -1
P_blow = -1

###########
landa_flr = 1.7

g = 9.81

delta_H = 2.45 * (10 ** 6)

K_thScr = 0.05 * (10 ** -3)

cap_leaf = 1200
s_MV12 = -0.1

####################
# Tinh cac gia tri can thiet
VP_airWinter = 5.7
VP_airSummer = 6.4
VP_outWinter = 0.7
VP_outSummer = 1.5

T_airWinter = 5.7
T_airSummer = 6.2
T_outWinter = 5.9
T_outSummer = 15.2

v_windWinter = 2.4
v_windSummer = 4.6

CO2_air = -1
CO2_top = -1

P_qh = -1
R_qh = -1

###################
R = 8.3144598 * 1000 # molar gas constant (J*kmol^-1 * K^-1
delta_H = 2.45 * (10 ** 6)  #nhiet hoa hoi rieng cua nuoc
M_air = 28.96               #molar mass of water
p_air0 = 1.20               #density of the air at sea level
n_heatVap = 4.43 * (10 ** (-8))
g = 9.81                    #acceleration of gravity
r_b = 275                   #boundary layer resistance
C_d_Gh = 0.75
C_w_Gh = 0.09
n_roofThr = 0.9
c_HECin = 1.86
COP_mechcool = 0
P_mechcool = 0


class Solver:
    def __init__(self, h_elevation = 0, A_flr = 1.4 * (10 ** 4), A_roof = 1.4*(10**3), A_side = 0, A_cov = 1.8 * (10 ** 4), h_air = 3.8, h_gh = 4.2, P_blow = 0, o_fog = 0, o_pad = 16.7, n_pad = 1, c_leakage = 10**-4,K_thScr = 0.05 * (10 ** -3), C_d = 0.75, C_w = 0.09, h_sideRoof = 0,h_vent = 0.68, n_insScr = 1, o_ventForce = 0):
        self.h_elevation = h_elevation  #do cao nha kinh so voi muc nuoc bien
        self.p_Air = self.p_air(self.h_elevation)    #density of the greenhouse air
        self.h_air = h_air      #chieu cao gian duoi
        self.p_Top = self.p_air(self.h_elevation + self.h_air)   #density of the air in the top room
        self.A_flr = A_flr      #dien tich nha kinh
        self.A_roof = A_roof
        self.A_side = A_side
        self.A_cov = A_cov
        self.h_top = h_gh - h_air      #chieu cao gian tren
        self.P_blow = P_blow    #kha nang sinh hoi nuoc cua may suoi
        self.o_fog = o_fog      #suc chua he thong phun suong
        self.o_pad = o_pad      #kha nang cho hoi nuoc di qua cua tam thong gio
        self.n_pad = n_pad      #hieu suat cua he thong thong gio (trong sach khong co cai nay)
        #x_out va x_air: khong ro   
        self.c_leakage = c_leakage  #do ro cua luoi
        self.K_thScr = K_thScr      #thermal screen flux coefficient
        self.C_d = C_d
        self.C_w = C_w
        self.h_sideRoof = h_sideRoof
        self.h_vent = h_vent
        self.n_insScr = n_insScr
        self.o_ventForce = o_ventForce
        
        
        
###################
    def p_air(self, elevate):
        return p_air0 * exp(g * M_air * elevate /(293.15 * R))

    def f_leakage(self, v_wind):
        if (v_wind < 0.25):
            return 0.25 * self.c_leakage
        else:
            return self.c_leakage * v_wind

    def f_thscr(self, U_thscr, T_air, T_top):
        return U_thscr * self.K_thScr * (abs(T_air - T_top) ** (2.0 / 3)) + (1 - U_thscr) * (g * (1 - U_thscr) / (2 * (self.p_Air + self.p_Top)/2.0) * abs(self.p_Air - self.p_Top)) ** (1.0 / 2)

    def f_VentRoofSide(self, U_roof, U_side, T_air, T_out, v_wind):
        try:
            temp = (U_roof * U_side * self.A_roof * self.A_side) / ((U_roof ** 2) * (self.A_roof ** 2) + (U_side ** 2) * (self.A_side ** 2))
            temp2 = 2 * g * self.h_sideRoof * (T_air - T_out) / ((T_air + T_out)/2.0)
            temp3 = (((U_roof * self.A_roof + U_side * self.A_side) / 2) ** (1 /2)) * self.C_w * (v_wind ** 2)
            return self.C_d / self.A_flr * ((temp * temp2 + temp3) ** (1 / 2))
        except:
            return 0
        
    #f_VentRoofSide khi A_roof = 0 --> f''_ventSide
    def f_VentSide_base(self, U_roof, U_side, T_air, T_out, v_wind):
        try:
            temp = (U_roof * U_side * 0 * self.A_side) / ((U_roof ** 2) * (0 ** 2) + (U_side ** 2) * (self.A_side ** 2))
            temp2 = 2 * g * self.h_sideRoof * (T_air - T_out) / ((T_air + T_out)/2.0)
            temp3 = (((U_roof * 0 + U_side * self.A_side) / 2) ** (1 /2)) * self.C_w * (v_wind ** 2)
            return self.C_d / self.A_flr * ((temp * temp2 + temp3) ** (1 / 2))
        except:
            return 0

    #f''_ventRoof
    def f_VentRoof_base(self, U_roof, T_air, T_out, v_wind):
        temp0 = U_roof * self.A_roof * self.C_d / 2.0 / self.A_flr
        temp1 = g * self.h_vent / 2 * (T_air - T_out) / (((T_air + T_out)/2.0) + 273.15) + self.C_w * (v_wind ** 2)
        return temp0 * (temp1 ** (1 / 2))
        
    def f_VentRoof(self, U_thrScr, U_roof, U_side, T_air, T_out, v_wind, n_roof):
        ff_ventRoof = self.f_VentRoof_base(U_roof, T_out, T_air, v_wind)
        ff_ventRoofSide = self.f_VentRoofSide(U_roof, U_side, T_air, T_out, v_wind)
        _f_leakage = self.f_leakage(v_wind)
        if (n_roof >= n_roofThr):
            return self.n_insScr * ff_ventRoof + 0.5  * _f_leakage
        else:
            return self.n_insScr * (U_thrScr * ff_ventRoof) + (1 - U_thrScr) * ff_ventRoofSide * n_roof + 0.5 * _f_leakage      

    def f_VentSide(self, U_thrScr, U_roof, U_side, T_air, T_out, v_wind, n_side):
        _f_leakage = self.f_leakage(v_wind)
        ff_ventSide = self.f_VentSide_base(U_roof, U_side, T_air, T_out, v_wind)
        ff_ventRoofSide = self.f_VentRoofSide(U_roof, U_side, T_air, T_out, v_wind)
        if (n_side >= n_roofThr):
            return self.n_insScr * ff_ventSide + 0.5  * _f_leakage
        else:
            return self.n_insScr * (U_thrScr * ff_ventSide) + (1 - U_thrScr) * ff_ventRoofSide * n_side + 0.5 * _f_leakage

    def f_VentForced(self, U_ventForce):
        return self.n_insScr * U_ventForce * self.o_ventForce / self.A_flr
        

    def MV_843(self, VP1, VP2, HEC):
        if (VP1 < VP2):
            return 0
        else:
            return (6.4 * (10.0 ** -9)) * HEC * (VP1 - VP2)
 
    def MV_845(self, VP1, T1, VP2, T2, f):
        return M_water * f * (VP1 / (T1 + 273.15) - VP2 / (T2 + 273.15)) / R

    def cap_VP_air(self, T_air):
        return (M_water * self.h_air)/(R * (T_air + 273.15))
    
    def cap_VP_top(self, T_top):
        return (M_water * self.h_top)/(R * (T_top + 273.15))

    def VEC_canAir(self, LAI, rb, rs):
        return (2 * self.p_Air * c_pAir * LAI) / (delta_H * y * (rb + rs))

    def MV_can_air(self, VP_can, VP_air, LAI, rb):
        VEC = self.VEC_canAir(LAI, rb, rs_min)
        return VEC * (VP_can - VP_air)   
    
    def MV_pad_air(self, U_pad, x_pad, x_out):
        return self.p_Air * (U_pad * self.o_pad) / self.A_flr * (self.n_pad * (x_pad - x_out) + x_out)

    def MV_fog_air(self, U_fog):
        return U_fog * self.o_fog / self.A_flr

    def MV_blow_air(self, n_heatVap, U_blow):
        return n_heatVap * U_blow * self.P_blow / self.A_flr

    def MV_airout_pad(self, U_pad, VP_air, T_air):
        return (U_pad * self.o_pad) / self.A_flr * M_water / R * VP_air / (T_air + 273.15)

    def HEC_air_mech(self, U_mechcool, T_air, T_mechcool, VP_air, VP_mech):
        top = U_mechcool * COP_mechcool * P_mechcool / self.A_flr
        bot = T_air - T_mechcool + 6.4 * 10**(-9) * delta_H * (VP_air - VP_mech)
        return top / bot

    def MV_air_mech(self, VP_air, VP_mech, U_mechcool, T_air, T_mechcool):
        HEC = self.HEC_air_mech(U_mechcool, T_air, T_mechcool, VP_air, VP_mech)
        return self.MV_843(VP_air, VP_mech, HEC)
        
    def HEC_air_thscr(self, U_thrScr, T_air, T_thscr):
        return 1.7 * U_thrScr * (abs(T_air - T_thscr)) ** (0.33)

    def MV_air_thscr(self, VP_air, VP_thscr, U_thrScr, T_air, T_thscr):
        HEC = self.HEC_air_thscr(U_thrScr, T_air, T_thscr)
        return self.MV_843(VP_air, VP_thscr, HEC)

    def HEC_top_covin(self, T_top, T_covin):
        return c_HECin * (T_top - T_covin)**(0.33) * self.A_cov / self.A_flr

    def MV_top_covin(self, VP_air, VP_mech, T_top, T_covin):
        HEC = self.HEC_top_covin(T_top, T_covin)
        return self.MV_843(VP_air, VP_mech, HEC)

    def MV_air_top(self, VP_air, T_air, VP_top, T_top, U_thscr):
        f_thscr_value = self.f_thscr(U_thscr, T_air, T_top)
        print("f_thscr_value: " + str(f_thscr_value))
        return self.MV_845(VP_air, T_air, VP_top, T_top, f_thscr_value)

    def MV_air_out(self, VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_side, U_ventForce):
        f_VentSide_value = self.f_VentSide(U_thrScr, U_roof, U_side, T_air, T_out, v_wind, n_side)
        f_VentForced_value = self.f_VentForced(U_ventForce)
        return self.MV_845(VP_air, T_air, VP_out, T_out, f_VentSide_value + f_VentForced_value)

    def MV_top_out(self, VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_roof):
        f_VentRoof_value = self.f_VentRoof(U_thrScr, U_roof, U_side, T_air, T_out, v_wind, n_roof)
        return self.MV_845(VP_air, T_air, VP_out, T_out, f_VentRoof_value)


    def dx(self, VP_air, T_air, VP_out, T_out, T_top, VP_top, VP_thscr, U_thrScr = 0, U_roof = 0, U_side = 0, v_wind = 0, n_side = 0, U_ventForce = 0, n_roof = 0, VP_mech = 0, T_covin = 0, U_thscr = 0, T_thscr = 0, U_mechcool = 0, T_mechcool = 0, U_pad = 0, U_blow = 0, U_fog = 0, x_pad = 0, x_out = 0, LAI = 0, rb = 0, VP_can = 0):
        MV_top_out_value = self.MV_top_out(VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_roof)
        MV_air_out_value = self.MV_air_out(VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_side, U_ventForce)
        MV_air_top_value = self.MV_air_top(VP_air, T_air, VP_top, T_top, U_thscr)
        MV_top_covin_value = self.MV_top_covin(VP_air, VP_mech, T_top, T_covin)
        MV_air_thscr_value = self.MV_air_thscr(VP_air, VP_thscr, U_thrScr, T_air, T_thscr)
        MV_air_mech_value = self.MV_air_mech(VP_air, VP_mech, U_mechcool, T_air, T_mechcool)
        MV_airout_pad_value = self.MV_airout_pad(U_pad, VP_air, T_air)
        MV_blow_air_value = self.MV_blow_air(n_heatVap, U_blow)
        MV_fog_air_value = self.MV_fog_air(U_fog)
        MV_pad_air_value = self.MV_pad_air(U_pad, x_pad, x_out)
        MV_can_air_value = self.MV_can_air(VP_can, VP_air, LAI, rb)
        cap_VP_top_value = self.cap_VP_top(T_top)
        cap_VP_air_value = self.cap_VP_air(T_air)
        
        '''print("BEGIN TEST")
        print(MV_top_out_value) # self.MV_top_out(VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_roof)
        print(MV_air_out_value) # self.MV_air_out(VP_air, T_air, VP_out, T_out, U_thrScr, U_roof, U_side, v_wind, n_side, U_ventForce)
        print(MV_air_top_value )# self.MV_air_top(VP_air, T_air, VP_top, T_top, U_thscr)
        print(MV_top_covin_value) # self.MV_top_covin(VP_air, VP_mech, T_top, T_covin)
        print(MV_air_thscr_value )# self.MV_air_thscr(VP_air, VP_mech, U_thrScr, T_air, T_thscr)
        print(MV_air_mech_value )# self.MV_air_mech(VP_air, VP_mech, U_mechcool, T_air, T_mechcool)
        print(MV_airout_pad_value) # self.MV_airout_pad(U_pad, VP_air, T_air)
        print(MV_blow_air_value )# self.MV_blow_air(n_heatVap, U_blow)
        print(MV_fog_air_value) # self.MV_fog_air(U_fog)
        print(MV_pad_air_value) # self.MV_pad_air(U_pad, x_pad, x_out)
        print(MV_can_air_value) # self.MV_can_air(VP_can, VP_air, LAI, rb)
        print(cap_VP_top_value) # self.cap_VP_top(T_top)
        print(cap_VP_air_value) # self.cap_VP_air(T_air)
        print("END TEST")'''
        
                     
        out1 = (MV_can_air_value + MV_blow_air_value + MV_fog_air_value +  MV_pad_air_value - MV_air_thscr_value - MV_air_top_value - MV_air_out_value - MV_air_mech_value - MV_airout_pad_value) / cap_VP_air_value
        out2 = (MV_air_top_value - MV_top_covin_value - MV_top_out_value) / cap_VP_top_value
        return out1, out2
        
'''test = Solver()
print(test.h_elevation)
print(test.p_Air)
print(test.h_air)# = h_air      #chieu cao gian duoi
print(test.p_Top) #= print(test.p_air(print(test.h_elevation + print(test.h_air)   #density of the air in the top room
print(test.A_flr) #= A_flr      #dien tich nha kinh
print(test.A_roof)# = A_roof
print(test.A_side) #= A_side
print(test.A_cov) #= A_cov
print(test.h_top) #= h_gh - h_air      #chieu cao gian tren
print(test.P_blow) #= P_blow    #kha nang sinh hoi nuoc cua may suoi
print(test.o_fog) #= o_fog      #suc chua he thong phun suong
print(test.o_pad)# o_pad      #kha nang cho hoi nuoc di qua cua tam thong gio
print(test.n_pad) #= n_pad      #hieu suat cua he thong thong gio (trong sach khong co cai nay)
#x_out va x_air: khong ro   
print(test.c_leakage) #= c_leakage  #do ro cua luoi
print(test.K_thScr) #= K_thScr      #thermal screen flux coefficient
print(test.C_d)# = C_d
print(test.C_w)# = C_w
print(test.h_sideRoof) #= h_sideRoof
print(test.h_vent) #= h_vent
print(test.n_insScr)# = n_insScr
print(test.o_ventForce)# = o_ventForce'''
