""" 
Methods to support implementation of extended HKF theory, 
the Deep Earth Water (DEW) model, the Standard Integrated Water Model (SWIM),
and the Debye-Hückel extivity coefficient model as extended by Helgeson.

Thermodynamic properties are output in Joules, Kelvin and bars.
Inputs are in Kelvin and bars.
"""

import numpy as np
cimport numpy as cnp # cimport gives us access to NumPy's C API

cdef extern from "born.h":
    double epsilon(double t, double p);
    double dEpsilonDt(double t, double p);
    double dEpsilonDp(double t, double p);
    double d2EpsilonDt2(double t, double p);
    double d2EpsilonDtDp(double t, double p);
    double d2EpsilonDp2(double t, double p);

    double born_B(double t, double p);
    double born_Q(double t, double p);
    double born_N(double t, double p);
    double born_U(double t, double p);
    double born_Y(double t, double p);
    double born_X(double t, double p);
    double born_dUdT(double t, double p);
    double born_dUdP(double t, double p);
    double born_dNdT(double t, double p);
    double born_dNdP(double t, double p);
    double born_dXdT(double t, double p);

    double Agamma(double t, double p);
    double dAgammaDt(double t, double p);
    double dAgammaDp(double t, double p);
    double d2AgammaDt2(double t, double p);
    double d2AgammaDtDp(double t, double p);
    double d2AgammaDp2(double t, double p);
    double d3AgammaDt3(double t, double p);
    double d3AgammaDt2Dp(double t, double p);
    double d3AgammaDtDp2(double t, double p);
    double d3AgammaDp3(double t, double p);

    double Bgamma(double t, double p);
    double dBgammaDt(double t, double p);
    double dBgammaDp(double t, double p);
    double d2BgammaDt2(double t, double p);
    double d2BgammaDtDp(double t, double p);
    double d2BgammaDp2(double t, double p);
    double d3BgammaDt3(double t, double p);
    double d3BgammaDt2Dp(double t, double p);
    double d3BgammaDtDp2(double t, double p);
    double d3BgammaDp3(double t, double p);

    double AsubG(double t, double p);
    double AsubH(double t, double p);
    double AsubJ(double t, double p);
    double AsubV(double t, double p);
    double AsubKappa(double t, double p);
    double AsubEx(double t, double p);
    double BsubG(double t, double p);
    double BsubH(double t, double p);
    double BsubJ(double t, double p);
    double BsubV(double t, double p);
    double BsubKappa(double t, double p);
    double BsubEx(double t, double p);

    double get_gSolvent_low_density_limit();
    void   set_gSolvent_low_density_limit(double value);
    double gSolvent(double t, double p);
    double DgSolventDt(double t, double p);
    double DgSolventDp(double t, double p);
    double D2gSolventDt2(double t, double p);
    double D2gSolventDtDp(double t, double p);
    double D2gSolventDp2(double t, double p);
    double D3gSolventDt3(double t, double p);
    double D3gSolventDt2Dp(double t, double p);
    double D3gSolventDtDp2(double t, double p);
    double D3gSolventDp3(double t, double p);
    double D4gSolventDt4(double t, double p);

cdef extern from "swim.h":
    ctypedef enum SWIM_RegionType:
        NotApplicable,
        DuanAndZhang2006,
        ZhangAndDuan2005,
        HoltenEtAl2014,
        WagnerEtAl2002
    double SWIM_getGibbsFreeEnergy(double t, double p, SWIM_RegionType region);
    double SWIM_getEnthalpy(double t, double p, SWIM_RegionType region);
    double SWIM_getEntropy(double t, double p, SWIM_RegionType region);
    double SWIM_getHeatCapacity(double t, double p, SWIM_RegionType region);
    double SWIM_getDcpDt(double t, double p, SWIM_RegionType region);
    double SWIM_getVolume(double t, double p, SWIM_RegionType region);
    double SWIM_getDvDt(double t, double p, SWIM_RegionType region);
    double SWIM_getDvDp(double t, double p, SWIM_RegionType region);
    double SWIM_getD2vDt2(double t, double p, SWIM_RegionType region);
    double SWIM_getD2vDtDp(double t, double p, SWIM_RegionType region);
    double SWIM_getD2vDp2(double t, double p, SWIM_RegionType region);

