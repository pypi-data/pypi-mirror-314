import numpy as np
import scipy
import scipy.optimize
import scipy.special
import warnings
import matplotlib.pyplot as plt
import astropy as ap

g=0.004317#newton's G in units of km/s, pc, Msun

def get_nfw_gc(c_triangle):
    return 1./(np.log(1.+c_triangle)-c_triangle/(1.+c_triangle))

def get_dehnen_core_gc(c_triangle):
    return ((1.+c_triangle)**3)/c_triangle**3

def get_dehnen_cusp_gc(c_triangle):
    return ((1.+c_triangle)**2)/c_triangle**2

def get_nfw_scale(triangle,h,m_triangle,c_triangle):#r_triangle, scale radius r_s and scale density rho_s, of NFW halo, units of pc and U(m_triangle) / u(r_scale)**3
    gc=get_nfw_gc(c_triangle)
    r_triangle=(2.*g*m_triangle/triangle/((1.e-4*h)**2))**0.3333333333333333#r_triangle in units of pc, where triangle is overdensity factor = [M_triangle / (4*pi*r_triangle**3)] / rho_crit_0, where rho_crit_0 = 3H_0^2/(8*pi*G), H_0 is hubble constant, m_triangle is given in units of Msun
    r_scale=r_triangle/c_triangle#scale radius in same units as r_triangle, where concentration is defined as c_triangle=r_triangle/r_scale
    return r_triangle,r_scale,gc*m_triangle/4./np.pi/r_scale**3

def get_dehnen_core_scale(triangle,h,m_triangle,c_triangle):#r_triangle, scale radius r_s and scale density rho_s, of NFW halo, units of pc and U(m_triangle) / u(r_scale)**3
    gc=get_dehnen_core_gc(c_triangle)
    r_triangle=(2.*g*m_triangle/triangle/((1.e-4*h)**2))**0.3333333333333333#r_triangle in units of pc, where triangle is overdensity factor = [M_triangle / (4*pi*r_triangle**3)] / rho_crit_0, where rho_crit_0 = 3H_0^2/(8*pi*G), H_0 is hubble constant, m_triangle is given in units of Msun
    r_scale=r_triangle/c_triangle#scale radius in same units as r_triangle, where concentration is defined as c_triangle=r_triangle/r_scale
    return r_triangle,r_scale,gc*m_triangle/(4./3.)/np.pi/r_scale**3

def get_dehnen_cusp_scale(triangle,h,m_triangle,c_triangle):#r_triangle, scale radius r_s and scale density rho_s, of NFW halo, units of pc and U(m_triangle) / u(r_scale)**3
    gc=get_dehnen_cusp_gc(c_triangle)
    r_triangle=(2.*g*m_triangle/triangle/((1.e-4*h)**2))**0.3333333333333333#r_triangle in units of pc, where triangle is overdensity factor = [M_triangle / (4*pi*r_triangle**3)] / rho_crit_0, where rho_crit_0 = 3H_0^2/(8*pi*G), H_0 is hubble constant, m_triangle is given in units of Msun
    r_scale=r_triangle/c_triangle#scale radius in same units as r_triangle, where concentration is defined as c_triangle=r_triangle/r_scale
    return r_triangle,r_scale,gc*m_triangle/(4./2.)/np.pi/r_scale**3

def get_abg_triangle_scale(triangle,h,m_triangle,c_triangle,alpha,beta,gamma):#r_triangle, scale radius r_s and scale density, rho_s, of abg halo, given triangle parameters, units of U(m_triangle)/U(r_triangle)**3
    r_triangle=(2.*g*m_triangle/triangle/((1.e-4*h)**2))**0.3333333333333333#r_triangle in units of pc, where triangle is overdensity factor = [M_triangle / (4*pi*r_triangle**3)] / rho_crit_0, where rho_crit_0 = 3H_0^2/(8*pi*G), H_0 is hubble constant, m_triangle is given in units of Msun
    r_scale=r_triangle/c_triangle#scale radius in same units as r_triangle, where concentration is defined as c_triangle=r_triangle/r_scale
        
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    z1=-c_triangle**alpha
    hf1=scipy.special.hyp2f1(a,b,c,z1)  
    return r_triangle,r_scale,m_triangle*(3.-gamma)/4./np.pi/(r_scale**3)/c_triangle**(3.-gamma)/hf1

def nfw_density(x,c_triangle):# returns rho_NFW(x) / rho_scale, where x = r / r_triangle
    cx=c_triangle*x #r / r_scale
    return 1./cx/(1.+cx)**2

def dehnen_core_density(x,c_triangle):# returns rho_NFW(x) / rho_scale, where x = r / r_triangle
    cx=c_triangle*x #r / r_scale
    return 1./(1.+cx)**4

def dehnen_cusp_density(x,c_triangle):# returns rho_NFW(x) / rho_scale, where x = r / r_triangle
    cx=c_triangle*x #r / r_scale
    return 1./cx/(1.+cx)**3

def nfw_mass(x,c_triangle):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
    gc=get_nfw_gc(c_triangle)
    cx=c_triangle*x #r / r_scale
    return gc*(np.log(1.+cx)-cx/(1.+cx))

