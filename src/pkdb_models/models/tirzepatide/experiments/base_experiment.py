"""Base class of the tirzepatide simulation experiments."""

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, ClassVar, NamedTuple

import pandas as pd
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from sbmlsim import Q
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.tirzepatide import MODEL
from pkdb_models.models.tirzepatide.tirzepatide_pk import calculate_tirzepatide_pk


class MolecularWeights(NamedTuple):
    """Molecular weights for the conversion of the data."""

    tir: Quantity
    tm: Quantity


class TirzepatideSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the tirzepatide simulation experiments."""

    pkpd_model = MODEL
    selections = (
        "time",
        # dosing
        "IVDOSE_tir",
        "SCDOSE_tir",
        "SCDEPOT_tir",
        # venous plasma
        "[Cve_tir]",
        "[Cve_tm]",
        "[Cve_tmtot]",
        # urine
        "Aurine_tm",
        # feces
        "Afeces_tm",
        # cases
        "KI__f_renal_function",
        "f_cirrhosis",
        "BW",
    )

    font: ClassVar[dict[str, Any]] = {"weight": "bold", "size": 22}
    scan_font: ClassVar[dict[str, Any]] = {"weight": "bold", "size": 15}
    tick_font_size = 15
    legend_font_size = 9
    suptitle_font_size = 25

    # labels
    label_time = "time"
    label_tir = "tirzepatide plasma"
    label_tm = "tirzepatide metabolites \n"
    label_tmtot = "tirzepatide and metabolites \n"
    label_tm_plasma = label_tm + "plasma"
    label_tmtot_plasma = label_tmtot + "plasma"

    label_tm_urine = label_tm + "urine"
    label_tm_feces = label_tm + "feces"

    labels: ClassVar[Mapping[str, str]] = {
        "time": "time",
        "[Cve_tir]": label_tir,
        "[Cve_tm]": label_tm_plasma,
        "[Cve_tmtot]": label_tmtot_plasma,
        "Aurine_tm": label_tm_urine,
        "Afeces_tm": label_tm_feces,
    }

    # units
    unit_time = "hr"
    unit_metabolite = "nM"
    unit_metabolite_urine = "µmole"
    unit_metabolite_feces = "µmole"
    unit_tir = unit_metabolite
    unit_tm = unit_metabolite
    unit_tmtot = unit_metabolite
    unit_tm_urine = unit_metabolite_urine
    unit_tm_feces = unit_metabolite_feces

    units: ClassVar[Mapping[str, str]] = {
        "time": unit_time,
        "[Cve_tir]": unit_tir,
        "[Cve_tm]": unit_tm,
        "[Cve_tmtot]": unit_tmtot,
        "Aurine_tm": unit_tm_urine,
        "Afeces_tm": unit_tm_feces,
    }

    # ----------- Renal map --------------
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    # molecular weights of tirzepatide and its metabolites
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        tir=Q(4813.527, "g/mole"),
        tm=Q(4813.527, "g/mole"),
    )

    def weekly_doses(
        self,
        doses: Sequence[float],
        preinit_changes: Mapping[str, Quantity | float],
        follow_up: float,
        step: float = 0.1,
    ) -> Simulation:
        """Get a simulation of weekly subcutaneous doses of tirzepatide.

        The doses [mg] are given every 7 days, the first one before the
        initialization. A later dose adds to the dose state (`SCDOSE_tir`),
        from which it is injected into the subcutaneous depot (`SCDEPOT_tir`)
        within seconds, so that it adds to the rest of the earlier doses. The
        simulation ends `follow_up` hours after the last dose and its time is
        shifted so that the last dose is at time 0.

        Args:
            doses: the doses [mg] of the weeks.
            preinit_changes: the changes of the subjects, applied before the
                initialization.
            follow_up: the hours after the last dose.
            step: the step of the uniform output grid [hr], every dose is on it.

        Returns:
            The simulation of the doses in hours.
        """
        week = 7 * 24  # [hr]
        end = week * (len(doses) - 1) + follow_up
        return Simulation(
            time_unit="hr",
            end=end,
            preinit_changes={
                **preinit_changes,
                "SCDOSE_tir": Q(doses[0], "mg"),
            },
            changes=[
                self.add_doses([week * k], {"SCDOSE_tir": Q(dose, "mg")})
                for k, dose in enumerate(doses)
                if k > 0
            ],
            time_shift=-week * (len(doses) - 1),
        )

    # --- Pharmacokinetic parameters ---
    # keys are the parameters of the non-compartmental analysis of pkpdutils,
    # see `tirzepatide_pk`; AUC and Cmax in nmole (`PK_UNITS` of the base has
    # µmole), the labels are those of the base
    pk_units: ClassVar[Mapping[str, str]] = {
        "auc_last": "nmole/l*hr",
        "auc_inf_obs": "nmole/l*hr",
        "cmax": "nmole/l",
        "tmax": "hr",
        "thalf": "hr",
        "lambda_z": "1/hr",
        "cl_f": "l/hr",
        "vz_f": "l",
        "Aurine_tm": "µmole",
        "Afeces_tm": "µmole",
    }

    def calculate_tirzepatide_pk(
        self, scans: Iterable[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of the scans.

        Args:
            scans: keys of the simulations, all simulations by default.

        Returns:
            The parameters of every scan by simulation key, per draw of the
            fitted parameters in a run over them (`uncertainty`).
        """
        keys = self._simulations if scans is None else scans
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            key: calculate_tirzepatide_pk(
                experiment=self, res=self.results[f"task_{key}"], across=across
            )
            for key in keys
        }
