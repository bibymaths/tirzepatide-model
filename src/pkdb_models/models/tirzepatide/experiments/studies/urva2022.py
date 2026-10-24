"""Simulation experiment of the study Urva2022."""

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


class Urva2022(TirzepatideSimulationExperiment):
    """Simulation experiment of Urva2022.

    A single subcutaneous dose of 5 mg tirzepatide in subjects with normal
    hepatic function and with mild, moderate and severe hepatic impairment
    (Child-Pugh A, B and C), the means of the groups (Fig 1A, mean and SD) and
    the individuals (Fig 1B-E). The controls are healthy (no type 2 diabetes,
    Table 1). Fasting is not reported. The individuals are the subjects of the
    means and are simulated as their group; their digitization is not reliable
    (the points of crossing lines are assigned to the wrong individuals, the
    means of the individuals at 672 hr are 2-3 times the means of Fig 1A).
    """

    bodyweight: ClassVar[dict[str, float]] = {  # [kg] (Table 1)
        "normal": 96.72,
        "mild": 82.75,
        "moderate": 95.12,
        "severe": 88.56,
    }

    groups: ClassVar[list[str]] = list(bodyweight.keys())

    group_labels: ClassVar[dict[str, str]] = {
        "normal": "Control",
        "mild": "Mild cirrhosis",
        "moderate": "Moderate cirrhosis",
        "severe": "Severe cirrhosis",
    }
    # the prefixes of the individuals of the groups (Fig 1B-E) and their number
    individuals: ClassVar[dict[str, tuple[str, int]]] = {
        "normal": ("N", 13),
        "mild": ("M", 6),
        "moderate": ("MO", 6),
        "severe": ("S", 7),
    }

    def sim_key(self, group: str) -> str:
        """Get the key of the simulation of a group."""
        return self.to_sid(f"sc_tir_hepatic_{group}")

    def individual_ids(self) -> dict[str, list[str]]:
        """Get the ids of the individuals by group, e.g. `N1`."""
        return {
            group: [f"{prefix}{k}" for k in range(1, n + 1)]
            for group, (prefix, n) in self.individuals.items()
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1A", "Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                if label.startswith("tirzepatide_"):
                    dset = DataSet.from_df(df_label, self.ureg)
                    if fig_id == "Fig1A":
                        dset.unit_conversion("mean", 1 / self.Mr.tir)
                    else:
                        dset.unit_conversion("value", 1 / self.Mr.tir)
                    dsets[self.to_sid(label)] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for group in self.groups:
            simulations[self.sim_key(group)] = Simulation(
                time_unit="hr",
                end=700,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight[group], "kg"),
                    "SCDOSE_tir": Q(5, "mg"),
                    "f_cirrhosis": Q(
                        self.cirrhosis_map[self.group_labels[group]], "dimensionless"
                    ),
                },
            )
        return simulations

    @staticmethod
    def metadata(group: str) -> PKPDMappingMetaData:
        """Get the metadata of the fit mappings of a group."""
        return PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.SC,
            application_form=ApplicationForm.SUBCUTANEOUS,
            dosing=Dosing.SINGLE,
            health=Health.HEALTHY if group == "normal" else Health.HEPATIC_IMPAIRMENT,
            fasting=Fasting.NR,
            coadministration=Coadministration.NONE,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.groups:
            sim_key = self.sim_key(group)
            mappings[f"fm_{sim_key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"tirzepatide_{group}"),
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
                metadata=self.metadata(group),
            )
        # the individuals, simulated as their group
        for group, ids in self.individual_ids().items():
            for individual in ids:
                mappings[self.to_sid(f"fm_sc_tir_hepatic_{individual}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"tirzepatide_{individual}"),
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_{self.sim_key(group)}",
                        xid="time",
                        yid="[Cve_tir]",
                    ),
                    metadata=self.metadata(group),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1A",
            name=f"{self.__class__.__name__} (hepatic impairment)",
        )
        fig2 = Figure(
            experiment=self,
            sid="Fig1",
            num_cols=2,
            num_rows=2,
            name=f"{self.__class__.__name__} (hepatic impairment, individuals)",
        )
        xaxis = Axis(self.label_time, unit=self.unit_time, min=-10, max=700)
        plots = fig.create_plots(
            xaxis=xaxis,
            yaxis=Axis(self.label_tir, unit=self.unit_tir),
            legend=True,
        )
        plots2 = fig2.create_plots(
            xaxis=xaxis,
            yaxis=Axis(self.label_tir, unit=self.unit_tir),
            legend=True,
        )
        colors = {
            group: self.cirrhosis_colors[label]
            for group, label in self.group_labels.items()
        }
        # simulations
        for group in self.groups:
            plots[0].add_data(
                task=f"task_{self.sim_key(group)}",
                xid="time",
                yid="[Cve_tir]",
                label=f"Sim {group}",
                color=colors[group],
            )
        # data
        for group in self.groups:
            plots[0].add_data(
                dataset=self.to_sid(f"tirzepatide_{group}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"Data {group}",
                color=colors[group],
            )
        # individuals
        for kp, (group, ids) in enumerate(self.individual_ids().items()):
            plots2[kp].set_title(group)
            plots2[kp].add_data(
                task=f"task_{self.sim_key(group)}",
                xid="time",
                yid="[Cve_tir]",
                label=f"Sim {group}",
                color=colors[group],
            )
            for individual in ids:
                plots2[kp].add_data(
                    dataset=self.to_sid(f"tirzepatide_{individual}"),
                    xid="time",
                    yid="value",
                    count="count",
                    color=colors[group],
                )
        return self.figures_by_sid(fig, fig2)


if __name__ == "__main__":
    MODEL.run_experiments(Urva2022, output_dir=Urva2022.__name__)