def dehnen_core_mass(x,c_triangle):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
    gc=get_dehnen_core_gc(c_triangle)
    cx=c_triangle*x #r / r_scale
    return gc*(cx**3)/(1.+cx)**3

def dehnen_cusp_mass(x,c_triangle):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
    gc=get_dehnen_cusp_gc(c_triangle)
    cx=c_triangle*x #r / r_scale
    return gc*(cx**2)/(1.+cx)**2

def fncore(x,r_core,n_core):#returns f^n(x) for coreNFW model (Read, Walker, Pascal 2018), where x=r/r_triangle, r_core=r_core/r_triangle
    return (np.tanh(np.float64(x)/r_core))**n_core

def cnfw_density(x,c_triangle,r_core,n_core):#returns rho_coreNFW(x) / rho_s, where x = r/r_triangle and rho_s is scale radius of NFW profile
    ncorem1=n_core-1.
    two=2.
    return fncore(x,r_core,n_core)*nfw_density(x,c_triangle)+n_core*fncore(x,r_core,ncorem1)*(1.-fncore(x,r_core,two))/(x**2)/get_nfw_gc(c_triangle)*nfw_mass(x,c_triangle)/r_core/(c_triangle**3)

def cnfw_mass(x,c_triangle,r_core,n_core):# returns M_cNFW(x) / m_triangle, where x=r/r_triangle, x=r/r_triangle, r_core=(core radius)/ r_triangle
    return fncore(x,r_core,n_core)*nfw_mass(x,c_triangle)

def cnfwt_density(x,c_triangle,r_core,n_core,r_tide,delta):#returns rho_coreNFWtides(x) / rho_0, where x = r/r_triangle
    if ((type(x) is float)|(type(x) is np.float64)):
        if x<r_tide:
            return cnfw_density(x,c_triangle,r_core,n_core)
        else:
            return cnfw_density(r_tide,c_triangle,r_core,n_core)*((x/r_tide)**(-delta_halo))
    elif ((type(x) is list)|(type(x) is np.ndarray)):
        val=np.zeros(len(x))
        val[x<r_tide]=cnfw_density(x[x<r_tide],c_triangle,r_core,n_core)
        val[x>=r_tide]=cnfw_density(r_tide,c_triangle,r_core,n_core)*((x[x>=r_tide]/r_tide)**(-delta_halo))
        return val
    
def cnfwt_mass(x,c_triangle,r_core,n_core,r_tide,delta):#returns M_cNFWt(x) / m_triangle, where x=r/r_triangle, r_core=(core radius)/r_triangle, r_tide=(tidal radius)/r_triangle
    if ((type(x) is float)|(type(x) is np.float64)):
        if x<r_tide:
            return cnfw_mass(x,c_triangle,r_core,n_core)
        else:
            return cnfw_mass(r_tide,c_triangle,r_core,n_core,r_tide)+cnfw_density(r_tide,c_triangle,r_core,n_core)*get_nfw_gc(c_triangle)/(3.-delta)*((c_triangle*r_tide)**3)*(((x/r_tide)**(3.-delta))-1.)
    elif ((type(x) is list)|(type(x) is np.ndarray)):
        val=np.zeros(len(x))
        val[x<r_tide]=cnfw_mass(x[x<r_tide],c_triangle,r_core,n_core)
        val[x>=r_tide]=cnfw_mass(r_tide,c_triangle,r_core,n_core)+cnfw_density(r_tide,c_triangle,r_core,n_core)*get_nfw_gc(c_triangle)/(3.-delta)*((c_triangle*r_tide)**3)*(((x[x>=r_tide]/r_tide)**(3.-delta))-1.)
        return val

def abg_triangle_density(x,c_triangle,alpha,beta,gamma):# returns rho_abg(x) / rho_scale, where x = r / r_triangle
    cx=params['c_triangle']*x #r / r_scale
    return 1./(cx**gamma)/(1.+cx**alpha)**((beta-gamma)/alpha)

def abg_triangle_mass(x,c_triangle,alpha,beta,gamma):# returns enclosed mass M_abg(x) / m_triangle, where x = r/r_triangle
    cx=c_triangle*x #r / r_scale
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    z1=-cx**alpha
    z2=-c_triangle**alpha
    hf1=scipy.special.hyp2f1(a,b,c,z1)  
    hf2=scipy.special.hyp2f1(a,b,c,z2)
    return ((cx/c_triangle)**(3.-gamma))*hf1/hf2

def get_plum_scale(luminosity_tot,r_scale):#nu0, normalization factor for luminosity density profile
    nu0=3.*luminosity_tot/4./np.pi/r_scale**3
    sigma0=luminosity_tot/np.pi/r_scale**2
    return nu0,sigma0

def get_exp_scale(luminosity_tot,r_scale):#nu0, normalization factor for luminosity density profile
    nu0=luminosity_tot/2./np.pi**2/r_scale**3
    sigma0=luminosity_tot/2./np.pi/r_scale**2
    return nu0,sigma0

