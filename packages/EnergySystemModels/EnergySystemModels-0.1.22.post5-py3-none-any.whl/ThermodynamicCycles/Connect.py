from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
def Fluid_connect( a=FluidPort(),b=FluidPort()):
    a.fluid=b.fluid
    a.P=b.P
    a.h=b.h
    a.F=b.F
    a.S=b.S
    a.T=b.T
    a.calculate_properties()
    b.calculate_properties()
    return "connectés"