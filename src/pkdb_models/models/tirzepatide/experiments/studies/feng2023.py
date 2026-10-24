"""Simulation experiment of the study Feng2023."""

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


class Feng2023(TirzepatideSimulationExperiment):
    """Simulation experiment of Feng2023.

    Weekly subcutaneous tirzepatide in Chinese adults with type 2 diabetes,
    titrated from 2.5 mg by 2.5 mg every 4 weeks, to 10 mg (cohort 1) or 15 mg
    (cohort 2). The profiles (Fig 1, mean and SD) follow the first dose of
    2.5 mg (week 0) and the fourth dose of 5 mg (week 7), 10 mg (week 15) and
    15 mg (week 23). One subject of cohort 1 stopped after 4 weeks (n = 9 at
    weeks 7 and 15, TabS1). Fasting is not reported.
    """

    bodyweights: ClassVar[dict[str, float]] = {
        "cohort1": 65.0,  # [kg]
        "cohort2": 67.6,  # [kg]
    }
    cohorts: ClassVar[list[str]] = list(bodyweights.keys())
    # the weekly doses [mg] up to the dose of a profile (the last dose)
    doses: ClassVar[dict[float, list[float]]] = {
        2.5: [2.5],
        5: [2.5] * 4 + [5] * 4,
        10: [2.5] * 4 + [5] * 4 + [7.5] * 4 + [10] * 4,
        15: [2.5] * 4 + [5] * 4 + [7.5] * 4 + [10] * 4 + [12.5] * 4 + [15] * 4,
    }
    # the final dose which a cohort does not have
    doses_missing: ClassVar[dict[str, float]] = {
        "cohort1": 15,
        "cohort2": 10,
    }
    colors: ClassVar[dict[float, str]] = {
        2.5: "crimson",
        5: "goldenrod",
        10: "limegreen",
        15: "steelblue",
    }

    def groups(self) -> list[tuple[str, float]]:
        """Get the cohorts and the doses [mg] of their profiles."""
        return [
            (cohort, dose_key)
            for cohort in self.cohorts
            for dose_key in self.doses
            if dose_key != self.doses_missing[cohort]
        ]

    def sim_key(self, cohort: str, dose: float) -> str:
        """Get the key of the simulation of a profile."""
        return self.to_sid(f"sc_tir_{cohort}_{dose}")

    def dset_key(self, cohort: str, dose: float) -> str:
        """Get the key of the dataset of a profile."""
        return self.to_sid(f"tirzepatide_{dose}_{cohort}".replace(".", "_"))

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
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
        for cohort, dose_key in self.groups():
            dose_values = self.doses[dose_key]
            # the data end 840 hr after the last dose, one week after a single dose
            simulations[self.sim_key(cohort, dose_key)] = self.weekly_doses(
                doses=dose_values,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweights[cohort], "kg"),
                },
                follow_up=870 if len(dose_values) > 1 else 7 * 24 + 10,
                step=0.5,
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for cohort, dose_key in self.groups():
            sim_key = self.sim_key(cohort, dose_key)
            mappings[f"fm_{sim_key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.dset_key(cohort, dose_key),
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
                    dosing=Dosing.MULTIPLE
                    if len(self.doses[dose_key]) > 1
                    else Dosing.SINGLE,
                    health=Health.T2DM,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=2,
            name=f"{self.__class__.__name__}",
        )
        # the three weekly doses before the dose of a profile (time 0) are shown
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-520, max=870),
            legend=True,
        )
        for kp, cohort in enumerate(self.cohorts):
            plots[kp].set_title(cohort.replace("cohort", "cohort "))
            plots[kp].set_yaxis(self.label_tir, unit=self.unit_tir)

        for cohort, dose_key in self.groups():
            kp = self.cohorts.index(cohort)

            # simulation
            plots[kp].add_data(
                task=f"task_{self.sim_key(cohort, dose_key)}",
                xid="time",
                yid="[Cve_tir]",
                label=f"Sim {dose_key:g} mg SC",
                color=self.colors[dose_key],
            )

            # data
            plots[kp].add_data(
                dataset=self.dset_key(cohort, dose_key),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"Data {dose_key:g} mg",
                color=self.colors[dose_key],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Feng2023, output_dir=Feng2023.__name__)
