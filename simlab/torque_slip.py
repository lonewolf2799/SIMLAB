import numpy as np
def torque_vs_slip(V,f):
    #Stator components
    r1 = 0.6 
    x1 = 1.0
    #Rotor components
    r2 = 0.3 # referred to the primary side
    x2 = 0.4 # referred to the primary side
    #Magnetising branch component
    xm = 27
    P = 4 # it is a 4 pole machine
    Ns = 120*f/P
    #print('NS = ', Ns)
    Ws = 2*np.pi*Ns/60
    V_phase = V/np.sqrt(3)
    Vth = V_phase * (xm/np.sqrt( r1**2+ (x1+xm)**2) )
    zth = ((1j*xm) * (r1 + 1j*x1))/(r1 + 1j*(x1+xm))
    #print(Vth)
    #print(zth)
    Rth = np.real(zth)    
    Xth = np.imag(zth)
    slip= []
    for i in range(-100,50,1):
        if(i == 0):
            slip.append(0.001)
        else:
            slip.append(i/50)
    #print(slip)
    #print('\n\n')
    Torq = []
    for i in range(0,len(slip)):
        t = (3 * (Vth**2) *r2/slip[i])/(Ws * (  ( Rth + r2/slip[i] )**2 + (Xth + x2)**2 ) )
        Torq.append(t)

    Nr = [(1-i)*Ns for i in slip] # Rotor Speed
    
    
    #figure = plt.figure(figsize = (10,5))
    #plt.plot(Nr,Torq,c = 'red')
    #plt.grid()
    #plt.show()

    return Torq,slip,Nr
    

    # df = pd.DataFrame(list(zip(slip,Nr,Torq)),columns = ['slip','Rotor Speed','Torque'])
    # return df