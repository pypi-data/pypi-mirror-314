# Importation des modules nécessaires
from AHU.air_humide import air_humide
from AHU.air_humide import air_humide_NB
from AHU.AirPort.AirPort import AirPort
import pandas as pd

class Object:
    """
    Classe représentant une unité de traitement d'air avec des propriétés thermodynamiques
    et des calculs associés à l'air humide. Elle calcule les propriétés de l'air en fonction
    de la température, de l'humidité relative, du débit d'air et de la pression.
    """
    
    def __init__(self):
        """
        Initialisation de l'objet. Définit les propriétés de l'air et initialise les objets
        AirPort pour l'entrée et la sortie de l'air.
        """
        self.Inlet = AirPort()  # Port d'entrée de l'air
        self.Outlet = AirPort()  # Port de sortie de l'air
        self.id = 1  # Identifiant de l'objet
        self.T = None  # Température de l'air (Celsius)
        self.RH = None  # Humidité relative de l'air (%)
        self.F = None  # Débit massique d'air (kg/s)
        self.Pv_sat = 0  # Pression de vapeur saturante (Pa)
        self.w = 0  # Humidité absolue de l'air (kg/kg)
        self.T_hum = 0  # Température humide (C)
        self.h = 0  # Enthalpie spécifique (J/kg)
        self.P = 101325  # Pression de l'air (Pa) - valeur standard à la mer
        self.F_m3h = None  # Débit volumique en m3/h (air humide)
        self.F_dry = None  # Débit d'air sec (kg/s)
        self.df = None  # DataFrame pour afficher les résultats

    def calculate(self):
        """
        Effectue les calculs thermodynamiques sur l'air humide. Calcule l'humidité absolue,
        l'enthalpie, le débit d'air sec et met à jour les propriétés d'entrée et de sortie.
        """
        
        # Si la pression d'entrée est spécifiée, on l'utilise pour les calculs
        if self.Inlet.P is not None:
            self.P = self.Inlet.P
        
        # Cas où T et RH sont définis
        if self.T is not None and self.RH is not None:
            #print(f"Calcul avec T={self.T}°C, RH={self.RH}%")  # Affichage des valeurs d'entrée
            # Calcul de la pression de vapeur saturante à partir de la température
            self.Pv_sat = air_humide.Air_Pv_sat(self.T)
            # Calcul de l'humidité absolue en fonction de la pression de vapeur saturante, de l'humidité relative et de la pression
            self.w = air_humide.Air_w(Pv_sat=self.Pv_sat, RH=self.RH, P=self.P)
            # Calcul de l'enthalpie spécifique de l'air humide à partir de la température et de l'humidité absolue
            self.h = air_humide.Air_h(T_db=self.T, w=self.w)
            # Mise à jour de l'humidité absolue et de l'enthalpie à l'entrée
            self.Inlet.w = self.w
            self.Inlet.h = self.h

            # Si un débit volumique est fourni, on le convertit en débit massique (kg/s)
            if self.F_m3h is not None:
                self.F = self.F_m3h * air_humide.Air_rho_hum(self.T, self.RH, self.P) / 3600  # Conversion m3/h à kg/s
        
        # Cas où seulement le débit d'air est disponible
        if self.Inlet.F is not None:
            self.F = self.Inlet.F
        
        # Si le débit massique est disponible, on l'affecte à l'entrée
        if self.F is not None:
            self.Inlet.F = self.F
        
        # Mise à jour de l'enthalpie et de l'humidité absolue à partir des valeurs de l'entrée
        if self.Inlet.h is not None:
            self.h = self.Inlet.h
        if self.Inlet.w is not None:
            self.w = self.Inlet.w
        
        # Calcul du débit d'air sec en fonction de l'air humide et de l'humidité absolue
        self.F_dry = self.F / (1 + (self.w / 1000))
        if self.Inlet.F_dry is None:
            self.Inlet.F_dry=self.F_dry
        self.Outlet.F_dry=self.F_dry
        # Mise à jour des propriétés de l'air à la sortie en fonction de l'entrée
        self.Outlet.w = self.Inlet.w
        self.Outlet.P = self.Inlet.P
        self.Outlet.h = self.Inlet.h
        self.Outlet.F = self.Inlet.F

        # Affichage des résultats après le calcul
        #print(f"Calcul 2 avec T={self.T}°C, RH={self.RH}%")  

        # Préparation des données pour créer un DataFrame et afficher les résultats
        data = {
            'ID': [self.id],  # Identifiant de l'objet
            'self.Outlet.T (C)': [self.Outlet.T],  # Température de l'air
            'self.Outlet.RH (%)': [self.Outlet.RH],  # Humidité relative
            'self.Outlet.F (kg/s)': [self.Outlet.F],  # Débit d'air en kg/s
            'self.Outlet.F_dry (kg/s)': [self.Outlet.F_dry],  # Débit d'air sec en kg/s
            'self.Outlet.P (Pa)': [self.Outlet.P],  # Pression de l'air
            'self.Outlet.h (kJ/kg)': [self.Outlet.h],  # Enthalpie spécifique
            'self.Outlet.w (g/kgdry)': [self.Outlet.w],  # Humidité absolue
            'self.Outlet.Pv_sat (Pa)': [self.Outlet.Pv_sat],  # Pression de vapeur saturante
        }

        # Convertir les données en DataFrame et transposer pour avoir les paramètres en lignes
        self.df = pd.DataFrame(data).T

