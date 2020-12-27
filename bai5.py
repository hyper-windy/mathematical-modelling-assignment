def cap_VP_air(h_air, T_air):
    M_water = 1
    R = 1
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

def MV_air_top():

def MV_air_out():

def MV_airout_pad():

def MV_air_mech():

def MV_top_out():

def MV_top_covin():
