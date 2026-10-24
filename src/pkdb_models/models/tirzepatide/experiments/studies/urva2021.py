"""Simulation experiment of the study Urva2021."""

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


class Urva2021(TirzepatideSimulationExperiment):
    """Simulation experiment of Urva2021.

    A single subcutaneous dose of 5 mg tirzepatide in subjects with normal
    renal function and with mild, moderate and severe renal impairment and end
    stage renal disease on dialysis, classified by the MDRD eGFR (Fig 2, mean
    and SD). The controls are healthy (no type 2 diabetes), 6 of the 31
    impaired subjects have type 2 diabetes (Table 1). Fasting is not reported.
    """

    bodyweight: ClassVar[dict[str, float]] = {  # [kg] (Table 1)
        "normal": 88.0,
        "mild": 93.1,
        "moderate": 83.8,
        "severe": 81.8,
        "end": 89.6,
    }
    # the mean MDRD eGFR of the individuals of the groups [ml/min/1.73 m^2]
    # (Fig 3A); the renal function is the eGFR relative to the GFR of the
    # model, 101 ml/min
    egfr: ClassVar[dict[str, float]] = {
        "normal": 101.4,
        "mild": 72.1,
        "moderate": 44.1,
        "severe": 15.2,
        "end": 8.2,
    }
    gfr_base = 101.0  # [ml/min]
    group_labels: ClassVar[dict[str, str]] = {
        "normal": "Normal renal function",
        "mild": "Mild renal impairment",
        "moderate": "Moderate renal impairment",
        "severe": "Severe renal impairment",
        "end": "End stage renal disease",
    }

    groups: ClassVar[list[str]] = list(bodyweight.keys())

    def sim_key(self, group: str) -> str:
        """Get the key of the simulation of a group."""
        return self.to_sid(f"sc_tir_renal_{group}")

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
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

        for group in self.groups:
            simulations[self.sim_key(group)] = Simulation(
                time_unit="hr",
                end=700,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight[group], "kg"),
                    "SCDOSE_tir": Q(5, "mg"),
                    "KI__f_renal_function": Q(
                        self.egfr[group] / self.gfr_base, "dimensionless"
                    ),
                },
            )
        return simulations

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
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.SC,
                    application_form=ApplicationForm.SUBCUTANEOUS,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY
                    if group == "normal"
                    else Health.RENAL_IMPAIRMENT,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            name=f"{self.__class__.__name__} (renal impairment)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time, min=-10, max=700),
            yaxis=Axis(self.label_tir, unit=self.unit_tir),
            legend=True,
        )
        colors = {
            group: self.renal_colors[label]
            for group, label in self.group_labels.items()
        }
        # simulations
        for group in self.groups:
            plots[0].add_data(
                task=f"task_{self.sim_key(group)}",
                xid="time",
                yid="[Cve_tir]",
                label=f"Sim {group} (eGFR {self.egfr[group]:g})",
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

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Urva2021, output_dir=Urva2021.__name__)