def get_a2bg_scale(luminosity_tot,r_scale,beta,gamma):#nu0, normalization factor for luminosity density profile
    alpha=2. 
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=beta/2.
    d=(beta-3.)/alpha
    nu0=luminosity_tot/2./np.pi/r_scale**3/scipy.special.gamma(d)/scipy.special.gamma(a)*scipy.special.gamma(b)
    sigma0=luminosity_tot/4./np.sqrt(np.pi)/(r_scale**2)*(beta-3.)*scipy.special.gamma(b)/scipy.special.gamma(a)/scipy.special.gamma(c)
    return nu0,sigma0

def get_abg_nu0(luminosity_tot,r_scale,alpha,beta,gamma):#nu0, normalization factor for luminosity density profile
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=beta/2.
    d=(beta-3.)/alpha
    nu0=luminosity_tot/4./np.pi/r_scale**3*alpha*scipy.special.gamma(b)/scipy.special.gamma(d)/scipy.special.gamma(a)
    sigma0=np.nan#haven't yet implemented, probably a numerical integration
    return nu0,sigma0

def plum_density(x):#nu(x) / nu0, x=r/r_scale
    return 1./(1.+x**2)**(2.5)

def plum_density_2d(x):#Sigma(X) / Sigma0, X=R/r_scale
    return 1./(1.+x**2)**2

def exp_density(x):#nu(x) / nu0, x=r/r_scale
    return scipy.special.kn(0,x)

def exp_density_2d(x):#Sigma(X) / Sigma0, X=R/r_scale
    return np.exp(-x)

def a2bg_density(x,beta,gamma):#nu(x) / nu0, x=r/r_scale
    return 1./(x**gamma)/(1.+x**2)**((beta-gamma)/2.)

def a2bg_density_2d(x,beta,gamma):#Sigma(X)/Sigma0, X=R/r_scale
    if x<1.e-50:
        x=1.e-50
    a=(beta-1.)/2.
    b=(beta-gamma)/2.
    c=beta/2.
    z1=-1./x**2
    hf1=scipy.special.hyp2f1(a,b,c,z1)  
    return x**(1.-beta)*hf1
    
def abg_density(x,alpha,beta,gamma):#nu(x) / nu0, x=r/r_scale
    return 1./(x**gamma)/(1.+x**alpha)**((beta-gamma)/alpha)

def abg_density_2d(x,alpha,beta,gamma):#Sigma(X)/Sigma0, X=R/r_scale
    return np.nan #requires numerical integration, haven't implemented this yet

def plum_number(x):#N(x) / N_tot, x=r/r_scale
    return (x**3)/(1.+x**2)**(1.5)

def exp_number(x):#N(x) / N_tot, x=r/r_scale
    if x>100:#fudge to overcome numerical error (function below returns nan)
        return 1.
    return 1./(3.*np.pi)*x*(3.*np.pi*scipy.special.kn(2,x)*scipy.special.modstruve(1,x)+scipy.special.kn(1,x)*(3.*np.pi*scipy.special.modstruve(2,x)-4.*x))

def a2bg_number(x,beta,gamma):#N(x)/N_tot, x=r/r_scale
    alpha=2.
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    d=(beta-3.)/alpha
    z1=-x**alpha
    z2=-np.inf**alpha
    hf1=scipy.special.hyp2f1(a,b,c,z1)  
    hf2=scipy.special.hyp2f1(a,b,c,z2)
    #return abg_number(x,2.,beta,gamma)
    return alpha/(3.-gamma)*(x**(3.-gamma))*hf1*scipy.special.gamma(b)/scipy.special.gamma(d)/scipy.special.gamma(a)
    
def abg_number(x,alpha,beta,gamma):#N(x)/N_tot, x=r/r_scale
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    d=(beta-3.)/alpha
    z1=-x**alpha
    z2=-np.inf**alpha
    hf1=scipy.special.hyp2f1(a,b,c,z1)  
    hf2=scipy.special.hyp2f1(a,b,c,z2)
    #return (x**(3.-gamma))*hf1/hf2 #should be equivalent to below
    return alpha/(3.-gamma)*(x**(3.-gamma))*hf1*scipy.special.gamma(b)/scipy.special.gamma(d)/scipy.special.gamma(a)

def plum_nscalenorm():#N(r_scale)/(nu0 *r_scale**3)
    return 4.*np.pi/3./(2.**1.5)

def exp_nscalenorm():#N(r_scale)/(nu0 *r_scale**3)
    return 2.*np.pi/3.*(3.*np.pi*scipy.special.kn(2,1.)*scipy.special.modstruve(1,1.)+scipy.special.kn(1,1.)*(3.*np.pi*scipy.special.modstruve(2,1.)-4.))

def a2bg_nscalenorm(beta,gamma):#N(r_scale)/(nu0 * r_scale**3)
    alpha=2.
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    z2=-1.
    hf2=scipy.special.hyp2f1(a,b,c,z2)
    return 4.*np.pi/(3.-gamma)*hf2
    
