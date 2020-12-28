##Du lieu lay o Netherland

n_heatCO2 = 0.057
n_heatVap = 4.43 * (10 ** (-8))
n_roofThr = 0.9
n_insScr = 1
n_side = 0
n_sideThr = 
n_pad =

C_d_Gh = 0.75
C_w_Gh = 0.09
C_macBuf = 

h_roof = 0
h_sideRoof = 0
h_vent = 0.68
h_air = 3.8
h_Gh = 4.2
h_flr = 0.02
h_Cbuf = 

A_flr = 1.4 * (10 ** 4)
A_roof =

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
r_sMin = 82
r_s = 


e_flr = 1
e_can = 1
e_sky = 1

M_water = 18
M_air = 28.96
M_ch2o = 30

c_leakage = 10**-4
c_pFlr = 0.88 * (10 ** 3)
c_pThr = 1.8 * (10 ** 3)
c_pAir = 

y = 65.8
w = 1.99 * (10 **-7)
R = 8314
o = 5.670 * (10 ** -8)
P = 
P_blow = 

landa_flr = 1.7

g = 9.81

delta_H = 2.45 * (10 ** 6)

K_thScr = 0.05 * (10 ** -3)

cap_leaf = 1200
####################
# Tinh cac gia tri can thiet


###################
def f_leakage(c_leakage, v_wind):
    if (v_wind < 0.25):
        return 0.25 * c_leakage
    else:
        return c_leakage * v_wind

def f_thscr(U_thscr, K_thscr, T_air, T_top, P_airMean, p_Air, p_Top):
    return U_thscr * K_thscr * abs(T_air - T_top) ** (2 / 3) + (1 - U_thscr) * (g * (1 - U_thscr) / (2 * P_airMean) * (p_Air - p_Top)) ** (1 / 3)

def f_VentRoofSide(C_d, C_w, A_flr, U_roof, U_side, A_roof, A_side, h_sideRoof, T_air, T_out, T_air_Mean ,v_wind):
    temp = (U_roof * U_side * A_roof * A_side) / ((U_roof ** 2) * (A_roof ** 2) + (U_side ** 2) * (A_side ** 2))
    temp2 = 2 * g * h_sideRoof * (T_air - T_out) / T_air_Mean
    temp3 = (((U_roof * A_roof + U_side * A_side) / 2) ** (1 /2)) * C_w * (v_wind ** 2)
    return C_d / A_flr * ((temp * temp2 + temp3) ** (1 / 2))

def f_VentRoof(U_roof, A_roof, C_d, A_flr, h_vent, T_out, T_air, T_tb, C_w, v_wind):
    temp0 = U_roof * A_roof * C_d / 2 / A_flr
    temp1 = g * h_vent / 2 * (T_air - T_out) / (T_tb + 273.15) + C_w * (v_wind ** 2)

    return temp0 * (temp1 ** (1 / 2))

def f_VentSide(n_roof, n_roofThr, n_insScr, ff_ventSide, f_leakage, U_thrScr, n_side):
    if (n_roof >= n_roofThr):
        return n_insScr * ff_ventSide + 0.5  * f_leakage
    else:
        return n_insScr * (U_thrScr * ff_ventSide) + (1 - U_thrScr) * ff_ventSide * n_side + 0.5 * f_leakage

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
    
def VEC_canAir(pAir, LAI, rb, rs, psy_const, c_p_Air):
    return (2 * pAir * c_p_Air * LAI) / (delta_H * psy_const * (rb + rs))
    
def MV_pad_air(p_air, f_pad, n_pad, x_pad, x_out):
    return p_air * f_pad * (n_pad * (x_pad - x_out) + x_out)

def MV_fog_air(U_fog, o_fog, A_flr):
    return U_fog * o_fog / A_flr

def MV_blow_air(n_heatVap, H_blowAir):
    return n_heatVap * H_blowAir

def MV_airout_pad(fpad, VP_air, T_air):
    return fpad * M_water / R * VP_air / (T_air + 273.15)

def MV_air_mech(VP1, VP2, HEC):
    return MV_843(VP1, VP2, HEC)

def MV_air_thscr(VP1, VP2, HEC):
    return MV_843(VP1, VP2, HEC)

def MV_top_covin(VP1, VP2, HEC):
    return MV_843(VP1, VP2, HEC)

def MV_air_top(VP1, T1, VP2, T2):
    return MV_845(VP1, T1, VP2, T2, f_thscr)

def MV_air_out(VP1, T1, VP2, T2):
    return MV_845(VP1, T1, VP2, T2, f_VentSide + f_VentForced)

def MV_top_out(VP1, T1, VP2, T2):
    return MV_845(VP1, T1, VP2, T2, f_VentRoof)

