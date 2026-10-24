"""Pharmacokinetics of tirzepatide in hepatic and renal impairment."""

from collections.abc import Mapping
from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.tirzepatide import MODEL
from pkdb_models.models.tirzepatide.experiments.base_experiment import (
    TirzepatideSimulationExperiment,
)


class HepaticRenalImpairment(TirzepatideSimulationExperiment):
    """A single subcutaneous dose in the degrees of hepatic and renal impairment."""

    maps: ClassVar[dict[str, Mapping[str, float]]] = {
        "hepatic": TirzepatideSimulationExperiment.cirrhosis_map,
        "renal": TirzepatideSimulationExperiment.renal_map,
    }
    parameters: ClassVar[dict[str, str]] = {
        "hepatic": "f_cirrhosis",
        "renal": "KI__f_renal_function",
    }
    colors: ClassVar[dict[str, Mapping[str, str]]] = {
        "hepatic": TirzepatideSimulationExperiment.cirrhosis_colors,
        "renal": TirzepatideSimulationExperiment.renal_colors,
    }

    impairments: ClassVar[list[str]] = list(maps.keys())

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}

        for impairment in self.impairments:
            parameter = self.parameters[impairment]

            for group, value in self.maps[impairment].items():
                simulations[self.to_sid(f"tir_{impairment}_{group}")] = Simulation(
                    time_unit="hr",
                    end=648,
                    preinit_changes={
                        **self.default_changes(),
                        "SCDOSE_tir": Q(5, "mg"),
                        parameter: Q(value, "dimensionless"),
                    },
                )
        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        figures = []

        for impairment in self.impairments:
            colors = self.colors[impairment]

            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"Fig_impairment_{impairment}"),
                num_rows=2,
                num_cols=2,
                name=f"{impairment.title()} impairment",
            )
            plots = fig.create_plots(xaxis=Axis("time", unit="week"), legend=True)
            for ksid, sid in enumerate(
                [
                    # plasma
                    "[Cve_tir]",
                    "[Cve_tm]",
                    # urine,
                    "Aurine_tm",
                    # feces
                    "Afeces_tm",
                ]
            ):
                plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])
                for group in self.maps[impairment]:
                    # simulations
                    plots[ksid].add_data(
                        task=self.to_sid(f"task_tir_{impairment}_{group}"),
                        xid="time",
                        yid=sid,
                        label=f"{group}",
                        color=colors[group],
                    )

            figures.append(fig)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(
        HepaticRenalImpairment, output_dir=HepaticRenalImpairment.__name__
    )