# Python instance of C enum variable
eos_type = NotApplicable

# here are the Cython "wrapper" signatures for DEW dielectric/Born/Debye-Huckel functions
def cy_DEW_epsilon(double t, double p):
    """ Returns the dielectric constant, input t (K), p (bars)
    """
    result = epsilon(<double> t, <double> p)
    return result

def cy_DEW_dEpsilonDt(double t, double p):
    """ Returns the D dielectric constant / Dt, input t (K), p (bars)
    """
    result = dEpsilonDt(<double> t, <double> p)
    return result

def cy_DEW_dEpsilonDp(double t, double p):
    """ Returns the D dielectric constant / Dp, input t (K), p (bars)
    """
    result = dEpsilonDp(<double> t, <double> p)
    return result

def cy_DEW_d2EpsilonDt2(double t, double p):
    """ Returns the D2 dielectric constant / Dt2, input t (K), p (bars)
    """
    result = d2EpsilonDt2(<double> t, <double> p)
    return result

def cy_DEW_d2EpsilonDtDp(double t, double p):
    """ Returns the D2 dielectric constant / Dt Dp, input t (K), p (bars)
    """
    result = d2EpsilonDtDp(<double> t, <double> p)
    return result

def cy_DEW_d2EpsilonDp2(double t, double p):
    """ Returns the D2 dielectric constant / Dp2, input t (K), p (bars)
    """
    result = d2EpsilonDp2(<double> t, <double> p)
    return result

def cy_DEW_born_B(double t, double p):
    """ Returns the Born B function value, input t (K), p (bars)
    """
    result = born_B(<double> t, <double> p)
    return result

def cy_DEW_born_Q(double t, double p):
    """ Returns the Born Q function value, input t (K), p (bars)
    """
    result = born_Q(<double> t, <double> p)
    return result

def cy_DEW_born_N(double t, double p):
    """ Returns the Born N function value, input t (K), p (bars)
    """
    result = born_N(<double> t, <double> p)
    return result

def cy_DEW_born_U(double t, double p):
    """ Returns the Born U function value, input t (K), p (bars)
    """
    result = born_U(<double> t, <double> p)
    return result

def cy_DEW_born_Y(double t, double p):
    """ Returns the Born Y function value, input t (K), p (bars)
    """
    result = born_Y(<double> t, <double> p)
    return result

def cy_DEW_born_X(double t, double p):
    """ Returns the Born X function value, input t (K), p (bars)
    """
    result = born_X(<double> t, <double> p)
    return result

def cy_DEW_born_dUdT(double t, double p):
    """ Returns the Born D U / Dt function value, input t (K), p (bars)
    """
    result = born_dUdT(<double> t, <double> p)
    return result

def cy_DEW_born_dUdP(double t, double p):
    """ Returns the Born D U / Dp function value, input t (K), p (bars)
    """
    result = born_dUdP(<double> t, <double> p)
    return result

def cy_DEW_born_dNdT(double t, double p):
    """ Returns the Born D N / Dt function value, input t (K), p (bars)
    """
    result = born_dNdT(<double> t, <double> p)
    return result

def cy_DEW_born_dNdP(double t, double p):
    """ Returns the Born D N / Dp function value, input t (K), p (bars)
    """
    result = born_dNdP(<double> t, <double> p)
    return result

def cy_DEW_born_dXdT(double t, double p):
    """ Returns the Born D X / Dt function value, input t (K), p (bars)
    """
    result = born_dXdT(<double> t, <double> p)
    return result

def cy_DEW_Agamma(double t, double p):
    """ Returns the Debye-Hückel Agamma function value, input t (K), p (bars)
    """
    result = Agamma(<double> t, <double> p)
    return result

