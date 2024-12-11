import os
os.environ["OMP_NUM_THREADS"] ="1" # export OMP_NUM_THREADS=4
os.environ["OPENBLAS64_NUM_THREADS"] ="1" # export OPENBLAS_NUM_THREADS=4
os.environ["MKL_NUM_THREADS"] ="1" # export MKL_NUM_THREADS=6
os.environ["VECLIB_MAXIMUM_THREADS"] ="1" # export VECLIB_MAXIMUM_THREADS=4
os.environ["NUMEXPR_NUM_THREADS"] ="1" # export NUMEXPR_NUM_THREADS=6
import warnings

from ppxf.ppxf import ppxf as pp
from ppxf.ppxf import losvd_rfft,rebin, robust_sigma,regularization
import numpy as np
from numpy.polynomial import legendre, hermite
from scipy import optimize, linalg, special
import time
from scipy.linalg import solveh_banded
from scipy.interpolate import interp1d

def losvd_rfft(pars, nspec, mom, nl, vsyst, factor, sigma_diff):
    """
    Analytic Fourier Transform (of real input) of the Gauss-Hermite LOSVD.
    Equation (38) of `Cappellari (2017)
    <https://ui.adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_

    """
    losvd_rfft = np.empty((nl,  nspec), dtype=complex)
    p = 0

    for k in range(nspec):  # nspec=2 for two-sided fitting, otherwise nspec=1
        s = 1 if k == 0 else -1  # s=+1 for left spectrum, s=-1 for right one
        vel, sig = vsyst + s*pars[0 + p], pars[1 + p]
        a, b = [vel, sigma_diff]/sig
        w = np.linspace(0, np.pi*factor*sig, nl)
        losvd_rfft[:,  k] = np.exp(1j*a*w - 0.5*(1 + b**2)*w**2)

        if mom > 2:
            n = np.arange(3, mom + 1)
            nrm = np.sqrt(special.factorial(n)*2**n)   # vdMF93 Normalization
            coeff = np.append([1, 0, 0], (s*1j)**n * pars[p - 1 + n]/nrm)
            poly = hermite.hermval(w, coeff)
            losvd_rfft[:,  k] *= poly
    p += mom

    return np.conj(losvd_rfft)


def band_matrix(wave):
    l=len(wave)
    # wave=l*wave/(wave[-1]-wave[0])
    del_lam2=(1./(wave[2:]-wave[:-2]))**2
    del_lam=1./(wave[1:]-wave[:-1])
    # del_lam2/=np.mean(del_lam2)
    # del_lam/=np.mean(del_lam)
    output = np.zeros((3 ,l))

    output[-1,:-2] += del_lam[1:]*del_lam[:-1]*del_lam2

    output[-2, 1:-1] += -del_lam2*(del_lam[1:]+del_lam[:-1])*del_lam[1:]
    output[-2, :-2] += -del_lam2*(del_lam[1:]+del_lam[:-1])*del_lam[:-1]

    output[-3, :-2] += del_lam2*del_lam[:-1]**2
    output[-3, 1:-1] += del_lam2*(del_lam[1:]+del_lam[:-1])**2
    output[-3, 2:] += del_lam2*del_lam[1:]**2

    return output


def smooth(gal, wave, weights, lam, p, n = 0):
    if weights is None:
        weights = 1
    w=0.5*np.ones(gal.shape)
    cal_diff = 1
    n0=n
    mat0=band_matrix(wave)
    while cal_diff > 1e-5:       
        wt=w*weights
        mat=mat0*lam
        mat[0]+=wt
        sm=solveh_banded(mat,wt*gal,overwrite_ab=True,overwrite_b=True, lower=True, check_finite=False)
        if n>20:
            break
        if n==n0:
            std=np.std(gal[weights==1])
        mask = gal > sm
        std=np.std(gal[np.where((gal<sm+6*(1-p)*std)&(gal>sm-6*p*std))])
        nw = p * mask + (1 - p) * (~mask)
        num=np.array(np.convolve(abs(gal-sm)>3*std,np.ones(10)/10,mode='same'),dtype='bool')
        nw[num]=0
        cal_diff = np.linalg.norm(nw - w)/np.maximum(np.linalg.norm(w), np.finfo(float).eps)
        w=nw
        n+=1
    return sm,wt

