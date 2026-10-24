# Tirzepatide

Physiologically based pharmacokinetic (PBPK) model of the dual GIP/GLP-1 receptor agonist tirzepatide after subcutaneous doses: the absorption from a subcutaneous depot (repeated doses add up, the bioavailable fraction of 0.8 is absorbed and the rest is degraded at the injection site), the distribution with albumin into the interstitial space (Vss about 7 l, a terminal half-life of about 5 days), the proteolytic cleavage and beta-oxidation of tirzepatide into its metabolites, whose clearance scales with the body weight, the distribution of the metabolites into a slow tissue pool (tirzepatide is most of the radioactivity in plasma) and their excretion in the urine (relative to the GFR) and, via the bile, in the feces. Tirzepatide itself is not excreted, so renal and hepatic impairment change only its metabolites, as in the studies. The metabolites are counted in tirzepatide equivalents, the unit of the radiolabel.

The published version of the model is [tirzepatide-model](https://github.com/matthiaskoenig/tirzepatide-model) ([doi:10.5281/zenodo.14976788](https://doi.org/10.5281/zenodo.14976788)).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fits, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_liver.py`, `model_kidney.py`) and the whole-body model (`model_body.py`). `models/factory.py` creates the SBML models, the flattened whole-body model which is simulated, the ODEs and the COMBINE archive in `models/output/`; the fitted values come from the adopted fits (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the clinical studies (`studies/`), the dose dependency and the hepatic and renal impairment (`misc/`) and the parameter scans of hepatic and renal function and body weight (`scans/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`.
- `fitting/`: the fit problem of the pharmacokinetics (`PK`), its parameters and the selection of the training, validation, aggregate and outlier data. The adopted fit is `PK_20261019_095941__4f772`.
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics.
- `tirzepatide_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils`.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies (`data/collect_data.py`).
- `latex/`: the table of the studies of the publication.
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.tirzepatide --action factory
run_simulation pkdb_models.models.tirzepatide --action list_experiments
run_simulation pkdb_models.models.tirzepatide --action simulate --experiments all
run_simulation pkdb_models.models.tirzepatide --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.tirzepatide --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.tirzepatide --adopt PK_<fit id>
run_report pkdb_models.models.tirzepatide --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.tirzepatide --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.tirzepatide.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fits of the model,
not from numbers in the code. `run_fit pkdb_models.models.tirzepatide --adopt <fit id>`
copies the record of a finished fit (its parameters, problem, profile
likelihood and Fisher information) into `models/output/fits/<fit id>/`, which is
tracked; the ids of the adopted fits are listed in `fits` of the model object
(`__init__.py`). The factory takes the fitted values and their uncertainty from
the records (`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`. A refit
is: fit, adopt, replace the id in `fits`, rebuild the model. See the
documentation of the repository on fitting (`docs/fitting.md`).
