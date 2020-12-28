class Dynamic:
    # n_HeatCO2 = 0.057  # not different
    # AFlr = 78000  #page 223, Texas
    # P_Blow = 500000
    # g = 9.81
    # cap_ExtCO2 = 430000  #page 114, Texas
    # cap_pad = 16.7 #page 237, Arizona

    def __init__(self, AFlr, n_HeatCO2, U_Blow, P_Blow, U_ExtCO2, cap_ExtCO2, U_pad, cap_pad, CO2_out, CO2_air, CO2_top,  U_ThScr, K_ThScr, T_air, T_top, g, h_roof, h_SideRoof, T_mean_air, p_mean_air, p_air, p_top, Cd, Cw, URoof, USide, ARoof, ASide, g, c_leakage, S_holes, n_side, n_sideThr, n_InsScr, U_VentForced, cap_VentForced, M_cbhd, P, R):
        self.AFlr = AFlr
        self.n_HeatCO2 = n_HeatCO2
        self. U_Blow = U_Blow
        self.P_Blow = P_Blow
        self.U_ExtCO2 = U_ExtCO2
        self.cap_ExtCO2 = cap_ExtCO2
        slef.U_pad = U_pad
        self.cap_pad = cap_pad
        slef.CO2_out = CO2_out
        self.CO2_air = CO2_air
        self.CO2_top = CO2_top
        self.U_ThScr = U_ThScr  
        self.K_ThScr = K_ThScr
        self.T_air = T_air
        self.T_top = T_top
        self.g = g
        self.h_roof = h_roof
        self.h_SideRoof = h_SideRoof
        self.T_mean_air = T_mean_air
        self.p_mean_air = p_mean_air
        self.p_air = p_air
        self.p_top = p_top
        self.Cd = Cd
        self.Cw = Cw
        self.URoof = URoof
        self.USide = USide
        self.ARoof = ARoof
        self.ASide = ASide
        self.c_leakage = c_leakage
        self.S_holes = s_holes
        self.n_side = n_side
        self.n_sideThr = n_sideThr
        self.n_InsScr = n_InsScr
        self.U_VentForced = U_VentForced
        self.cap_VentForced = cap_VentForced
        self.M_cbhd = M_cbhd
        self.R = R
        self.MC_blow_air = MC_blow_air(U_Blow, n_HeatCO2, P_Blow, AFlr)
        self.MC_ext_air = MC_ext_air(U_ExtCO2, cap_ExtCO2, AFlr)
        self.f_leakage = f_leakage(v_wind, c_leakage)
        self.MC_pad_air = MC_pad_air(U_pad, cap_pad, CO2_out, CO2_air, AFlr)
        self.f_ThScr = f_ThScr(U_ThScr, K_ThScr, T_air, T_top, g, p_mean_air, p_air, p_top)
        self.MC_air_top = MC_air_top(CO2_air, CO2_top, f_ThScr)
        self.fff_VentSide = f_VentRoofSide(Cd, AFlr, URoof, 0, USide, ASide, g, h_SideRoof, T_air, T_out, T_mean_air, Cw, v_wind)
        self.f_VentRoofSide = f_VentRoofSide(Cd, AFlr, URoof, ARoof, USide, ASide, g, h_SideRoof, T_air, T_out, T_mean_air, Cw, v_wind)
        self.f_VentSide = f_VentSide(n_side, n_sideThr, n_InsScr, \self.f_leakage, self.fff_VentSide, self.f_VentRoofSide)
        self.f_VentForced = f_VentForced(n_InsScr, U_VentForced, cap_VentForced, AFlr)
        self.MC_air_out = MC_air_out(CO2_air, CO2_out, self.f_VentSide, self.f_VentForced)
        self.f_VentRoofSide = f_VentRoofSide(Cd, AFlr, URoof, ARoof, USide, ASide, g, h_SideRoof, T_air, T_out, T_mean_air, Cw, v_wind)
        self.redutionfactor = redutionfactor(S_holes)
        self.fff_VentRoof = fff_VentRoof(Cd, URoof, ARoof, AFlr, g, h_roof, T_air, T_out, T_mean_air, Cw, v_wind)
        self.hCBuf = hCBuf(CBuf, C_Max_Buf)
        self.P =  P(PMax, Res, CO2_air, CO2_05)
        self.MC_air_can = MC_air_can(M_cbhd, self.hCBuf, self.P, R)
        self.k = k(LAI, k_T0, e, Ha, R, T, T0)
        self.f = f()
        self.PMaxT = PmaxT(self.k, self.f)
        self.I = I(I0, K, e, LAI, m)
        self.L = L(L0, K, e, LAI, m)
        self.pMaxLT = pMaxLT(P_MLT, PmaxT, self.L, L05)
        

    def MC_blow_air(U_Blow, n_HeatCO2, P_Blow, AFlr):      # (3) luong CO2 tu may suoi den gian duoi
        return (n_HeatCO2 * U_Blow * P_Blow)/AFlr

    def MC_ext_air(U_ExtCO2, cap_ExtCO2, AFlr):       
        # (4) luong CO2 tu ben thu ba den gian duoi
        return (U_ExtCO2 * cap_ExtCO2)/AFlr

    def MC_pad_air(U_pad, cap_pad, CO2_out, CO2_air, AFlr):       
        # (5) luong CO2 tu thong gio de gian duoi
        return (U_pad * cap_pad)*(CO2_out - CO2_air)/AFlr

    def MC_air_top(CO2_air, CO2_top, f_ThScr):       
        # (6) luong CO2 tu gian duoi den gian tren
        return f_ThScr*(CO2_air - CO2_top)

    def f_ThScr(U_ThScr, K_ThScr, T_air, T_top, g, p_mean_air, p_air, p_top):          
        #(7) toc do luu thong CO2 qua man chan nhiet
        return U_ThScr * K_ThScr * (abs(T_air - T_top)**(2/3)) + (1 - U_ThScr) * sqrt(g * (1 - U_ThScr) * abs(p_air - p_top) / (2 * p_mean_air))
   
    def MC_air_out(CO2_air, CO2_out, f_VentSide, f_VentForced):       
        # (9) luong CO2 di tu gian duoi ra ben ngoai
        return (f_VentSide + f_VentForced)*(CO2_air - CO2_out)

    def f_VentRoofSide(Cd, AFlr, URoof, ARoof, USide, ASide, g, h_SideRoof, T_air, T_out, T_mean_air, Cw, v_wind):     
        #(10) tong quat mo hinh cho nhieu loai nha kinh khac nhau
        return Cd/AFlr*sqrt(pow((URoof*USide*ARoof*ASide),2)*2*g*h_SideRoof*(T_air - T_out)/((pow(URoof*ARoof, 2) + pow(USide*ASide, 2))*T_mean_air) + pow((URoof*ARoof + USide*ASide)/2,2)*Cw*pow(v_wind, 2), U_VentForced, cap_VentForced)
    
    def redutionfactor(S_holes):   #(11)
        return S_holes*(2 - S_holes)
    
    def f_leakage(v_wind, c_leakage):    #(12) wind speed, coefficient of leakage
        if v_wind < 0.25:
            return 0.25*c_leakage
        else:
            return v_wind*c_leakage
    
    def f_VentSide(n_side, n_sideThr, n_InsScr, f_leakage, fff_VentSide, f_VentRoofSide):        #(13) toc do gio cua he thong quat tren tuong bao xung quanh nha kinh
        if n_side >= n_sideThr:
            return n_InsScr*fff_VentSide + 0.5*f_leakage
        else:
            return n_InsScr*(U_ThScr*fff_VentSide + (1 - U_ThScr)*fVentRoofSide*n_side) + 0.5*f_leakage
    
    def f_VentForced(n_InsScr, U_VentForced, cap_VentForced, AFlr):      # (14) toc do gio tu he thong quat ben trong nha kinh
        return (n_InsScr * U_VentForced * cap_VentForced)/AFlr
    
    def MC_top_out(f_VentRoof, CO2_top, CO2_out):       # (15) luong khi di tu gian tren ra ngoai
        return f_VentRoof*(CO2_top - CO2_out)
    
    def f_VentRoof(n_roof, n_roofThr, n_side, n_InsScr, fff_VentRoof, f_leakage):        #(16) toc do luong khong khi di qua o mo mai nha kinh
        if n_roof >= n_roofThr:
            return (n_InsScr*fff_VentRoof + 0.5*f_leakage)
        else:
            return (n_InsScr*(U_ThScr*fff_VentRoof + (1 - U_ThScr)*f_VentRoofSide*n_side) + 0.5*f_leakage)   

    def fff_VentRoof(Cd, URoof, ARoof, AFlr, g, h_roof, T_air, T_out, T_mean_air, Cw, v_wind):      #(17)
        return (Cd*URoof*ARoof/(2*AFlr)*sqrt(g*h_roof*(T_air - T_out)/(2*T_mean_air) +Cw*pow(v_wind, 2)))

    def MC_air_can(M_cbhd, hCBuf, self.P, R):       # (18) luong CO2 bi hap thu vao trong tan la
        return M_cbhd*hCBuf()*(P-R)
    
    def hCBuf(CBuf, C_Max_Buf):            # (19) he so the hien su ngung qua trinh quang hop
        if CBuf > C_Max_Buf:
            return 0
        else:
            return 1
    
    def P(PMax, Res, CO2_air, CO2_05):               #(22)
        return (-(CO2_air + CO2_05 + Res*PMax) + sqrt(pow((CO2_air + CO2_05 + Res*PMax),2) - 4*Res*CO2_air*PMax)/(2*Res)

    def PmaxT(k, f):            #(25) toc do quang hop toi da
        return k, f
   
    def I(I0, K , e, LAI, m):                #(26) nang luong sau khi vao tan la
        return (I0*K*pow(e, -(K*LAI)))/(1-m)
    
    def L(L0, K, e, LAI, m):                #(27) nang luong tan la nhan duoc
        return L0*(1 - (K*power(e, -(K.LAI)))/(1-m))
    
    def k(LAI, k_T0, e, Ha, R, T, T0):                #(28) toc do phan ung cho toan bo la cay (reaction rate)
        return LAI * k(T0) * pow(e, -(Ha/R)*(1/T - 1/T0))
    
    def pMaxLT(P_MLT, PmaxT, L, L05):           #(29) toc do quang hop toi da
        return (P_MLT * PmaxT() * L)/(L + L05)
        #(3)-(7), (9)-(19), (22), (25), (28), (24), (27) và (29)

def main():
    #khai bao cac hang o day
    R = 8.31446261815324 #J/(K*M)

    obj = Dynamic()
main()