def cy_DEW_dAgammaDt(double t, double p):
    """ Returns the Debye-Hückel D Agamma / Dt function value, input t (K), p (bars)
    """
    result = dAgammaDt(<double> t, <double> p)
    return result

def cy_DEW_dAgammaDp(double t, double p):
    """ Returns the Debye-Hückel D Agamma / Dp function value, input t (K), p (bars)
    """
    result = dAgammaDp(<double> t, <double> p)
    return result

def cy_DEW_d2AgammaDt2(double t, double p):
    """ Returns the Debye-Hückel D2 Agamma / Dt2 function value, input t (K), p (bars)
    """
    result = d2AgammaDt2(<double> t, <double> p)
    return result

def cy_DEW_d2AgammaDtDp(double t, double p):
    """ Returns the Debye-Hückel D2 Agamma / Dt Dp function value, input t (K), p (bars)
    """
    result = d2AgammaDtDp(<double> t, <double> p)
    return result

def cy_DEW_d2AgammaDp2(double t, double p):
    """ Returns the Debye-Hückel D2 Agamma / Dp2 function value, input t (K), p (bars)
    """
    result = d2AgammaDp2(<double> t, <double> p)
    return result

def cy_DEW_d3AgammaDt3(double t, double p):
    """ Returns the Debye-Hückel D3 Agamma / Dt3 function value, input t (K), p (bars)
    """
    result = d3AgammaDt3(<double> t, <double> p)
    return result

def cy_DEW_d3AgammaDt2Dp(double t, double p):
    """ Returns the Debye-Hückel D3 Agamma / Dt2 Dp function value, input t (K), p (bars)
    """
    result = d3AgammaDt2Dp(<double> t, <double> p)
    return result

def cy_DEW_d3AgammaDtDp2(double t, double p):
    """ Returns the Debye-Hückel D3 Agamma / Dt Dp2 function value, input t (K), p (bars)
    """
    result = d3AgammaDtDp2(<double> t, <double> p)
    return result

def cy_DEW_d3AgammaDp3(double t, double p):
    """ Returns the Debye-Hückel D3 Agamma / Dp3 function value, input t (K), p (bars)
    """
    result = d3AgammaDp3(<double> t, <double> p)
    return result

def cy_DEW_Bgamma(double t, double p):
    """ Returns the Debye-Hückel Bgamma function value, input t (K), p (bars)
    """
    result = Bgamma(<double> t, <double> p)
    return result

def cy_DEW_dBgammaDt(double t, double p):
    """ Returns the Debye-Hückel D Bgamma / Dt function value, input t (K), p (bars)
    """
    result = dBgammaDt(<double> t, <double> p)
    return result

def cy_DEW_dBgammaDp(double t, double p):
    """ Returns the Debye-Hückel D Bgamma / Dp function value, input t (K), p (bars)
    """
    result = dBgammaDp(<double> t, <double> p)
    return result

def cy_DEW_d2BgammaDt2(double t, double p):
    """ Returns the Debye-Hückel D2 Bgamma / Dt2 function value, input t (K), p (bars)
    """
    result = d2BgammaDt2(<double> t, <double> p)
    return result

def cy_DEW_d2BgammaDtDp(double t, double p):
    """ Returns the Debye-Hückel D2 Bgamma / Dt Dp function value, input t (K), p (bars)
    """
    result = d2BgammaDtDp(<double> t, <double> p)
    return result

def cy_DEW_d2BgammaDp2(double t, double p):
    """ Returns the Debye-Hückel D2 Bgamma / Dp2 function value, input t (K), p (bars)
    """
    result = d2BgammaDp2(<double> t, <double> p)
    return result

def cy_DEW_d3BgammaDt3(double t, double p):
    """ Returns the Debye-Hückel D3 Bgamma / Dt3 function value, input t (K), p (bars)
    """
    result = d3BgammaDt3(<double> t, <double> p)
    return result

def cy_DEW_d3BgammaDt2Dp(double t, double p):
    """ Returns the Debye-Hückel D3 Bgamma / Dt2 Dp function value, input t (K), p (bars)
    """
    result = d3BgammaDt2Dp(<double> t, <double> p)
    return result

