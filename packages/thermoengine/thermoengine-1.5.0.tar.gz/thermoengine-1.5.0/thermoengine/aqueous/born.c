#include "born.h"
#include "swim.h"

#include <float.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static const double R  =  8.3144598;
static const double MW = 18.01528;

// Sverjensky et at. (2014), GCA, 129, 125-145

static const double a1 = -1.57637700752506e-3;
static const double a2 =  6.81028783422197e-2;
static const double a3 =  7.54875480393944e-1;

static const double b1 = -8.01665106535394e-5;
static const double b2 = -6.87161761831994e-2;
static const double b3 =  4.74797272182151e0;

// "a" coefficient on a Kelvin basis
static const double aTK1 = -5.8274486041453000E-02;
static const double aTK2 =  2.2389805995733700E+00;
static const double aTK3 = -2.0249736922093000E+01;

// "b" coefficient on a Kelvin basis
static const double bTK1 =  5.7128535105795700E-02;
static const double bTK2 = -2.2591436511452200E+00;
static const double bTK3 =  2.6398103834434400E+01;

#define mask_rho       1
#define mask_drhodt    2
#define mask_drhodp    3
#define mask_d2rhodt2  4
#define mask_d2rhodtdp 5
#define mask_d2rhodp2  6

double SWIM_getVolume(double t, double p, SWIM_RegionType region);
double SWIM_getDvDt(double t, double  p, SWIM_RegionType region);
double SWIM_getDvDp(double t, double p, SWIM_RegionType region);
double SWIM_getD2vDt2(double t, double p, SWIM_RegionType region);
double SWIM_getD2vDtDp(double t, double p, SWIM_RegionType region);
double SWIM_getD2vDp2(double t, double p, SWIM_RegionType region);

static double loadDensityProperties(int mask, double t, double p) {
    double v       = 10.0*SWIM_getVolume(t, p, NotApplicable);
    if (mask == mask_rho)       return MW/v;
    if (mask == mask_drhodt)    {
        double dvdt    = 10.0*SWIM_getDvDt(t, p, NotApplicable);
        return -MW*dvdt/v/v;
    }
    if (mask == mask_drhodp)    {
        double dvdp    = 10.0*SWIM_getDvDp(t, p, NotApplicable);
        return -MW*dvdp/v/v;
    }
    if (mask == mask_d2rhodt2)  {
        double dvdt    = 10.0*SWIM_getDvDt(t, p, NotApplicable);
        double d2vdt2  = 10.0*SWIM_getD2vDt2(t, p, NotApplicable);
        return MW*(2.0*dvdt*dvdt/v/v/v - d2vdt2/v/v);
    }
    if (mask == mask_d2rhodtdp) {
        double dvdt    = 10.0*SWIM_getDvDt(t, p, NotApplicable);
        double dvdp    = 10.0*SWIM_getDvDp(t, p, NotApplicable);
        double d2vdtdp = 10.0*SWIM_getD2vDtDp(t, p, NotApplicable);
        return MW*(2.0*dvdt*dvdp/v/v/v - d2vdtdp/v/v);
    }
    if (mask == mask_d2rhodp2)  {
        double dvdp    = 10.0*SWIM_getDvDp(t, p, NotApplicable);
        double d2vdp2  = 10.0*SWIM_getD2vDp2(t, p, NotApplicable);
        return MW*(2.0*dvdp*dvdp/v/v/v - d2vdp2/v/v);
    }
    return 0.0;
}

// Model of Johnson and Norton (1991)

