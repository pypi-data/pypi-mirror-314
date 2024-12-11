from pathlib import Path

from os import path
import glob

import numpy as np
from scipy import ndimage
from astropy.io import fits
import ppxf.ppxf_util as util
from scipy import interpolate
from scipy import ndimage
from scipy.stats import norm
import matplotlib.pyplot as plt




def _wave_convert(lam):
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

###############################################################################

def vac_to_air(lam_vac):
    """
    Convert vacuum to air wavelengths

    :param lam_vac - Wavelength in Angstroms
    :return: lam_air - Wavelength in Angstroms

    """
    return lam_vac/_wave_convert(lam_vac)

###############################################################################

def air_to_vac(lam_air):
    """
    Convert air to vacuum wavelengths

    :param lam_air - Wavelength in Angstroms
    :return: lam_vac - Wavelength in Angstroms

    """
    return lam_air*_wave_convert(lam_air)

###############################################################################


def single_gaussian(lam, diff, line_wave, FWHM_gal, v, sig1):
    c = 299792.458
    n = lam.size
    flux=np.zeros(n)
    sig0 = FWHM_gal/2.355/line_wave
    sig=np.sqrt(sig0**2+sig1**2)
    log_line=np.log(line_wave*(1+v/c))
    num=np.where(abs(lam-log_line)<10*sig)
    flux[num]=norm.cdf(lam[num]+diff[num]/2,log_line,sig)-norm.cdf(lam[num]-diff[num]/2,log_line,sig)


def gaussian(lam, line_wave, FWHM_gal, comp=None, pars=None):
    c = 299792.458
    line_wave = np.asarray(line_wave)

    if callable(FWHM_gal):
        FWHM_gal = FWHM_gal(line_wave)
    if comp is None:
        comp=np.zeros(line_wave.shape)
        pars=np.zeros(2)
    n = lam.size
    diff=np.pad(np.diff(lam),(1,0))+np.pad(np.diff(lam),(0,1))
    diff[1:-1]=diff[1:-1]/2
    line=[]
    sig0 = FWHM_gal/2.355/line_wave
    for i in range(line_wave.shape[0]):
        flux=np.zeros(n)
        v, sig1=pars[int(0 + 2*comp[i])], pars[int(1 + 2*comp[i])]/c
        sig=np.sqrt(sig0[i]**2+sig1**2)
        log_line=np.log(line_wave[i]*(1+v/c))
        num=np.where(abs(lam-log_line)<10*sig)
        flux[num]=norm.cdf(lam[num]+diff[num]/2,log_line,sig)-norm.cdf(lam[num]-diff[num]/2,log_line,sig)
        line.append(flux)
    return np.array(line).T



def all_temp_make(temp_a,lam_temp,lam_range_gal, tie_balmer=False, limit_doublets=False):
    gas_templates, gas_names, l_wave = emission_lines(np.log(lam_temp), 2.76, lam_range_gal=lam_range_gal, tie_balmer=tie_balmer, limit_doublets=limit_doublets)  
    num=np.where((lam_temp>5400)&(lam_temp<5600))   
    temp_a /= np.mean(temp_a[num],0)
    
    templates = np.column_stack([temp_a, gas_templates])
    start = [0, 180.]
    n_temps = temp_a.shape[1]
    n_forbidden = np.sum(["[" in a or "HeI" in a for a in gas_names])
    n_balmer = len(gas_names) - n_forbidden
    component = np.array([0]*n_temps + [1]*n_balmer + [2]*n_forbidden)
    gas_component = np.array(component) >0
    moments = [2, 2, 2]
    start = [start, start, start]
    return templates,start,moments,component,gas_component,gas_names