def cy_DEW_d3BgammaDtDp2(double t, double p):
    """ Returns the Debye-Hückel D3 Bgamma / Dt Dp2 function value, input t (K), p (bars)
    """
    result = d3BgammaDtDp2(<double> t, <double> p)
    return result

def cy_DEW_d3BgammaDp3(double t, double p):
    """ Returns the Debye-Hückel D3 Bgamma / Dp3 function value, input t (K), p (bars)
    """
    result = d3BgammaDp3(<double> t, <double> p)
    return result

def cy_DEW_AsubG(double t, double p):
    """ Returns the Debye-Hückel AsubG function value, input t (K), p (bars)
    """
    result = AsubG(<double> t, <double> p)
    return result

def cy_DEW_AsubH(double t, double p):
    """ Returns the Debye-Hückel AsubH function value, input t (K), p (bars)
    """
    result = AsubH(<double> t, <double> p)
    return result

def cy_DEW_AsubJ(double t, double p):
    """ Returns the Debye-Hückel AsubJ function value, input t (K), p (bars)
    """
    result = AsubJ(<double> t, <double> p)
    return result

def cy_DEW_AsubV(double t, double p):
    """ Returns the Debye-Hückel AsubV function value, input t (K), p (bars)
    """
    result = AsubV(<double> t, <double> p)
    return result

def cy_DEW_AsubKappa(double t, double p):
    """ Returns the Debye-Hückel AsubKappa function value, input t (K), p (bars)
    """
    result = AsubKappa(<double> t, <double> p)
    return result

def cy_DEW_AsubEx(double t, double p):
    """ Returns the Debye-Hückel AsubEx function value, input t (K), p (bars)
    """
    result = AsubEx(<double> t, <double> p)
    return result

def cy_DEW_BsubG(double t, double p):
    """ Returns the Debye-Hückel BsubG function value, input t (K), p (bars)
    """
    result = BsubG(<double> t, <double> p)
    return result

def cy_DEW_BsubH(double t, double p):
    """ Returns the Debye-Hückel BsubH function value, input t (K), p (bars)
    """
    result = BsubH(<double> t, <double> p)
    return result

def cy_DEW_BsubJ(double t, double p):
    """ Returns the Debye-Hückel BsubJ function value, input t (K), p (bars)
    """
    result = BsubJ(<double> t, <double> p)
    return result

def cy_DEW_BsubV(double t, double p):
    """ Returns the Debye-Hückel BsubV function value, input t (K), p (bars)
    """
    result = BsubV(<double> t, <double> p)
    return result

def cy_DEW_BsubKappa(double t, double p):
    """ Returns the Debye-Hückel BsubKappa function value, input t (K), p (bars)
    """
    result = BsubKappa(<double> t, <double> p)
    return result

def cy_DEW_BsubEx(double t, double p):
    """ Returns the Debye-Hückel BsubEx function value, input t (K), p (bars)
    """
    result = BsubEx(<double> t, <double> p)
    return result

# here are the Cython "wrapper" signatures for extended-HKF the "g" function
def cy_HKF_get_gSolvent_low_density_limit():
    """ Returns the water density limit below which the g-function has a value of zero
    """
    result = get_gSolvent_low_density_limit()
    return result

def cy_HKF_set_gSolvent_low_density_limit(double value):
    """ Sets the water density limit (g/cm^3) below which the g-function has a value of zero
    """
    set_gSolvent_low_density_limit(<double> value)

def cy_HKF_gSolvent(double t, double p):
    """ Returns the extended HKF g-function value, input t (K), p (bars)
    """
    result = gSolvent(<double> t, <double> p)
    return result

def cy_HKF_DgSolventDt(double t, double p):
    """ Returns the extended HKF D g-function / Dt value, input t (K), p (bars)
    """
    result = DgSolventDt(<double> t, <double> p)
    return result

def cy_HKF_DgSolventDp(double t, double p):
    """ Returns the extended HKF D g-function / Dp value, input t (K), p (bars)
    """
    result = DgSolventDp(<double> t, <double> p)
    return result