def abg_nscalenorm(alpha,beta,gamma):#N(r_scale)/(nu0 * r_scale**3)
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    c=(3.-gamma+alpha)/alpha
    z2=-1.
    hf2=scipy.special.hyp2f1(a,b,c,z2)
    return 4.*np.pi/(3.-gamma)*hf2

def plum_ntotnorm():#N(r=infinity)/(nu0 * r_scale**3)
    return 4.*np.pi/3.

def exp_ntotnorm():#N(r=infinity)/(nu0 * r_scale**3)
    return 2.*(np.pi**2)

def a2bg_ntotnorm(beta,gamma):#N(r=infinity)/(nu0 * r_scale**3)
    alpha=2.
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    #c=(3.-gamma+alpha)/alpha
    d=(beta-3.)/alpha
    return 2.*np.pi*scipy.special.gamma(d)*scipy.special.gamma(a)/scipy.special.gamma(b)

def abg_ntotnorm(alpha,beta,gamma):#N(r=infinity)/(nu0 * r_scale**3)
    a=(3.-gamma)/alpha
    b=(beta-gamma)/alpha
    #c=(3.-gamma+alpha)/alpha
    d=(beta-3.)/alpha
    return 4.*np.pi/alpha*scipy.special.gamma(d)*scipy.special.gamma(a)/scipy.special.gamma(b)



def get_dmhalo(model,**params):
    
    class dmhalo:
        
        def __init__(self,model=None,triangle=None,h=None,m_triangle=None,c_triangle=None,r_triangle=None,r_core=None,n_core=None,r_tide=None,delta=None,alpha=None,beta=None,gamma=None,rho_scale=None,r_scale=None,v_max=None,r_max=None,func_density=None,func_mass=None,func_vcirc=None):

            self.model=model
            self.triangle=triangle
            self.h=h
            self.m_triangle=m_triangle
            self.c_triangle=c_triangle
            self.r_triangle=r_triangle
            self.r_core=r_core
            self.n_core=n_core
            self.r_tide=r_tide
            self.delta=delta
            self.alpha=alpha
            self.beta=beta
            self.gamma=gamma
            self.rho_scale=rho_scale
            self.r_scale=r_scale
            self.v_max=v_max
            self.r_max=r_max
            self.func_density=func_density
            self.func_mass=func_mass
            self.func_vcirc=func_vcirc

    if model=='nfw':
        
        r_triangle,r_scale,rho_scale=get_nfw_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'])
        
        def func_density(x):
            return nfw_density(x,params['c_triangle'])
        def func_mass(x):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
            return nfw_mass(x,params['c_triangle'])

    if model=='dehnen_core':
        
        r_triangle,r_scale,rho_scale=get_dehnen_core_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'])
        
        def func_density(x):
            return dehnen_core_density(x,params['c_triangle'])
        def func_mass(x):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
            return dehnen_core_mass(x,params['c_triangle'])

    if model=='dehnen_cusp':
        
        r_triangle,r_scale,rho_scale=get_dehnen_cusp_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'])
        
        def func_density(x):
            return dehnen_cusp_density(x,params['c_triangle'])
        def func_mass(x):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
            return dehnen_cusp_mass(x,params['c_triangle'])

    elif model=='abg_triangle':

        r_triangle,r_scale,rho_scale=get_abg_triangle_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'],params['alpha'],params['beta'],params['gamma'])

        def func_density(x):
            return abg_triangle_density(x,params['c_triangle'],params['alpha'],params['beta'],params['gamma'])
        def func_mass(x):
            return abg_triangle_mass(x,params['c_triangle'],params['alpha'],params['beta'],params['gamma'])

    elif model=='cnfw':
        
        r_triangle,r_scale,rho_scale=get_nfw_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'])
        
        def func_density(x):
            return cnfw_density(x,params['c_triangle'],params['r_core'],params['n_core'])
        def func_mass(x):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
            return cnfw_mass(x,params['c_triangle'],params['r_core'],params['n_core'])

    elif model=='cnfwt':
        
        r_triangle,r_scale,rho_scale=get_nfw_scale(params['triangle'],params['h'],params['m_triangle'],params['c_triangle'])
        
        def func_density(x):
            return cnfwt_density(x,params['c_triangle'],params['r_core'],params['n_core'],params['r_tide'],params['delta'])
        def func_mass(x):# returns enclosed mass M(x) / m_triangle, where x = r/r_triangle
            return cnfwt_mass(x,params['c_triangle'],params['r_core'],params['n_core'],params['r_tide'],params['delta'])
        
    def func_vcirc(x):# returns circular velocity, km/s
        return np.sqrt(g*func_mass(x)*params['m_triangle']/(x*r_triangle))

    def neg_vcirc2(x):
        if x<0.:
            return 1.e+30
        return -func_mass(x)/x
        
    res=scipy.optimize.minimize(neg_vcirc2,[1.],method='nelder-mead',options={'xatol': 1e-8, 'disp': True})
    r_max=res.x[0]*r_triangle
    v_max=func_vcirc(res.x[0])

    if model=='nfw':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    if model=='dehnen_core':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    if model=='dehnen_cusp':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    elif model=='abg_triangle':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,alpha=params['alpha'],beta=params['beta'],gamma=params['gamma'],rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    elif model=='cnfw':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,r_core=params['r_core'],n_core=params['n_core'],rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    elif model=='cnfwt':
        return dmhalo(model=model,triangle=params['triangle'],h=params['h'],m_triangle=params['m_triangle'],c_triangle=params['c_triangle'],r_triangle=r_triangle,r_core=params['r_core'],n_core=params['n_core'],r_tide=params['r_tide'],delta=params['delta'],rho_scale=rho_scale,r_scale=r_scale,v_max=v_max,r_max=r_max,func_density=func_density,func_mass=func_mass,func_vcirc=func_vcirc)
    else:
        raise TypeError('DM halo not properly specified!')
    
