"""Simulation experiment of the study Coskun2018."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.tirzepatide import MODEL
from pkdb_models.models.tirzepatide.experiments.base_experiment import (
    TirzepatideSimulationExperiment,
)


class Coskun2018(TirzepatideSimulationExperiment):
    """Simulation experiment of Coskun2018.

    Phase 1 study (NCT02759107) of subcutaneous tirzepatide. Single ascending
    doses (SAD, 0.25-8 mg) and four weekly doses (MAD, days 1, 8, 15 and 22,
    fixed or titrated 5/5/8/10 mg) in healthy, mostly Asian men, and four
    weekly doses in people with type 2 diabetes (POC, fixed or titrated to 10
    and 15 mg). The profiles of MAD and POC follow the dose of day 22 (Fig1_FDA,
    Fig2_FDA), mean and SD; the counts are the n of the dose groups (Table 2,
    TabS2). Fasting is not reported.
    """

    bodyweights: ClassVar[dict[str, float]] = {
        "SAD": 71.9,  # kg
        "MAD": 71.1,  # kg
        "POC": 86.0,  # kg
    }

    # the weekly doses [mg] of the arms by the dose of the data (the last dose)
    regimens: ClassVar[dict[str, dict[float, list[float]]]] = {
        "SAD": {dose: [dose] for dose in [0.25, 0.5, 1, 2.5, 5, 8]},
        "MAD": {
            0.5: [0.5] * 4,
            1.5: [1.5] * 4,
            4.5: [4.5] * 4,
            10: [5, 5, 8, 10],
        },
        "POC": {
            0.5: [0.5] * 4,
            5: [5] * 4,
            10: [5, 5, 10, 10],
            15: [5, 5, 10, 15],
        },
    }
    figure_ids: ClassVar[dict[str, str]] = {
        "SAD": "Fig1_EMA",
        "MAD": "Fig1_FDA",
        "POC": "Fig2_FDA",
    }

    colors: ClassVar[dict[float, str]] = {
        0.25: "crimson",
        0.5: "goldenrod",
        1: "limegreen",
        2.5: "steelblue",
        5: "indigo",
        8: "saddlebrown",
        1.5: "darkorange",
        4.5: "purple",
        10: "deepskyblue",
        15: "darkred",
    }

    def sim_key(self, cohort: str, dose: float) -> str:
        """Get the key of the simulation of an arm."""
        return self.to_sid(f"sc_tir_{cohort.lower()}_{dose}")

    def dset_key(self, cohort: str, dose: float) -> str:
        """Get the key of the dataset of an arm."""
        return self.to_sid(f"tirzepatide_{cohort.lower()}{dose}".replace(".", "_"))

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}

        for fig_id in self.figure_ids.values():
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                if label.startswith("tirzepatide_"):
                    dset = DataSet.from_df(df_label, self.ureg)
                    dset.unit_conversion("mean", 1 / self.Mr.tir)
                    dsets[self.to_sid(label)] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for cohort, regimens in self.regimens.items():
            preinit_changes = {
                **self.default_changes(),
                "BW": Q(self.bodyweights[cohort], "kg"),
            }
            for dose, doses in regimens.items():
                # the data end 672 hr after a single dose and 840 hr after the
                # last of the weekly doses
                simulations[self.sim_key(cohort, dose)] = self.weekly_doses(
                    doses=doses,
                    preinit_changes=preinit_changes,
                    follow_up=700 if cohort == "SAD" else 870,
                    step=0.5,
                )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for cohort, regimens in self.regimens.items():
            for dose in regimens:
                sim_key = self.sim_key(cohort, dose)
                mappings[f"fm_{sim_key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.dset_key(cohort, dose),
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_{sim_key}",
                        xid="time",
                        yid="[Cve_tir]",
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.SC,
                        application_form=ApplicationForm.SUBCUTANEOUS,
                        dosing=Dosing.SINGLE if cohort == "SAD" else Dosing.MULTIPLE,
                        health=Health.T2DM if cohort == "POC" else Health.HEALTHY,
                        fasting=Fasting.NR,
                        coadministration=Coadministration.NONE,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = []

        for cohort, regimens in self.regimens.items():
            fig = Figure(
                experiment=self,
                sid=self.to_sid(self.figure_ids[cohort]),
                num_rows=1,
                name=f"{self.__class__.__name__} ({cohort})",
            )
            # the weekly doses before the last one (time 0) are shown
            plots = fig.create_plots(
                xaxis=Axis(
                    self.label_time,
                    unit=self.unit_time,
                    min=-10 if cohort == "SAD" else -520,
                    max=700 if cohort == "SAD" else 870,
                ),
                legend=True,
            )
            plots[0].set_yaxis(self.label_tir, unit=self.unit_tir)

            for dose, doses in regimens.items():
                if len(doses) == 1:
                    regimen = f"{doses[0]:g}"
                elif len(set(doses)) == 1:
                    regimen = f"{len(doses)} x {doses[0]:g}"
                else:
                    regimen = "/".join(f"{d:g}" for d in doses)
                plots[0].add_data(
                    task=f"task_{self.sim_key(cohort, dose)}",
                    xid="time",
                    yid="[Cve_tir]",
                    label=f"Sim {regimen} mg SC",
                    color=self.colors[dose],
                )
                plots[0].add_data(
                    dataset=self.dset_key(cohort, dose),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {dose:g} mg",
                    color=self.colors[dose],
                )

            figures.append(fig)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(Coskun2018, output_dir=Coskun2018.__name__)
