##Du lieu lay o Netherland

n_heatCO2 = 0.057
n_heatVap = 4.43 * (10 ** (-8))
n_roofThr = 0.9
n_insScr = 1
n_side = 
n_sideThr = 
n_pad =

h_roof = 0
h_sideRoof = 0
h_vent = 0.68
h_air = 3.8
h_Gh = 4.2
h_flr = 0.02

H_blowAir

A_flr = 1.4 * (10 ** 4)
A_roof =

C_d =
C_w =

M_ch2o = 30

o_fog = 0
o_pad = 16.7
o_ventForce = 0
o_exitCO2 = 7.2 * (10 ** 4)

s_insScr = 1

p_water = 1000
p_thrScr = 0.2 * (10**3)
p_flr = 2300
p_air0 = 1.20
p_air = 

r_b = 275
r_s = 
r_sMin = 82


Delta_H = 2.45 * (10 ** 6)

K_thScr = 0.05 * (10 ** -3)

e_flr = 1
e_can = 1
e_sky = 1

landa_flr = 1.7

g = 9.81

M_water = 18
M_air = 28.96

y = 65.8
w = 1.99 * (10 **-7)
R = 8314
o = 5.670 * (10 ** -8)

c_leakage = 10**-4
c_pFlr = 0.88 * (10 ** 3)
c_pThr = 1.8 * (10 ** 3)
c_pAir

cap_leaf = 1200
####################
def f_leakage(v_wind):
    if (v_wind < 0.25):
        return 0.25 * c_leakage
    else:
        return c_leakage * v_wind

def f_VentForced(n_roof):
    if (n_roof > n_roofThr):
        return n_insScr

def MV_843(VP1, VP2, HEC):
    if (VP1 < VP2):
        return 0
    else:
        return (6.4 * (10.0 ** -9)) * HEC * (VP1 - VP2)
 
def MV_845(VP1, T1, VP2, T2, f):
    return M_water * R * f * (VP1 / (T1 + 273.15) - VP2 / (T2 + 273.15))



def cap_VP_air(h_air, T_air):
    return (M_water * h_air)/(R * T_air + 273.15)
  
def MV_can_air(VP_can, VP_air, pAir, LAI, rb, rs):
    VEC = VEC_canAir(pAir, LAI, rb,rs)
    return VEC * (VP_can - VP_air)
    
def VEC_canAir(pAir, LAI, rb,rs):
    c_p_Air = 
    delta_H = 
    psy_const = 
    return (2 * pAir * c_p_Air * LAI) / (delta_H * psy_const * (rb + rs))
    
def MV_pad_air():

def MV_fog_air():

def MV_blow_air():

def MV_air_thscr():

def f_thscr(U_thscr, K_thscr, T_air, T_top, P_airMean, p_Air, p_Top):
    return U_thscr * K_thscr * abs(T_air - T_top) ** (2 / 3) + (1 - U_thscr) * (g * (1 - U_thscr) / (2 * P_airMean) * (p_Air - p_Top)) ** (1 / 3)
    
def MV_air_top(M_water, R, VP1, T1, VP2, T2):
    return MV_845(M_water, R, VP1, T1, VP2, T2, f_thscr)

def f_VentSide():


def MV_air_out(VP1, T1, VP2, T2):
    return MV_845(VP1, T1, VP2, T2, f_VentSide + f_VentForced)

def MV_airout_pad(fpad, M_water, R, VP_air, T_air):
    return fpad * M_water / R * VP_air / (T_air + 273.15)

def MV_air_mech():

def f_VentRoof():

def MV_top_out(M_water, R, VP1, T1, VP2, T2):
    return MV_845(M_water, R, VP1, T1, VP2, T2, f_VentRoof)

def MV_top_covin():