def wave_convert(lam):
    """
    Convert between vacuum and air wavelengths using
    equation (1) of Ciddor 1996, Applied Optics 35, 1566
        http://doi.org/10.1364/AO.35.001566

    :param lam - Wavelength in Angstroms
    :return: conversion factor

    """
    lam = np.asarray(lam)
    sigma2 = (1e4/lam)**2
    fact = 1 + 5.792105e-2/(238.0185 - sigma2) + 1.67917e-3/(57.362 - sigma2)

    return fact


def Line_wave(line_wave=None, air=True):
    if line_wave is None:
        line_wave=np.array([3798.983, 3836.479, 3890.158, 3934.777, 3971.202, 4102.899, 4341.691,
                            4862.691, 6564.632, 3727.092, 3729.875, 6718.294, 6732.674,
                            3968.59, 3869.86, 4687.015, 5877.243, 4960.295, 5008.240,
                            6302.040, 6365.535, 6549.860, 6585.271, 6718.29, 6732.67])

    if air:
        line_wave /= wave_convert(line_wave)
    return line_wave



def temp_l_make(temp, lam, l, p, weights=None,  gas_component=None, lam_weight=None,  norm_lambda=5500, delta_lambda=200):
    """
    make smoothed continuum templates from stellar templates

    """ 
    temp_a = temp.reshape(temp.shape[0],-1)
    m, n = temp_a.shape
    if weights is None:
        weights = np.ones(m)
    elif not np.array_equal(lam_weight, lam):
        f=interp1d(lam_weight,weights,kind='nearest',bounds_error=False,fill_value=0)
        weights=np.array(f(lam),dtype='bool')
    lam_temp = lam
    temp_l = np.zeros((lam_temp.shape[0],n))

    if gas_component is None:
        gas_component = np.zeros(n,dtype=bool)


    for i in range(gas_component.size-np.count_nonzero(gas_component)):
        if isinstance(l, (int, float)):
            temp_l[:,i],mask=smooth(temp[:,i], np.log(lam), weights, lam=l,p=p)
        else:
            tmp0=np.empty((l.shape[0],m))
            for j in range(l.shape[0]):
                tmp0[j],mask=smooth(temp[:,i], np.log(lam), weights, lam=l[j],p=p)
            temp_l[:,i]=np.mean(tmp0,0)

    temp_l[:, gas_component] = 0

    num = num=np.where(abs(lam_temp-norm_lambda)<delta_lambda)   
    mean = np.mean(temp_a[num].T[~gas_component],1)
    temp_a[:, ~gas_component] /= mean
    temp_l[:, ~gas_component] /= mean
    return lam_temp, temp_a, temp_l


def c_l_make(temp, lam, weights, l, p, gas_component=None):
    """
    make smoothed continuum templates from stellar templates

    """   
    m, n = temp.shape
    if weights is None:
        weights = np.ones(m)
    temp_l = np.zeros((lam.shape[0],n))

    if gas_component is None:
        gas_component = np.zeros(n,dtype=bool)


    for i in range(gas_component.size-np.count_nonzero(gas_component)):
        if isinstance(l, (int, float)):
            temp_l[:,i],mask=smooth(temp[:,i], np.log(lam), weights, lam=l,p=p)
        else:
            tmp0=np.empty((l.shape[0],m))
            for j in range(l.shape[0]):
                tmp0[j],mask=smooth(temp[:,i], np.log(lam), weights, lam=l[j],p=p)
            temp_l[:,i]=np.mean(tmp0,0)

    temp_l[:, gas_component] = 0
    return temp_l




