# Modèle de l'échangeur
from AHU.AirPort.AirPort import AirPort
from AHU.air_humide import air_humide
import pandas as pd

class Object:
    def __init__(self):
        # Initialisation des ports d'entrée et de sortie
        self.id=2 #identifiant de l'objet
        self.Inlet1 = AirPort()  # Air frais entrant
        self.Outlet1 = AirPort()  # Air frais sortant
        self.Inlet2 = AirPort()  # Air extrait entrant
        self.Outlet2 = AirPort()  # Air extrait sortant

        # Paramètres de l'échangeur
        self.h_efficiency = None  # Efficacité enthalpique (calculée)
        self.T_efficiency = 80    # Efficacité en température (%)
        self.heat_transfer = None  # Transfert de chaleur (W)
        self.T1o = None  # Température de sortie de l'air frais (°C)
        self.df=None

    def calculate(self):
        # Détermination du débit massique minimum
        min_flow = min(self.Inlet1.F_dry, self.Inlet2.F_dry)
        
        # Cas hivernal : l'air extrait est plus chaud que l'air extérieur
        if self.Inlet2.T >= self.Inlet1.T:
            # Calcul de la température de sortie de l'air frais
            self.T1o = self.Inlet1.T + (self.T_efficiency / 100) * (self.Inlet2.T - self.Inlet1.T)
            print(f"T1o : {self.T1o}")

            # Calcul de l'enthalpie de sortie de l'air frais
            self.Outlet1.h = air_humide.Air_h(T_db=self.T1o, w=self.Inlet1.w)
            self.Outlet1.w = self.Inlet1.w  # L'humidité absolue reste constante

            # Calcul du transfert de chaleur
            self.heat_transfer = (self.Outlet1.h - self.Inlet1.h) * self.Inlet1.F_dry
            print(f"self.heat_transfer,{self.heat_transfer}")

            # Calcul de l'efficacité enthalpique
            self.h_efficiency = 100 * self.Inlet1.F_dry * (self.Outlet1.h - self.Inlet1.h) / (min_flow * (self.Inlet2.h - self.Inlet1.h))
            print(f"h_efficiency,{self.h_efficiency}")

            # Calcul des propriétés de sortie de l'air extrait
            self.Outlet2.h = -(self.heat_transfer / self.Inlet2.F_dry) + self.Inlet2.h
            
            # Calcul de la température de rosée avant condensation
            self.Tdp_dry = air_humide.Air_T_dp(w=self.Inlet2.w)
            print(f"température de rosée avant condensation Tdp,{self.Tdp_dry}")
            
            # Calcul de la température de rosée selon l'enthalpie de sortie d'air vicié
            self.Tdp_wet = air_humide.Air_T_dp(h=self.Outlet2.h)
            print(f"Tdp,{self.Tdp_wet}")
            
            # Vérification de la condensation
            if self.Tdp_wet <= self.Tdp_dry:
                print("condensation")
                self.Outlet2.w = air_humide.Air_w(h=self.Outlet2.h, RH=100)
            else:
                print("pas de condensation")
                self.Outlet2.w = self.Inlet2.w

            print(f"Outlet2.w ,{self.Outlet2.w}")
            print(f"Outlet2.T ,{self.Outlet2.T}")
           
        # Cas estival : l'air extérieur est plus chaud que l'air extrait
        else:
            # Calcul de l'enthalpie de sortie de l'air frais
            self.Outlet1.h = self.Inlet1.h - self.efficiency / 100 * (min_flow * (self.Inlet1.h - self.Inlet2.h)) / self.Inlet1.F_dry
   
        # Conservation du débit massique et de l'humidité absolue
        self.Outlet1.F_dry = self.Inlet1.F_dry
        self.Outlet1.w = self.Inlet1.w
        self.Outlet2.F_dry = self.Inlet2.F_dry

        data = {
            'ID': [self.id],  # Identifiant de l'objet

            'Heat recovery (kW)': [self.heat_transfer],
            'sefficacité échangeur T_efficiency (%)': [self.T_efficiency],
            'rendement thermique (rapport des enthalpies) h_efficiency (%)': [self.h_efficiency],

            'self.Inlet1.T (C)': [self.Inlet1.T],  # Température de l'air
            'self.Outlet1.T (C)': [self.Outlet1.T],  # Température de l'air
            'self.Inlet2.T (C)': [self.Inlet2.T],  # Température de l'air
            'self.Outlet2.T (C)': [self.Outlet2.T],  # Température de l'air

            'self.Inlet1.RH (%)': [self.Inlet1.RH],  # Humidité relative
            'self.Outlet1.RH (%)': [self.Outlet1.RH],  # Humidité relative
            'self.Inlet2.RH (%)': [self.Inlet2.RH],  # Humidité relative
            'self.Outlet2.RH (%)': [self.Outlet2.RH],  # Humidité relative


            'self.Inlet1.F (kg/s)': [self.Inlet1.F],  # Débit d'air en kg/s
            'self.Inlet1.F_dry (kg/s)': [self.Inlet1.F_dry],  # Débit d'air sec en kg/s
            'self.Outlet1.F (kg/s)': [self.Outlet1.F],  # Débit d'air en kg/s
            'self.Outlet1.F_dry (kg/s)': [self.Outlet1.F_dry],  # Débit d'air sec en kg/s
            'self.Inlet2.F (kg/s)': [self.Inlet2.F],  # Débit d'air en kg/s
            'self.Inlet2.F_dry (kg/s)': [self.Inlet2.F_dry],  # Débit d'air sec en kg/s
            'self.Outlet2.F (kg/s)': [self.Outlet2.F],  # Débit d'air en kg/s
            'self.Outlet2.F_dry (kg/s)': [self.Outlet2.F_dry],  # Débit d'air sec en kg/s

            'self.Inlet1.P (Pa)': [self.Inlet1.P],  # Pression de l'air
            'self.Outlet1.P (Pa)': [self.Outlet1.P],  # Pression de l'air
            'self.Inlet2.P (Pa)': [self.Inlet2.P],  # Pression de l'air
            'self.Outlet2.P (Pa)': [self.Outlet2.P],  # Pression de l'air

            'self.Inlet1.h (kJ/kg)': [self.Inlet1.h],  # Enthalpie spécifique
            'self.Outlet1.h (kJ/kg)': [self.Outlet1.h],  # Enthalpie spécifique
            'self.Inlet2.h (kJ/kg)': [self.Inlet2.h],  # Enthalpie spécifique
            'self.Outlet2.h (kJ/kg)': [self.Outlet2.h],  # Enthalpie spécifique

            'self.Inlet1.w (gH2O/kgdry)': [self.Inlet1.w],  # Humidité absolue
            'self.Outlet1.w (gH2O/kgdry)': [self.Outlet1.w],  # Humidité absolue
            'self.Inlet2.w (gH2O/kgdry)': [self.Inlet2.w],  # Humidité absolue
           'self.Outlet2.w (gH2O/kgdry)': [self.Outlet2.w],  # Humidité absolue


            'self.Inlet1.Pv_sat (Pa)': [self.Inlet1.Pv_sat],  # Pression de vapeur saturante
            'self.Outlet1.Pv_sat (Pa)': [self.Outlet1.Pv_sat],  # Pression de vapeur saturante
            'self.Inlet2.Pv_sat (Pa)': [self.Inlet2.Pv_sat],  # Pression de vapeur saturante
            'self.Outlet2.Pv_sat (Pa)': [self.Outlet2.Pv_sat],  # Pression de vapeur saturante
        }

        # Convertir les données en DataFrame et transposer pour avoir les paramètres en lignes
        self.df = pd.DataFrame(data).T
       