def get_tracer(model,**params):

    class tracer:

        def __init__(self,model=None,luminosity_tot=None,upsilon=None,r_scale=None,nu0=None,sigma0=None,nscalenorm=None,ntotnorm=None,alpha=None,beta=None,gamma=None,rhalf_2d=None,rhalf_3d=None,func_density=None,func_density_2d=None,func_number=None):

            self.model=model
            self.luminosity_tot=luminosity_tot
            self.upsilon=upsilon
            self.r_scale=r_scale
            self.nu0=nu0
            self.sigma0=sigma0
            self.nscalenorm=nscalenorm
            self.ntotnorm=ntotnorm
            self.alpha=alpha
            self.beta=beta
            self.gamma=gamma
            self.rhalf_2d=rhalf_2d
            self.rhalf_3d=rhalf_3d
            self.func_density=func_density
            self.func_density_2d=func_density_2d
            self.func_number=func_number

    if model=='plum':

        rhalf_2d,rhalf_3d,xxx,yyy=get_rhalf(model,params['r_scale'],bigsigma0=1.,ellipticity=0.)
        nu0,sigma0=get_plum_scale(params['luminosity_tot'],params['r_scale'])
        def func_density(x):
            return plum_density(x)
        def func_density_2d(x):
            return plum_density_2d(x)
        def func_number(x):
            return plum_number(x)
        
        return tracer(model=model,luminosity_tot=params['luminosity_tot'],r_scale=params['r_scale'],upsilon=params['upsilon'],nu0=nu0,sigma0=sigma0,nscalenorm=plum_nscalenorm(),ntotnorm=plum_ntotnorm(),rhalf_2d=rhalf_2d,rhalf_3d=rhalf_3d,func_density=func_density,func_density_2d=func_density_2d,func_number=func_number)

    if model=='exp':

        rhalf_2d,rhalf_3d,xxx,yyy=get_rhalf(model,params['r_scale'],bigsigma0=1.,ellipticity=0.)
        nu0,sigma0=get_exp_scale(params['luminosity_tot'],params['r_scale'])
        def func_density(x):
            return exp_density(x)
        def func_density_2d(x):
            return exp_density_2d(x)
        def func_number(x):
            return exp_number(x)
        
        return tracer(model=model,luminosity_tot=params['luminosity_tot'],r_scale=params['r_scale'],upsilon=params['upsilon'],nu0=nu0,sigma0=sigma0,nscalenorm=exp_nscalenorm(),ntotnorm=exp_ntotnorm(),rhalf_2d=rhalf_2d,rhalf_3d=rhalf_3d,func_density=func_density,func_density_2d=func_density_2d,func_number=func_number)
    
    if model=='a2bg':

        rhalf_2d,rhalf_3d,xxx,yyy=get_rhalf(model,params['r_scale'],bigsigma0=1.,ellipticity=0.,beta=params['beta'],gamma=params['gamma'])
        nu0,sigma0=get_a2bg_scale(params['luminosity_tot'],params['r_scale'],params['beta'],params['gamma'])
        def func_density(x):
            return a2bg_density(x,params['beta'],params['gamma'])
        def func_density_2d(x):
            return a2bg_density_2d(x,params['beta'],params['gamma'])
        def func_number(x):
            return a2bg_number(x,params['beta'],params['gamma'])
        
        return tracer(model=model,luminosity_tot=params['luminosity_tot'],r_scale=params['r_scale'],upsilon=params['upsilon'],nu0=nu0,sigma0=sigma0,nscalenorm=a2bg_nscalenorm(params['beta'],params['gamma']),ntotnorm=a2bg_ntotnorm(params['beta'],params['gamma']),beta=params['beta'],gamma=params['gamma'],rhalf_2d=rhalf_2d,rhalf_3d=rhalf_3d,func_density=func_density,func_density_2d=func_density_2d,func_number=func_number)
    
    if model=='abg':

        rhalf_2d,rhalf_3d,xxx,yyy=get_rhalf(model,params['r_scale'],bigsigma0=1.,ellipticity=0.,alpha=params['alpha'],beta=params['beta'],gamma=params['gamma'])
        nu0,sigma0=get_abg_scale(params['luminosity_tot'],params['r_scale'],params['alpha'],params['beta'],params['gamma'])
        def func_density(x):
            return abg_density(x,params['alpha'],params['beta'],params['gamma'])
        def func_density_2d(x):
            return abg_density_2d(x,params['alpha'],params['beta'],params['gamma'])
        def func_number(x):
            return abg_number(x,params['alpha'],params['beta'],params['gamma'])
        
        return tracer(model=model,luminosity_tot=params['luminosity_tot'],r_scale=params['r_scale'],upsilon=params['upsilon'],nu0=nu0,sigma0=sigma0,nscalenorm=abg_nscalenorm(params['alpha'],params['beta'],params['gamma']),ntotnorm=abg_ntotnorm(params['alpha'],params['beta'],params['gamma']),alpha=params['alpha'],beta=params['beta'],gamma=params['gamma'],rhalf_2d=rhalf_2d,rhalf_3d=rhalf_3d,func_density=func_density,func_density_2d=func_density_2d,func_number=func_number)