def galaxy_l_make(galaxy, lam, noise, l, p, Z = None, mask = None, line_wave = None, broadline = False, flux_mask = False, FWHM=0, norm_lambda = 5500, delta_lambda = 200):
    c = 299792.458   
    line_wave=Line_wave(line_wave = line_wave)
    lamt = np.repeat(lam[np.newaxis, :], len(line_wave), axis=0)
    s=galaxy.shape[0]
    
    if mask is None:
        mask=np.zeros(s)

    if Z is None:
        if flux_mask:
            mask[np.where(np.sum(abs(lamt.T-line_wave).T<np.sqrt((500*lam/c)**2+FWHM**2),0)>0)]=1

    else:
        sky_line_wave=np.array([5578.5, 6301.7, 7246.0]) 
        lamt_sky = np.repeat(lam[np.newaxis, :], len(sky_line_wave), axis=0)
        if flux_mask:
            if broadline:
                mask[np.where((np.sum(abs(lamt.T-line_wave).T<np.sqrt((2000*lam/c)**2+FWHM**2),0)>0)|(np.sum(abs(lamt_sky.T-sky_line_wave).T<np.sqrt((2000*lam/c)**2+FWHM**2),0)>0))]=1

            else:
                mask[np.where((np.sum(abs(lamt.T-line_wave).T<np.sqrt((500*lam/c)**2+FWHM**2),0)>0)|(np.sum(abs(lamt_sky.T-sky_line_wave).T<np.sqrt((2000*lam/c)**2+FWHM**2),0)>0))]=1


    noise[noise<=0]=max(noise)

    if isinstance(l, (int, float)):
        galaxy0,mask=smooth(galaxy, np.log(lam), weights=~np.array(mask,dtype='bool'), lam=l,p=p)
    else:
        s1=l.shape[0]
        galaxy0=np.empty((s1,s))
        mask0=np.empty((s1,s))
        for i in range(s1):
            galaxy0[i],mask0[i]=smooth(galaxy, np.log(lam), weights=~np.array(mask,dtype='bool'), lam=l[i],p=p)
        galaxy0=np.mean(galaxy0,0)
        mask=np.array(np.sum(mask0,0),dtype='bool')
    noise_l=0
    noise0=np.sqrt(noise**2+(noise_l*galaxy/galaxy0)**2)/galaxy0

    num=np.where(abs(lam-norm_lambda)<delta_lambda)
    mean_gal=np.ma.mean(np.ma.array(galaxy[num],mask=~np.array(mask[num],dtype='bool')))
    galaxy/=mean_gal
    galaxy0/=mean_gal
    noise0/=mean_gal
    
    return lam, galaxy,galaxy0,mean_gal, noise/mean_gal,noise0, mask==0


