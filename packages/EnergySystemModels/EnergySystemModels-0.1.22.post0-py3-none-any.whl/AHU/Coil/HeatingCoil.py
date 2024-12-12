from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB

from AHU.AirPort.AirPort import AirPort

class Object:
    def __init__(self):
        self.Inlet=AirPort() 
        self.Outlet=AirPort()
        self.P=0
        self.P_drop=0
        self.id=2
        # données air neuf
        self.T_in=0
        self.hi=0
        self.wi=12
        self.F=0
        self.F_dry=0
        
        #consigne
        self.To_target=20
        # calcul Outlet Coil
        self.ho=0
        self.Q_th=12
        self.RH_out=0
       
        
    def calculate(self):
        
          #connecteur  
        self.Outlet.P=self.Inlet.P-self.P_drop
      
        self.wi=self.Inlet.w
        self.P=self.Inlet.P
        self.hi=self.Inlet.h
        self.F=self.Inlet.F
        # print("cond self.F",self.F)
        self.T_in=air_humide_NB.Air3_Tdb(self.wi/1000,self.Inlet.P,self.hi)
        self.F_dry=(self.F)/(1+self.wi/1000) #[kg air sec/s]
        ''' Témpérature fluide entré Coil < Température consigne -> Rechauffement sensible'''
        if self.To_target>self.T_in:
            
            self.ho=air_humide.Air_h(T_db=self.To_target,w=self.wi)
            # self.ho=air_humide_NB.Air2_Hs(self.To_target, air_humide_NB.Air4_RH(self.To_target,self.Outlet.P, self.wi/1000), self.Outlet.P) 
          #  print("ho=",self.ho)
            self.F_dry=(self.F)/(1+self.wi/1000) # [kg air sec/s]
           # print("self.F_dry=",self.F_dry,"self.Inlet.P=",self.Inlet.P,"self.F=",self.F)
            self.Q_th=(self.ho-self.hi)*self.F_dry
           # print("self.Q_th=",self.Q_th)
            self.RH_out=air_humide.Air_RH(Pv_sat=air_humide.Air_Pv_sat(self.To_target),w=self.wi,P=self.Outlet.P) #parametrer la pression
           # print("self.RH_out=",self.RH_out)
        
            ''' Température fluide entrée Coil > température de consigne -> Aucune action'''    
        else:
            self.ho=self.hi
            self.Q_th=0
 
              
       
        #connecteur   
      
          
        self.Outlet.w=self.Inlet.w
        
        self.Outlet.h=self.ho
        
        self.Outlet.F=self.F_dry*(1+self.Outlet.w/1000)  #[kg air sec/s] * [m3/kg air sec] =[m3/s]
        self.Outlet.F_dry=self.F_dry
#
        # print(self.Outlet.w/1000, self.Outlet.P, self.Outlet.h)       
        # self.Twb_out=air_humide_NB.Air3_Twb(self.Outlet.w/1000, self.Outlet.P, self.Outlet.h)


