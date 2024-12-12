from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB
from AHU.AirPort.AirPort import AirPort



        

class Object:
    def __init__(self):
        
        self.Inlet1=AirPort() 
        self.Inlet2=AirPort() 
        self.Outlet=AirPort()
        self.id=1
        self.T=5
        self.RH = 60
        self.F = 10000
        self.Pv_sat=0
        self.w=0
        self.T_hum=0
        self.h=0
        self.P=101325
        
        self.F_dry=0
        self.F_dry1=0
        self.F_dry2=0
        
        
    def calculate(self):
        
        # self.F = self.F_m3h * air_humide.Air_rho_hum(self.T, self.RH, self.P)/3600 #kg/s
        # self.F = self.F/3600 #m3/s
        #Connecteur Inlet
                        
        self.Pv_sat=air_humide.Air_Pv_sat(self.T)
       # print("Pvsat=",self.Pv_sat)
        self.w=air_humide.Air_w(Pv_sat=self.Pv_sat,RH=self.RH,P=self.P)
       # print("w=",self.w)
        self.T_hum=air_humide.Air_T_wb(T_db=self.T,RH=self.RH)
      #  print("self.T_hum=",self.T_hum)
        self.h=air_humide.Air_h(T_db=self.T, w=self.w)
      #  print("self.h=",self.h)
        
        self.F_dry1=self.Inlet1.F/(1+self.Inlet1.w)
        self.F_dry2=self.Inlet2.F/(1+self.Inlet2.w)

        #connecteur   
      
        #self.Inlet1.w=self.w
        #self.Inlet.P=
        self.Outlet.w=(self.Inlet1.w*self.F_dry1+self.Inlet2.w*self.F_dry2)/(self.F_dry1+self.F_dry2)
        self.Outlet.P=min(self.Inlet1.P,self.Inlet2.P)
        self.Outlet.h=(self.Inlet1.h*self.F_dry1+self.Inlet2.h*self.F_dry2)/(self.F_dry1+self.F_dry2)
        self.Outlet.F=self.Inlet1.F+self.Inlet2.F 
        self.T_outlet=air_humide_NB.Air3_Tdb(self.Outlet.w/1000,self.Outlet.P,self.Outlet.h)
        self.F_dry=(self.Outlet.F)/(1+self.Outlet.w/1000)
    
    
    



