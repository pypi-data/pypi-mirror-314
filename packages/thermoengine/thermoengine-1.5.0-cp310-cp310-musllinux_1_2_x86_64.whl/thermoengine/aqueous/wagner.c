
#include  "wagner.h"

#include <float.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include  "steam.h"
#include  "region4.h"
#include  "backwards.h"
#include  "b23.h"
#include  "derivs.h"
#include  "zeroin.h"
#include  "region3.h"
#include  "solver2.h"
#include  "steam_ph.h"
#include  "steam_ps.h"
#include  "steam_Ts.h"
#include  "steam_pT.h"
#include  "steam_pv.h"
#include  "steam_Tx.h"
#include  "region1.h"
#include  "viscosity.h"
#include  "thcond.h"
#include  "surftens.h"

static const double MolesPerKg = 55.508435;

double WagnerEtAl2002_getGibbsFreeEnergy(double t, double p) {
    SteamState S = freesteam_set_pT(p*1.0e5, t);
    double result = (freesteam_h(S) - t*freesteam_s(S))/MolesPerKg;
    return result;
}

double WagnerEtAl2002_getEnthalpy(double t, double p) {
    SteamState S = freesteam_set_pT(p*1.0e5, t);
    double result = freesteam_h(S)/MolesPerKg;
    return result;
}

double WagnerEtAl2002_getEntropy(double t, double p) {
    SteamState S = freesteam_set_pT(p*1.0e5, t);
    double result = freesteam_s(S)/MolesPerKg;
    return result;
}

double WagnerEtAl2002_getHeatCapacity(double t, double p) {
    SteamState S = freesteam_set_pT(p*1.0e5, t);
    double result = freesteam_cp(S)/MolesPerKg;
    return result;
}

double WagnerEtAl2002_getDcpDt(double t, double p) {
    static double EPS = -1.0;
    if (EPS == -1.0) EPS = sqrt(DBL_EPSILON);
    SteamState S = freesteam_set_pT(p*1.0e5, t*(1.0+EPS));
    double result  = freesteam_cp(S);
    S = freesteam_set_pT(p*1.0e5, t*(1.0-EPS));
    result -= freesteam_cp(S);
    result *= 1.0/t/2.0/EPS/MolesPerKg; // e5
    return  result;
}

double WagnerEtAl2002_getVolume(double t, double p) {
    SteamState S = freesteam_set_pT(p*1.0e5, t);
    double result = 1.0e5*freesteam_v(S)/MolesPerKg;
    return  result;
}

double WagnerEtAl2002_getDvDt(double t, double p) {
    static double EPS = -1.0;
    if (EPS == -1.0) EPS = sqrt(DBL_EPSILON);
    SteamState S = freesteam_set_pT(p*1.0e5, t*(1.0+EPS));
    double result  = freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t*(1.0-EPS));
    result -= freesteam_v(S);
    result *= 1.0e5/t/2.0/EPS/MolesPerKg;
    return  result;
}

double WagnerEtAl2002_getDvDp(double t, double p) {
    static double EPS = -1.0;
    if (EPS == -1.0) EPS = sqrt(DBL_EPSILON);
    SteamState S = freesteam_set_pT(p*1.0e5*(1.0+EPS), t);
    double result  = freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS), t);
    result -= freesteam_v(S);
    result *= 1.0e5/p/2.0/EPS/MolesPerKg;
    return  result;
}

double WagnerEtAl2002_getD2vDt2(double t, double p) {
    static double EPS2 = -1.0;
    if (EPS2 == -1.0) EPS2 = sqrt(sqrt(DBL_EPSILON));
    SteamState S = freesteam_set_pT(p*1.0e5, t*(1.0+2.0*EPS2));
    double result  = -(1.0/12.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t*(1.0+EPS2));
    result +=  (4.0/3.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t);
    result += -(5.0/2.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t*(1.0-EPS2));
    result +=  (4.0/3.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t*(1.0-2.0*EPS2));
    result += -(1.0/12.0)*freesteam_v(S);
    result *= 1.0e5/t/t/EPS2/EPS2/MolesPerKg;
    return  result;
}

double WagnerEtAl2002_getD2vDtDp(double t, double p) {
    static double EPS2 = -1.0;
    if (EPS2 == -1.0) EPS2 = sqrt(sqrt(DBL_EPSILON));
    SteamState S = freesteam_set_pT(p*1.0e5*(1.0+2.0*EPS2), t*(1.0+2.0*EPS2));
    double result  = -44.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0+2.0*EPS2), t*(1.0-2.0*EPS2));
    result +=  44.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-2.0*EPS2), t*(1.0+2.0*EPS2));
    result +=  44.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-2.0*EPS2), t*(1.0-2.0*EPS2));
    result += -44.0*freesteam_v(S);

    S = freesteam_set_pT(p*1.0e5*(1.0+EPS2), t*(1.0+EPS2));
    result +=  74.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0+EPS2), t*(1.0-EPS2));
    result += -74.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS2), t*(1.0+EPS2));
    result += -74.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS2), t*(1.0-EPS2));
    result +=  74.0*freesteam_v(S);

    S = freesteam_set_pT(p*1.0e5*(1.0+2.0*EPS2), t*(1.0+EPS2));
    result +=  63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0+EPS2), t*(1.0+2.0*EPS2));
    result +=  63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-2.0*EPS2), t*(1.0-EPS2));
    result +=  63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS2), t*(1.0-2.0*EPS2));
    result +=  63.0*freesteam_v(S);

    S = freesteam_set_pT(p*1.0e5*(1.0+EPS2), t*(1.0-2.0*EPS2));
    result += -63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0+2.0*EPS2), t*(1.0-EPS2));
    result += -63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-2.0*EPS2), t*(1.0+EPS2));
    result += -63.0*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS2), t*(1.0+2.0*EPS2));
    result += -63.0*freesteam_v(S);

    result *= 1.0e5/600.0/p/EPS2/t/EPS2/MolesPerKg;
    return  result;
}

double WagnerEtAl2002_getD2vDp2(double t, double p) {
    static double EPS2 = -1.0;
    if (EPS2 == -1.0) EPS2 = sqrt(sqrt(DBL_EPSILON));
    SteamState S = freesteam_set_pT(p*1.0e5*(1.0+2.0*EPS2), t);
    double result  = -(1.0/12.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0+EPS2), t);
    result +=  (4.0/3.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5, t);
    result += -(5.0/2.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-EPS2), t);
    result +=  (4.0/3.0)*freesteam_v(S);
    S = freesteam_set_pT(p*1.0e5*(1.0-2.0*EPS2), t);
    result += -(1.0/12.0)*freesteam_v(S);
    result *= 1.0e5/p/p/EPS2/EPS2/MolesPerKg;
    return  result;
}
