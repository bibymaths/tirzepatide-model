"""Sensitivity analysis of the tirzepatide model.

The outputs are the pharmacokinetic parameters of tirzepatide in plasma after a
single subcutaneous dose (the non-compartmental analysis of `pkpdutils`, an
extravascular dose, `Route.ORAL` of pkpdutils, which has no subcutaneous route)
and the AUC and the maximum of its metabolites in plasma. The parameters are
the parameters of the model with bounds of +-15 % around their value. The
analyses are run as a script, the local analysis by default:

    python -m pkdb_models.models.tirzepatide.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.tirzepatide.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the groups of the
renal function, leaves out `KI__f_renal_function`. The environment variable
`PKPDSIM_SENSITIVITY_N` replaces the numbers of samples of the global analyses
for a quick run, see `pkpdsim.sensitivity.sample_size`.

The model without tirzepatide is stationary, so the simulation of a group
starts with the dose. The dose is followed for `END_HR` hours, about twelve
half-lives of tirzepatide (about 135 hr) and ten of its metabolites in plasma
(about 165 hr, they leave their tissue pool slowly), long enough for their
terminal phase.
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Formula, Simulation

from pkdb_models.models.tirzepatide import MODEL, MODEL_PATH
from pkdb_models.models.tirzepatide.experiments.base_experiment import (
    TirzepatideSimulationExperiment,
)
from pkdb_models.models.tirzepatide.fitting.parameters import (
    parameters_pk as fit_parameters,
)

#: subcutaneous dose of tirzepatide of the analysis [mg]
DOSE_TIR = 5
#: the hours after the dose, ten weeks
END_HR = 1680
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal plasma concentration after 5 mg (1e-4 mM), so that the
#: noise of the integrator is not the terminal phase
LLOQ = 1e-8
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of tirzepatide -> unit of the output
PK_OUTPUTS_TIR: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: outputs of the non-compartmental analysis of the metabolites, without a dose
PK_OUTPUTS_TM: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`SCDOSE_tir` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("tir_auc_inf_obs", "tirzepatide AUC∞"),
    SensitivityOutput("tir_cmax", "tirzepatide Cmax"),
    SensitivityOutput("tir_tmax", "tirzepatide tmax"),
    SensitivityOutput("tir_thalf", "tirzepatide Half-life"),
    SensitivityOutput("tir_vz_f", "tirzepatide Vz/F"),
    SensitivityOutput("tir_cl_f", "tirzepatide CL/F"),
    SensitivityOutput("tm_auc_inf_obs", "metabolites AUC∞"),
    SensitivityOutput("tm_cmax", "metabolites Cmax"),
]


def _pk_observables(
    sid: str, outputs: Mapping[str, str], dose: str | None
) -> list[PK | Formula]:
    """Get the non-compartmental analysis of a substance in plasma and its outputs.

    Args:
        sid: the substance, `tir` or `tm`.
        outputs: the outputs of the analysis with their units.
        dose: the dose of the substance, `None` for the metabolites.
    """
    pk_id = f"pk_{sid}"
    return [
        PK(
            pk_id,
            f"[Cve_{sid}]",
            dose=dose,
            route="oral" if dose is not None else None,
            options=NCAOptions(lloq=LLOQ),
            parameters=list(outputs),
        ),
        *(
            Formula(
                f"{sid}_{key}",
                f"{pk_id}.{key} / at(Mr_{sid}, 0)"
                if key in PK_PER_DOSE_MASS
                else f"{pk_id}.{key}",
                unit=unit,
            )
            for key, unit in outputs.items()
        ),
    ]


#: the observables of a simulation, the outputs with their units; the ids of
#: the analyses (`pk_tir`, `pk_tm`) are no species of the model
OBSERVABLES = [
    *_pk_observables("tir", PK_OUTPUTS_TIR, dose="SCDOSE_tir"),
    *_pk_observables("tm", PK_OUTPUTS_TM, dose=None),
]

#: the output times [hr]: every 0.1 hr in the first two days after the dose
#: (absorption and maximum), every 2 hr after them
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 48, 481),
                np.linspace(48, END_HR, (END_HR - 48) // 2 + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single subcutaneous dose at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={**changes, "SCDOSE_tir": Q(DOSE_TIR, "mg")},
    )


#: the groups the analyses are run for: the classes of the renal function of
#: the simulation experiments (normal renal function is the control); the
#: renal function changes only the metabolites, tirzepatide is not excreted
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup(
        uid,
        name,
        sensitivity_simulation(
            {"KI__f_renal_function": TirzepatideSimulationExperiment.renal_map[name]}
        ),
        TirzepatideSimulationExperiment.renal_colors[name],
    )
    for uid, name in [
        ("control", "Normal renal function"),
        ("mildRenal", "Mild renal impairment"),
        ("moderateRenal", "Moderate renal impairment"),
        ("severeRenal", "Severe renal impairment"),
        ("endStageRenal", "End stage renal disease"),
    ]
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # molecular weights
            "Mr_tir",
            "Mr_tm",
            # reference values and conversions
            "BW_ref",
            "conversion_min_per_day",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters
            "SCDOSE_tir",
            "IVDOSE_tir",
            "ti_tir",
            "Ri_tir",
            # the injection into the depot within seconds, no kinetics
            "Ksc_injection_tir",
            # unused volumes
            "Vurine",
            "Vfeces",
            "GU__Vchain",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in ["KI__f_renal_function"]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