def emission_lines(ln_lam_temp, FWHM_gal, lam_range_gal=None, comp=np.zeros(19), params=np.array([0,0]),
                   tie_balmer=False, limit_doublets=False, vacuum=False):
    """
    Generates an array of Gaussian emission lines to be used as gas templates in pPXF.

    ****************************************************************************

    **ADDITIONAL LINES CAN BE ADDED BY EDITING THE CODE OF THIS PROCEDURE, WHICH 
    IS MEANT AS A TEMPLATE TO BE COPIED AND MODIFIED BY THE USERS AS NEEDED**

    ****************************************************************************

    Generally, these templates represent the instrumental line spread function
    (LSF) at the set of wavelengths of each emission line. In this case, pPXF
    will return the intrinsic (i.e. astrophysical) dispersion of the gas lines.

    Alternatively, one can input FWHM_gal=0, in which case the emission lines
    are delta-functions and pPXF will return a dispersion which includes both
    the instrumental and the intrinsic dispersion.

    For accuracy the Gaussians are integrated over the pixels boundaries.
    This can be changed by setting `pixel`=False.

    The [OI], [OIII] and [NII] doublets are fixed at theoretical flux ratio~3.

    The [OII] and [SII] doublets can be restricted to physical range of ratios.

    The Balmer Series can be fixed to the theoretically predicted decrement.

    Input Parameters
    ----------------

    ln_lam_temp: array_like
        is the natural log of the wavelength of the templates in Angstrom.
        ``ln_lam_temp`` should be the same as that of the stellar templates.
    lam_range_gal: array_like
        is the estimated rest-frame fitted wavelength range. Typically::

            lam_range_gal = np.array([np.min(wave), np.max(wave)])/(1 + z),

        where wave is the observed wavelength of the fitted galaxy pixels and
        z is an initial rough estimate of the galaxy redshift.
    FWHM_gal: float or func
        is the instrumental FWHM of the galaxy spectrum under study in Angstrom.
        One can pass either a scalar or the name "func" of a function
        ``func(wave)`` which returns the FWHM for a given vector of input
        wavelengths.
    pixel: bool, optional
        Set this to ``False`` to ignore pixels integration (default ``True``).
    tie_balmer: bool, optional
        Set this to ``True`` to tie the Balmer lines according to a theoretical
        decrement (case B recombination T=1e4 K, n=100 cm^-3).

        IMPORTANT: The relative fluxes of the Balmer components assumes the
        input spectrum has units proportional to ``erg/(cm**2 s A)``.
    limit_doublets: bool, optional
        Set this to True to limit the ratio of the [OII] and [SII] doublets to
        the ranges allowed by atomic physics.

        An alternative to this keyword is to use the ``constr_templ`` keyword
        of pPXF to constrain the ratio of two templates weights.

        IMPORTANT: when using this keyword, the two output fluxes (flux_1 and
        flux_2) provided by pPXF for the two lines of the doublet, do *not*
        represent the actual fluxes of the two lines, but the fluxes of the two
        input *doublets* of which the fit is a linear combination.
        If the two doublets templates have line ratios rat_1 and rat_2, and
        pPXF prints fluxes flux_1 and flux_2, the actual ratio and flux of the
        fitted doublet will be::

            flux_total = flux_1 + flux_1
            ratio_fit = (rat_1*flux_1 + rat_2*flux_2)/flux_total

        EXAMPLE: For the [SII] doublet, the adopted ratios for the templates are::

            ratio_d1 = flux([SII]6716/6731) = 0.44
            ratio_d2 = flux([SII]6716/6731) = 1.43.

        When pPXF prints (and returns in pp.gas_flux)::

            flux([SII]6731_d1) = flux_1
            flux([SII]6731_d2) = flux_2

        the total flux and true lines ratio of the [SII] doublet are::

            flux_total = flux_1 + flux_2
            ratio_fit([SII]6716/6731) = (0.44*flux_1 + 1.43*flux_2)/flux_total

        Similarly, for [OII], the adopted ratios for the templates are::

            ratio_d1 = flux([OII]3729/3726) = 0.28
            ratio_d2 = flux([OII]3729/3726) = 1.47.

        When pPXF prints (and returns in pp.gas_flux)::

            flux([OII]3726_d1) = flux_1
            flux([OII]3726_d2) = flux_2

        the total flux and true lines ratio of the [OII] doublet are::

            flux_total = flux_1 + flux_2
            ratio_fit([OII]3729/3726) = (0.28*flux_1 + 1.47*flux_2)/flux_total

    vacuum:  bool, optional
        set to ``True`` to assume wavelengths are given in vacuum.
        By default the wavelengths are assumed to be measured in air.

    Output Parameters
    -----------------

    emission_lines: ndarray
        Array of dimensions ``[ln_lam_temp.size, line_wave.size]`` containing
        the gas templates, one per array column.

    line_names: ndarray
        Array of strings with the name of each line, or group of lines'

    line_wave: ndarray
        Central wavelength of the lines, one for each gas template'
    """


    if lam_range_gal is None:
        lam_range_gal=np.exp([min(ln_lam_temp),max(ln_lam_temp)])
    if tie_balmer:
        line_names = np.array(['H10', 'H9', 'H8', 'Heps','Balmer'])
        line_wave =np.array([3798.983, 3836.479, 3890.158, 3971.202,  6564.632])# np.mean(wave[w]) if np.any(w) else np.mean(wave)   
        balmer = (lam_range_gal[0] < line_wave) & (line_wave < lam_range_gal[1])     
        n_balmer=sum(balmer)
        # Balmer decrement for Case B recombination (T=1e4 K, ne=100 cm^-3)
        # from Storey & Hummer (1995) https://ui.adsabs.harvard.edu/abs/1995MNRAS.272...41S
        # In electronic form https://cdsarc.u-strasbg.fr/viz-bin/Cat?VI/64
        # See Table B.7 of Dopita & Sutherland (2003) https://www.amazon.com/dp/3540433627
        # Also see Table 4.2 of Osterbrock & Ferland (2006) https://www.amazon.co.uk/dp/1891389343/
        wave = balmer
        if not vacuum:
            wave = vac_to_air(wave)
        gauss = gaussian(ln_lam_temp, wave[-4:], FWHM_gal, comp[:n_balmer-1], params)
        ratios = np.array([ 0.259, 0.468, 1, 2.86]) # [0.0530, 0.0731, 0.105, 0.159,]
        ratios *= wave[-2]/wave[-4:]  # Account for varying log-sample size in Angstrom
        emission_lines = np.vstack([gaussian(ln_lam_temp, wave[:-4], FWHM_gal, comp[:n_balmer], params).T, gauss @ ratios]).T
        line_names = line_names[balmer]
        line_wave = line_wave[balmer]


    else:
            #        Balmer:     H10       H9         H8        Heps    Hdelta    Hgamma    Hbeta     Halpha
        line_wave = np.array([3798.983, 3836.479, 3890.158, 3971.202, 4102.899, 4341.691, 4862.691, 6564.632])  # vacuum wavelengths
        line_names = np.array(['H10', 'H9', 'H8', 'Heps', 'Hdelta', 'Hgamma', 'Hbeta', 'Halpha'])
        balmer=(lam_range_gal[0] < line_wave) & (line_wave < lam_range_gal[1])
        n_balmer=sum(balmer)
        if not vacuum:
            line_wave = vac_to_air(line_wave)
        emission_lines = gaussian(ln_lam_temp, line_wave[balmer], FWHM_gal, comp[:n_balmer], params)
        line_names = line_names[balmer]
        line_wave = line_wave[balmer]

    if limit_doublets:
        # The line ratio of this doublet lam3727/lam3729 is constrained by
        # atomic physics to lie in the range 0.28--1.47 (e.g. fig.5.8 of
        # Osterbrock & Ferland (2006) https://www.amazon.co.uk/dp/1891389343/).
        # We model this doublet as a linear combination of two doublets with the
        # maximum and minimum ratios, to limit the ratio to the desired range.
        #       -----[OII]-----
        wave = np.array([3727.092, 3729.875])    # vacuum wavelengths
        n_OII = sum((lam_range_gal[0] < wave) & (wave < lam_range_gal[1]))
        if not vacuum:
            wave = vac_to_air(wave)
        if n_OII >0:
            names = np.array(['[OII]3726_d1', '[OII]3726_d2'])
            gauss = gaussian(ln_lam_temp, wave, FWHM_gal, comp[n_balmer:n_balmer+n_OII], params)
            doublets = gauss @ [[1, 1], [0.28, 1.47]]  # produces *two* doublets
            emission_lines = np.column_stack([emission_lines, doublets])
            line_names = np.append(line_names, names)
            line_wave = np.append(line_wave, wave)
        

        # The line ratio of this doublet lam6717/lam6731 is constrained by
        # atomic physics to lie in the range 0.44--1.43 (e.g. fig.5.8 of
        # Osterbrock & Ferland (2006) https://www.amazon.co.uk/dp/1891389343/).
        # We model this doublet as a linear combination of two doublets with the
        # maximum and minimum ratios, to limit the ratio to the desired range.
        #        -----[SII]-----
        wave = np.array([6718.294, 6732.674])    # vacuum wavelengths
        n_SII = sum((lam_range_gal[0] < wave) & (wave < lam_range_gal[1]))
        n_OSII=n_OII+n_SII
        if not vacuum:
            wave = vac_to_air(wave)
        if n_SII >0:
            names = np.array(['[SII]6731_d1', '[SII]6731_d2'])
            gauss = gaussian(ln_lam_temp, wave, FWHM_gal, comp[n_balmer+n_OII:n_balmer+n_OSII], params)
            doublets = gauss @ [[0.44, 1.43], [1, 1]]  # produces *two* doublets
            emission_lines = np.column_stack([emission_lines, doublets])
            line_names = np.append(line_names, names)
            line_wave = np.append(line_wave, wave)

    else:

        # Here the two doublets are free to have any ratio
        #         -----[OII]-----     -----[SII]-----
        wave = np.array([3727.092, 3729.875, 6718.294, 6732.674])  # vacuum wavelengths
        OSII=(lam_range_gal[0] < wave) & (wave < lam_range_gal[1])
        n_OSII = sum(OSII)
        if not vacuum:
            wave = vac_to_air(wave)
        names = np.array(['[OII]3726', '[OII]3729', '[SII]6716', '[SII]6731'])
        gauss = gaussian(ln_lam_temp, wave[OSII], FWHM_gal, comp[n_balmer:n_balmer+n_OSII], params)
        emission_lines = np.column_stack([emission_lines, gauss])
        line_names = np.append(line_names, names[OSII])
        line_wave = np.append(line_wave, wave[OSII])

    # Here the lines are free to have any ratio
    #       -----[NeIII]-----    HeII      HeI
    wave = np.array([3968.59, 3869.86, 4687.015, 5877.243])  # vacuum wavelengths
    free = (lam_range_gal[0] < wave) & (wave < lam_range_gal[1])
    n_free= sum(free)
    if not vacuum:
        wave = vac_to_air(wave)
    names = np.array(['[NeIII]3968', '[NeIII]3869', 'HeII4687', 'HeI5876'])
    gauss = gaussian(ln_lam_temp, wave[free], FWHM_gal, comp[n_balmer+n_OSII:n_balmer+n_OSII+n_free], params)
    emission_lines = np.column_stack([emission_lines, gauss])
    line_names = np.append(line_names, names[free])
    line_wave = np.append(line_wave, wave[free])

    ######### Doublets with fixed ratios #########

    # To keep the flux ratio of a doublet fixed, we place the two lines in a single template
    #        -----[OIII]-----
    wave = [4960.295, 5008.240]    # vacuum wavelengths
    n_OIII = sum((lam_range_gal[0] < wave) & (wave < lam_range_gal[1]))
    if not vacuum:
        wave = vac_to_air(wave)
    if n_OIII>0:
        doublet = gaussian(ln_lam_temp, wave, FWHM_gal, comp[n_balmer+n_OSII+n_free]*np.ones(2), params) @ [0.33, 1]
        emission_lines = np.column_stack([emission_lines, doublet])
        line_names = np.append(line_names, '[OIII]5007_d')  # single template for this doublet
        line_wave = np.append(line_wave, wave[1])

    # To keep the flux ratio of a doublet fixed, we place the two lines in a single template
    #        -----[OI]-----
    wave = [6302.040, 6365.535]    # vacuum wavelengths
    n_OI = sum((lam_range_gal[0] < wave) & (wave < lam_range_gal[1]))
    if not vacuum:
        wave = vac_to_air(wave)
    if n_OI>0:
        doublet = gaussian(ln_lam_temp, wave, FWHM_gal, comp[n_balmer+n_OSII+n_free+1]*np.ones(2), params) @ [1, 0.33]
        emission_lines = np.column_stack([emission_lines, doublet])
        line_names = np.append(line_names, '[OI]6300_d')  # single template for this doublet
        line_wave = np.append(line_wave, wave[0])

    # To keep the flux ratio of a doublet fixed, we place the two lines in a single template
    #       -----[NII]-----
    wave = [6549.860, 6585.271]    # air wavelengths
    n_NII = sum((lam_range_gal[0] < wave) & (wave < lam_range_gal[1]))
    if not vacuum:
        wave = vac_to_air(wave)
    if n_NII>0:
        doublet = gaussian(ln_lam_temp, wave, FWHM_gal, comp[n_balmer+n_OSII+n_free+2]*np.ones(2), params) @ [0.33, 1]
        emission_lines = np.column_stack([emission_lines, doublet])
        line_names = np.append(line_names, '[NII]6583_d')  # single template for this doublet
        line_wave = np.append(line_wave, wave[1])

    return emission_lines, line_names, line_wave


