from math import exp,sqrt
R = 8.31446261815324 * 1000   # J/(K*M)
p_air0 = 1.20               #density of the air at sea level
M_air = 28.96               #molar mass of water
g = 9.81
n_HeatCO2 = 0.057
n_roofThr = 0.9
n_sideThr = n_roofThr
c_leakage = 10**(-4)
LAI = 3
n_co2Air_stom = 0.67
J_max_leaf = 210
c_gamma = 1.7
M_ch2o = 30 * (10 ** -3)    #maybe 30???
par_can = 100
alpha = 0.385
e_curvate_deg = 0.7 #degree of curvature of the electron transport rate
T_25_k = 298.15 #reference temperature for J_pot
E_j = 37 * (10**3)  #activation energy for J_pot
H_j = 22 * (10**4)  #deactivation energy for J_pot
S_entropy = 710             #entropy term for J_pot
class Dynamic:
    def __init__(self, h_elevation = 0, h_air = 3.8, h_gh = 4.2, h_vent = 0.68,U_Blow = 0, P_Blow = 0, A_Flr = 1.4*10**4, U_ExtCO2 =0, cap_ExtCO2 = 72000, U_pad = 0, cap_pad = 0, U_ThScr = 0, K_ThScr = 0.05*(10**(-3)), C_d = 0.75, C_w = 0.09, URoof = 0, USide = 0, ASide = 0, h_SideRoof = 0, S_holes = 1, n_roof = n_roofThr, U_VentForced = 0, cap_VentForced = 0):
        self.h_elevation = h_elevation  # do cao nha kinh so voi muc nuoc bien
        self.p_Air = self.p_air(self.h_elevation)  # density of the greenhouse air
        self.h_air = h_air  # chieu cao gian duoi
        self.h_vent = h_vent
        self.h_gh = h_gh
        self.p_Top = self.p_air(self.h_elevation + self.h_air)  # density of the air in the top room
        self.h_top = h_gh - self.h_air
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
        self.U_VentForced = U_VentForced
        self.cap_VentForced = cap_VentForced

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

    def MC_air_out(self, CO2_air, CO2_out, T_air, T_out, v_wind):
        # (9) luong CO2 di tu gian duoi ra ben ngoai
        f_VentSide_value = self.f_VentSide(T_air, T_out, v_wind)
        f_VentForced_value = self.f_VentForced()
        return (f_VentSide_value + f_VentForced_value)*(CO2_air - CO2_out)


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
            return self.C_d*self.USide*self.ASide*v_wind/2/self.A_Flr
        except:
            return 0

    def redutionfactor(self):   #(11)
        return self.S_holes*(2 - self.S_holes)

    def f_leakage(self,v_wind):    #(12) wind speed, coefficient of leakage
        if v_wind < 0.25:
            return 0.25*c_leakage
        else:
            return v_wind*c_leakage

    def f_VentSide(self,T_air, T_out, v_wind):  # (13) toc do gio cua he thong quat tren tuong bao xung quanh nha kinh
        n_InsScr = self.redutionfactor()
        f_leakage_value = self.f_leakage(v_wind)
        fff_VentSide_value = self.fff_VentSide(T_air, T_out, v_wind)
        f_VentRoofSide_value = self.f_VentRoofSide(T_air,T_out,v_wind)
        if self.n_side >= n_sideThr:
            return n_InsScr * fff_VentSide_value + 0.5 * f_leakage_value
        else:
            return n_InsScr * (self.U_Thscr * fff_VentSide_value + (1 - self.U_Thscr) * f_VentRoofSide_value * self.n_side) + 0.5 * f_leakage_value

    def f_VentForced(self):  # (14) toc do gio tu he thong quat ben trong nha kinh
        n_InsScr = self.redutionfactor()
        return (n_InsScr * self.U_VentForced * self.cap_VentForced) / self.A_Flr

    def MC_top_out(self, CO2_top, CO2_out,T_air, T_out, v_wind):  # (15) luong khi di tu gian tren ra ngoai
        f_VentRoof_value = self.f_VentRoof(T_air, T_out, v_wind)
        return f_VentRoof_value * (CO2_top - CO2_out)

    # f''_ventRoof
    def fff_VentRoof(self, T_air, T_out, v_wind):
        if self.n_roof <= n_roofThr:
            return self.C_d*self.URoof*self.ARoof*v_wind/2/self.A_Flr
        else :
            temp0 = self.URoof * self.ARoof * self.C_d / 2.0 / self.A_Flr
            temp1 = g * self.h_vent / 2 * (T_air - T_out) / (((T_air + T_out) / 2.0) + 273.15) + self.C_w * (v_wind ** 2)
            return temp0 * (temp1 ** (1.0 / 2))

    def f_VentRoof(self, T_air, T_out, v_wind):        #(16) toc do luong khong khi di qua o mo mai nha kinh
        n_InsScr = self.redutionfactor()
        fff_VentRoof_value = self.fff_VentRoof(T_air, T_out, v_wind)
        f_leakage_value = self.f_leakage(v_wind)
        f_VentRoofSide_value = self.f_VentRoofSide(T_air, T_out, v_wind)
        if self.n_roof >= n_roofThr:
            return (n_InsScr * fff_VentRoof_value + 0.5*f_leakage_value)
        else:
            return (n_InsScr*(self.U_Thscr*fff_VentRoof_value + (1 - self.U_Thscr)*f_VentRoofSide_value* self.n_side) + 0.5*f_leakage_value)

    def calJpot(self,T_can):
        J_max_can = LAI * J_max_leaf
        second = exp(E_j * (T_can + 273.15 - T_25_k)/(8.314*(T_can + 273.15 - T_25_k)))
        third = (1 + exp((S_entropy * T_25_k - H_j) / (8.314 * T_25_k))) / (1 + exp((S_entropy * (T_can + 273.15) - H_j) / (8.314 * (T_can + 273.15))))
        return J_max_can * second * third


    def electronTrans(self, T_can):
        J_pot = self.calJpot(T_can)
        top1 = J_pot + alpha * par_can
        top2 = ((J_pot + alpha * par_can)**2 - 4*e_curvate_deg * J_pot * alpha * par_can)**(1.0/2.0)
        bot = 2 * e_curvate_deg
        return (top1 - top2) / bot

    def co2Stom(self,CO2_air):
        return n_co2Air_stom * CO2_air

    def gamma(self,T_can):
        J_max_can = LAI * J_max_leaf
        return (J_max_leaf / J_max_can)*c_gamma * T_can + 20 * c_gamma * (1 - J_max_leaf/J_max_can)

    def photoRate(self,CO2_air, T_can):
        J = self.electronTrans(T_can)
        gamma = self.gamma(T_can)
        CO2_stom = self.co2Stom(CO2_air)
        top = J * (CO2_stom - gamma)
        bot = 4 * (CO2_stom + 2*gamma)
        return top/bot


    def MC_air_can(self, CO2_air, T_can):  # (18) luong CO2 bi hap thu vao trong tan la
        hCBuf = 1
        P = self.photoRate(CO2_air, T_can)
        R = P * (self.gamma(T_can) / self.co2Stom(CO2_air))
        return M_ch2o * hCBuf * (P - R)

    def dx(self, CO2_out, CO2_air, CO2_top, T_air, T_top, T_out, T_can, v_wind):
        MC_blow_air_value = self.MC_blow_air()
        MC_ext_air_value = self.MC_ext_air()
        MC_pad_air_value = self.MC_pad_air(CO2_out, CO2_air)
        MC_air_can_value = self.MC_air_can(CO2_air, T_can)
        MC_air_top_value = self.MC_air_top(CO2_air,CO2_out,T_air, T_top)
        MC_air_out_value = self.MC_air_out(CO2_air,CO2_out, T_air, T_out, v_wind)
        MC_top_out_value = self.MC_top_out(CO2_top, CO2_out, T_air, T_out, v_wind)
        cap_CO2air = self.h_air
        cap_CO2top = self.h_top

        vCO2_air = (MC_blow_air_value + MC_ext_air_value + MC_pad_air_value - MC_air_can_value - MC_air_top_value - MC_air_out_value)/cap_CO2air
        vCO2_top = (MC_air_top_value - MC_top_out_value)/cap_CO2top
        return vCO2_air, vCO2_top