def get_anisotropy(model,**params):

    class anisotropy:

        def __init__(self,model=None,beta_0=None,beta_inf=None,r_beta=None,n_beta=None,f_beta=None,beta=None):

            self.model=model
            self.beta_0=beta_0
            self.beta_inf=beta_inf
            self.r_beta=r_beta
            self.n_beta=n_beta
            self.f_beta=f_beta
            self.beta=beta

    if model=='read':

        def beta(x):#x = r / r_beta
            return params['beta_0']+(params['beta_inf']-params['beta_0'])/(1.+x**(-params['n_beta']))
        def f_beta(x):# x = r / r_beta
            return x**(2.*params['beta_inf'])*(1.+x**(-params['n_beta']))**(2.*(params['beta_inf']-params['beta_0'])/params['n_beta'])
    
        return anisotropy(model=model,beta_0=params['beta_0'],beta_inf=params['beta_inf'],r_beta=params['r_beta'],n_beta=params['n_beta'],f_beta=f_beta,beta=beta)
    
    else:
        raise TypeError('anisotropy model not properly specified!')


def get_rhalf(model,r_scale,**params):

    if model=='plum':
        rhalf_2d=r_scale
        rhalf_3d=1.30476909*r_scale
        nu0=3*params['bigsigma0']/4/r_scale
        ntot=(1.-params['ellipticity'])*np.pi*r_scale**2*params['bigsigma0']
    elif model=='exp':
        rhalf_2d=1.67835*r_scale
        rhalf_3d=2.22352*r_scale
        nu0=params['bigsigma0']/np.pi/r_scale
        ntot=(1.-params['ellipticity'])*2.*np.pi*r_scale**2*params['bigsigma0']
    elif model=='a2bg':
        def rootfind_2bg_2d(x,beta,gamma):
            return 0.5-np.sqrt(np.pi)*scipy.special.gamma((beta-gamma)/2)/2/scipy.special.gamma(beta/2)/scipy.special.gamma((3-gamma)/2)*x**(3-beta)*scipy.special.hyp2f1((beta-3)/2,(beta-gamma)/2,beta/2,-1/x**2)
        def rootfind_2bg_3d(x,beta,gamma):
            return -0.5+2*scipy.special.gamma((beta-gamma)/2)/scipy.special.gamma((beta-3)/2)/scipy.special.gamma((3-gamma)/2)/(3-gamma)*x**(3-gamma)*scipy.special.hyp2f1((3-gamma)/2,(beta-gamma)/2,(5-gamma)/2,-x**2)
        low0=1.e-20
        high0=1.e+20
        if ((type(r_scale) is float)|(type(r_scale) is np.float64)):
            rhalf_2d=r_scale*scipy.optimize.brentq(rootfind_2bg_2d,low0,high0,args=(params['beta'],params['gamma']),xtol=1.e-12,rtol=1.e-6,maxiter=1000,full_output=False,disp=True)
            rhalf_3d=r_scale*scipy.optimize.brentq(rootfind_2bg_3d,low0,high0,args=(params['beta'],params['gamma']),xtol=1.e-12,rtol=1.e-6,maxiter=100,full_output=False,disp=True)
        else:
            rhalf_2d=[]
            rhalf_3d=[]
            for i in range(0,len(r_scale)):
                rhalf_2d.append(r_scale[i]*scipy.optimize.brentq(rootfind_2bg_2d,low0,high0,args=(params['beta'][i],params['gamma'][i]),xtol=1.e-12,rtol=1.e-6,maxiter=1000,full_output=False,disp=True))
                rhalf_3d.append(r_scale[i]*scipy.optimize.brentq(rootfind_2bg_3d,low0,high0,args=(params['beta'][i],params['gamma'][i]),xtol=1.e-12,rtol=1.e-6,maxiter=100,full_output=False,disp=True))
            rhalf_2d=np.array(rhalf_2d)
            rhalf_3d=np.array(rhalf_3d)
        nu0=params['bigsigma0']*scipy.special.gamma(params['beta']/2)/np.sqrt(np.pi)/r_scale/scipy.special.gamma((params['beta']-1)/2)
        ntot=(1.-params['ellipticity'])*4.*np.sqrt(np.pi)*r_scale**2*params['bigsigma0']/(params['beta']-3)*scipy.special.gamma((3-params['gamma'])/2)*scipy.special.gamma(params['beta']/2)/scipy.special.gamma((params['beta']-params['gamma'])/2)

    elif model=='abg':
        def rootfind_abg_2d(x,alpha,beta,gamma):
            return np.nan#not computed yet, projection of abg model requires numerical integration
        def rootfind_abg_3d(x,alpha,beta,gamma):
            a=(3.-gamma)/alpha
            b=(beta-gamma)/alpha
            c=(3.-gamma+alpha)/alpha
            d=(beta-3.)/alpha
            z1=-x**alpha
            return -0.5+(x**(3.-gamma))*scipy.special.hyp2f1(a,b,c,z1)*scipy.special.gamma(b)/scipy.special.gamma(d)/scipy.special.gamma(c)
        low0=1.e-20
        high0=1.e+20
        if ((type(r_scale) is float)|(type(r_scale) is np.float64)):
            rhalf_2d=np.nan#not computed yet, projection of abg model requires numerical integration
            rhalf_3d=r_scale*scipy.optimize.brentq(rootfind_abg_3d,low0,high0,args=(params['alpha'],params['beta'],params['gamma']),xtol=1.e-12,rtol=1.e-6,maxiter=100,full_output=False,disp=True)
        else:
            rhalf_2d=[]
            rhalf_3d=[]
            for i in range(0,len(r_scale)):
                rhalf_2d.append(np.nan)#not computed yet, projection of abg model requires numerical integration
                rhalf_3d.append(r_scale[i]*scipy.optimize.brentq(rootfind_abg_3d,low0,high0,args=(params['alpha'],params['beta'][i],params['gamma'][i]),xtol=1.e-12,rtol=1.e-6,maxiter=100,full_output=False,disp=True))
            rhalf_2d=np.array(rhalf_2d)
            rhalf_3d=np.array(rhalf_3d)
        nu0=np.nan#not yet computed
        ntot=np.nan#not yet computed

    elif model=='captured_truncated':
        return
    else:
        raise ValueError('error in model specification')
    return rhalf_2d,rhalf_3d,nu0,ntot
    

