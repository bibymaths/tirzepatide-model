[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14976788.svg)](https://doi.org/10.5281/zenodo.14976788)
[![GitHub Action](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/python.yml/badge.svg)](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/python.yml)
[![GitHub Action](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/docker.yml/badge.svg)](https://github.com/matthiaskoenig/tirzepatide-model/actions/workflows/docker.yml)

# tirzepatide model
This repository provides the tirzepatide physiologically based pharmacokinetic (PBPK) model: the subcutaneous absorption of tirzepatide, its distribution with albumin into the interstitial space, its proteolytic cleavage, the distribution of its metabolites into a slow tissue pool and their excretion in the urine and the feces.

The model is distributed as [SBML](http://sbml.org) format available from [`tirzepatide_body_flat.xml`](./models/tirzepatide_body_flat.xml) with 
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftirzepatide-model%2Fmain%2Fmodels%2Ftirzepatide_body_flat.xml) and [model equations](./models/tirzepatide_body_flat.md).

The COMBINE archive is available from [`tirzepatide_model.omex`](./tirzepatide_model.omex).

![model overview](./figures/tirzepatide_model.png)

### Comp submodels
* **liver** submodel [`tirzepatide_liver.xml`](./models/tirzepatide_liver.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftirzepatide-model%2Fmain%2Fmodels%2Ftirzepatide_liver.xml) and [equations](./models/tirzepatide_liver.md).
* **kidney** submodel [`tirzepatide_kidney.xml`](./models/tirzepatide_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftirzepatide-model%2Fmain%2Fmodels%2Ftirzepatide_kidney.xml) and [equations](./models/tirzepatide_kidney.md).
* **intestine** submodel [`tirzepatide_intestine.xml`](./models/tirzepatide_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftirzepatide-model%2Fmain%2Fmodels%2Ftirzepatide_intestine.xml) and [equations](./models/tirzepatide_intestine.md).
* **whole-body** submodel [`tirzepatide_body.xml`](./models/tirzepatide_body.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Ftirzepatide-model%2Fmain%2Fmodels%2Ftirzepatide_body.xml) and [equations](./models/tirzepatide_body.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14976788.svg)](https://doi.org/10.5281/zenodo.14976788)

> Mishra, A. & König, M. (2025).
> *Physiologically based pharmacokinetic (PBPK) model of tirzepatide.*   
> Zenodo. [https://doi.org/10.5281/zenodo.14976788](https://doi.org/10.5281/zenodo.14976788)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.


## Run simulations
### python
Clone the repository 
```bash
git clone https://github.com/matthiaskoenig/tirzepatide-model.git
cd tirzepatide-model
```

#### uv
Run the complete analysis with uv (https://docs.astral.sh/uv/getting-started/installation/):
```bash
uv run run_simulation pkdb_models.models.tirzepatide -a all -r results
```

#### pip
If you use pip install the package via
```bash
pip install -e .
```
Run the complete analysis in the environment via:
```bash
run_simulation pkdb_models.models.tirzepatide -a all -r results
```

### docker
Simulations can also be run within a docker container:

```bash
docker run -v "${PWD}/results:/results" -it matthiaskoenig/tirzepatide:latest /bin/bash
```

Run the complete analysis:
```bash
uv run run_simulation pkdb_models.models.tirzepatide -a all -r /results
```
The results are written into the mounted `/results` folder on the host.

In case of permission issues with the mounted folder, adjust ownership and access rights with:
```bash
sudo chown $(id -u):$(id -g) -R "${PWD}/results"
sudo chmod 775 "${PWD}/results"
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2025-2026 Matthias König, [Systems Medicine of the Liver](https://livermetabolism.com)
