#ifndef INCLUDE_BORN
#define INCLUDE_BORN

/***********************************************
 * Sverjensky et at. (2014), GCA, 129, 125-145 *
 * Using the SWIM model for water densities    *
 ***********************************************/

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

double get_gSolvent_low_density_limit(void);
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

#endif
