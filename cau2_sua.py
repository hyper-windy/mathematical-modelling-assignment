from math import exp,sqrt
R = 8.31446261815324 * 1000   # J/(K*M)
p_air0 = 1.20               #density of the air at sea level
M_air = 28.96               #molar mass of water
g = 9.81
n_HeatCO2 = 0.057
n_roofThr = 0.9
class Dynamic:
    def __init__(self, h_elevation = 0, h_air = 3.8, h_gh = 4.2,U_Blow = 0, P_Blow = 0, A_Flr = 1.4*10**4, U_ExtCO2 =0, cap_ExtCO2 = 72000, U_pad = 0, cap_pad = 0, U_ThScr = 0, K_ThScr = 0.05*(10**(-3)), C_d = 0.75, C_w = 0.09, URoof = 0, USide = 0, ASide = 0, h_SideRoof = 0, S_holes = 1, n_roof = n_roofThr):
        self.h_elevation = h_elevation  # do cao nha kinh so voi muc nuoc bien
        self.p_Air = self.p_air(self.h_elevation)  # density of the greenhouse air
        self.h_air = h_air  # chieu cao gian duoi
        self.p_Top = self.p_air(self.h_elevation + self.h_air)  # density of the air in the top room
        self.h_top = self.h_gh - self.h_air
        self.A_Flr = A_Flr
        self.U_Blow = U_Blow
        self.P_Blow = P_Blow
        self.U_ExtCO2 = U_ExtCO2
        self.cap_ExtCO2 = cap_ExtCO2
        self.U_pad = U_pad
        self.cap_pad = cap_pad
        self.U_Thscr = U_ThScr
        self.K_ThScr = K_ThScr
        self.C_d = C_d
        self.C_w = C_w
        self.URoof = URoof
        self.USide = USide
        self.ARoof = A_Flr / 10
        self.ASide = ASide
        self.h_SideRoof = h_SideRoof
        self.S_holes = S_holes
        self.n_roof = n_roof
        self.n_side = n_roof

    def p_air(self, elevate):
        return p_air0 * exp(g * M_air * elevate / (293.15 * R))

    def MC_blow_air(self):      # (3) luong CO2 tu may suoi den gian duoi
        return (n_HeatCO2 * self.U_Blow * self.P_Blow)/self.A_Flr

    def MC_ext_air(self):
        # (4) luong CO2 tu ben thu ba den gian duoi
        return (self.U_ExtCO2 * self.cap_ExtCO2)/self.A_Flr

    def MC_pad_air(self, CO2_out, CO2_air):
        #cap_pad = u_pad/A_FLr?
        # (5) luong CO2 tu thong gio de gian duoi
        return (self.U_pad * self.cap_pad)*(CO2_out - CO2_air)/self.A_Flr

    def MC_air_top(self,CO2_air, CO2_top, T_air, T_top):
        f_ThScr_value = self.f_ThScr(T_air, T_top)
        # (6) luong CO2 tu gian duoi den gian tren
        return f_ThScr_value*(CO2_air - CO2_top)


    def f_ThScr(self, T_air, T_top):
        #(7) toc do luu thong CO2 qua man chan nhiet
        p_mean_air = (self.p_Air + self.p_Top) / 2.0
        temp1 = self.U_Thscr * self.K_ThScr * (abs(T_air - T_top)**(2/3))
        temp2 = (1 - self.U_Thscr) * sqrt((g * (1 - self.U_Thscr) * abs(self.p_Air - self.p_Top) / (2 * p_mean_air)))
        return temp1 + temp2

    def MC_air_out(self, CO2_air, CO2_out, f_VentSide, f_VentForced):
        # (9) luong CO2 di tu gian duoi ra ben ngoai
        f_VentSide_value =
        return (f_VentSide + f_VentForced)*(CO2_air - CO2_out)


    def f_VentRoofSide(self, T_air, T_out, v_wind):
        try:
            T_mean_air = (T_air + T_out) / 2.0
            #(10) tong quat mo hinh cho nhieu loai nha kinh khac nhau
            #return Cd/A_Flr*sqrt(pow((URoof*USide*ARoof*ASide),2)*2*g*h_SideRoof*(T_air - T_out)/((pow(URoof*ARoof, 2) + pow(USide*ASide, 2))*T_mean_air) + pow((URoof*ARoof + USide*ASide)/2,2)*Cw*pow(v_wind, 2), U_VentForced, cap_VentForced)
            temp1 = (self.URoof* self.USide * self.ARoof * self.ASide)**2 * 2*g*self.h_SideRoof * (T_air - T_out) / ((self.URoof * self.ARoof)**2 + (self.USide * self.ASide)**2) / T_mean_air
            temp2 = pow((self.URoof * self.ARoof + self.USide * self.ASide) / 2, 2) * self.C_w * v_wind**2
            return self.C_d / self.A_Flr * sqrt(temp1 + temp2)
        except:
            return 0

    def fff_VentSide(self, T_air, T_out, v_wind):
        try:
            temp = (self.URoof * self.USide * 0 * self.ASide) / ((self.URoof ** 2) * (0 ** 2) + (self.USide ** 2) * (self.ASide ** 2))
            temp2 = 2 * g * self.h_SideRoof * (T_air - T_out) / ((T_air + T_out) / 2.0)
            temp3 = (((self.URoof * 0 + self.USide * self.ASide) / 2) ** (1.0 / 2)) * self.C_w * (v_wind ** 2)
            return self.C_d / self.A_Flr * ((temp * temp2 + temp3) ** (1.0 / 2))
        except:
            return 0

    def redutionfactor(self):   #(11)
        return self.S_holes*(2 - self.S_holes)

    # f''_ventRoof
    def fff_VentRoof(self, T_air, T_out, v_wind):
        temp0 = self.URoof * self.ARoof * self.C_d / 2.0 / self.A_Flr
        temp1 = g * self.h / 2 * (T_air - T_out) / (((T_air + T_out) / 2.0) + 273.15) + self.C_w * (v_wind ** 2)
        return temp0 * (temp1 ** (1.0 / 2))

    def f_VentRoof(self, n_InsScr, fff_VentRoof, f_leakage):        #(16) toc do luong khong khi di qua o mo mai nha kinh
        if self.n_roof >= n_roofThr:
            return (n_InsScr*fff_VentRoof + 0.5*f_leakage)
        else:
            return (n_InsScr*(self.U_Thscr*fff_VentRoof + (1 - U_ThScr)*f_VentRoofSide* self.n_side) + 0.5*f_leakage)

