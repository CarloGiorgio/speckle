import numpy as np
import numpy.random as rng
from scipy.stats import norm

def specklesAlgorithm(img):
        """
        Modulìus sqaured and shifted pattern
        """
        return FT.fftshift(abs(FT.fft2(img))**2)

indexCorrelation = lambda k,N,nu=2: 2*(1-((x-1)/(N-1))**nu)**2-1



class speckle:
    def __init__(self,L1,L2):
        self.L1 = L1
        self.L2 = L2
        self.size = (L1,L2)
        J,I = np.indices(self.size)
        self.J = J - J.mean()
        self.I = I - I.mean()
        self.img = np.zeros(self.size,dtype = complex)
    
    def setRadialMask(self,x0 = 0,y0 = 0):
        """Set the radial mask for the 

        Args:
            r0 (_type_): _description_
            x0 (int, optional): _description_. Defaults to 0.
            y0 (int, optional): _description_. Defaults to 0.
            
        """
        self.RR = np.sqrt((self.I-x0)**2+(self.J-x0)**2)
        
        
    def speckleFromPhase(self,r0,phi):
    """
    Generate speckle pattern from a uniform phase one
    """
    self.img = self.img*0
    self.img = np.where(RR<r0,np.exp(1j*phi),self.img)
    return specklesAlgorithm(self.img)
    
    def generate(self,r0):
        """
        Generate single speckles pattern
        """
        self.img = self.img*0
        phi = 2*np.pi*np.random.random(self.size)
        return self.speckleFromPhase(r0,phi)
    

    
    def performCorrelation(self,A,B,correlation):
        """
        Perform the correlation between 2 normal random variables 
        with 'correlation' as correlation coefficient
        """
        
        z1 = 1/np.sqrt(2)*(np.sqrt(1+correlation)*A - np.sqrt(1-correlation)*B)
        z2 = 1/np.sqrt(2)*(np.sqrt(1+correlation)*A + np.sqrt(1-correlation)*B) 
        return z1,z2
    
    def specklesCorrelatedFromPhase(self,phi1,phi2,r0,correlation):
        """
        Generation of correlated speckles from normal phase already determined
        """
        z1,z2 = self.performCorrelation(phi1,phi2,correlation)
        t1 = norm.cdf(z1)
        t2 = norm.cdf(z2)
        img1 = speckleFromPhase(r0,2*np.pi*t1)
        img2 = speckleFromPhase(r0,2*np.pi*t2)
        return img1,img2
    
    
    def specklesCorrelated(self,r0,correlation):
        """
        Generation of correlated speckles from phase
        """
        phi1 = rng.normal(size = self.size)
        phi2 = rng.normal(size = self.size)
        return self.specklesCorrelatedFromPhase(phi1,phi2,r0,correlation)
    
    
    
    def setTimeSerie(self):
        """
        Save the first pattern and the target pattern.
        """
        self.img1 = rng.normal(size = self.size)
        self.img2 = rng.normal(size = self.size)
        
    def specklesTimeSeries(self,r0,k,N,nu = 2):
        """
        Perform the correlation and evaluate the evolution.
        """
        if not hasattr(self,'img1'):
            self.setTimeSerie()
        correlation = indexCorrelation(k,N,nu)
        img1,_  = self.specklesCorrelatedFromPhase(self.img1,self.img2,r0,correlation)
        return img1