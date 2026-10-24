"""Parameters to optimize in the tirzepatide fits."""

from sbmlsim.fit import FitParameter

#: the pharmacokinetics of tirzepatide: its subcutaneous absorption, its
#: distribution with albumin into the interstitial space and its cleavage. The
#: bioavailability `Fsc_tir` is not fitted: without intravenous data it only
#: shifts the clearance and the volumes against each other, it is the absolute
#: bioavailability of 80 % (label). Neither is the exchange flow of the tissue
#: distribution `ftissue_tir`, which the subcutaneous data only bound from
#: below (fit PK_20261017_142031__74569: flat above 0.1 l/min), it is 0.15 l/min
parameters_pk_tir: list[FitParameter] = [
    # tmax 24-48 hr, about 1.4e-3/min (half-life of the depot 8 hr); the start
    # values are those of fit PK_20261019_094858__a49bf
    FitParameter(
        pid="Ksc_tir",
        start_value=1.44e-3,
        lower_bound=2e-4,
        upper_bound=1e-2,
        unit="1/min",
    ),
    # CL = F * CL/F = 0.8 * (0.03-0.062 l/hr) = 4e-4 to 8e-4 l/min
    FitParameter(
        pid="TIR2TM_k",
        start_value=6.34e-4,
        lower_bound=2e-4,
        upper_bound=3e-3,
        unit="l/min",
    ),
    # Vss = F * Vss/F = 0.8 * 9-10 l, 2-3 l of it in the tissues
    FitParameter(
        pid="Kp_tir",
        start_value=0.036,
        lower_bound=0.005,
        upper_bound=0.5,
        unit="dimensionless",
    ),
]

#: the distribution and the excretion of the metabolites (Martin2024: 66 % in
#: the urine, 33 % in the feces, tirzepatide about 80 % of the radioactivity in
#: plasma): the volume of the slow tissue pool, the renal excretion relative to
#: the GFR and the biliary excretion. The start values are those of fit
#: PK_20261019_094858__a49bf. The exchange flow of the pool `ftissue_tm` is not
#: fitted, the data bound it from below only (the profile of that fit is flat
#: above 0.02 l/min), it is 0.036 l/min. The intestinal transit into the feces
#: `GU__TMEXC_k` is not fitted, the cumulative recovery does not identify it
#: (fit PK_20261017_142031__74569: flat from 12 hr to 5 days), it is the whole
#: gut transit of about 2 days
parameters_pk_tm: list[FitParameter] = [
    # the volume of the pool, Kp_tm * the tissue volume (about 60 l)
    FitParameter(
        pid="Kp_tm",
        start_value=0.13,
        lower_bound=0.01,
        upper_bound=10,
        unit="dimensionless",
    ),
    # renal clearance about 0.012 * 101 ml/min = 0.07 l/hr
    FitParameter(
        pid="KI__TMEX_f",
        start_value=0.012,
        lower_bound=1e-4,
        upper_bound=1,
        unit="dimensionless",
    ),
    # biliary clearance about 3.7e-4/min * 1.9 l (liver) = 0.04 l/hr
    FitParameter(
        pid="LI__TMBEX_k",
        start_value=3.7e-4,
        lower_bound=1e-6,
        upper_bound=1e-2,
        unit="1/min",
    ),
]

#: the parameters of the pharmacokinetic fit
parameters_pk: list[FitParameter] = parameters_pk_tir + parameters_pk_tm
