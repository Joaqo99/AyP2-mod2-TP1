import numpy as np

#Velocidad del sonido [m/s2]
c_o = 343
#Densidad del aire 
ro_o = 1.18
#Frecuencias de interés tercio octava (f_to) [Hz]
f_to = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]


def sigma(frec_critica, l1, l2):


    sigmalist = []

    f11 = (((c_o)**2)/(4*frec_critica))*((1/(l1**2))+(1/(l2**2)))

    for i in range(len(f_to)):

        sig1 = 1/np.sqrt(1-(frec_critica/(f_to[i])))
        sig2 = 4*l1*l2*((f_to[i])/c_o)**2
        sig3 = np.sqrt((2*np.pi*(f_to[i])*(l1+l2))/(16*c_o))
        lmda = np.sqrt((f_to[i])/frec_critica)
        delta1 = ((1-lmda**2)*np.log((1+lmda)/(1-lmda ))+2*lmda)/(4*((np.pi)**2)*(1-lmda**2 )**1.5)
        delta2 = ((8*c_o**2)*(1-2*(lmda)**2))/((frec_critica**2)*(np.pi**4)*l1*l2*lmda*(np.sqrt(1-(lmda**2))))

        if f11 <= (frec_critica/2):
            if f_to[i] >= frec_critica:
                sigma = sig1
                
            else:                    #si f < fc
                if f_to[i] > frec_critica/2:
                    delta2 = 0
                sigma = ((2*(l1+l2)*c_o*delta1)/(l1*l2*frec_critica)) + delta2
                
            if f_to[i] < f11 < frec_critica/2 and sigma > sig2:
                sigma = sig2

            if sigma > 2:
                sigma = 2
            sigmalist.append(sigma)    

                
        else:    #f11 > frec_critica/2:
            if f_to[i] < frec_critica and sig2 < sig3:
                sigma = sig2
                
            elif f_to[i] > frec_critica and sig1 < sig3:
                sigma = sig1

            else:
                sigma = sig3

            if sigma > 2:
                sigma = 2
            sigmalist.append(sigma)    

    return sigmalist

def nabla_fun(k_o, l_x, l_y):
    """
    Calculates the 'nabla' parameter based on geometrical and wave properties.

    Parameters:
    - k_o (list or array): Wave numbers corresponding to specific frequencies.
    - l_x (float): The length of the material in the x-direction (meters).
    - l_y (float): The length of the material in the y-direction (meters).

    Returns:
    - nabla (list): A list of 'nabla' values, calculated for each wave number in `k_o`.
    """
    nabla = []
    for i in range(len(f_to)):
        nabla_i = -0.964 - (0.5+(l_y/(np.pi*l_x)))*np.log(l_y/l_x) + ((5*l_y)/(2*np.pi*l_x)) - (1/(4*np.pi*l_x*l_y*(k_o[i]**2)))
        nabla.append(nabla_i)
    return nabla

def sigma_f_fun(nabla, k_o, l_x, l_y):
    """
    Calculates the 'nabla' parameter based on geometrical and wave properties.

    Parameters:
    - k_o (list or array): Wave numbers corresponding to specific frequencies.
    - l_x (float): The length of the material in the x-direction (meters).
    - l_y (float): The length of the material in the y-direction (meters).

    Returns:
    - nabla (list): A list of 'nabla' values, calculated for each wave number in `k_o`.
    """
    sigma_f =[]
    for i in range(len(f_to)):
        sigma_f_i = 0.5*(np.log(k_o[i]*((l_x*l_y)**(1/2)))-nabla[i])
        if sigma_f_i > 2:
            sigma_f_i = 2    
        sigma_f.append(sigma_f_i)   
    
    return sigma_f



                    
                    
                 




