import numpy as np


#Velocidad del sonido [m/s2]
c_o = 343
#Densidad del aire 
ro_o = 1.18
#Frecuencias de interés tercio octava (f_to) [Hz]
f_to = [20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]

def sigma(frec_critica, l1, l2):

    sigmalist = []

    f11 = (((c_o)**2)/4*frec_critica)*((1/(l1**2))+(1/(l2**2)))

    for i in range(len(f_to)):

        sig1 = 1/np.sqrt(1-(frec_critica/(f_to[i])))
        sig2 = 4*l1*l2*((f_to[i])/c_o)**2
        sig3 = np.sqrt((np.pi*(f_to[i])*(l1+l2))/(16*c_o))
        lmda = np.sqrt((f_to[i])/frec_critica)
        delta1 = ((1-lmda**2)*np.log((1+lmda)/(1-lmda))+2*lmda)/(4*((np.pi)**2)*(1-lmda**2)**1.5)
        delta2 = ((8*c_o**2)*(1-2*(lmda)**2))/((frec_critica**2)*(np.pi**4)*l1*l2*lmda*(np.sqrt(1-(lmda**2))))

        if f11 <= (frec_critica/2):
            if f_to[i] >= frec_critica:
                sigma = sig1
                
            else:                    #si f < fc
                if f_to[i] > frec_critica/2:
                    delta2 = 0
                sigma = ((2*(l1+l2)*c_o*delta1)/(l1*l2*frec_critica))+delta2
                
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

#Pruebas


sig = sigma(3185,6,4)
print(sig)
                    
                    
                 