static double JN_epsilon(double t, double p) {
    double rho = loadDensityProperties(mask_rho, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
                
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;

    double epsilon = k0 + k1*rho + k2*rho*rho + k3*rho*rho*rho + k4*rho*rho*rho*rho;
    return epsilon;
}

static double JN_dEpsilonDt(double t, double p) {
    double  rho   = loadDensityProperties(mask_rho, t, p);
    double DrhoDt = loadDensityProperties(mask_drhodt, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;
    double Dk1Dt = -14.70333593*DT_hatDt/T_hat/T_hat;
    double Dk2Dt = -212.8462733*DT_hatDt/T_hat/T_hat + 19.55210915*DT_hatDt;
    double Dk3Dt = 83.3034798*DT_hatDt/T_hat/T_hat + 32.13240048*DT_hatDt - 2.0*6.69409865*T_hat*DT_hatDt;
    double Dk4Dt = 2.0*37.86202045*DT_hatDt/T_hat/T_hat/T_hat - 68.87359646*DT_hatDt/T_hat/T_hat;
    
    double DepsilonDt = Dk1Dt*rho + k1*DrhoDt + Dk2Dt*rho*rho + 2.0*k2*rho*DrhoDt + Dk3Dt*rho*rho*rho 
                      + 3.0*k3*rho*rho*DrhoDt + Dk4Dt*rho*rho*rho*rho + 4.0*k4*rho*rho*rho*DrhoDt;
    return DepsilonDt;
}

static double JN_dEpsilonDp(double t, double p) {
    double  rho   = loadDensityProperties(mask_rho, t, p);
    double DrhoDp = loadDensityProperties(mask_drhodp, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;

    double DepsilonDp = k1*DrhoDp + 2.0*k2*rho*DrhoDp + 3.0*k3*rho*rho*DrhoDp + 4.0*k4*rho*rho*rho*DrhoDp;
    return DepsilonDp;
}

static double JN_d2EpsilonDt2(double t, double p) {
    double   rho    = loadDensityProperties(mask_rho, t, p);
    double  DrhoDt  = loadDensityProperties(mask_drhodt, t, p);
    double D2rhoDt2 = loadDensityProperties(mask_d2rhodt2, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;
    double Dk1Dt = -14.70333593*DT_hatDt/T_hat/T_hat;
    double Dk2Dt = -212.8462733*DT_hatDt/T_hat/T_hat + 19.55210915*DT_hatDt;
    double Dk3Dt = 83.3034798*DT_hatDt/T_hat/T_hat + 32.13240048*DT_hatDt - 2.0*6.69409865*T_hat*DT_hatDt;
    double Dk4Dt = 2.0*37.86202045*DT_hatDt/T_hat/T_hat/T_hat - 68.87359646*DT_hatDt/T_hat/T_hat;
    double D2k1Dt2 = 2.0*14.70333593*DT_hatDt*DT_hatDt/T_hat/T_hat/T_hat;
    double D2k2Dt2 = 2.0*212.8462733*DT_hatDt*DT_hatDt/T_hat/T_hat/T_hat;
    double D2k3Dt2 = -2.0*83.3034798*DT_hatDt*DT_hatDt/T_hat/T_hat/T_hat - 2.0*6.69409865*DT_hatDt*DT_hatDt;
    double D2k4Dt2 = -3.0*2.0*37.86202045*DT_hatDt*DT_hatDt/T_hat/T_hat/T_hat/T_hat + 2.0*68.87359646*DT_hatDt*DT_hatDt/T_hat/T_hat/T_hat;
    
    double D2epsilonDt2 = D2k1Dt2*rho + Dk1Dt*DrhoDt + Dk1Dt*DrhoDt + k1*D2rhoDt2
                        + D2k2Dt2*rho*rho + 2.0*Dk2Dt*rho*DrhoDt + 2.0*Dk2Dt*rho*DrhoDt + 2.0*k2*DrhoDt*DrhoDt 
                        + 2.0*k2*rho*D2rhoDt2 + D2k3Dt2*rho*rho*rho + 3.0*Dk3Dt*rho*rho*DrhoDt
                        + 3.0*Dk3Dt*rho*rho*DrhoDt + 2.0*3.0*k3*rho*DrhoDt*DrhoDt + 3.0*k3*rho*rho*D2rhoDt2
                        + D2k4Dt2*rho*rho*rho*rho + 4.0*Dk4Dt*rho*rho*rho*DrhoDt + 4.0*Dk4Dt*rho*rho*rho*DrhoDt 
                        + 3.0*4.0*k4*rho*rho*DrhoDt*DrhoDt + 4.0*k4*rho*rho*rho*D2rhoDt2;
    return D2epsilonDt2;
}

static double JN_d2EpsilonDtDp(double t, double p) {
    double   rho     = loadDensityProperties(mask_rho, t, p);
    double  DrhoDp   = loadDensityProperties(mask_drhodp, t, p);
    double  DrhoDt   = loadDensityProperties(mask_drhodt, t, p);
    double D2rhoDtDp = loadDensityProperties(mask_d2rhodtdp, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;
    double Dk1Dt = -14.70333593*DT_hatDt/T_hat/T_hat;
    double Dk2Dt = -212.8462733*DT_hatDt/T_hat/T_hat + 19.55210915*DT_hatDt;
    double Dk3Dt = 83.3034798*DT_hatDt/T_hat/T_hat + 32.13240048*DT_hatDt - 2.0*6.69409865*T_hat*DT_hatDt;
    double Dk4Dt = 2.0*37.86202045*DT_hatDt/T_hat/T_hat/T_hat - 68.87359646*DT_hatDt/T_hat/T_hat;

    double D2epsilonDtDp = Dk1Dt*DrhoDp + k1*D2rhoDtDp + 2.0*Dk2Dt*rho*DrhoDp + 2.0*k2*DrhoDp*DrhoDt 
                         + 2.0*k2*rho*D2rhoDtDp + 3.0*Dk3Dt*rho*rho*DrhoDp + 2.0*3.0*k3*rho*DrhoDp*DrhoDt 
                         + 3.0*k3*rho*rho*D2rhoDtDp + 4.0*Dk4Dt*rho*rho*rho*DrhoDp 
                         + 3.0*4.0*k4*rho*rho*DrhoDp*DrhoDt + 4.0*k4*rho*rho*rho*D2rhoDtDp;

    return D2epsilonDtDp;
}

static double JN_d2EpsilonDp2(double t, double p) {
    double   rho    = loadDensityProperties(mask_rho, t, p);
    double  DrhoDp  = loadDensityProperties(mask_drhodp, t, p);
    double D2rhoDp2 = loadDensityProperties(mask_d2rhodp2, t, p);
    double T_hat = t/298.15;
    double DT_hatDt = 1.0/298.15;
    double k0 = 1.0;
    double k1 = 14.70333593/T_hat;
    double k2 = 212.8462733/T_hat - 115.4445173 + 19.55210915*T_hat;
    double k3 = -83.3034798/T_hat + 32.13240048 * T_hat - 6.69409865*T_hat*T_hat;
    double k4 = -37.86202045/(T_hat*T_hat) + 68.87359646/T_hat - 27.29401652;
    
    double D2epsilonDp2 = k1*D2rhoDp2 + 2.0*k2*DrhoDp*DrhoDp + 2.0*k2*rho*D2rhoDp2 + 2.0*3.0*k3*rho*DrhoDp*DrhoDp 
                        + 3.0*k3*rho*rho*D2rhoDp2 + 3.0*4.0*k4*rho*rho*DrhoDp*DrhoDp + 4.0*k4*rho*rho*rho*D2rhoDp2;
    return D2epsilonDp2;
}

// Model of Sverjensky et al. (2014)

static double DM_epsilon(double t, double p) {
    double tc = t - 273.15;
    double rho = loadDensityProperties(mask_rho, t, p);
    double rhoExponent = 0.0, expExponent = 0.0;
    if (tc > 0.0) {
        rhoExponent = a1*tc + a2*sqrt(tc) + a3;
        expExponent = b1*tc + b2*sqrt(tc) + b3;

    } else {
        rhoExponent = aTK1*t + aTK2*sqrt(t) + aTK3;
        expExponent = bTK1*t + bTK2*sqrt(t) + bTK3;
    }
    return exp(expExponent)*pow(rho, rhoExponent);
}

static double DM_dEpsilonDt(double t, double p) {
    double tc = t - 273.15;
    if (tc < 0.0) return 0.0;
    double  rho   = loadDensityProperties(mask_rho, t, p);
    double DrhoDt = loadDensityProperties(mask_drhodt, t, p);
    double  rhoExponent   = a1*tc + a2*sqrt(tc) + a3;
    double DrhoExponentDt = a1 + a2/2.0/sqrt(tc);
    double  expExponent = b1*tc + b2*sqrt(tc) + b3;
    double DexpExponentDt = b1 + b2/2.0/sqrt(tc);

    // d f(t,p)^g(t) / dt = g(t) * f(t,p)^[g(t)-1] * f'(t*,p) + f(t,p)^g(t) * ln[f(t,p)] * g'(t)
    double DepsilonDt = DexpExponentDt*exp(expExponent)*pow(rho, rhoExponent)
                      + exp(expExponent)*(  rhoExponent*pow(rho, rhoExponent-1.0)*DrhoDt
                                          + pow(rho, rhoExponent)*log(rho)*DrhoExponentDt
                                         );
    return DepsilonDt;
}

static double DM_dEpsilonDp(double t, double p) {
    double tc = t - 273.15;
    if (tc < 0.0) return 0.0;
    double  rho   = loadDensityProperties(mask_rho, t, p);
    double DrhoDp = loadDensityProperties(mask_drhodp, t, p);
    double  rhoExponent = a1*tc + a2*sqrt(tc) + a3;
    double  expExponent = b1*tc + b2*sqrt(tc) + b3;

    // d f(t,p)^g(t) / dp = g(t) * f(t,p)^[g(t)-1] * f'(t,p*)
    double DepsilonDp = exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*DrhoDp;
    return DepsilonDp;
}

static double DM_d2EpsilonDt2(double t, double p) {
    double tc = t - 273.15;
    if (tc < 0.0) return 0.0;
    double   rho    = loadDensityProperties(mask_rho, t, p);
    double  DrhoDt  = loadDensityProperties(mask_drhodt, t, p);
    double D2rhoDt2 = loadDensityProperties(mask_d2rhodt2, t, p);
    double  rhoExponent     = a1*tc + a2*sqrt(tc) + a3;
    double  DrhoExponentDt  = a1 + a2/2.0/sqrt(tc);
    double D2rhoExponentDt2 = - a2/2.0/2.0/pow(tc, 3.0/2.0);
    double   expExponent    = b1*tc + b2*sqrt(tc) + b3;
    double  DexpExponentDt  = b1 + b2/2.0/sqrt(tc);
    double D2expExponentDt2 = - b2/2.0/2.0/pow(tc, 3.0/2.0);

    double DpowOfRowToTheRhoExponent   =       rhoExponent*pow(rho, rhoExponent-1.0)*DrhoDt + pow(rho, rhoExponent)    *log(rho)*DrhoExponentDt;
    double DpowOfRowToTheRhoExponentM1 = (rhoExponent-1.0)*pow(rho, rhoExponent-2.0)*DrhoDt + pow(rho, rhoExponent-1.0)*log(rho)*DrhoExponentDt;

    double DepsilonDt = D2expExponentDt2*exp(expExponent)*pow(rho, rhoExponent)
                      + DexpExponentDt*DexpExponentDt*exp(expExponent)*pow(rho, rhoExponent)
                      + DexpExponentDt*exp(expExponent)*DpowOfRowToTheRhoExponent
                      + DexpExponentDt*exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*DrhoDt
                      + exp(expExponent)*DrhoExponentDt*pow(rho, rhoExponent-1.0)*DrhoDt
                      + exp(expExponent)*rhoExponent*DpowOfRowToTheRhoExponentM1*DrhoDt
                      + exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*D2rhoDt2
                      + DexpExponentDt*exp(expExponent)*pow(rho, rhoExponent)*log(rho)*DrhoExponentDt
                      + exp(expExponent)*DpowOfRowToTheRhoExponent*log(rho)*DrhoExponentDt
                      + exp(expExponent)*pow(rho, rhoExponent)*(DrhoDt/rho)*DrhoExponentDt
                      + exp(expExponent)*pow(rho, rhoExponent)*log(rho)*D2rhoExponentDt2;
    return DepsilonDt;
}

static double DM_d2EpsilonDtDp(double t, double p) {
    double tc = t - 273.15;
    if (tc < 0.0) return 0.0;
    double   rho     = loadDensityProperties(mask_rho, t, p);
    double  DrhoDp   = loadDensityProperties(mask_drhodp, t, p);
    double  DrhoDt   = loadDensityProperties(mask_drhodt, t, p);
    double D2rhoDtDp = loadDensityProperties(mask_d2rhodtdp, t, p);
    double  rhoExponent   = a1*tc + a2*sqrt(tc) + a3;
    double DrhoExponentDt = a1 + a2/2.0/sqrt(tc);
    double  expExponent = b1*tc + b2*sqrt(tc) + b3;
    double DexpExponentDt = b1 + b2/2.0/sqrt(tc);

    // d2 f(t,p)^g(t) / dtdp = g(t) * [g(t)-1] * f(t,p)^[g(t)-2] * f'(t*,p) * f'(t,p*)
    //                       + g(t) * f(t,p)^[g(t)-1] * f''(t*,p*)
    //                       + g(t) * f(t,p)^[g(t)-1] * ln[f(t,p)] * g'(t) * f'(t,p*)
    //                       + f(t,p)^[g(t)-1] * f'(t,p*) * g'(t)
    double D2epsilonDtDp = DexpExponentDt*exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*DrhoDp
                         + exp(expExponent)*rhoExponent*(rhoExponent-1.0)*pow(rho, rhoExponent-2.0)*DrhoDt*DrhoDp
                         + exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*D2rhoDtDp
                         + exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*log(rho)*DrhoExponentDt*DrhoDp
                         + exp(expExponent)*pow(rho, rhoExponent-1.0)*DrhoExponentDt*DrhoDp;

    return D2epsilonDtDp;
}

static double DM_d2EpsilonDp2(double t, double p) {
    double tc = t - 273.15;
    if (tc < 0.0) return 0.0;
    double   rho    = loadDensityProperties(mask_rho, t, p);
    double  DrhoDp  = loadDensityProperties(mask_drhodp, t, p);
    double D2rhoDp2 = loadDensityProperties(mask_d2rhodp2, t, p);
    double  rhoExponent = a1*tc + a2*sqrt(tc) + a3;
    double  expExponent = b1*tc + b2*sqrt(tc) + b3;

    // d2 f(t,p)^g(t) / dp2 = g(t) * [g(t)-1] * f(t,p)^[g(t)-2] * f'(t,p*) * f'(t,p*) + g(t) * f(t,p)^[g(t)-1] * f''(t,p**)
    double D2epsilonDp2 = exp(expExponent)*rhoExponent*(rhoExponent-1.0)*pow(rho, rhoExponent-2.0)*DrhoDp*DrhoDp
                        + exp(expExponent)*rhoExponent*pow(rho, rhoExponent-1.0)*D2rhoDp2;
    return D2epsilonDp2;
}

// Smoothed values derived from the two models

static const double width_of_DM_to_JN_smooth_interval  = 1000.0;
static const double center_of_DM_to_JN_smooth_interval = 5000.0;

static double smooth(double p, double DM_value, double JN_value) {
    double result = 0.0;
    if (p < center_of_DM_to_JN_smooth_interval) {
        double weight = 1.0/2.0 + tanh((p-center_of_DM_to_JN_smooth_interval)/width_of_DM_to_JN_smooth_interval)/2.0;
        if (weight < 0.001) weight = 0.0;
        result += weight*DM_value + (1.0-weight)*JN_value;
    } else {
        double weight = 1.0/2.0 - tanh((p-center_of_DM_to_JN_smooth_interval)/width_of_DM_to_JN_smooth_interval)/2.0;
        if (weight < 0.001) weight = 0.0;
        result += weight*JN_value + (1.0-weight)*DM_value;
    }
    return result;
}

double epsilon(double t, double p) {
    double DM_value = DM_epsilon(t, p);
    double JN_value = JN_epsilon(t, p);
    return smooth(p, DM_value, JN_value);
}

double dEpsilonDt(double t, double p) {
    double DM_value = DM_dEpsilonDt(t, p);
    double JN_value = JN_dEpsilonDt(t, p);
    return smooth(p, DM_value, JN_value);
}

double dEpsilonDp(double t, double p) {
    double DM_value = DM_dEpsilonDp(t, p);
    double JN_value = JN_dEpsilonDp(t, p);
    return smooth(p, DM_value, JN_value);
}

double d2EpsilonDt2(double t, double p) {
    double DM_value = DM_d2EpsilonDt2(t, p);
    double JN_value = JN_d2EpsilonDt2(t, p);
    return smooth(p, DM_value, JN_value);
}

double d2EpsilonDtDp(double t, double p) {
    double DM_value = DM_d2EpsilonDtDp(t, p);
    double JN_value = JN_d2EpsilonDtDp(t, p);
    return smooth(p, DM_value, JN_value);
}

double d2EpsilonDp2(double t, double p) {
    double DM_value = DM_d2EpsilonDp2(t, p);
    double JN_value = JN_d2EpsilonDp2(t, p);
    return smooth(p, DM_value, JN_value);
}

// Born and Debye-Huckel functions

double born_B(double t, double p) {
    double Epsilon = epsilon(t, p);
    return -1.0/Epsilon;
}

double born_Q(double t, double p) {
    double Epsilon = epsilon(t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    return DepsilonDp/Epsilon/Epsilon;
}

double born_N(double t, double p) {
    double Epsilon = epsilon(t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double D2epsilonDp2 = d2EpsilonDp2(t, p);
    return - 2.0*DepsilonDp*DepsilonDp/Epsilon/Epsilon/Epsilon  + D2epsilonDp2/Epsilon/Epsilon;
}

double born_U(double t, double p) {
    double Epsilon = epsilon(t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double D2epsilonDtDp = d2EpsilonDtDp(t, p);
    return D2epsilonDtDp/Epsilon/Epsilon - 2.0*DepsilonDp*DepsilonDt/Epsilon/Epsilon/Epsilon;
}

double born_Y(double t, double p) {
    double Epsilon = epsilon(t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    return DepsilonDt/Epsilon/Epsilon;
}

double born_X(double t, double p) {
    double Epsilon = epsilon(t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double D2epsilonDt2 = d2EpsilonDt2(t, p);

    double  dlnEpsilonDt  = DepsilonDt/Epsilon;
    double d2lnEpsilonDt2 = -DepsilonDt*DepsilonDt/Epsilon/Epsilon + D2epsilonDt2/Epsilon;

    return (d2lnEpsilonDt2 - dlnEpsilonDt*dlnEpsilonDt)/Epsilon;
}

#define EPS 1.0e-6

double born_dUdT(double t, double p) {
    double Uplus = born_U(t*(1.0+EPS), p);
    double Uminus = born_U(t*(1.0-EPS), p);
    return (Uplus-Uminus)/2.0/(t*EPS);
}

double born_dUdP(double t, double p) {
    double Uplus = born_U(t, p*(1.0+EPS));
    double Uminus = born_U(t, p*(1.0-EPS));
    return (Uplus-Uminus)/2.0/(p*EPS);
}

double born_dNdT(double t, double p) {
    return born_dUdP(t, p);
}

double born_dNdP(double t, double p) {
    double Nplus = born_N(t, p*(1.0+EPS));
    double Nminus = born_N(t, p*(1.0-EPS));
    return (Nplus-Nminus)/2.0/(p*EPS);
}

double born_dXdT(double t, double p) {
    double Xplus = born_X(t*(1.0+EPS), p);
    double Xminus = born_X(t*(1.0-EPS), p);
    return (Xplus-Xminus)/2.0/(t*EPS);
}

double Agamma(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    return 1.824829238e6*sqrt(rho)/pow(Epsilon*t, 3.0/2.0);
}

double dAgammaDt(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    return 1.824829238e6*dRhoDt/2.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
    - 3.0*1.824829238e6*sqrt(rho)*(DepsilonDt*t + Epsilon)/2.0/pow(Epsilon*t, 5.0/2.0);
}

double dAgammaDp(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    return 1.824829238e6*dRhoDp/2.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0) - 3.0*1.824829238e6*sqrt(rho)*DepsilonDp*t/2.0/pow(Epsilon*t, 5.0/2.0);
}

double d2AgammaDt2(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    double D2epsilonDt2 = d2EpsilonDt2(t, p);
    double d2RhoDt2 = loadDensityProperties(mask_d2rhodt2, t, p);
    double result = 1.824829238e6*d2RhoDt2/2.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
    - 1.824829238e6*dRhoDt*dRhoDt/4.0/pow(rho, 3.0/2.0)/pow(Epsilon*t, 3.0/2.0)
    - 3.0*1.824829238e6*dRhoDt*(DepsilonDt*t+Epsilon)/4.0/sqrt(rho)/pow(Epsilon*t, 5.0/2.0)
    - 3.0*1.824829238e6*dRhoDt*(DepsilonDt*t+Epsilon)/4.0/sqrt(rho)/pow(Epsilon*t, 5.0/2.0)
    - 3.0*1.824829238e6*sqrt(rho)*(D2epsilonDt2*t+2.0*DepsilonDt)/2.0/pow(Epsilon*t, 5.0/2.0)
    + 15.0*1.824829238e6*sqrt(rho)*(DepsilonDt*t+Epsilon)*(DepsilonDt*t+Epsilon)/4.0/pow(Epsilon*t, 7.0/2.0);
    return result;
}

double d2AgammaDtDp(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    double D2epsilonDtDp = d2EpsilonDtDp(t, p);
    double d2RhoDtDp = loadDensityProperties(mask_d2rhodtdp, t, p);

    double result = 1.824829238e6*d2RhoDtDp/2.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
                  - 1.824829238e6*dRhoDt*dRhoDp/4.0/pow(rho, 3.0/2.0)/pow(Epsilon*t, 3.0/2.0)
                  - 3.0*1.824829238e6*dRhoDt*DepsilonDp*t/4.0/sqrt(rho)/pow(Epsilon*t, 5.0/2.0)
                  - 3.0*1.824829238e6*dRhoDp*(DepsilonDt*t + Epsilon)/sqrt(rho)/4.0/pow(Epsilon*t, 5.0/2.0)
                  - 3.0*1.824829238e6*sqrt(rho)*(D2epsilonDtDp*t + DepsilonDp)/2.0/pow(Epsilon*t, 5.0/2.0)
                  + 5.0*3.0*1.824829238e6*sqrt(rho)*(DepsilonDt*t + Epsilon)*DepsilonDp*t/4.0/pow(Epsilon*t, 7.0/2.0);
    return result;
}

double d2AgammaDp2(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    double D2epsilonDp2 = d2EpsilonDp2(t, p);
    double d2RhoDp2 = loadDensityProperties(mask_d2rhodp2, t, p);
    double result = 1.824829238e6*d2RhoDp2/2.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
                  - 1.824829238e6*dRhoDp*dRhoDp/4.0/pow(rho, 3.0/2.0)/pow(Epsilon*t, 3.0/2.0)
                  - 3.0*1.824829238e6*dRhoDp*DepsilonDp*t/4.0/sqrt(rho)/pow(Epsilon*t, 5.0/2.0)
                  - 3.0*1.824829238e6*dRhoDp*DepsilonDp*t/4.0/sqrt(rho)/pow(Epsilon*t, 5.0/2.0)
                  - 3.0*1.824829238e6*sqrt(rho)*D2epsilonDp2*t/2.0/pow(Epsilon*t, 5.0/2.0)
                  + 5.0*3.0*1.824829238e6*sqrt(rho)*DepsilonDp*t*DepsilonDp*t/4.0/pow(Epsilon*t, 7.0/2.0);
    return result;
}

double d3AgammaDt3(double t, double p) {
    double d2AgammaDt2plus  = d2AgammaDt2(t*(1.0+EPS), p);
    double d2AgammaDt2minus = d2AgammaDt2(t*(1.0-EPS), p);
    return (d2AgammaDt2plus-d2AgammaDt2minus)/2.0/(t*EPS);
}

double d3AgammaDt2Dp(double t, double p) {
    double d2AgammaDt2plus  = d2AgammaDt2(t, p*(1.0+EPS));
    double d2AgammaDt2minus = d2AgammaDt2(t, p*(1.0-EPS));
    return (d2AgammaDt2plus-d2AgammaDt2minus)/2.0/(p*EPS);
}

double d3AgammaDtDp2(double t, double p) {
    double d2AgammaDp2plus  = d2AgammaDp2(t*(1.0+EPS), p);
    double d2AgammaDp2minus = d2AgammaDp2(t*(1.0-EPS), p);
    return (d2AgammaDp2plus-d2AgammaDp2minus)/2.0/(t*EPS);
}

double d3AgammaDp3(double t, double p) {
    double d2AgammaDp2plus  = d2AgammaDp2(t, p*(1.0+EPS));
    double d2AgammaDp2minus = d2AgammaDp2(t, p*(1.0-EPS));
    return (d2AgammaDp2plus-d2AgammaDp2minus)/2.0/(p*EPS);
}

double Bgamma(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    return 50.29158649e8*sqrt(rho)/sqrt(Epsilon*t);
}

double dBgammaDt(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    return 50.29158649e8*dRhoDt/2.0/sqrt(rho)/sqrt(Epsilon*t) - 50.29158649e8*(DepsilonDt*t+Epsilon)*sqrt(rho)/2.0/pow(Epsilon*t, 3.0/2.0);
}

double dBgammaDp(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    return 50.29158649e8*dRhoDp/2.0/sqrt(rho)/sqrt(Epsilon*t) - 50.29158649e8*sqrt(rho)*DepsilonDp*t/2.0/pow(Epsilon*t, 3.0/2.0);
}

double d2BgammaDt2(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    double D2epsilonDt2 = d2EpsilonDt2(t, p);
    double d2RhoDt2 = loadDensityProperties(mask_d2rhodt2, t, p);
    double result = 50.29158649e8*d2RhoDt2/2.0/sqrt(rho)/sqrt(Epsilon*t)
    - 50.29158649e8*dRhoDt*dRhoDt/4.0/pow(rho, 3.0/2.0)/sqrt(Epsilon*t)
    - 50.29158649e8*dRhoDt*(DepsilonDt*t+Epsilon)/4.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
    - 50.29158649e8*(D2epsilonDt2*t+2.0*DepsilonDt)*sqrt(rho)/2.0/pow(Epsilon*t, 3.0/2.0)
    - 50.29158649e8*(DepsilonDt*t+Epsilon)*dRhoDt/sqrt(rho)/4.0/pow(Epsilon*t, 3.0/2.0)
    + 3.0*50.29158649e8*(DepsilonDt*t+Epsilon)*sqrt(rho)*(DepsilonDt*t+Epsilon)/4.0/pow(Epsilon*t, 5.0/2.0);
    return result;
}

double d2BgammaDtDp(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDt = dEpsilonDt(t, p);
    double dRhoDt = loadDensityProperties(mask_drhodt, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    double D2epsilonDtDp = d2EpsilonDtDp(t, p);
    double d2RhoDtDp = loadDensityProperties(mask_d2rhodtdp, t, p);
    double result = 50.29158649e8*d2RhoDtDp/2.0/sqrt(rho)/sqrt(Epsilon*t)
                  - 50.29158649e8*dRhoDt*dRhoDp/4.0/pow(rho, 3.0/2.0)/sqrt(Epsilon*t)
                  - 50.29158649e8*dRhoDt*DepsilonDp*t/4.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
                  - 50.29158649e8*(D2epsilonDtDp*t+DepsilonDp)*sqrt(rho)/2.0/pow(Epsilon*t, 3.0/2.0)
                  - 50.29158649e8*(DepsilonDt*t+Epsilon)*dRhoDp/4.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
                  + 3.0*50.29158649e8*(DepsilonDt*t+Epsilon)*sqrt(rho)*DepsilonDp*t/4.0/pow(Epsilon*t, 5.0/2.0);
    return result;
}

double d2BgammaDp2(double t, double p) {
    double Epsilon = epsilon(t, p);
    double rho = loadDensityProperties(mask_rho, t, p);
    double DepsilonDp = dEpsilonDp(t, p);
    double dRhoDp = loadDensityProperties(mask_drhodp, t, p);
    double D2epsilonDp2 = d2EpsilonDp2(t, p);
    double d2RhoDp2 = loadDensityProperties(mask_d2rhodp2, t, p);
    double result = 50.29158649e8*d2RhoDp2/2.0/sqrt(rho)/sqrt(Epsilon*t)
                  - 50.29158649e8*dRhoDp*dRhoDp/4.0/pow(rho, 3.0/2.0)/sqrt(Epsilon*t)
                  - 50.29158649e8*dRhoDp*DepsilonDp*t/4.0/sqrt(rho)/pow(Epsilon*t, 3.0/2.0)
                  - 50.29158649e8*DepsilonDp*t*dRhoDp/sqrt(rho)/4.0/pow(Epsilon*t, 3.0/2.0)
                  - 50.29158649e8*sqrt(rho)*D2epsilonDp2*t/2.0/pow(Epsilon*t, 3.0/2.0)
                  + 3.0*50.29158649e8*sqrt(rho)*DepsilonDp*t*DepsilonDp*t/4.0/pow(Epsilon*t, 5.0/2.0);
    return result;
}

double d3BgammaDt3(double t, double p) {
    double d2BgammaDt2plus  = d2BgammaDt2(t*(1.0+EPS), p);
    double d2BgammaDt2minus = d2BgammaDt2(t*(1.0-EPS), p);
    return (d2BgammaDt2plus-d2BgammaDt2minus)/2.0/(t*EPS);
}

double d3BgammaDt2Dp(double t, double p) {
    double d2BgammaDt2plus  = d2BgammaDt2(t, p*(1.0+EPS));
    double d2BgammaDt2minus = d2BgammaDt2(t, p*(1.0-EPS));
    return (d2BgammaDt2plus-d2BgammaDt2minus)/2.0/(p*EPS);
}

double d3BgammaDtDp2(double t, double p) {
    double d2BgammaDp2plus  = d2BgammaDp2(t*(1.0+EPS), p);
    double d2BgammaDp2minus = d2BgammaDp2(t*(1.0-EPS), p);
    return (d2BgammaDp2plus-d2BgammaDp2minus)/2.0/(t*EPS);
}

double d3BgammaDp3(double t, double p) {
    double d2BgammaDp2plus  = d2BgammaDp2(t, p*(1.0+EPS));
    double d2BgammaDp2minus = d2BgammaDp2(t, p*(1.0-EPS));
    return (d2BgammaDp2plus-d2BgammaDp2minus)/2.0/(p*EPS);
}

double AsubG(double t, double p) {
    return -2.0*log(10.0)*R*t*Agamma(t, p);
}

double AsubH(double t, double p) {
    double dAGoverTdT = -2.0*log(10.0)*R*dAgammaDt(t, p);
    return -dAGoverTdT*t*t;
}

double AsubJ(double t, double p) {
    double  dAGoverTdT  = -2.0*log(10.0)*R*dAgammaDt(t, p);
    double d2AGoverTdT2 = -2.0*log(10.0)*R*d2AgammaDt2(t, p);
    return -d2AGoverTdT2*t*t - 2.0*dAGoverTdT*t;
}

double AsubV(double t, double p) {
    return -2.0*log(10.0)*R*t*dAgammaDp(t, p);
}

double AsubKappa(double t, double p) {
    return -2.0*log(10.0)*R*t*d2AgammaDp2(t, p);
}

double AsubEx(double t, double p) {
    return -2.0*log(10.0)*R*dAgammaDp(t, p) - 2.0*log(10.0)*R*t*d2AgammaDtDp(t, p);
}

double BsubG(double t, double p) {
    return -2.0*log(10.0)*R*t*Bgamma(t, p);
}

double BsubH(double t, double p) {
    return 2.0*log(10.0)*R*t*t*dBgammaDt(t, p);
}

double BsubJ(double t, double p) {
    return 4.0*log(10.0)*R*t*dBgammaDt(t, p) + 2.0*log(10.0)*R*t*t*d2BgammaDt2(t, p);
}

double BsubV(double t, double p) {
    return -2.0*log(10.0)*R*t*dBgammaDp(t, p);
}

double BsubKappa(double t, double p) {
    return -2.0*log(10.0)*R*t*d2BgammaDp2(t, p);
}

double BsubEx(double t, double p) {
    return -2.0*log(10.0)*R*dBgammaDp(t, p) - 2.0*log(10.0)*R*t*d2BgammaDtDp(t, p);
}

double SWIM_getRho(double t, double p);
double SWIM_getDrhoDt(double t, double p);
double SWIM_getDrhoDp(double t, double p);
double SWIM_getD2rhoDt2(double t, double p);
double SWIM_getD2rhoDtDp(double t, double p);
double SWIM_getD2rhoDp2(double t, double p);

// Shock et al., 1992, J. Chem. Soc. Faraday Trans. 88(6) 803-826
static const double agP   = -2.037662;
static const double agPP  =  5.747000e-3;
static const double agPPP = -6.557892e-6;
static const double bgP   =  6.107361;
static const double bgPP  = -1.074337e-2;
static const double bgPPP =  1.268348e-5;
static const double ag1   =  3.66666e-16;
static const double ag2   = -1.504956e-10;
static const double ag3   =  5.01799e-14;

static double psat(double tc) {
    double result = 0.0;
    result +=  1.44021565e+00;
    result += -2.75944904e-02*tc;
    result +=  3.50602876e-04*tc*tc;
    result += -2.44834016e-06*tc*tc*tc;
    result +=  1.57085668e-08*tc*tc*tc*tc;
    return result;
}

static double g_low_density_limit = 0.35;

double get_gSolvent_low_density_limit(void) {
    return g_low_density_limit;
}

void set_gSolvent_low_density_limit(double value) {
    g_low_density_limit = value;
}

double gSolvent(double t, double p) {
    double rho = SWIM_getRho(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double aG = agP + agPP*tc + agPPP*tc*tc;
        double bG = bgP + bgPP*tc + bgPPP*tc*tc;

        double f = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            f += (pow((tc-155.0)/300.0, 4.8) + ag1*pow((tc-155.0)/300.0, 16.0))
               * (ag2*pow(1000.0-p, 3.0) + ag3*pow(1000.0-p, 4.0));
        }

        return aG * pow(1.0-rho, bG) - f;
    }
}

double DgSolventDt(double t, double p) {
    double rho    = SWIM_getRho(t, p);
    double DrhoDt = SWIM_getDrhoDt(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double  aG   = agP + agPP*tc +     agPPP*tc*tc;
        double daGdt =       agPP    + 2.0*agPPP*tc;
        double  bG   = bgP + bgPP*tc +     bgPPP*tc*tc;
        double dbGdt =       bgPP    + 2.0*bgPPP*tc;

        double g = aG * pow(1.0-rho, bG);
        double dgdt = daGdt*pow(1.0-rho, bG) + g*(dbGdt*log(1.0-rho) - bG*DrhoDt/(1.0-rho));

        double dfdt = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            // Note that Sverjensky et al. (2014) has an entirely independent function for this derivative
            // which I have not adopted, prefering internal consistency to accuracy
            dfdt += ((4.8/300.0)*pow((tc-155.0)/300.0, 3.8) + ag1*(16.0/300.0)*pow((tc-155.0)/300.0, 15.0))
                  * (ag2*pow(1000.0-p, 3.0) + ag3*pow(1000.0-p, 4.0));
        }

        return dgdt - dfdt;
    }
}

double DgSolventDp(double t, double p) {
    double rho    = SWIM_getRho(t, p);
    double DrhoDp = SWIM_getDrhoDp(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double aG = agP + agPP*tc + agPPP*tc*tc;
        double bG = bgP + bgPP*tc + bgPPP*tc*tc;

       double dgdp = -aG*bG*DrhoDp*pow(1.0-rho, bG-1.0);

        double dfdp = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            dfdp += (pow((tc-155.0)/300.0, 4.8) + ag1*pow((tc-155.0)/300.0, 16.0))
                  * (-3.0*ag2*pow(1000.0-p, 2.0) - 4.0*ag3*pow(1000.0-p, 3.0));
        }

        return dgdp - dfdp;
    }
}

double D2gSolventDt2(double t, double p) {
    double   rho    = SWIM_getRho(t, p);
    double  DrhoDt  = SWIM_getDrhoDt(t, p);
    double D2rhoDt2 = SWIM_getD2rhoDt2(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double   aG    = agP + agPP*tc +     agPPP*tc*tc;
        double  daGdt  =       agPP    + 2.0*agPPP*tc;
        double d2aGdt2 =                 2.0*agPPP;
        double   bG    = bgP + bgPP*tc +     bgPPP*tc*tc;
        double  dbGdt  =       bgPP    + 2.0*bgPPP*tc;
        double d2bGdt2 =                 2.0*bgPPP;

        double g = aG * pow(1.0-rho, bG);
        double d2gdt2 = d2aGdt2*pow(1.0-rho, bG)
                      + 2.0*daGdt*pow(1.0-rho, bG)*(dbGdt*log(1.0-rho) - bG*DrhoDt/(1.0-rho))
                      + g*pow(dbGdt*log(1.0-rho) - bG*DrhoDt/(1.0-rho), 2.0)
                      + g*(d2bGdt2*log(1.0-rho) - 2.0*dbGdt*DrhoDt/(1.0-rho) -bG*pow(DrhoDt/(1.0-rho), 2.0) - bG*D2rhoDt2/(1.0-rho));

        double d2fdt2 = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            d2fdt2 += ((3.8/300.0)*(4.8/300.0)*pow((tc-155.0)/300.0, 2.8) + ag1*(15.0/300.0)*(16.0/300.0)*pow((tc-155.0)/300.0, 14.0))
                    * (ag2*pow(1000.0-p, 3.0) + ag3*pow(1000.0-p, 4.0));
        }

        return d2gdt2 - d2fdt2;
    }
}

double D2gSolventDtDp(double t, double p) {
    double   rho     = SWIM_getRho(t, p);
    double  DrhoDt   = SWIM_getDrhoDt(t, p);
    double  DrhoDp   = SWIM_getDrhoDp(t, p);
    double D2rhoDtDp = SWIM_getD2rhoDtDp(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double  aG   = agP + agPP*tc +     agPPP*tc*tc;
        double daGdt =       agPP    + 2.0*agPPP*tc;
        double  bG   = bgP + bgPP*tc +     bgPPP*tc*tc;
        double dbGdt =       bgPP    + 2.0*bgPPP*tc;

        double g = aG * pow(1.0-rho, bG);
        double d2gdtdp = -bG*daGdt*DrhoDp*pow(1.0-rho, bG-1.0)
                       + g*(-dbGdt*DrhoDp/(1.0-rho) - bG*DrhoDt*DrhoDp/pow(1.0-rho, 2.0) - bG*D2rhoDtDp/(1.0-rho))
                       - aG*bG*DrhoDp*pow(1.0-rho, bG-1.0)*(dbGdt*log(1.0-rho) - bG*DrhoDt/(1.0-rho));

        double d2fdtdp = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            d2fdtdp += ((4.8/300.0)*pow((tc-155.0)/300.0, 3.8) + ag1*(16.0/300.0)*pow((tc-155.0)/300.0, 15.0))
                     * (-3.0*ag2*pow(1000.0-p, 2.0) - 4.0*ag3*pow(1000.0-p, 3.0));
        }

        return d2gdtdp - d2fdtdp;
    }
}

double D2gSolventDp2(double t, double p) {
    double   rho    = SWIM_getRho(t, p);
    double  DrhoDp  = SWIM_getDrhoDp(t, p);
    double D2rhoDp2 = SWIM_getD2rhoDp2(t, p);
    double tc = t - 273.15;

    if      (rho >= 1.0) return 0.0;
    else if ((p >= 500.0 ) && (rho <=   g_low_density_limit)) return 0.0;
    else if ((p <  500.0 ) && (p   >= 220.46) && (tc >= 373.917)) return 0.0;
    else if ((p <  220.46) && (p   >=   1.00) && (p > psat(tc))) return 0.0;
    else {
        double aG = agP + agPP*tc + agPPP*tc*tc;
        double bG = bgP + bgPP*tc + bgPPP*tc*tc;

        double d2gdp2 = aG*bG*(bG-1.0)*pow(1.0-rho, bG-2.0)*DrhoDp*DrhoDp
                      - aG*bG*pow(1.0-rho, bG-1.0)*D2rhoDp2;

        double d2fdp2 = 0.0;
        if ((p <= 1000) && (tc >= 155.0) && (tc <= 355.0)) {
            d2fdp2 += (pow((tc-155.0)/300.0, 4.8) + ag1*pow((tc-155.0)/300.0, 16.0))
                    * (6.0*ag2*(1000.0-p) + 12.0*ag3*pow(1000.0-p, 2.0));
        }

        return d2gdp2 - d2fdp2;
    }
}

double D3gSolventDt3(double t, double p) {
    double D2gSolventDt2plus  = D2gSolventDt2(t*(1.0+EPS), p);
    double D2gSolventDt2minus = D2gSolventDt2(t*(1.0-EPS), p);
    return (D2gSolventDt2plus-D2gSolventDt2minus)/2.0/(t*EPS);
}

double D3gSolventDt2Dp(double t, double p) {
    double D2gSolventDt2plus  = D2gSolventDt2(t, p*(1.0+EPS));
    double D2gSolventDt2minus = D2gSolventDt2(t, p*(1.0-EPS));
    return (D2gSolventDt2plus-D2gSolventDt2minus)/2.0/(p*EPS);
}

double D3gSolventDtDp2(double t, double p) {
    double D2gSolventDp2plus  = D2gSolventDp2(t*(1.0+EPS), p);
    double D2gSolventDp2minus = D2gSolventDp2(t*(1.0-EPS), p);
    return (D2gSolventDp2plus-D2gSolventDp2minus)/2.0/(t*EPS);
}

double D3gSolventDp3(double t, double p) {
    double D2gSolventDp2plus  = D2gSolventDp2(t, p*(1.0+EPS));
    double D2gSolventDp2minus = D2gSolventDp2(t, p*(1.0-EPS));
    return (D2gSolventDp2plus-D2gSolventDp2minus)/2.0/(p*EPS);
}

#define EPS2 1.0e-3

double D4gSolventDt4(double t, double p) {
    double result  = -(1.0/12.0)*D2gSolventDt2(t*(1.0+2.0*EPS2), p);
           result +=  (4.0/ 3.0)*D2gSolventDt2(t*(1.0+    EPS2), p);
           result += -(5.0/ 2.0)*D2gSolventDt2(t,                p);
           result +=  (4.0/ 3.0)*D2gSolventDt2(t*(1.0-    EPS2), p);
           result += -(1.0/12.0)*D2gSolventDt2(t*(1.0-2.0*EPS2), p);
    return  result;
}
