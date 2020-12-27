n_heatCO2 = 0.057
n_heatVap = 4.43 * 10 ** (-8)
p_water = 1000
g = 9.81
M_water = 18
M_air = 28.96
R = 8314

####################
def MV_845(VP1, T1, VP2, T2, f):
    return M_water * R * f * (VP1 / (T1 + 273.15) - VP2 / (T2 + 273.15))

def cap_VP_air(h_air, T_air):
    return (M_water * h_air)/(R * T_air + 273.15)

def MV_8_43(VP1, VP2, HEC):
    if (VP1 < VP2):
        return 0
    else:
        return (6.4 * (10.0 ** -9)) * HEC * (VP1 - VP2)
    
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
    return U_thscr * K_thscr * abs(T_air - T_top) ** (2 / 3) + (1 - U_thscr) * (g * (1 - U_thscr) / (2 * p_airMean) * (p_Air - p_Top)) ** (1 / 3)
    
def MV_air_top(M_water, R, VP1, T1, VP2, T2):
    return MV_845(M_water, R, VP1, T1, VP2, T2, f_thscr)

def f_VentSide():

def f_VentForced():

def MV_air_out(VP1, T1, VP2, T2):
    return MV_845(VP1, T1, VP2, T2, f_VentSide + f_VentForced)

def MV_airout_pad(fpad, M_water, R, VP_air, T_air):
    return fpad * M_water / R * VP_air / (T_air + 273.15)

def MV_air_mech():

def f_VentRoof():

def MV_top_out(M_water, R, VP1, T1, VP2, T2):
    return MV_845(M_water, R, VP1, T1, VP2, T2, f_VentRoof)

def MV_top_covin():


