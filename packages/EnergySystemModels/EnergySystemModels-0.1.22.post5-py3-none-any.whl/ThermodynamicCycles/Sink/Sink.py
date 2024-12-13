from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
from datetime import datetime

class Object:
    def __init__(self):
        self.Timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #Input and Output Connector
       # self.Inlet=FluidPort() 
        self.Inlet=FluidPort()

        #output Data
        self.fluid=None #"air"
        self.F_Sm3s=0
        self.F_m3s=0
        self.Po_bar=0
        self.To_degC=0

        self.F_Sm3h=0
        self.F_m3h=0
        self.F_kgh=0
        


        

        #Initial Values
        self.Inlet.fluid=None #"air"
        self.Inlet.P=None #101325
        self.F=None #0.1
        self.H=None
        self.D=None
        
        self.Q=0
        self.fluid_quality="liquid"
        self.df = pd.DataFrame()
       
    
        
    def calculate (self):
        try:
            self.F=self.Inlet.F
            self.fluid=self.Inlet.fluid
            self.Po_bar=self.Inlet.P/100000
        
            #calcul de l'état du fluid
            try:
                self.To_degC=PropsSI("T", "P", 100000*self.Po_bar, "H", self.Inlet.h,self.fluid)-273.15
            except:
                self.To_degC=0-273.15

            if (100000*self.Po_bar)<PropsSI("Pcrit",self.fluid): #comparer à la pression critique
                Hv=PropsSI("H", "P", 100000*self.Po_bar, "Q", 1, self.fluid)
            # print("Hv=",Hv)
                Hl=PropsSI("H", "P", 100000*self.Po_bar, "Q", 0, self.fluid)
            #  print("Hl=",Hl)
                self.Q=1-((Hv-self.Inlet.h)/(Hv-Hl))
                
                if self.Q>=1:
                # print(self.fluid+" vapeur"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="vapor"
                elif (self.Q<1 and self.Q>0):
                # print(self.fluid+" diphasique"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="two-phase"
                else:
                    #print(self.fluid+" liquide"+"%.2f" % self.Q) #"%d" % 
                    self.fluid_quality="liquid"
            # print("Qualité=",self.Q)
                
            else:
                #print(self.fluid+" supercritique") #"%d" % 
                self.fluid_quality="supercritical"
                
            
            if (100000*self.Po_bar)<PropsSI("Pcrit",self.fluid): #comparer à la pression critique
                if self.Q>1:
                    self.F_m3s=self.Inlet.F/PropsSI("D", "P", 100000*self.Po_bar, "T", (self.To_degC+273.15), self.fluid)
                elif (self.Q<=1 and self.Q>=0):
                    self.F_m3s=self.Q*self.Inlet.F/PropsSI("D", "P", 100000*self.Po_bar, "Q", 1, self.fluid)+(1-self.Q)*self.Inlet.F/PropsSI("D", "P", 100000*self.Po_bar, "Q", 0, self.fluid)
                else:
                    self.F_m3s=self.Inlet.F/PropsSI("D", "P", 100000*self.Po_bar, "T", (self.To_degC+273.15), self.fluid)        
            else:    
                self.F_m3s=self.Inlet.F/PropsSI("D", "P", 100000*self.Po_bar, "T", (self.To_degC+273.15), self.fluid)
            
            self.F_Sm3s=self.Inlet.F/PropsSI("D", "P", 100000*1.01325, "T", (15+273.15), self.fluid)

            self.F_Sm3h=self.F_Sm3s*3600
            self.F_m3h=self.F_m3s*3600
            self.F_kgh=self.Inlet.F*3600

            self.H=self.Inlet.h*self.F
            self.D=PropsSI("D", "P", 100000*self.Po_bar, "T", (self.To_degC+273.15), self.fluid)
            
            self.Inlet.calculate_properties()
       

            self.df = pd.DataFrame({'Sink': [self.Timestamp,self.Inlet.fluid,self.Inlet.F,self.Inlet.P,self.Inlet.h,self.H,self.fluid_quality,self.Q,self.D,self.F_Sm3h,self.F_m3h,self.F_kgh,], },
                        index = ['Timestamp','sk_fluid','sk_F_kgs','sk_P(Pa)','sk_h(J/kg)','sk_H(W)','sk_fluid_quality','sk_Q','sk_Density (kg/m3)','sk_F_Sm3h','sk_F_m3h', 'sk_F_kgh',])
            #print(self.df)
            
        except:
            print('''Error! please connect the sink to another model or check that: \nInlet.fluid, Inlet.F, Inlet.P and Inlet.h \nare known''')