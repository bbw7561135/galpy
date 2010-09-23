import numpy as nu
from scipy import integrate
from OrbitTop import OrbitTop
from galpy.potential_src.linearPotential import evaluatelinearForces,\
    evaluatelinearPotentials
import galpy.util.bovy_plot as plot
class linearOrbit(OrbitTop):
    """Class that represents an orbit in a (effectively) one-dimensional potential"""
    def __init__(self,vxvv=[1.,0.]):
        """
        NAME:
           __init__
        PURPOSE:
           Initialize a linear orbit
        INPUT:
           vxvv - [x,vx]
        OUTPUT:
        HISTORY:
           2010-07-13 - Written - Bovy (NYU)
        """
        self.vxvv= vxvv
        return None

    def integrate(self,t,pot):
        """
        NAME:
           integrate
        PURPOSE:
           integrate the orbit
        INPUT:
           t - list of times at which to output (0 has to be in this!)
           pot - potential instance or list of instances
        OUTPUT:
           (none) (get the actual orbit using getOrbit()
        HISTORY:
           2010-07-13 - Written - Bovy (NYU)
        """
        self.t= nu.array(t)
        self._pot= pot
        self.orbit= _integrateLinearOrbit(self.vxvv,pot,t)

    def E(self,pot=None):
        """
        NAME:
           E
        PURPOSE:
           calculate the energy
        INPUT:
           pot=
        OUTPUT:
           energy
        HISTORY:
           2010-09-15 - Written - Bovy (NYU)
        """
        if pot is None:
            try:
                pot= self._pot
            except AttributeError:
                raise AttributeError("Integrate orbit or specify pot=")
        return evaluatelinearPotentials(self.vxvv[0],pot)+\
            self.vxvv[1]**2./2.

    def e(self):
        """
        NAME:
           e
        PURPOSE:
           calculate the eccentricity
        INPUT:
        OUTPUT:
           eccentricity
        HISTORY:
           2010-09-15 - Written - Bovy (NYU)
        """
        raise AttributeError("linearOrbit does not have an eccentricity")

    def rap(self):
        raise AttributeError("linearOrbit does not have an apocenter")

    def rperi(self):
        raise AttributeError("linearOrbit does not have a pericenter")

    def zmax(self):
        raise AttributeError("linearOrbit does not have a zmax")

    def plotE(self,*args,**kwargs):
        """
        NAME:
           plotE
        PURPOSE:
           plot E(.) along the orbit
        INPUT:
           pot - Potential instance or list of instances in which the orbit was
                 integrated
           d1= - plot Ez vs d1: e.g., 't', 'x', 'vx'
           +bovy_plot.bovy_plot inputs
        OUTPUT:
           figure to output device
        HISTORY:
           2010-07-10 - Written - Bovy (NYU)
        """
        if not kwargs.has_key('pot'):
            try:
                pot= self._pot
            except AttributeError:
                raise AttributeError("Integrate orbit first or specify pot=")
        else:
            pot= kwargs['pot']
            kwargs.pop('pot')
        if kwargs.has_key('d1'):
            d1= kwargs['d1']
            kwargs.pop('d1')
        else:
            d1= 't'
        self.Es= [evaluatelinearPotentials(self.orbit[ii,0],pot)+
                 self.orbit[ii,1]**2./2.
                 for ii in range(len(self.t))]
        if d1 == 't':
            plot.bovy_plot(nu.array(self.t),nu.array(self.Es)/self.Es[0],
                           *args,**kwargs)
        elif d1 == 'x':
            plot.bovy_plot(self.orbit[:,0],nu.array(self.Es)/self.Es[0],
                           *args,**kwargs)
        elif d1 == 'vx':
            plot.bovy_plot(self.orbit[:,1],nu.array(self.Es)/self.Es[0],
                           *args,**kwargs)

    def _callRect(self,*args):
        kwargs['rect']= False
        vxvv= self.__call__(*args,**kwargs)     

def _integrateLinearOrbit(vxvv,pot,t):
    """
    NAME:
       integrateLinearOrbit
    PURPOSE:
       integrate a one-dimensional orbit
    INPUT:
       vxvv - initial condition [x,vx]
       pot - linearPotential or list of linearPotentials
       t - list of times at which to output (0 has to be in this!)
    OUTPUT:
       [:,2] array of [x,vx] at each t
    HISTORY:
       2010-07-13- Written - Bovy (NYU)
    """
    return integrate.odeint(_linearEOM,vxvv,t,args=(pot,),rtol=10.**-8.)

def _linearEOM(y,t,pot):
    """
    NAME:
       linearEOM
    PURPOSE:
       the one-dimensional equation-of-motion
    INPUT:
       y - current phase-space position
       t - current time
       pot - (list of) linearPotential instance(s)
    OUTPUT:
       dy/dt
    HISTORY:
       2010-07-13 - Bovy (NYU)
    """
    return [y[1],evaluatelinearForces(y[0],pot,t=t)]
