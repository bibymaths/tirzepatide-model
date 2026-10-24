"""Dose dependency of the pharmacokinetics of tirzepatide."""

from typing import ClassVar, override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.tirzepatide import MODEL
from pkdb_models.models.tirzepatide.experiments.base_experiment import (
    TirzepatideSimulationExperiment,
)


class DoseDependencyExperiment(TirzepatideSimulationExperiment):
    """Weekly intravenous and subcutaneous doses of tirzepatide."""

    routes: ClassVar[dict[str, list[str]]] = {
        "tir": ["IV", "SC"],
    }
    doses: ClassVar[list[float]] = [0, 2.5, 5, 10, 20]  # [mg]
    colors: ClassVar[list[str]] = [
        "black",
        "tab:orange",
        "tab:blue",
        "tab:red",
        "tab:green",
    ]

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        week = 7 * 24  # [hr]

        for substance, routes in self.routes.items():
            for route in routes:
                for dose in self.doses:
                    # a dose every week for 5 weeks, 8 weeks after the last dose
                    simulations[self.to_sid(f"tir_{substance}_{route}_{dose}")] = (
                        Simulation(
                            time_unit="hr",
                            end=12 * week,
                            preinit_changes={
                                **self.default_changes(),
                                f"{route}DOSE_{substance}": Q(dose, "mg"),
                            },
                            changes=[
                                self.add_doses(
                                    [week * k for k in range(1, 5)],
                                    {f"{route}DOSE_{substance}": Q(dose, "mg")},
                                ),
                            ],
                            time_shift=-5 * week,
                        )
                    )

        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        return {
            **self.figure_pk(),
        }

    def figure_pk(self) -> dict[str, Figure]:
        """Plasma concentrations and excretion of tirzepatide and its metabolites."""
        figures = []
        for substance, routes in self.routes.items():
            for route in routes:
                fig = Figure(
                    experiment=self,
                    sid=self.to_sid(f"Fig_dose_dependency_pk_{substance}_{route}"),
                    num_rows=2,
                    num_cols=2,
                    name=f"Dose Dependency {substance}_{route}",
                    settings={"legend_scope": "row"},
                )
                # the five weekly doses and the eight weeks after the last dose
                plots = fig.create_plots(xaxis=Axis("time", unit="week"), legend=True)
                sids = [
                    # plasma
                    "[Cve_tir]",
                    "[Cve_tm]",
                    # urine,
                    "Aurine_tm",
                    # feces
                    "Afeces_tm",
                ]
                for ksid, sid in enumerate(sids):
                    plots[ksid].set_yaxis(label=self.labels[sid], unit=self.units[sid])
                    for kval, dose in enumerate(self.doses):
                        plots[ksid].add_data(
                            task=self.to_sid(f"task_tir_{substance}_{route}_{dose}"),
                            xid="time",
                            yid=sid,
                            label=f"{dose} mg",
                            color=self.colors[kval],
                        )

                figures.append(fig)

        return self.figures_by_sid(*figures)


if __name__ == "__main__":
    MODEL.run_experiments(
        DoseDependencyExperiment, output_dir=DoseDependencyExperiment.__name__
    )
