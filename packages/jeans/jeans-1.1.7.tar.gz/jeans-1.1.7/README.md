# jeans

A package for calculating properties of (spherical) dark matter halos and embedded (spherical) stellar populations, including integration of the (spherical) Jeans equation in 2D (observed projections) and 3D.

Author: Matthew G. Walker (2024) 

# Instructions 

* Install jeans. You can either pip install the released version or install from github

```
pip install jeans
```
# Available Dark Matter Halo Models

The alpha/beta/gamma ('abg_triangle') halo has mass density profile $\rho(r)=\frac{\rho_s}{(r/r_s)^{\gamma}[1+(r/r_s)^{\alpha}]^{(\beta-\gamma)/\alpha}}$.

The Navarro-Frenk-White ('nfw') halo is a special case of the above, with $(\alpha,\beta,\gamma)=(1,3,1)$, but can be called directly. 

The Dehnen Cusp ('dehnen_cusp') halo is a special case of the 'abg' halo, with $(\alpha,\beta,\gamma)=(1,4,1)$, but can be called directly.

The Dehnen Core ('dehnen_core') halo is a special case of the 'abg' halo, with $(\alpha,\beta,\gamma)=(1,4,0)$, but can be called directly. 

The core-NFW ('cnfw') halo is by Read et al. (arXiv:1805.06934), defined in terms of the enclosed mass profile, $M_{\rm cNFW}(r)=M_{\rm NFW}(r)f^n$, where $M_{\rm NFW}(r)$ is the enclosed mass profile of the NFW halo and $f^n=[\tanh(r/r_c)]^n$, with $r_c$ a core radius.

The core-NFW-tides ('cnfwt') halo is by Read et al. (arXiv:1805.06934), with density profile $\rho_{\rm cNFWt}(r)=\rho_{\rm cNFW}(r)$ for $r<r_{\rm t}$ and $\rho_{\rm cNFWt}(r)=\rho_{\rm cNFW}(r_{\rm t})(r/r_{\rm t})^{-\delta}$, allowing for power-law decrease in density beyond `tidal' radius $r_{\rm t}$.

For cNFW and cNFWt models, the standard definitions of parameters $M_{\triangle}$, $c_{\triangle}$ and $r_{\triangle}$ apply to the density and mass profile of the corresponding NFW halo that would be obtained by setting $r_{\rm c}=0$ and $r_{\rm t}=\infty$.


# Available Models for Tracer component

The alpha/beta/gamma ('abg') model has number density profile $\nu(r)=\frac{\nu_0}{(r/r_s)^{\gamma}[1+(r/r_s)^{\alpha}]^{(\beta-\gamma)/\alpha}}$.

The Plummer model is a special case of the 'abg' model, with $(\alpha,\beta,\gamma)=(2,5,0)$, but can be called directly.

The 'a2bg' model is a special case of the 'abg' model, with $\alpha=2$, but can be called directly.

The exponential model is defined in terms of projected density, $\Sigma(R)=\Sigma_0\exp(-R/r_s)$.

# Available Models for velocity dispersion anisotropy of the tracer component

The only model currently implemented is that of Read et al. (arXiv:1805.06934): $\beta(r)\equiv 1-\sigma^2_{\rm t}/\sigma^2_{\rm r}=\beta_0+(\beta_{\infty}-\beta_0)/(1+(r/r_{\beta})^{-n})$, where $\sigma_{\rm r}$ is the radial component of the velocity dispersion and $\sigma_{\rm t}=\sigma_{\theta}=\sigma_{\phi}$ is the tangential component (the two angular components have equal magnitude in the absence of rotation).  

# Usage

In order to create an object representing, e.g., an NFW halo with overdensity parameter $\triangle=200$, halo mass given by $M_{\triangle}=1\times 10^{10}M_{\odot}$ and concentration $c_{\triangle}=r_{\triangle}/r_s=10$, where $M_{\triangle}\equiv M(r_{\triangle})$ is the mass enclosed within a sphere of radius $r_{\triangle}$ and the mean halo density within a sphere of radius $r_{\triangle}$ is $\triangle$ times the cosmological critical density given by $3H_0/(8\pi G)$, with $h\equiv H_0/100$ (km/s/Mpc)$^{-1}$:

```nfw=jeans.get_dmhalo('nfw',triangle=200,h=0.7,m_triangle=1.e+10,c_triangle=10)```

The object stores the input halo parameters as well as the corresponding scale radius and scale density ('r_scale', 'rho_scale'), maximum circular velocity ('v_max'), radius where vmax occurs ('r_max'), and (3d) radial functions for the mass density ('density'), enclosed mass ('mass'), and circular velocity ('vcirc').

For the core-NFW-tides halo, e.g., this would become

```cnfwt=jeans.get_dmhalo('cnfwt',triangle=200,h=0.7,m_triangle=1.e+10,c_triangle=10,r_core=0.3,n_core=1.,r_tide=1.,delta=5.)```

***Note that for cNFW and cNFWt models, $r_{\rm c}$ and $r_{\rm t}$ must be specified in units of $r_{\triangle}$.***

To create an object representing, e.g., a tracer component following a Plummer profile with scale radius 100 pc (units of pc assumed, for compatibility with DM halos), total luminosity 1000 $L_{\odot}$, and tracer mass-to-light ratio $\Upsilon=1$ (solar units):

```plum=jeans.get_tracer('plum',luminosity_tot=1000.,r_scale=100.,upsilon=1.)```

The tracer object stores the input parameters as well as the normalization constants for 3D and (projected) 2D density profiles ('nu0' and 'sigma0', respectively), the number of tracer particles within a sphere of radius r_scale (normalized by nu0 * r_scale^3, 'nscalenorm'), and within a sphere of radius infinity (normalized by nu0 * r_scale^3, 'ntotnorm'), the 2D and 3D halflight radii ('rhalf_2d' and rhalf_3d') in units of pc, and functions for the 3D number density ('density'), 2D projected number density ('density_2d'), and cumulative number ('number').

For the 'abg' tracer model, this would become

```a2bg=jeans.get_tracer('a2bg',luminosity_tot=1000.,r_scale=100.,upsilon=1.,alpha=1.6,beta=7.,gamma=0.4)```

To create an object representing the tracer component's velocity dispersion anisotropy:

```anisotropy=jeans.get_anisotropy('read',beta_0=-0.3,beta_inf=0.8,r_beta=1.,n_beta=1.)```

***Note that $r_{\beta}$ must be specified in units of $r_{\rm scale}$, the scale radius assigned to the tracer population.***

The anisotropy object stores the input parameters as well functions for the anisotropy profile ('beta') and the function $\exp(2\int\frac{\beta}{r}dr)$ ('f_beta'), which appears in the Jeans equations.

# Examples 

For examples of ...

# Acknowledgement