class temp(object):

    def __init__(self,filename,velscale,FWHM_gal=2.76,FWHM_tem=2.51,normalize=False):
        
        #filename='/public/home/lujiafeng_ZJU/CCC/BC03_MaNGA_tpl_chab_L_300.fits'

        hdu=fits.open(filename)
        tpl_wave=hdu[0].data
        tpl_metal=np.log10(hdu[1].data/0.02)
        tpl_age=np.log10(hdu[2].data)
        
        Nwave=len(tpl_wave)     # 3324 A ~ 9297 A
        Nmetal=len(tpl_metal)
        Nage=len(tpl_age)

        ssp=hdu[5].data[:,1]

        lam_range_temp=[tpl_wave[0],tpl_wave[-1]]
        sspNew0,log_lam_temp=util.log_rebin(lam_range_temp,ssp,velscale=velscale)[:2]
        #log_lam_temp=util.log_rebin(lam_range_temp,ssp,velscale=velscale)[1]

        Nwave=len(sspNew0)

        templates=np.empty((Nwave,Nage,Nmetal))
        age_grid=np.empty((Nage,Nmetal))
        metal_grid=np.empty((Nage,Nmetal))

        FWHM_dif=np.sqrt(FWHM_gal**2-FWHM_tem**2)
        sigma=FWHM_dif/2.355/(tpl_wave[1]-tpl_wave[0])
        
        for m in range(Nmetal):
            ssp_metal=hdu[m+3].data
            for a in range(Nage):
                ssp0=ssp_metal[:,a]
                if np.isscalar(FWHM_gal):
                    ssp_new=ndimage.gaussian_filter1d(ssp0,sigma)
                else:
                    ssp_new=util.gaussian_filter1d(ssp0,sigma)
                #sspNew=util.log_rebin(lam_range_temp,ssp_new,velscale=velscale)[0]
                f=interpolate.interp1d(tpl_wave,ssp_new,kind='linear',fill_value="extrapolate")
                sspNew=f(np.exp(log_lam_temp))
                
                if normalize:
                    sspNew/=np.mean(sspNew)
                templates[:,a,m]=sspNew
                age_grid[a,m]=tpl_age[a]
                metal_grid[a,m]=tpl_metal[m]

        self.templates=templates/np.median(templates)
        self.log_lam_temp=log_lam_temp
        self.age_grid=age_grid
        self.metal_grid=metal_grid
        self.n_ages=Nage
        self.n_metal=Nmetal


    def plot(self,weights,nodots=False,colorbar=True,**kwargs):

        assert self.age_grid.shape==self.metal_grid.shape==weights.shape,\
                "Input weight dimensions do not match"

        xgrid=self.age_grid
        ygrid=self.metal_grid
        util.plot_weights_2d(xgrid,ygrid,weights,\
                nodots=nodots,colorbar=colorbar,**kwargs)

    def mean_age_metal(self,weights,quiet=False):

        assert self.age_grid.shape==self.metal_grid.shape==weights.shape,\
                "Input weight dimensions do not match"
        
        log_age_grid=self.age_grid
        metal_grid=self.metal_grid

        mean_log_age=np.sum(weights*log_age_grid)/np.sum(weights)
        mean_metal=np.sum(weights*metal_grid)/np.sum(weights)

        if not quiet:
            print('Weighted <logAge> [yr]: %.3g' % mean_log_age)
            print('Weighted <[M/H]>: %.3g' % mean_metal)

        return mean_log_age,mean_metal


