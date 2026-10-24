"""Parameter fit problems for tirzepatide.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the training data a fit is evaluated on but
not fitted to. The metadata of a mapping describes its curve, what a fit does
with the curve is decided here.

The training data are the single doses and the exactly encoded repeated doses
of subjects without an impairment of the kidneys or the liver (healthy, type 2
diabetes, obesity). The validation data has four parts, each a different
question: the doses (`DOSE_VALIDATION`, repeated doses which the single doses
of the training predict), the populations (`POPULATION_VALIDATION`, the
groups with an impaired renal or hepatic function, which the model predicts
without fitted parameters of their own), the interactions
(`INTERACTION_VALIDATION`) and the limitations (`LIMITATION_VALIDATION`, data
of a population, a formulation or a process the model does not describe). The
summaries of data which is fitted one by one are excluded
(`AGGREGATE_MAPPINGS`).
"""

from pkpdsim.fit import mapping_metadata
from pkpdsim.metadata import Coadministration, Health
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.tirzepatide import DATA_PATHS, TIRZEPATIDE_PATH
from pkdb_models.models.tirzepatide.experiments.studies import (
    Coskun2018,
    Feng2023,
    Furihata2022,
    Martin2024,
    Urva2021,
    Urva2022,
)

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    Coskun2018,
    Feng2023,
    Furihata2022,
    Martin2024,
    Urva2021,
    Urva2022,
]

#: the health of the training data: tirzepatide is given to people with type
#: 2 diabetes and obesity, whose kidneys and liver are not impaired
TRAINING_HEALTH: frozenset[Health] = frozenset(
    {Health.HEALTHY, Health.T2DM, Health.OBESE, Health.NR}
)

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {
    # tirzepatide in plasma (LC-MS/MS): its AUC is 109 % of the AUC of the
    # total radioactivity of the same subjects (Table 1, the authors ascribe it
    # to the two assays), impossible for a parent with metabolites, and its
    # Cmax per dose is 1.4 to 2 times that of every other study, while the
    # total radioactivity agrees with them. Fitted, it would push the
    # metabolites in plasma towards zero against the excretion of 99 % of the
    # dose as metabolites
    "Martin2024": {"fm_sc_tir_plasma_tir"},
}

#: the validation of the doses: repeated doses which the single doses of the
#: training predict
DOSE_VALIDATION: NamedMappings = {
    # the proof of concept arms of people with type 2 diabetes, 4 weekly doses
    # up to 15 mg with a titration: their CL/F (0.07-0.09 l/hr) is higher
    # than that of the single and repeated doses of the healthy subjects
    "Coskun2018": {
        "fm_sc_tir_poc_0p5",
        "fm_sc_tir_poc_5",
        "fm_sc_tir_poc_10",
        "fm_sc_tir_poc_15",
    },
}

#: the validation of the populations: the groups with an impaired renal or
#: hepatic function. `filter_health` lets the validation data through for this
#: reason, every other group with an impairment stays out of the selection
POPULATION_VALIDATION: NamedMappings = {
    # mild, moderate and severe renal impairment and end stage renal disease,
    # the renal function from the measured eGFR of the groups
    "Urva2021": {
        "fm_sc_tir_renal_mild",
        "fm_sc_tir_renal_moderate",
        "fm_sc_tir_renal_severe",
        "fm_sc_tir_renal_end",
    },
    # mild, moderate and severe hepatic impairment (Child-Pugh A, B, C)
    "Urva2022": {
        "fm_sc_tir_hepatic_mild",
        "fm_sc_tir_hepatic_moderate",
        "fm_sc_tir_hepatic_severe",
    },
}

#: the validation of the interactions: no study of the model has an
#: interacting drug
INTERACTION_VALIDATION: NamedMappings = {}

#: the validation of the limitations of the model: valid data of a population,
#: a formulation or a process the model does not describe, which would distort
#: the fitted parameters of the processes it does describe
#: (none: the total radioactivity in plasma of Martin2024 is training data
#: since the metabolites distribute into a tissue pool, it identifies `Kp_tm`
#: and `ftissue_tm`)
LIMITATION_VALIDATION: NamedMappings = {}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: a mean of subjects would count the subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the individuals of the hepatic groups: the subjects of the group means,
    # whose points cannot be assigned to an individual reliably
    "Urva2022": {
        f"fm_sc_tir_hepatic_{group}{k}"
        for group, n in [("M", 6), ("MO", 6), ("N", 13), ("S", 7)]
        for k in range(1, n + 1)
    },
}

#: the validation questions by name
QUESTIONS: dict[str, NamedMappings] = {
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "interactions": INTERACTION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}

#: the validation data
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(*(mappings.get(study, set()) for mappings in QUESTIONS.values()))
    for mappings in QUESTIONS.values()
    for study in mappings
}


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_health(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No impaired renal or hepatic function, besides the validation data."""
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    return mapping_metadata(fit_mapping).health in TRAINING_HEALTH


def filter_coadministration(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No coadministered drug, besides the validation data."""
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    return mapping_metadata(fit_mapping).coadministration == Coadministration.NONE


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`), the groups with an impairment (`filter_health`)
    and the arms with a coadministered drug (`filter_coadministration`). The
    outliers are `OUTLIER_MAPPINGS`, the validation data is
    `VALIDATION_MAPPINGS`. Neither kind enters the cost; both are simulated
    and evaluated with the training data, so a report says how the fitted
    parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=TIRZEPATIDE_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
            filter_health,
            filter_coadministration,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data: tirzepatide in plasma and the excretion of its metabolites."""
    return mapping_collections([])


if __name__ == "__main__":
    console.rule(title=f_collections_pk.__name__, align="left", style="white")
    f_collections_pk()
