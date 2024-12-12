#ifndef INCLUDE_HOLTEN
#define INCLUDE_HOLTEN

double HoltenEtAl2014_homogeneousIceNucleationTemperatureForPressureInBars(double p);
double HoltenEtAl2014_homogeneousIceNucleationPressureForTemperatureInK(double t);
double HoltenEtAl2014_getGibbsFreeEnergy(double t, double p);
double HoltenEtAl2014_getEnthalpy(double t, double p);
double HoltenEtAl2014_getEntropy(double t, double p);
double HoltenEtAl2014_getHeatCapacity(double t, double p);
double HoltenEtAl2014_getDcpDt(double t, double p);
double HoltenEtAl2014_getVolume(double t, double p);
double HoltenEtAl2014_getDvDt(double t, double p);
double HoltenEtAl2014_getDvDp(double t, double p);
double HoltenEtAl2014_getD2vDt2(double t, double p);
double HoltenEtAl2014_getD2vDtDp(double t, double p);
double HoltenEtAl2014_getD2vDp2(double t, double p);

#endif