def cy_HKF_D2gSolventDt2(double t, double p):
    """ Returns the extended HKF D2 g-function / Dt2 value, input t (K), p (bars)
    """
    result = D2gSolventDt2(<double> t, <double> p)
    return result

def cy_HKF_D2gSolventDtDp(double t, double p):
    """ Returns the extended HKF D2 g-function / Dt Dp value, input t (K), p (bars)
    """
    result = D2gSolventDtDp(<double> t, <double> p)
    return result

def cy_HKF_D2gSolventDp2(double t, double p):
    """ Returns the extended HKF D2 g-function / Dp2 value, input t (K), p (bars)
    """
    result = D2gSolventDp2(<double> t, <double> p)
    return result

def cy_HKF_D3gSolventDt3(double t, double p):
    """ Returns the extended HKF D3 g-function / Dt3 value, input t (K), p (bars)
    """
    result = D3gSolventDt3(<double> t, <double> p)
    return result

def cy_HKF_D3gSolventDt2Dp(double t, double p):
    """ Returns the extended HKF D3 g-function / Dt2 Dp value, input t (K), p (bars)
    """
    result = D3gSolventDt2Dp(<double> t, <double> p)
    return result

def cy_HKF_D3gSolventDtDp2(double t, double p):
    """ Returns the extended HKF D3 g-function / Dt Dp2 value, input t (K), p (bars)
    """
    result = D3gSolventDtDp2(<double> t, <double> p)
    return result

def cy_HKF_D3gSolventDp3(double t, double p):
    """ Returns the extended HKF D3 g-function / Dp3 value, input t (K), p (bars)
    """
    result = D3gSolventDp3(<double> t, <double> p)
    return result

def cy_HKF_D4gSolventDt4(double t, double p):
    """ Returns the extended HKF D4 g-function / Dt4 value, input t (K), p (bars)
    """
    result = D4gSolventDt4(<double> t, <double> p)
    return result

# here are the Cython "wrapper" signatures for SWIM 
def cy_SWIM_aqueous_identifier():
    """ Standard Water Integrated Model, str, identifier
    """
    result = 'Std-H2O-Int-Model'
    return result
def cy_SWIM_aqueous_calib_identifier():
    """ Standard Water Integrated Model, str, identifier
    """
    return cy_SWIM_aqueous_identifier()

def cy_SWIM_aqueous_name():
    """ Standard Water Integrated Model, str, name
    """
    result = 'SWIM'
    return result
def cy_SWIM_aqueous_calib_name():
    """ Standard Water Integrated Model, str, name
    """
    return cy_SWIM_aqueous_name()

def cy_SWIM_aqueous_formula():
    """ Standard Water Integrated Model, str, formula
    """
    result = 'H2O'
    return result
def cy_SWIM_aqueous_calib_formula():
    """ Standard Water Integrated Model, str, formula
    """
    return cy_SWIM_aqueous_formula()

def cy_SWIM_aqueous_mw():
    """ Standard Water Integrated Model, double, molecular weight
    """
    result = 18.01528
    return result
def cy_SWIM_aqueous_calib_mw():
    """ Standard Water Integrated Model, double, molecular weight
    """
    return cy_SWIM_aqueous_mw()

def cy_SWIM_aqueous_elements():
    """ Standard Water Integrated Model, numpy array, element stoichiometry
    """
    np_array = np.zeros(106)
    np_array[1] = 2.0
    np_array[8] = 1.0
    return np_array
def cy_SWIM_aqueous_calib_elements():
    """ Standard Water Integrated Model, numpy array, element stoichiometry
    """
    return cy_SWIM_aqueous_elements()

