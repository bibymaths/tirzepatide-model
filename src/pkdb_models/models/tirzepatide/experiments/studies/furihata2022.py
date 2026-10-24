"""Simulation experiment of the study Furihata2022."""

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


class Furihata2022(TirzepatideSimulationExperiment):
    """Simulation experiment of Furihata2022.

    Eight weekly subcutaneous doses of tirzepatide in Japanese adults with type
    2 diabetes, in three groups (Table 1, Fig 1): 5 mg weeks 1-8; 10 mg as
    2.5 mg weeks 1-2, 5 mg weeks 3-4 and 10 mg weeks 5-8; 15 mg as 5 mg weeks
    1-2, 10 mg weeks 3-6 and 15 mg weeks 7-8. The profiles follow the first
    dose (week 1, Fig 1A) and the last dose (week 8, Fig 1B), mean and SD;
    the counts are those of TabS1. Fasting is not reported.
    """

    # the body weights of the groups [kg] (Table 1)
    bodyweights: ClassVar[dict[int, float]] = {
        5: 75.4,
        10: 74.9,
        15: 73.3,
    }
    # the weekly doses [mg] of the groups
    doses: ClassVar[dict[int, list[float]]] = {
        5: [5] * 8,
        10: [2.5] * 2 + [5] * 2 + [10] * 4,
        15: [5] * 2 + [10] * 4 + [15] * 2,
    }
    colors: ClassVar[dict[int, str]] = {
        5: "crimson",
        10: "goldenrod",
        15: "limegreen",
    }
    # the profiles: the first dose (week 1) and the last dose (week 8)
    weeks: ClassVar[dict[str, Dosing]] = {
        "week1": Dosing.SINGLE,
        "week8": Dosing.MULTIPLE,
    }

    def sim_key(self, week: str, group: int) -> str:
        """Get the key of the simulation of a profile of a group."""
        return self.to_sid(f"sc_tir_{week}_{group}")

    @staticmethod
    def dset_key(week: str, group: int) -> str:
        """Get the key of the dataset of a profile of a group."""
        return f"tirzepatide_{group}" + ("_multi" if week == "week8" else "")

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
        for group, doses in self.doses.items():
            preinit_changes = {
                **self.default_changes(),
                "BW": Q(self.bodyweights[group], "kg"),
            }
            # the first dose, one week
            simulations[self.sim_key("week1", group)] = self.weekly_doses(
                doses=doses[:1],
                preinit_changes=preinit_changes,
                follow_up=7 * 24 + 10,
                step=0.5,
            )
            # the weekly doses, 840 hr after the last dose
            simulations[self.sim_key("week8", group)] = self.weekly_doses(
                doses=doses,
                preinit_changes=preinit_changes,
                follow_up=870,
                step=0.5,
            )
        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.doses:
            for week, dosing in self.weeks.items():
                sim_key = self.sim_key(week, group)
                mappings[f"fm_{sim_key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.dset_key(week, group),
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
                        dosing=dosing,
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
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )

        plots[0].set_xaxis(Axis(self.label_time, unit=self.unit_time, min=-5, max=178))
        # the weekly doses before the last one (time 0) are shown
        plots[1].set_xaxis(
            Axis(self.label_time, unit=self.unit_time, min=-520, max=870)
        )
        plots[0].set_title("week 1")
        plots[1].set_title("week 8")
        for plot in plots:
            plot.set_yaxis(self.label_tir, unit=self.unit_tir)

        for group, doses in self.doses.items():
            regimen = "/".join(f"{d:g}" for d in dict.fromkeys(doses))
            for kp, week in enumerate(self.weeks):
                plots[kp].add_data(
                    task=f"task_{self.sim_key(week, group)}",
                    xid="time",
                    yid="[Cve_tir]",
                    label=f"Sim {group} mg group ({regimen} mg)",
                    color=self.colors[group],
                )
                plots[kp].add_data(
                    dataset=self.dset_key(week, group),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {group} mg group",
                    color=self.colors[group],
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Furihata2022, output_dir=Furihata2022.__name__)
