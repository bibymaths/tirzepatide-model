"""Simulation experiment of the study Martin2024."""

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


class Martin2024(TirzepatideSimulationExperiment):
    """Simulation experiment of Martin2024.

    Mass balance of a single subcutaneous dose of about 2.9 mg tirzepatide
    (a 1:1 mixture of [14C]-labelled and unlabelled tirzepatide) in 6 healthy
    men (78.6 kg). Plasma tirzepatide (LC-MS/MS) and plasma total radioactivity
    (Fig 3, mean and SD) of the same subjects and dose, and the cumulative
    recovery of the radioactivity in urine and feces (Fig 4, the
    extrapolated recovery of the authors, mean and SD) as amounts of the dose.
    Radioactivity is counted in tirzepatide equivalents. Fasting is not
    reported.

    The two plasma assays disagree: the AUC of tirzepatide (LC-MS/MS) is 109 %
    of the AUC of the total radioactivity (Table 1), which the authors ascribe
    to the variability between the two methods (Discussion). Its Cmax per dose
    (453 ng/ml for 2.9 mg, 156 ng/ml per mg) is 1.4 to 2 times that of the
    single doses of Coskun2018 (5 mg: 76, 8 mg: 109 ng/ml per mg), while the
    total radioactivity (327 ng-eq/ml, 113 ng-eq/ml per mg) agrees with them.
    """

    bodyweight = 78.6  # [kg]
    dose = 2.9  # [mg]
    colors: ClassVar[dict[str, str]] = {
        "[Cve_tir]": "tab:blue",
        "[Cve_tmtot]": "black",
        "Aurine_tm": "tab:orange",
        "Afeces_tm": "tab:brown",
    }
    # the datasets of the observables
    sinfo: ClassVar[dict[str, str]] = {
        "[Cve_tir]": "tirzepatide_plasma_TIR",
        "[Cve_tmtot]": "tir_and_tm_plasma_TIRC14",
        "Aurine_tm": "tm_urine_TIRC14",
        "Afeces_tm": "tm_feces_TIRC14",
    }
    # the keys of the fit mappings of the observables
    mapping_keys: ClassVar[dict[str, str]] = {
        "[Cve_tir]": "fm_sc_tir_plasma_tir",
        "[Cve_tmtot]": "fm_sc_tir_plasma_tmtot",
        "Aurine_tm": "fm_sc_tir_urine_tm",
        "Afeces_tm": "fm_sc_tir_feces_tm",
    }
    tissue_metadata: ClassVar[dict[str, Tissue]] = {
        "[Cve_tir]": Tissue.PLASMA,
        "[Cve_tmtot]": Tissue.PLASMA,
        "Aurine_tm": Tissue.URINE,
        "Afeces_tm": Tissue.FECES,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig4"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                if label.startswith("tir"):
                    dset.unit_conversion("mean", 1 / self.Mr.tir)
                if label.startswith("tm"):
                    dset.unit_conversion("mean", 1 / self.Mr.tm)
                dsets[self.to_sid(label)] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "sc_tir": Simulation(
                time_unit="hr",
                end=900,
                preinit_changes={
                    **self.default_changes(),
                    "BW": Q(self.bodyweight, "kg"),
                    "SCDOSE_tir": Q(self.dose, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for sid, dset_key in self.sinfo.items():
            mappings[self.mapping_keys[sid]] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(dset_key),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task="task_sc_tir",
                    xid="time",
                    yid=sid,
                ),
                metadata=PKPDMappingMetaData(
                    tissue=self.tissue_metadata[sid],
                    route=Route.SC,
                    application_form=ApplicationForm.SUBCUTANEOUS,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    coadministration=Coadministration.NONE,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig3_Fig4",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit=self.unit_time), legend=True
        )
        for k, (sid, dset_key) in enumerate(self.sinfo.items()):
            plots[k].set_yaxis(self.labels[sid], unit=self.units[sid])
            # simulation
            plots[k].add_data(
                task="task_sc_tir",
                xid="time",
                yid=sid,
                label=f"Sim {self.dose} mg SC",
                color=self.colors[sid],
            )
            # data
            plots[k].add_data(
                dataset=self.to_sid(dset_key),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"Data {self.dose} mg",
                color=self.colors[sid],
            )
        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Martin2024, output_dir=Martin2024.__name__)