def cy_SWIM_aqueous_g(double t, double p):
    """ Standard Water Integrated Model, Gibbs energy, input t (K), p (bars)
    """
    result = SWIM_getGibbsFreeEnergy(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_g(double t, double p):
    """ Standard Water Integrated Model, Gibbs energy, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_g(t, p)

def cy_SWIM_aqueous_dgdt(double t, double p):
    """ Standard Water Integrated Model, D Gibbs energy / Dt, input t (K), p (bars)
    """
    result = -SWIM_getEntropy(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_dgdt(double t, double p):
    """ Standard Water Integrated Model, D Gibbs energy / Dt, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_dgdt(t, p)

def cy_SWIM_aqueous_dgdp(double t, double p):
    """ Standard Water Integrated Model, D Gibbs energy / Dp, input t (K), p (bars)
    """
    result = SWIM_getVolume(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_dgdp(double t, double p):
    """ Standard Water Integrated Model, D Gibbs energy / Dp, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_dgdp(t, p)

def cy_SWIM_aqueous_d2gdt2(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dt2, input t (K), p (bars)
    """
    result = -SWIM_getHeatCapacity(<double> t, <double> p, eos_type)/t
    return result
def cy_SWIM_aqueous_calib_d2gdt2(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dt2, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d2gdt2(t, p)

def cy_SWIM_aqueous_d2gdtdp(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dt Dp, input t (K), p (bars)
    """
    result = SWIM_getDvDt(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_d2gdtdp(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dt Dp, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d2gdtdp(t, p)

def cy_SWIM_aqueous_d2gdp2(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dp2, input t (K), p (bars)
    """
    result = SWIM_getDvDp(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_d2gdp2(double t, double p):
    """ Standard Water Integrated Model, D2 Gibbs energy / Dp2, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d2gdp2(t, p)

def cy_SWIM_aqueous_d3gdt3(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt3, input t (K), p (bars)
    """
    result  = -SWIM_getDcpDt(<double> t, <double> p, eos_type)/t
    result += SWIM_getHeatCapacity(<double> t, <double> p, eos_type)/t/t
    return result
def cy_SWIM_aqueous_calib_d3gdt3(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt3, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d3gdt3(t, p)

def cy_SWIM_aqueous_d3gdt2dp(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt2 Dp, input t (K), p (bars)
    """
    result = SWIM_getD2vDt2(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_d3gdt2dp(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt2 Dp, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d3gdt2dp(t, p)

def cy_SWIM_aqueous_d3gdtdp2(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt Dp2, input t (K), p (bars)
    """
    result = SWIM_getD2vDtDp(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_d3gdtdp2(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dt Dp2, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d3gdtdp2(t, p)

def cy_SWIM_aqueous_d3gdp3(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dp3, input t (K), p (bars)
    """
    result = SWIM_getD2vDp2(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_d3gdp3(double t, double p):
    """ Standard Water Integrated Model, D3 Gibbs energy / Dp3, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_d3gdp3(t, p)

def cy_SWIM_aqueous_s(double t, double p):
    """ Standard Water Integrated Model, Entropy, input t (K), p (bars)
    """
    result = SWIM_getEntropy(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_s(double t, double p):
    """ Standard Water Integrated Model, Entropy, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_s(t, p)

def cy_SWIM_aqueous_v(double t, double p):
    """ Standard Water Integrated Model, Volume, input t (K), p (bars)
    """
    result = SWIM_getVolume(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_v(double t, double p):
    """ Standard Water Integrated Model, Volume, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_v(t, p)

def cy_SWIM_aqueous_cv(double t, double p):
    """ Standard Water Integrated Model, Heat Capacity at constant volume, input t (K), p (bars)
    """
    result = t*cy_SWIM_aqueous_v(t, p)*(cy_SWIM_aqueous_alpha(t, p))**2/cy_SWIM_aqueous_beta(t, p)
    return cy_SWIM_aqueous_cp(t, p) - result
def cy_SWIM_aqueous_calib_cv(double t, double p):
    """ Standard Water Integrated Model, Heat Capacity at constant volume, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_cv(t, p)

def cy_SWIM_aqueous_cp(double t, double p):
    """ Standard Water Integrated Model, Heat Capacity at constant pressure, input t (K), p (bars)
    """
    result = SWIM_getHeatCapacity(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_cp(double t, double p):
    """ Standard Water Integrated Model, Heat Capacity at constant pressure, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_cp(t, p)

def cy_SWIM_aqueous_dcpdt(double t, double p):
    """ Standard Water Integrated Model, D Heat Capacity at constant pressure / Dt, input t (K), p (bars)
    """
    result = SWIM_getDcpDt(<double> t, <double> p, eos_type)
    return result
def cy_SWIM_aqueous_calib_dcpdt(double t, double p):
    """ Standard Water Integrated Model, D Heat Capacity at constant pressure / Dt, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_dcpdt(t, p)

def cy_SWIM_aqueous_alpha(double t, double p):
    """ Standard Water Integrated Model, Thermal Expansion, input t (K), p (bars)
    """
    result = cy_SWIM_aqueous_d2gdtdp(t, p)/cy_SWIM_aqueous_v(t, p)
    return result
def cy_SWIM_aqueous_calib_alpha(double t, double p):
    """ Standard Water Integrated Model, Thermal Expansion, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_alpha(t, p)

def cy_SWIM_aqueous_beta(double t, double p):
    """ Standard Water Integrated Model, Compressibility, input t (K), p (bars)
    """
    result = -cy_SWIM_aqueous_d2gdp2(t, p)/cy_SWIM_aqueous_v(t, p)
    return result
def cy_SWIM_aqueous_calib_beta(double t, double p):
    """ Standard Water Integrated Model, Compressibility, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_beta(t, p)

def cy_SWIM_aqueous_K(double t, double p):
    """ Standard Water Integrated Model, Bulk Modulus, input t (K), p (bars)
    """
    result = 1.0/cy_SWIM_aqueous_beta(t, p)
    return result
def cy_SWIM_aqueous_calib_K(double t, double p):
    """ Standard Water Integrated Model, Bulk Modulus, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_K(t, p)

def cy_SWIM_aqueous_Kp(double t, double p):
    """ Standard Water Integrated Model, D Bulk Modulus / Dp, input t (K), p (bars)
    """
    result  = (cy_SWIM_aqueous_d2gdp2(t, p)/cy_SWIM_aqueous_v(t, p))**2
    result -= cy_SWIM_aqueous_d3gdp3(t, p)/cy_SWIM_aqueous_v(t, p)
    return result
def cy_SWIM_aqueous_calib_Kp(double t, double p):
    """ Standard Water Integrated Model, D Bulk Modulus / Dp, input t (K), p (bars)
    """
    return cy_SWIM_aqueous_Kp(t, p)

# Methods below only apply to calibration models

def cy_SWIM_aqueous_get_param_number():
    return 1
def cy_SWIM_aqueous_get_param_names():
    result = []
    result.append('EOS/0-auto/1-DZ2006/2-ZD2005/3-Holten/4-Wagner')
    return result
def cy_SWIM_aqueous_get_param_units():
    result = []
    result.append('None')
    return result
def cy_SWIM_aqueous_get_param_values():
    np_array = np.array([eos_type])
    return np_array
def cy_SWIM_aqueous_set_param_values(np_array):
    global eos_type
    n = len(np_array)
    assert n == 1, 'Specify one parameter.'
    assert np_array[0] >= 0 and np_array[0] <5, '0 <= value <= 4'
    eos_type = np_array[0]
    return True
def cy_SWIM_aqueous_get_param_value(int index):
    assert index == 0, 'Only permitted index value is zero.'
    result = eos_type
    return result
def cy_SWIM_aqueous_set_param_value(int index, int value):
    global eos_type
    assert index == 0, 'Only permitted index value is zero.'
    assert isinstance(value, int), 'Value must be an integer'
    assert value >= 0 and value < 5, '0 <= value <= 4'
    eos_type = value
    return True
def cy_SWIM_aqueous_dparam_g(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_dgdt(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_dgdp(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d2gdt2(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d2gdtdp(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d2gdp2(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d3gdt3(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d3gdt2dp(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d3gdtdp2(double t, double p, int index):
    return 0
def cy_SWIM_aqueous_dparam_d3gdp3(double t, double p, int index):
    return 0