def integrate(bigx,dmhalo,tracer,anisotropy,**params):
    
    if 'component' not in params:
        params['component']=['los','rad','tan','3d']#default is to calculate all three projected components and both 3D components (3D angular components are equal)
    if not 'upper_limit' in params:#default upper limit is infinity, common alternative is dmhalo.r_triangle
        params['upper_limit']=np.inf
    if not 'epsrel' in params:
        params['epsrel']=1.49e-8
    if not 'epsabs' in params:
        params['epsabs']=1.49e-8
    if not 'limit' in params:
        params['limit']=50

    class jeans_integral:
        def __init__(self,bigsigmasigmalos2=None,bigsigmasigmarad2=None,bigsigmasigmatan2=None,nusigmarad2=None,nusigmatan2=None):
            self.bigsigmasigmalos2=bigsigmasigmalos2
            self.bigsigmasigmarad2=bigsigmasigmarad2
            self.bigsigmasigmatan2=bigsigmasigmatan2
            self.nusigmarad2=nusigmarad2
            self.nusigmatan2=nusigmatan2
        
    def integrand1(x_halo,dmhalo,tracer,anisotropy):
        x_beta=x_halo*dmhalo.r_triangle/tracer.r_scale/anisotropy.r_beta# r / r_beta
        x_tracer=x_halo*dmhalo.r_triangle/tracer.r_scale# r / r_scale
        mass=dmhalo.func_mass(x_halo)+tracer.func_number(x_tracer)*tracer.luminosity_tot*tracer.upsilon/dmhalo.m_triangle
        return mass*tracer.func_density(x_tracer)*anisotropy.f_beta(x_beta)/x_halo**2
    
    def integrand_los(x_halo,dmhalo,tracer,anisotropy):
        x_beta=x_halo*dmhalo.r_triangle/tracer.r_scale/anisotropy.r_beta# r / r_beta
        min0=x_halo
        max0=params['upper_limit']
        int1=scipy.integrate.quad(integrand1,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])
        return (1.-anisotropy.beta(x_beta)*(bigx/x_halo)**2)/np.sqrt(1.-(bigx/x_halo)**2)/anisotropy.f_beta(x_beta)*int1[0]

    def integrand_rad(x_halo,dmhalo,tracer,anisotropy):
        x_beta=x_halo*dmhalo.r_triangle/tracer.r_scale/anisotropy.r_beta# r / r_beta
        min0=x_halo
        max0=params['upper_limit']
        int1=scipy.integrate.quad(integrand1,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])
        return (1.-anisotropy.beta(x_beta)+anisotropy.beta(x_beta)*(bigx/x_halo)**2)/np.sqrt(1.-(bigx/x_halo)**2)/anisotropy.f_beta(x_beta)*int1[0]

    def integrand_tan(x_halo,dmhalo,tracer,anisotropy):
        x_beta=x_halo*dmhalo.r_triangle/tracer.r_scale/anisotropy.r_beta# r / r_beta
        min0=x_halo
        max0=params['upper_limit']
        int1=scipy.integrate.quad(integrand1,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])
        return (1.-anisotropy.beta(x_beta))/np.sqrt(1.-(bigx/x_halo)**2)/anisotropy.f_beta(x_beta)*int1[0]
    
    min0=bigx
    max0=params['upper_limit']

    if min0==max0:
        bigsigmasigmalos2=0.
        bigsigmasigmarad2=0.
        bigsigmasigmatan2=0.
        nusigmarad2=0.
        nusigmatan2=0.
        
    else:
        
        if '3d' in params['component']:
            x_beta=x_halo*dmhalo.r_triangle/tracer.r_scale/anisotropy.r_beta# r / r_beta
            nusigmarad2=g*dmhalo.m_triangle/dmhalo.r_triangle/anisotropy.f_beta(x_beta)*scipy.integrate.quad(integrand1,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])[0]#sigma^2_r(x) * nu(x) / nu0, sigma_r(x) is 3D radial velocity dispersion at x=r/r_triangle
            nusigmatan2=nusigmar2*(1.-anisotropy.beta(x_beta))#sigma^2_t(x) * nu(x) / nu0, sigma_t(x) is 3D tangential velocity dispersion at x=r/r_triangle, equals both the theta component and the phi component
    
        if 'los' in params['component']:
            bigsigmasigmalos2=2.*g*dmhalo.m_triangle*scipy.integrate.quad(integrand_los,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])[0]#sigma^2_los(X) * Sigma(X) / nu0
        if 'rad' in params['component']:
            bigsigmasigmarad2=2.*g*dmhalo.m_triangle*scipy.integrate.quad(integrand_rad,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])[0]#sigma^2_rad(X) * Sigma(X) / nu0
        if 'tan' in params['component']:
            bigsigmasigmatan2=2.*g*dmhalo.m_triangle*scipy.integrate.quad(integrand_tan,min0,max0,args=(dmhalo,tracer,anisotropy),epsrel=params['epsrel'],epsabs=params['epsabs'])[0]#sigma^2_tan(X) * Sigma(X) / nu0
            
    return jeans_integral(bigsigmasigmalos2=bigsigmasigmalos2,bigsigmasigmarad2=bigsigmasigmarad2,bigsigmasigmatan2=bigsigmasigmatan2,nusigmarad2=nusigmarad2,nusigmatan2=nusigmatan2)

