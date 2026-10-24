"""Pharmacokinetic parameters of the tirzepatide scans.

The parameters are the non-compartmental analysis of `pkpdutils`, named like
the variables of its `NCAResult` (e.g. `auc_inf_obs`, `cmax`, `tmax`, `thalf`,
`lambda_z`, `cl_f`, `vz_f`), with the unit of every parameter in
`<name>_unit`. Tirzepatide is analysed in plasma with its subcutaneous dose, an
extravascular dose (`Route.ORAL` of pkpdutils, which has no subcutaneous
route; the analysis of an extravascular dose is the same), its metabolites
without a dose, i.e., without clearance and volume. The concentrations below
`LLOQ_FRACTION` of the maximum are below the limit of quantification, so that
the noise of the integrator is not the terminal phase.

A scan has one dimension, the scanned parameter; a run over the draws of the
fitted parameters (`run_simulation pkdb_models.models.tirzepatide
--uncertainty`) adds the dimension of the draws. The parameters are
calculated for every point of every dimension, a row per point with its
position along each dimension (the columns `point` and, with draws, `draw`),
see `summarize`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame, scan_nca
from pkpdsim.scan import scan_dimensions, start_values
from pkpdutils import Route
from sbmlsim import Q
from sbmlsim.result import ScanResult

if TYPE_CHECKING:
    from pkdb_models.models.tirzepatide.experiments.base_experiment import (
        TirzepatideSimulationExperiment,
    )

#: subcutaneous dose of the scans
DOSE = "SCDOSE_tir"
#: the analytes -> their concentration and whether the dose is theirs
ANALYTES: dict[str, tuple[str, bool]] = {
    "tir": ("[Cve_tir]", True),
    "tm": ("[Cve_tm]", False),
}
#: the names of the analytes, the column `substance` of the parameters
SUBSTANCES: dict[str, str] = {
    "tir": "tirzepatide",
    "tm": "tirzepatide metabolites",
}
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def _rows(
    df: pd.DataFrame, res: ScanResult, across: str | None, substance: str
) -> pd.DataFrame:
    """Get the rows of the analysis of an analyte in a scan, in the order of the points.

    The scan has one dimension besides the draws `across`; its position is the
    column `point`, the position of the draw the column `draw`, followed by
    the name of the analyte (`substance`); the rows are ordered by the point
    and then the draw.

    Raises:
        ValueError: if the scan has not one dimension besides the draws.
    """
    dims = scan_dimensions(res, across)
    if len(dims) != 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    names = {dims[0]: "point", **({across: "draw"} if across is not None else {})}
    df = df.rename(columns=names)
    positions = list(names.values())
    df = df.sort_values(positions, kind="stable", ignore_index=True)
    df.insert(0, "substance", substance)
    return df[[*positions, *(c for c in df.columns if c not in positions)]]


def pk_parameters(
    experiment: TirzepatideSimulationExperiment,
    res: ScanResult,
    across: str | None,
    analyte: str,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of an analyte in every simulation of a scan.

    The non-compartmental analysis of all simulations at once; the metabolites
    have no dose.

    Args:
        experiment: experiment of the scan, for the molecular weight.
        res: result of the scan.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.
        analyte: the analyte, a key of `ANALYTES`.

    Returns:
        One row per simulation with its position (`point`, and `draw` with
        draws), the name of the analyte (`substance`), the parameters and
        their units (`<name>_unit`).
    """
    concentration, with_dose = ANALYTES[analyte]
    substance = SUBSTANCES[analyte]
    if with_dose:
        # the dose in the substance unit of the concentration, which `cl_f`
        # and `vz_f` require
        dose = Q(start_values(res, DOSE).values, res.units[DOSE]) / experiment.Mr.tir
        result = scan_nca(
            res,
            concentration,
            dose=dose,
            route=Route.ORAL,
            substance=substance,
            lloq_fraction=LLOQ_FRACTION,
        )
    else:
        result = scan_nca(
            res,
            concentration,
            dose=None,
            route=None,
            substance=substance,
            lloq_fraction=LLOQ_FRACTION,
        )
    return _rows(nca_frame(result).drop(columns="nca_flags"), res, across, substance)


def calculate_tirzepatide_pk(
    experiment: TirzepatideSimulationExperiment,
    res: ScanResult,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a scan.

    Args:
        experiment: experiment of the scan.
        res: result of the scan, a scan of a subcutaneous dose.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.

    Returns:
        One row per simulation of the scan and analyte, with its position
        (`point`, and `draw` with draws).
    """
    return pd.concat(
        [pk_parameters(experiment, res, across, analyte) for analyte in ANALYTES],
        ignore_index=True,
    )


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