class ewfit(pp):
    def __init__(self, templates, galaxy, noise, velscale, start, 
                 templates_l=None, galaxy_l=None, noise_l = None, Z=None, bias=None,
                 bounds=None, clean=False, component=0, constr_templ=None,
                 constr_kinem=None, degree=4, dust=None, fixed=None,
                 fraction=None, ftol=1e-4, gas_component=None, gas_names=None,
                 gas_reddening=None, gas_reddening_func=None, tie_balmer=False, limit_doublets=False, FWHM=2.76,
                 global_search=False, goodpixels=None, lam=None, lam_temp=None,
                 linear = False, linear_method = 'lsq_box', mask = None,
                 method = 'capfit', mdegree = 0, moments = 2, phot = None, plot = False,
                 quiet = False, reddening = None, reddening_func = None, reg_dim = None,
                 reg_ord = 2, reg_step = None, regul = 0, sigma_diff = 0, sky = None,
                 templates_rfft = None, tied = None, trig = False, velscale_ratio = 1,
                 vsyst = 0, x0=None, line_wave = None, l=1e-7,p=0.5):
        
        self.l=l
        self.p=p
        self.tie_balmer=tie_balmer
        self.limit_doublets=limit_doublets
        self.gas_component=gas_component
        self.FWHM = FWHM
        self.pars = np.inf * np.ones(sum(moments))
        self.weights = None
        self.gal_temp=None
        self.gal_temp_l=None
        self.s1=0
        self.s2=0
        self.ncmake=0
        self.bestfit_emm = 0
        self.line_wave = line_wave
        self.Z = Z
        self.njevt = 0

        if galaxy_l is None:
            s=time.time()
            lam, galaxy, self.galaxy_l, self.mean_gal, noise, self.noise_l, self.mask0 = galaxy_l_make(galaxy, lam, noise, self.l, self.p, line_wave = self.line_wave, Z= self.Z, mask=mask, flux_mask = True, FWHM=self.FWHM)
            if not quiet:
                print('Data processing time: %ss' %(round(time.time()-s, 3)))
        else:
            assert galaxy.shape == galaxy_l.shape, "galaxy and galaxy_l must have the same size"
            self. galaxy_l = galaxy_l
            self.noise_l = noise_l

        if templates_l is None:
            s=time.time()
            lam_temp, templates, self.templates_l = temp_l_make(templates, lam_temp, self.l, self.p, weights = ~self.mask0, gas_component=gas_component, lam_weight = lam)
            if not quiet:
                print('Templates processing time: %ss' %(round(time.time()-s, 3)))
        else:
            assert templates.shape == templates_l.shape, "templates and templates_l must have the same size"
            self.templates_l = templates_l
      

        super().__init__(templates, galaxy, noise, velscale, start, bias,
                 bounds, clean, component, constr_templ,
                 constr_kinem, degree, dust, fixed,
                 fraction, ftol, gas_component, gas_names,
                 gas_reddening, gas_reddening_func,
                 global_search, goodpixels, lam, lam_temp,
                 linear, linear_method, mask,
                 method, mdegree, moments, phot, plot,
                 quiet, reddening, reddening_func, reg_dim,
                 reg_ord, reg_step, regul, sigma_diff, sky,
                 templates_rfft, tied, trig, velscale_ratio,vsyst, x0)
        

        self.att_curve,self.att_curve_smooth=self.attcurve()


    def set_lam_input(self, bounds, start):

        if self.lam is not None:
            assert self.lam.shape == self.galaxy.shape, "GALAXY and LAM must have the same size"
            c = 299792.458  # Speed of light in km/s
            d_ln_lam = np.diff(np.log(self.lam[[0, -1]]))/(self.lam.size - 1)
            assert np.isclose(self.velscale, c*d_ln_lam), \
                "Must be `velscale = c*Delta[ln(lam)]` (eq.8 of Cappellari 2017)"

        if (self.lam_temp is not None) and (self.lam is not None):
            assert self.lam_temp.size == self.templates.shape[0], \
                "`lam_temp` must have length `templates.shape[0]`"
            assert self.vsyst == 0, \
                "`vsyst` is redundant when both `lam` and `lam_temp` are given"
            d_ln_lam = np.diff(np.log(self.lam_temp[[0, -1]]))/(self.lam_temp.size - 1)
            assert np.isclose(self.velscale/self.velscale_ratio, c*d_ln_lam), \
                "Must be `velscale/velscale_ratio = c*Delta[ln(lam_temp)]` (eq.8 of Cappellari 2017)"
            self.templates_full = self.templates.copy()
            self.lam_temp_full = self.lam_temp.copy()
            if bounds is None:
                vlim = np.array([-2900, 2900])  # As 2e3 nonlinear_fit() +900 for 3sigma
            else:
                vlim = [np.array(b[0]) - s[0] for b, s in zip(bounds, start)]
                vlim = np.array([np.max(vlim) + 900, np.min(vlim) - 900])
            lam_range = self.lam[[0, -1]]*np.exp(vlim/c)
            assert (self.lam_temp[0] <= lam_range[0]) and (self.lam_temp[-1] >= lam_range[1]), \
                "The `templates` must cover the full wavelength range of the " \
                "`galaxy` for the adopted velocity starting guess"
            ok = (self.lam_temp > lam_range[0]) & (self.lam_temp < lam_range[1])
            self.templates = self.templates[ok, :]
            self.templates_l = self.templates_l[ok, :]
            self.lam_temp = self.lam_temp[ok]
            self.npix_temp = self.templates.shape[0]
            lam_temp_min = np.mean(self.lam_temp[:self.velscale_ratio])
            self.vsyst = c*np.log(lam_temp_min/self.lam[0])/self.velscale
        elif self.templates.shape[0]/self.velscale_ratio > 2*self.galaxy.shape[0]:
            print("WARNING: The template is > 2x longer than the galaxy. You may "
                    "be able to save some computation time by truncating it or by "
                    "providing both `lam` and `lam_temp` for an automatic truncation")
        self.npad = 2**int(np.ceil(np.log2(self.templates.shape[0])))
        self.templates_l_rfft = np.fft.rfft(self.templates_l[:,~self.gas_component], self.npad, axis=0)

    def c_make(self, pars0):
        # self.templates_l_rfft = np.fft.rfft(self.templates_l, self.npad, axis=0)
        nspec, npix, ngh = self.nspec, self.npix, self.ngh
        # This array `c` is used for estimating predictions
        npoly = (self.degree + 1)*nspec  # Number of additive polynomials in fit
        nrows_spec = npix*nspec
        nrows_temp = nrows_spec + self.phot_npix
        ncols = npoly + self.ntemp + self.nsky

        if self.gal_temp is None:
            c = np.zeros((nrows_temp, ncols))
            c_l = np.zeros((nrows_temp, ncols))
        else:
            c = self.gal_temp
            c_l=self.gal_temp_l

        bool_mask=np.array([1]*nrows_spec+[0]*(nrows_temp-nrows_spec),dtype='bool')


        # Fill first columns of the Design Matrix with polynomials
        x = np.linspace(-1, 1, npix)
        if self.degree >= 0:
            vand = self.polyvander(x, self.degree)
            c[: npix, : npoly//nspec] = vand
            c_l[: npix, : npoly//nspec] = vand
            if nspec == 2:
                c[npix : nrows_spec, npoly//nspec : npoly] = vand  # poly for right spectrum
                c_l[npix : nrows_spec, npoly//nspec : npoly] = vand  # poly for right spectrum

        star_mom=np.unique(self.component[~self.gas_component])
        star_ind = [np.arange(self.moments[:q].sum(), self.moments[:q+1].sum()) for q in star_mom]
        ind0 = [np.arange(self.moments[:q].sum(), self.moments[:q+1].sum()) for q in range(self.moments.shape[0])]

        for q, mom in zip(range(self.moments.shape[0]), self.moments):
            ind = ind0[q]
            if (self.pars[ind] != pars0[ind]).any():
                lvd_rfft = losvd_rfft(pars0[ind], nspec, mom, self.templates_rfft.shape[0],
                                      self.vsyst, self.velscale_ratio, self.sigma_diff)
                index = np.where(self.component==q)[0]
                tmp = np.empty((nspec, self.npix))
                tmp_l = np.empty((nspec, self.npix))
                for j, template_rfft in zip( index , self.templates_rfft[:, index].T):  # loop over column templates
                    for k in range(nspec):
                        tt = np.fft.irfft(template_rfft*lvd_rfft[:, k], self.npad)
                        tmp[k] = rebin(tt[:self.npix*self.velscale_ratio], self.velscale_ratio)
                    c[bool_mask, npoly + j] = tmp.ravel()

                # c_l[bool_mask, npoly:] = c_l_make(c[bool_mask, npoly:], self.lam, ~self.mask0, self.l, self.p) 

                    if not self.gas_component[j]: 
                        for k in range(nspec):
                            tt_l = np.fft.irfft(self.templates_l_rfft[:, j]*lvd_rfft[:, k], self.npad)
                            tmp_l[k] = rebin(tt_l[:self.npix*self.velscale_ratio], self.velscale_ratio)
                        c_l[bool_mask, npoly + j] = tmp_l.ravel()

        w = npoly + np.arange(self.ntemp)  
        self.gas_component0 = np.append(np.zeros(npoly,dtype='bool'), self.gas_component)
        self.star_component0 = np.append(np.zeros(npoly,dtype='bool'), ~self.gas_component)

        if (self.pars[star_ind] != pars0[star_ind]).any():
            
            mpoly = gas_mpoly = None
            if self.mdegree > 0:
                pars_mpoly = pars0[ngh : ngh + self.mdegree*self.nspec]
                if nspec == 2:  # Different multiplicative poly for left/right spectra
                    mpoly1 = self.polyval(x, np.append(1.0, pars_mpoly[::2]))
                    mpoly2 = self.polyval(x, np.append(1.0, pars_mpoly[1::2]))
                    mpoly = np.append(mpoly1, mpoly2).clip(0.1)
                else:
                    mpoly = self.polyval(x, np.append(1.0, pars_mpoly)).clip(0.1)
                c[: nrows_spec,  w[~self.gas_component]] *= mpoly[:, None]
                c_l[: nrows_spec,  w[~self.gas_component]] *= mpoly[:, None] 

            if self.dust is not None:
                j0 = ngh + self.mdegree*self.nspec
                for d in self.dust:
                    j1 = j0 +  len(d["start"])
                    stars_redd = d["func"](self.lam, *pars0[j0:j1])
                    # if (self.pars[gas_ind] == pars0[gas_ind]).any():
                    #     d_comp=d["component"][~self.gas_component]
                    # else:
                    d_comp=d["component"]
                    c[: nrows_spec, w[d_comp]] *= stars_redd[:, None]
                    c_l[: nrows_spec, w[d_comp]] *= stars_redd[:, None]
                    j0 = j1

            if self.phot_npix:
                c[nrows_spec :, w] = self.phot_templates
                if self.dust is not None:
                    j0 = ngh + self.mdegree*self.nspec
                    for d in self.dust:
                        j1 = j0 + len(d["start"])
                        phot_redd = d["func"](self.phot_lam[:, d["component"]], *pars0[j0:j1])
                        c[nrows_spec :, w[d["component"]]] *= phot_redd
                        j0 = j1

            if self.nsky > 0:
                k = npoly + self.ntemp
                c[: npix, k : k + self.nsky//nspec] = self.sky
                if nspec == 2:
                    c[npix : nrows_spec, k + self.nsky//nspec : k + self.nsky] = self.sky  # Sky for right spectrum
        
        return c, c_l

    def linear_fit(self, pars0):

        s1=time.time()
        self.gal_temp, self.gal_temp_l = self.c_make(pars0) 

        self.temp_std=np.std(self.gal_temp[:,~self.gas_component]-self.gal_temp_l[:,~self.gas_component],0)
        self.temp_std /= np.mean(self.temp_std)
        self.gal_temp0 = self.gal_temp.copy()
        self.gal_temp0_l = self.gal_temp_l.copy()
        self.gal_temp0[:,~self.gas_component]/=self.temp_std
        self.gal_temp0_l[:,~self.gas_component]/=self.temp_std

        s2=time.time()
        self.s1+=s2-s1
        self.ncmake+=1
        self.pars = pars0      
        nspec, npix, ngh = self.nspec, self.npix, self.ngh
        npoly = (self.degree + 1)*nspec  # Number of additive polynomials in fit
        nrows_spec = npix*nspec
        nrows_temp = nrows_spec + self.phot_npix
        ncols = npoly + self.ntemp + self.nsky
        mpoly = gas_mpoly = None

        if self.regul > 0:
            if self.reg_ord == 1:
                nr = self.reg_dim.size
                nreg = nr*np.prod(self.reg_dim)
            elif self.reg_ord == 2:
                nreg = np.prod(self.reg_dim)
        else:
            nreg = 0

        A_l_tmp=(self.gal_temp0_l.T[~self.gas_component0]-1)
        tmp=self.gal_temp0.T.copy()
        tmp_0 = self.gal_temp0.T[~self.gas_component0] * self.galaxy_l
        nrows_all = nrows_temp + nreg
        a = np.zeros((nrows_all, ncols))
        # self.params=pars
        m = 1
        while m > 0:
            q=0
            self.cal_diff=np.inf
            cal_diff=1
            cal_diff0=np.inf
            while ((0>self.cal_diff-cal_diff) or (self.cal_diff-cal_diff>1e-5)) or cal_diff0>1e-5:  
                self.cal_diff = cal_diff
                q+=1
                if self.weights is None:                
                    bt_ew = 1
                    tmp[~self.gas_component0] = tmp_0 - A_l_tmp * self.galaxy
                else:
                    bt_ew = self.bestfit_stellar_ew
                    tmp[~self.gas_component0] = tmp_0 - A_l_tmp * (bt_ew * self.galaxy_l)
                       
                if self.noise.ndim == 2:
                    # input NOISE is a npix*npix covariance matrix
                    a[: nrows_temp, :] = self.noise @ tmp
                    b = self.noise @ self.galaxy
                else:
                    # input NOISE is a 1sigma error vector
                    a[: nrows_temp, :] = (tmp/self.noise).T # Weight columns with errors
                    b = self.galaxy / self.noise

                if self.regul > 0:
                    regularization(a, npoly, nrows_temp, self.reg_dim, self.reg_ord, self.regul, self.reg_step)

                # Select the spectral region to fit and solve the over-conditioned system
                # using SVD/BVLS. Use unweighted array for estimating bestfit predictions.
                # Iterate to exclude pixels deviating >3*sigma if clean=True.

                if nreg > 0:
                    aa = a[np.append(self.goodpixels, np.arange(nrows_temp, nrows_all)), :]
                    bb = np.append(b[self.goodpixels], np.zeros(nreg))
                else:
                    aa = a[self.goodpixels, :]
                    bb = b[self.goodpixels]
                self.nfev += 1
                self.weights = self.solve_linear(aa, bb, npoly)

                # self.weights[~self.gas_component0] = self.weights[~self.gas_component0]*self.temp_std
                # self.weights[~self.gas_component0] /= np.sum(self.weights[~self.gas_component0])


                # tmp[~self.gas_component0] = tmp_0 - A_l_tmp * (bt_ew * self.galaxy_l_t)
                self.bestfit = tmp.T @ self.weights
                self.bestfit_stellar = np.dot(self.gal_temp0[:,~self.gas_component0],self.weights[~self.gas_component0])
                self.bestfit_stellar_l = np.dot(self.gal_temp0_l[:,~self.gas_component0],self.weights[~self.gas_component0])
                self.bestfit_stellar_ew = self.bestfit_stellar/self.bestfit_stellar_l
                # self.galaxy_l_t, maskt = smooth(self.bestfit, self.lam, ~self.mask0, self.l, self.p, n = 0)
                
                if self.noise.ndim == 2:
                    # input NOISE is a npix*npix covariance matrix
                    err = (self.noise @ (self.galaxy - self.bestfit))[self.goodpixels]
                else:
                    # input NOISE is a 1sigma error vector
                    err = ((self.galaxy - self.bestfit)/self.noise)[self.goodpixels]
                
                cal_diff = np.linalg.norm(err)/err.size
                cal_diff0 = np.linalg.norm(bt_ew - self.bestfit_stellar_ew)/np.linalg.norm(bt_ew)
                if q>=3 and ((0>self.cal_diff-cal_diff) or (self.cal_diff-cal_diff>1e-3)) and cal_diff0<1e-3:
                    break
                elif q>=5:
                    break


            if self.noise.ndim == 2:
                # input NOISE is a npix*npix covariance matrix
                err = (self.noise @ (self.galaxy - self.bestfit))[self.goodpixels]
            else:
                # input NOISE is a 1sigma error vector
                err = ((self.galaxy - self.bestfit)/self.noise)[self.goodpixels]

            self.bestfit_emm = np.dot(self.gal_temp0[:,self.gas_component0], self.weights[self.gas_component0])
            self.bestfit0 = self.bestfit_stellar + self.bestfit_emm

            if self.clean:
                w = np.abs(err) < 3  # select residuals smaller than 3*sigma
                m = err.size - w.sum()
                if m > 0:
                    self.goodpixels = self.goodpixels[w]
                    if not self.quiet:
                        print('Outliers:', m)
            else:
                break


        self.matrix = self.gal_temp0 
        self.matrix_l = self.gal_temp0_l         # Return LOSVD-convolved templates matrix
        self.mpoly = mpoly
        self.gas_mpoly = gas_mpoly
        
        self.weights[~self.gas_component0] /= self.temp_std
        self.weights[~self.gas_component0] /= np.sum(self.weights[~self.gas_component0])
        self.weights0 = self.weights

        # Penalize the solution towards (h3, h4, ...) = 0 if the inclusion of
        # these additional terms does not significantly decrease the error.
        # The lines below implement eq.(8)-(9) in Cappellari & Emsellem (2004)
        if np.any(self.moments > 2) and self.bias > 0:
            D2 = p = 0
            for mom in self.moments:  # loop over kinematic components
                if mom > 2:
                    D2 += np.sum(pars0[2 + p : mom + p]**2)  # eq.(8) CE04
                p += mom
            err += self.bias*robust_sigma(err, zero=True)*np.sqrt(D2)  # eq.(9) CE04
            # self.nfev += 1
        self.s2+=time.time()-s2
        return err
    
    def attcurve(self):
        bestfit = self.bestfit_stellar
        gal_emm = self.galaxy - self.bestfit_emm
        att=-2.5*np.log10(gal_emm/self.bestfit_stellar)
        att_sm=2.5*np.log10(self.bestfit_stellar_l/self.galaxy_l)
        num=np.where((self.lam>5400)&(self.lam<5600))

        return att-np.mean(att[num]), att_sm-np.mean(att_sm[num])