def integrate_isotropic(bigx,dmhalo,tracer,**params):
    if not 'upper_limit' in params:#default upper limit is infinity, common alternative is dmhalo.r_triangle
        params['upper_limit']=np.inf
    if not 'epsrel' in params:
        params['epsrel']=1.49e-8
    if not 'epsabs' in params:
        params['epsabs']=1.49e-8
    if not 'limit' in params:
        params['limit']=50
        
    def integrand1(x_halo,dmhalo,tracer):
        x_tracer=x_halo*dmhalo.r_triangle/tracer.r_scale# r / r_scale
        mass=dmhalo.func_mass(x_halo)+tracer.func_number(x_tracer)*tracer.luminosity_tot*tracer.upsilon/dmhalo.m_triangle
        return np.sqrt(1.-(bigx/x_halo)**2)*mass*tracer.func_density(x_tracer)/x_halo
    
    min0=bigx
    max0=params['upper_limit']
    return 2.*g*dmhalo.m_triangle*scipy.integrate.quad(integrand1,min0,max0,args=(dmhalo,tracer),epsrel=params['epsrel'],epsabs=params['epsabs'])[0]#sigma^2_LOS(X) * Sigma(X) / nu0

def projected_virial(x_halo,dmhalo,tracer):#computes integral for Wlos from Errani etal (2018)
    x_tracer=x_halo*dmhalo.r_triangle/tracer.r_scale
    totalmass=dmhalo.func_mass(x_halo)+tracer.func_number(x_tracer)*tracer.luminosity_tot*tracer.upsilon/dmhalo.m_triangle
    return x_halo*tracer.func_density(x_tracer)*totalmass

def get_virial(dmhalo,tracer,**params):
    if not 'epsrel' in params:
        params['epsrel']=1.e-13
    if not 'epsabs' in params:
        params['epsabs']=0.
    if not 'limit' in params:
        params['limit']=500

    min0=0.
    max0=np.inf
    val1=scipy.integrate.quad(projected_virial,min0,max0,args=(dmhalo,tracer),epsabs=params['epsabs'],epsrel=params['epsrel'],limit=params['limit'])
    vvar=val1[0]*4.*np.pi*g/3.*dmhalo.m_triangle*(dmhalo.r_triangle**2)/tracer.ntotnorm/tracer.r_scale**3
    mu=g*(dmhalo.func_mass(tracer.rhalf_2d/dmhalo.r_triangle)+tracer.func_number(tracer.rhalf_2d/tracer.r_scale)*tracer.luminosity_tot*tracer.upsilon)*dmhalo.m_triangle/tracer.rhalf_2d/vvar
    return vvar,mu

