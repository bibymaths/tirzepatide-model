"""The simulation experiments of the tirzepatide model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.tirzepatide import MODEL
from pkdb_models.models.tirzepatide.experiments.misc import (
    DoseDependencyExperiment,
    HepaticRenalImpairment,
)
from pkdb_models.models.tirzepatide.experiments.scans import TirzepatideParameterScan
from pkdb_models.models.tirzepatide.experiments.studies import (
    Coskun2018,
    Feng2023,
    Furihata2022,
    Martin2024,
    Urva2021,
    Urva2022,
)

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    "studies": [
        Coskun2018,
        Feng2023,
        Furihata2022,
        Martin2024,
        Urva2021,
        Urva2022,
    ],
    "misc": [
        DoseDependencyExperiment,
        HepaticRenalImpairment,
    ],
    "scans": [
        TirzepatideParameterScan,
    ],
    "hepatic_impairment": [
        Urva2022,
    ],
    "renal_impairment": [
        Urva2021,
    ],
}
EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"] + EXPERIMENTS["scans"]


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")
