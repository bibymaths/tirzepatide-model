"""Tirzepatide body model."""

from typing import NotRequired, TypedDict

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    PORT_SUFFIX,
    AssignmentRule,
    Compartment,
    ExternalModelDefinition,
    Model,
    Parameter,
    RateRule,
    Reaction,
    ReplacedElement,
    Species,
    Submodel,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import (
    BQB,
    SBO,
)

from pkdb_models.models.tirzepatide.models import annotations, templates
from pkdb_models.models.tirzepatide.models.fits import FITS


# -----------------------------------------------------------------------------
# Whole Body Metabolism
# -----------------------------------------------------------------------------
class U(templates.U):
    """Units of the body model."""

    cm = UnitDefinition("cm")
    hr = UnitDefinition("hr")
    kg = UnitDefinition("kg")

    l_per_hr = UnitDefinition("l_per_hr", "l/hr")
    l_per_kg = UnitDefinition("l_per_kg", "l/kg")
    l_per_min_kg = UnitDefinition("l_per_min_kg", "l/min/kg")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")

    m2_per_kg = UnitDefinition("m2_per_kg", "meter^2/kg")

    mg_per_day = UnitDefinition("mg_per_day", "mg/day")
    mg_per_g = UnitDefinition("mg_per_g", "mg/g")
    mg_per_hr = UnitDefinition("mg_per_hr", "mg/hr")
    mg_per_l = UnitDefinition("mg_per_l", "mg/l")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")

    min_per_day = UnitDefinition("min_per_day", "min/day")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")

    ml = UnitDefinition("ml")
    ml_per_l = UnitDefinition("ml_per_l", "ml/l")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    ml_per_s = UnitDefinition("ml_per_s", "ml/s")
    ml_per_s_kg = UnitDefinition("ml_per_s_kg", "ml/s/kg")

    mmole_per_hr = UnitDefinition("mmole_per_hr", "mmole/hr")
    mmole_per_l = UnitDefinition("mmole_per_l", "mmole/l")
    mmole_per_min_kg = UnitDefinition("mmole_per_min_kg", "mmole/min/kg")
    mmole_per_hr_ml = UnitDefinition("mmole_per_hr_ml", "mmole/hr/ml")

    mul_per_g = UnitDefinition("mulitre_per_g", "microlitre/g")
    mul_per_min_mg = UnitDefinition("mul_per_min_mg", "microliter/min/mg")

    per_hr = UnitDefinition("per_hr", "1/hr")
    per_min_kg = UnitDefinition("per_min_kg", "1/min/kg")

    s_per_min = UnitDefinition("s_per_min", "s/min")
    mmHg = UnitDefinition("mmHg", "133.32239 N/m^2")


_m = Model(
    "tirzepatide_body",
    name="Tirzepatide body model",
    notes="""
    # Tirzepatide body model

    Physiological based pharmacokinetic (PBPK) model of tirzepatide in Human.

    Tirzepatide is given subcutaneously: the dose enters a depot, from which
    the fraction `Fsc_tir` (the absolute bioavailability, 80 %) is absorbed
    into the venous plasma and the rest is degraded at the injection site to
    the metabolites. Tirzepatide is bound to albumin (99 %) and distributes
    with it into the interstitial space of the tissues (`ftissue_tir`,
    `Kp_tir`). It is eliminated by proteolytic cleavage of the peptide
    backbone and beta-oxidation of the C20 fatty diacid (`TIR2TM`), which
    scales with the body weight; tirzepatide itself is not excreted. The
    metabolites are excreted in the urine with a clearance relative to the
    glomerular filtration rate (kidney submodel) and in the bile (liver
    submodel), from where they reach the feces through an intestinal transit
    chain (intestine submodel).

    The metabolites are one species counted in tirzepatide equivalents (the
    molecular weight of tirzepatide), which is what the measurements of the
    radiolabel are (ng-eq/ml, % of the dose). They keep the C20 fatty diacid
    and distribute into a slow tissue pool (`ftissue_tm`, `Kp_tm`), from which
    they return to the plasma and are excreted over weeks: tirzepatide is
    about 80 % of the radioactivity in plasma, while the excretion of the
    radiolabel lags behind the cleavage (Martin2024).
    """
    + terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.HAS_TAXON, "taxonomy/9606"),
        (BQB.HAS_TAXON, "VTO:0011993"),
        (BQB.HAS_TAXON, "snomedct/337915000"),
        (BQB.IS_DESCRIBED_BY, "doi:10.5281/zenodo.14976788"),
    ],
)

_m.ports = []
_m.deletions = []
_m.replaced_elements = []


class SubstanceBody(TypedDict):
    """Definition of a substance transported in the whole-body model."""

    name: str
    unit: UnitDefinition
    cinit: float  # initial concentration [mmole/l]
    Mr: float  # molecular weight [g/mole]
    IVDOSE: NotRequired[float]  # intravenous dose [mg]
    SCDOSE: NotRequired[float]  # subcutaneous dose [mg]
    PODOSE: NotRequired[float]  # oral dose [mg]
    ftissue: NotRequired[float]  # distribution in tissues [litre_per_min]


SUBSTANCES_BODY: dict[str, SubstanceBody] = {
    "tir": {
        "name": "tirzepatide",
        "unit": U.mmole,
        # initial concentration
        "cinit": 0.0,  # [mmole/l]
        # Molecular weight
        "Mr": 4813.527,  # [g/mole]
        # iv doses [mg]
        "IVDOSE": 0,  # venous plasma
        "SCDOSE": 0,  # subcutaneous
        # distribution with albumin into the interstitial space: the escape
        # from the plasma, ftissue * Kp = 0.005 l/min (about 10 %/hr of the
        # plasma, the transcapillary escape of albumin is about 5 %/hr), the
        # volume of distribution Kp * the tissue volume, about 2 l (the
        # steady state volume 7.3 l = 0.8 * Vss/F of about 9 l). Kp is fitted
        # (`fits.FITS`), ftissue is not: without intravenous data the distribution is hidden
        # in the absorption, the subcutaneous data only bound it from below
        # (0.04 l/min, profile likelihood flat above 0.1 l/min)
        "ftissue": 0.15,  # [l/min]
    },
    "tm": {
        "name": "tirzepatide metabolites",
        "unit": U.mmole,
        # initial concentration
        "cinit": 0.0,  # [mmole/l]
        # Molecular weight
        # the metabolites are counted in tirzepatide equivalents, the unit of
        # the radiolabel (ng-eq/ml, % of the dose)
        "Mr": 4813.527,  # [g/mole]
        # the slow tissue pool of the metabolites (the fatty diacid and the
        # linker bound to albumin and taken up in the tissues): in the plasma
        # volume alone the metabolites exceed tirzepatide from day 7 on (46 %
        # of the plasma radioactivity is the parent), Martin2024 measured 80 %
        # with no metabolite above 6 %, while 30 % of the dose is cleaved but
        # not yet excreted at day 7. Kp is fitted (`fits.FITS`),
        # ftissue is not: the excretion and the radioactivity of Martin2024
        # bound it from below (0.02 l/min), the profile likelihood is flat
        # above (fit PK_20261019_094858__a49bf, minimum at 0.036 l/min,
        # correlated with Kp); it is the minimum of the profile
        "ftissue": 0.036,  # [l/min]
    },
}

# -----------------------------------------------------------------------------
# Submodels
# -----------------------------------------------------------------------------
COMPARTMENTS_BODY = {
    "ki": "kidney",
    "li": "liver",
    "lu": "lung",
    "gu": "gut",
    "re": "rest",
    "ar": "arterial blood",
    "ve": "venous blood",
    "po": "portal vein",
    "hv": "hepatic vein",
}

SUBMODEL_SID_DICT = {  # tissue to submodel mapping
    "ki": "KI",  # kidney
    "li": "LI",  # liver
    "gu": "GU",  # gut/intestine
}

kidney_id = "tirzepatide_kidney"
liver_id = "tirzepatide_liver"
gut_id = "tirzepatide_intestine"

_m.external_model_definitions = [
    ExternalModelDefinition(
        sid="kidney",
        name="kidney model definition",
        source=f"{kidney_id}.xml",
        modelRef=kidney_id,
    ),
    ExternalModelDefinition(
        sid="liver",
        name="liver model definition",
        source=f"{liver_id}.xml",
        modelRef=liver_id,
    ),
    ExternalModelDefinition(
        sid="gut", name="gut model definition", source=f"{gut_id}.xml", modelRef=gut_id
    ),
]

_m.submodels = [
    Submodel(sid=SUBMODEL_SID_DICT["ki"], modelRef="kidney", name="kidney submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["li"], modelRef="liver", name="liver submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["gu"], modelRef="gut", name="gut submodel"),
]

# -------------------------------------------------------------------------------------------------
# Compartments
# -------------------------------------------------------------------------------------------------
_m.compartments = [
    Compartment(
        "Vre",
        metaId="meta_Vre",
        value=1,
        unit=U.liter,
        constant=False,
        name="rest of body",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["re"],
    ),
    Compartment(
        "Vgu",
        metaId="meta_Vgu",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vki",
        metaId="meta_Vki",
        value=1,
        unit=U.liter,
        constant=False,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vli",
        metaId="meta_Vli",
        value=1,
        unit=U.liter,
        constant=False,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
    ),
    Compartment(
        "Vlu",
        metaId="meta_Vlu",
        value=1,
        unit=U.liter,
        constant=False,
        name="lung",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["lu"],
    ),
    Compartment(
        "Vve",
        metaId="meta_Vve",
        value=1,
        unit=U.liter,
        constant=False,
        name="venous blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ve"],
    ),
    Compartment(
        "Var",
        metaId="meta_Var",
        value=1,
        unit=U.liter,
        constant=False,
        name="arterial blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ar"],
    ),
    Compartment(
        "Vurine",
        metaId="meta_Vurine",
        value=1,
        unit=U.liter,
        constant=True,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["urine"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Vpo",
        metaId="meta_Vpo",
        value=1,
        unit=U.liter,
        constant=False,
        name="portal plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["po"],
    ),
    Compartment(
        "Vhv",
        metaId="meta_Vhv",
        value=1,
        unit=U.liter,
        constant=False,
        name="hepatic venous plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["hv"],
    ),
]

# create plasma and tissue compartments (for correct blood volume)
for cid in COMPARTMENTS_BODY:
    if cid not in ["ar", "ve", "po", "hv"]:
        _m.compartments.extend(
            [
                Compartment(
                    f"V{cid}_tissue",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} tissue",
                    metaId=f"meta_V{cid}_tissue",
                    port=True,
                    annotations=[
                        *annotations.compartments["parenchyma"],
                        *[
                            (BQB.IS_PART_OF, aid[1])
                            for aid in annotations.compartments[cid]
                        ],
                    ],
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                ),
                Compartment(
                    f"V{cid}_plasma",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} plasma",
                    metaId=f"meta_V{cid}_plasma",
                    port=True,
                    annotations=[
                        *annotations.compartments["plasma"],
                        *[
                            (BQB.IS_PART_OF, aid[1])
                            for aid in annotations.compartments[cid]
                        ],
                    ],
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                ),
            ]
        )

# calculate gut lumen
_m.compartments.append(
    Compartment(
        "Vgulumen",
        metaId="meta_Vgulumen",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut lumen",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
    )
)
_m.parameters = [
    Parameter("f_lumen", 0.9, name="fraction lumen of intestine", unit=U.dimensionless)
]
_m.rules = [
    AssignmentRule("Vgulumen", "f_lumen * Vgu", unit=U.liter),
]


# replace volumes of submodels
_m.replaced_elements.extend(
    [
        # kidney
        ReplacedElement(
            sid="Vki_tissue_RE",
            metaId="Vki_tissue_RE",
            elementRef="Vki_tissue",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vki{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vki_plasma_RE",
            metaId="Vki_plasma_RE",
            elementRef="Vki_plasma",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vurine_RE",
            metaId="Vurine_RE",
            elementRef="Vurine",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vurine{PORT_SUFFIX}",
        ),
        # liver
        ReplacedElement(
            sid="Vli_tissue_RE",
            metaId="Vli_tissue_RE",
            elementRef="Vli_tissue",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vli{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vli_plasma_RE",
            metaId="Vli_plasma_RE",
            elementRef="Vli_plasma",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgulumen_RE1",
            metaId="Vgulumen_RE1",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        # intestine
        ReplacedElement(
            sid="Vgu_plasma_RE",
            metaId="Vgu_plasma_RE",
            elementRef="Vgu_plasma",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgulumen_RE2",
            metaId="Vgulumen_RE2",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vfeces_RE",
            metaId="Vfeces_RE",
            elementRef="Vfeces",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vfeces{PORT_SUFFIX}",
        ),
    ]
)

# -------------------------------------------------------------------------------------------------
# Species
# -------------------------------------------------------------------------------------------------
_m.species = []
for sid, sdict in SUBSTANCES_BODY.items():
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}"
        else:
            # plasma compartment
            sid_ex = f"C{cid}_plasma_{sid}"
            cid_ex = f"V{cid}_plasma"

        _m.species.append(
            Species(
                sid_ex,
                metaId=f"meta_{sid_ex}",
                initialConcentration=sdict["cinit"],
                compartment=cid_ex,
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} ({cname} plasma)",
                hasOnlySubstanceUnits=False,
                port=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )

    # tissue species
    for cid, cname in COMPARTMENTS_BODY.items():
        if "ftissue" in sdict and cid not in ["ve", "ar", "li", "ki", "gu", "po", "hv"]:
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}_tissue"

            _m.species.extend(
                [
                    Species(
                        sid_ex,
                        metaId=f"meta_{sid_ex}",
                        initialConcentration=sdict["cinit"],
                        compartment=cid_ex,
                        substanceUnit=sdict["unit"],
                        name=f"{sdict['name']} ({cname})",
                        hasOnlySubstanceUnits=False,
                        port=True,
                        sboTerm=SBO.SIMPLE_CHEMICAL,
                        annotations=annotations.species[sid],
                    )
                ]
            )

    # urine metabolites dummy species
    if sid in ["tm"]:
        _m.species.extend(
            [
                Species(
                    f"Aurine_{sid}",
                    metaId=f"meta_Aurine_{sid}",
                    initialConcentration=0,
                    compartment="Vurine",
                    substanceUnit=sdict["unit"],
                    name=f"{sdict['name']} (urine)",
                    hasOnlySubstanceUnits=True,
                    sboTerm=SBO.SIMPLE_CHEMICAL,
                    annotations=annotations.species[sid],
                ),
            ]
        )

    # feces metabolites
    if sid in ["tm"]:
        _m.species.append(
            Species(
                f"Afeces_{sid}",
                metaId=f"meta_Afeces_{sid}",
                initialConcentration=0,
                compartment="Vfeces",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (feces)",
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )
        _m.species.append(
            Species(
                f"Clumen_{sid}",
                metaId=f"meta_Clumen_{sid}",
                initialConcentration=0,
                compartment="Vgulumen",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (lumen)",
                hasOnlySubstanceUnits=False,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )

# replace species
replaced_species = {
    "li": ["tm"],
    "ki": ["tm"],
    "gu": [],
}

# blood to external species
for tkey, skey_list in replaced_species.items():
    for skey in skey_list:
        _m.replaced_elements.extend(
            [
                ReplacedElement(
                    sid=f"C{tkey}_plasma_{skey}_RE",
                    metaId=f"C{tkey}_plasma_{skey}_RE",
                    elementRef=f"C{tkey}_plasma_{skey}",
                    submodelRef=SUBMODEL_SID_DICT[tkey],
                    portRef=f"{skey}_ext{PORT_SUFFIX}",
                ),
            ]
        )

# urine species replacements
for skey in ["tm"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Aurine_{skey}_RE",
            metaId=f"Aurine_{skey}_RE",
            elementRef=f"Aurine_{skey}",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"{skey}_urine{PORT_SUFFIX}",
        )
    )

# feces species replacements
for skey in ["tm"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Afeces_{skey}_RE",
            metaId=f"Afeces_{skey}_RE",
            elementRef=f"Afeces_{skey}",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"{skey}_feces{PORT_SUFFIX}",
        )
    )

# intestine species replacements
for skey in ["tm"]:
    _m.replaced_elements.extend(
        [
            ReplacedElement(
                sid=f"Clumen_{skey}_RE1",
                metaId=f"Clumen_{skey}_RE1",
                elementRef=f"Clumen_{skey}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{skey}_lumen{PORT_SUFFIX}",
            ),
            ReplacedElement(
                sid=f"Clumen_{skey}_RE2",
                metaId=f"Clumen_{skey}_RE2",
                elementRef=f"Clumen_{skey}",
                submodelRef=SUBMODEL_SID_DICT["li"],
                portRef=f"{skey}_lumen{PORT_SUFFIX}",
            ),
        ]
    )

# -------------------------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------------------------
_m.parameters.extend(
    [
        # whole body data
        Parameter(
            "BW",
            75,
            U.kg,
            constant=True,
            name="body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "BW_ref",
            75,
            U.kg,
            constant=True,
            name="reference body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes=(
                "Body weight at which the exchange flows of the tissue "
                "distribution (`ftissue_<sid>`) are given; they scale with the "
                "body weight as the volumes, the blood flows and the renal "
                "clearance do."
            ),
        ),
        Parameter(
            "HEIGHT",
            170,
            U.cm,
            constant=True,
            name="height [cm]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HR",
            70,
            U.per_min,
            constant=True,
            name="heart rate [1/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HRrest",
            70,
            U.per_min,
            constant=True,
            name="heart rate [1/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "MAP",
            100,
            U.mmHg,
            constant=True,
            name="mean arterial pressure [mmHg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "BSA",
            0,
            U.m2,
            constant=False,
            name="body surface area [m^2]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "COBW",
            1.548,
            U.ml_per_s_kg,
            constant=True,
            name="cardiac output per bodyweight [ml/s/kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "f_cardiac_function",
            1.0,
            U.dimensionless,
            constant=False,
            name="heart function",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            1.0: normal function;
            <1.0: reduced function as reduced cardiac output;
            """,
        ),
        Parameter(
            "CO",
            108.33,
            U.ml_per_s,
            constant=False,
            name="cardiac output [ml/s]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "QC",
            108.33 * 1000 * 60,
            U.l_per_min,
            constant=False,
            name="cardiac output [L/hr]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "COHRI",
            150,
            U.ml,
            constant=True,
            name="increase of cardiac output per heartbeat [ml/min*min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue volumes
        Parameter(
            "Fblood",
            0.02,
            U.dimensionless,
            constant=False,
            name="blood fraction of organ volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HCT",
            0.51,
            U.dimensionless,
            constant=True,
            metaId="meta_HCT",
            name="hematocrit",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue volumes
        Parameter(
            "FVgu",
            0.0171,
            U.l_per_kg,
            constant=True,
            name="gut fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVki",
            0.0044,
            U.l_per_kg,
            constant=True,
            name="kidney fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVli",
            0.0210,
            U.l_per_kg,
            constant=True,
            name="liver fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVlu",
            0.0076,
            U.l_per_kg,
            constant=True,
            name="lung fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVre",
            0,
            U.l_per_kg,
            constant=False,
            name="rest of body fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # calculated based on other tissues
        Parameter(
            "FVve",
            0.0514,
            U.l_per_kg,
            constant=True,
            name="venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVar",
            0.0257,
            U.l_per_kg,
            constant=True,
            name="arterial fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVpo",
            0.001,
            U.l_per_kg,
            constant=True,
            name="portal fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVhv",
            0.001,
            U.l_per_kg,
            constant=True,
            name="hepatic venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue blood flows
        Parameter(
            "FQgu",
            0.18,
            U.dimensionless,
            constant=True,
            name="gut fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
        Assumed FQgu is the sum of FQgu + FQsp + FQpa for correct portal blood flow.
        with FQgu=0.146, FQsp=0.017, FQpa=0.017
        """,
        ),
        Parameter(
            "FQki",
            0.190,
            U.dimensionless,
            constant=True,
            name="kidney fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQh",
            0.215,
            U.dimensionless,
            constant=True,
            name="hepatic (venous side) fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQlu",
            1,
            U.dimensionless,
            constant=True,
            name="lung fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQre",
            0,
            U.dimensionless,
            constant=False,
            name="rest of body fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "conversion_min_per_day",
            1440,
            U.min_per_day,
            constant=True,
            name="Conversion factor min to hours",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "f_cirrhosis",
            0,
            U.dimensionless,
            constant=True,
            name="severity of cirrhosis [0, 0.95]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (BQB.IS, "ncit/C2951"),  # Cirrhosis
                (BQB.IS, "efo/0001422"),  # cirrhosis of liver
            ],
        ),
        Parameter(
            "f_shunts",
            0,
            U.dimensionless,
            constant=False,
            name="fraction of portal venous blood shunted by the liver",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (
                    BQB.IS,
                    "hp/HP:0002629",
                ),  # Gastrointestinal arteriovenous malformation
            ],
        ),
        Parameter(
            "f_tissue_loss",
            0,
            U.dimensionless,
            constant=False,
            name="fraction of lost parenchymal liver volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
    ]
)


for sid, sdict in SUBSTANCES_BODY.items():
    if "PODOSE" in sdict:
        # Parameter for intestine model
        _m.parameters.extend(
            [
                Parameter(
                    f"PODOSE_{sid}",
                    sdict["PODOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"oral dose {sid} [mg]",
                ),
            ]
        )
        _m.replaced_elements.extend(
            [
                ReplacedElement(
                    sid=f"PODOSE_{sid}_RE",
                    metaId=f"PODOSE_{sid}_RE",
                    elementRef=f"PODOSE_{sid}",
                    submodelRef=SUBMODEL_SID_DICT["gu"],
                    portRef=f"PODOSE_{sid}{PORT_SUFFIX}",
                ),
            ]
        )

_m.rules.extend(
    [
        AssignmentRule("f_shunts", "f_cirrhosis", unit=U.dimensionless),
        AssignmentRule("f_tissue_loss", "f_cirrhosis", unit=U.dimensionless),
    ]
)

# renal function
_m.parameters.extend(
    [
        Parameter(
            "f_GFR_Qki",
            101 / 1.32354,
            U.ml_per_l,
            constant=True,
            name="relationship GFR and Qki",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            GFR per renal blood flow (76.3 ml/l, a ratio of 0.0763). Calibrated
            so that the healthy GFR is 101 ml/min at the renal blood flow of
            1.32354 l/min of 75 kg, the normal GFR of the classes of renal
            impairment (`pkpdsim.impairment`).
            """,
        ),
        Parameter(
            "GFR_base",
            np.nan,
            U.ml_per_min,
            constant=False,
            name="glomerular filtration rate (healthy)",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            The GFR of healthy kidneys, which scales with the renal blood flow
            and so with the body weight; the GFR is `KI__f_renal_function`
            times this rate.
            """,
        ),
    ]
)

replaced_parameters: dict[str, list[str]] = {
    "li": [],
    "gu": [],
    "ki": ["GFR_base"],
}

for ckey, pids in replaced_parameters.items():
    for pid in pids:
        _m.replaced_elements.append(
            ReplacedElement(
                sid=f"{pid}_{ckey}_RE",
                metaId=f"{pid}_{ckey}_RE",
                elementRef=f"{pid}",
                submodelRef=SUBMODEL_SID_DICT[ckey],
                portRef=f"{pid}{PORT_SUFFIX}",
            )
        )

# species specific parameters
for sid, sdict in SUBSTANCES_BODY.items():
    _m.parameters.extend(
        [
            # molecular weights
            Parameter(
                f"Mr_{sid}",
                sdict["Mr"],
                U.g_per_mole,
                constant=True,
                name=f"Molecular weight {sid} [g/mole]",
                sboTerm=SBO.MOLECULAR_MASS,
            ),
        ]
    )

    # tissue distribution
    if "ftissue" in sdict:
        _m.parameters.extend(
            [
                Parameter(
                    f"ftissue_{sid}",
                    sdict["ftissue"],
                    U.l_per_min,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"tissue distribution {sid}",
                    notes="Exchange flow at the reference body weight `BW_ref`.",
                ),
                Parameter(
                    f"Kp_{sid}",
                    **FITS.parameter(f"Kp_{sid}", unit=U.dimensionless),
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"tissue/plasma partition coefficient {sid}",
                ),
            ]
        )

# -------------------------------------------------------------------------------------------------
# AssignmentRules
# -------------------------------------------------------------------------------------------------
_m.rules.extend(
    [
        # Rest body volume
        AssignmentRule(
            "FVre",
            "1.0 l_per_kg - (FVgu + FVki + FVli + FVlu + FVve + FVar)",
            U.l_per_kg,
        ),
        # Rest body perfusion
        AssignmentRule("FQre", "1.0 dimensionless - (FQki + FQh)", U.dimensionless),
        # Body surface area (Haycock1978)
        AssignmentRule(
            "BSA",
            "0.024265 m2 * power(BW/1 kg, 0.5378) * power(HEIGHT/1 cm, 0.3964)",
            U.m2,
        ),
        # cardiac output (depending on heart rate and bodyweight)
        AssignmentRule(
            "CO",
            "f_cardiac_function*BW*COBW + (HR-HRrest)*COHRI / 60 s_per_min",
            U.ml_per_s,
        ),
        # cardiac output (depending on bodyweight)
        AssignmentRule("QC", "CO/1000 ml_per_l * 60 s_per_min", U.l_per_min),
        # volumes
        AssignmentRule("Vgu", "BW*FVgu", U.liter),
        AssignmentRule("Vki", "BW*FVki", U.liter),
        AssignmentRule("Vli", "BW*FVli", U.liter),
        AssignmentRule("Vlu", "BW*FVlu", U.liter),
        AssignmentRule("Vre", "BW*FVre", U.liter),
        # venous and arterial blood volume (corrected for tissue blood volumes)
        AssignmentRule(
            "Vve",
            "BW*FVve - FVve/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
            U.liter,
        ),
        AssignmentRule(
            "Var",
            "BW*FVar - FVar/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
            U.liter,
        ),
        AssignmentRule(
            "Vpo",
            "(1 dimensionless - HCT) * (BW*FVpo - FVpo/(FVar+FVve+FVpo+FVhv) "
            "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
            U.liter,
        ),
        AssignmentRule(
            "Vhv",
            "(1 dimensionless - HCT) * (BW*FVhv - FVhv/(FVar+FVve+FVpo+FVhv) "
            "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
            U.liter,
        ),
        # blood flows
        AssignmentRule("Qgu", "QC*FQgu", U.l_per_min, name="gut blood flow"),
        AssignmentRule("Qki", "QC*FQki", U.l_per_min, name="kidney blood flow"),
        AssignmentRule(
            "Qh", "QC*FQh", U.l_per_min, name="hepatic (venous side) blood flow"
        ),
        AssignmentRule(
            "Qha", "Qh - Qgu", U.l_per_min, name="hepatic artery blood flow"
        ),
        AssignmentRule("Qlu", "QC*FQlu", U.l_per_min, name="lung blood flow"),
        AssignmentRule("Qre", "QC*FQre", U.l_per_min, name="rest of body blood flow"),
        AssignmentRule("Qpo", "Qgu", U.l_per_min, name="portal blood flow"),
        # glomerular filtration rate of healthy kidneys
        AssignmentRule(
            "GFR_base",
            "f_GFR_Qki * Qki",
            U.ml_per_min,
            name="glomerular filtration rate (healthy)",
        ),
    ]
)

# Volumes for explicit tissue models
for cid, cname in COMPARTMENTS_BODY.items():
    if cid not in ["ve", "ar", "po", "hv"]:
        _m.rules.append(
            # plasma volume associated with tissue
            AssignmentRule(
                f"V{cid}_plasma",
                value=f"V{cid} * Fblood * (1 dimensionless - HCT)",
                unit=U.liter,
                name=f"plasma volume of {cname}",
            ),
        )

        if cid == "li":
            _m.rules.append(
                # Cirrhosis: Adjustment of fractional liver tissue volume
                AssignmentRule(
                    f"V{cid}_tissue",
                    value=f"V{cid}*(1 dimensionless - f_tissue_loss) * (1 dimensionless - Fblood)",
                    unit=U.liter,
                    name=f"tissue volume of {cname}",
                ),
            )
        else:
            _m.rules.append(
                AssignmentRule(
                    f"V{cid}_tissue",
                    value=f"V{cid}*(1 dimensionless - Fblood)",
                    unit=U.liter,
                    name=f"tissue volume of {cname}",
                ),
            )

# --------------------------------------------------------------------------------------------------
# Reactions
# --------------------------------------------------------------------------------------------------
_m.reactions = []

for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # --------------------
    # tissue distribution
    # --------------------
    if "ftissue" in sdict:
        for cid in COMPARTMENTS_BODY:
            if cid not in ["ve", "ar", "li", "gu", "ki", "po", "hv"]:
                _m.reactions.append(
                    Reaction(
                        sid=f"transport_{cid}_{sid}",
                        name=f"transport {sname}",
                        formula=(
                            f"ftissue_{sid} * BW/BW_ref * (C{cid}_plasma_{sid}*Kp_{sid} - C{cid}_{sid})",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} <-> C{cid}_{sid}",
                        compartment=f"V{cid}_tissue",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                )

    if "IVDOSE" in sdict:
        _m.reactions.extend(
            [
                # --------------------
                # iv dose application
                # --------------------
                Reaction(
                    sid=f"iv_{sid}",
                    name=f"iv {sname}",
                    formula=(f"Ki_{sid}*IVDOSE_{sid}/Mr_{sid}", U.mmole_per_min),
                    equation=f"-> Cve_{sid}",
                    sboTerm=SBO.TRANSPORT_REACTION,
                    annotations=[(BQB.IS, "ncit/C38276")],
                    compartment="Vve",
                ),
            ]
        )

    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            continue
        # --------------------
        # ve -> lung -> ar
        # --------------------
        if cid == "lu":
            rid_in = f"Flow_ve_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"

            rid_out = f"Flow_{cid}_ar_{sid}"
            name_out = f"outflow {cname} {sname}"

            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Cve_{sid}", U.mmole_per_min),
                        equation=f"Cve_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Car_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> ve
        # --------------------
        if cid in ["ki", "re"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_ve_{sid}"
            name_out = f"outflow {cname} {sname}"

            # only distribution in plasma volume
            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> po
        # --------------------
        if cid in ["gu"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_po_{sid}"
            name_out = f"outflow {cname} {sname}"

            _m.reactions.extend(
                [
                    # only distribution in plasma volume
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cpo_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> li
        # po -> li
        # li -> hv -> ve
        # --------------------
        if cid == "li":
            # liver
            _m.reactions.extend(
                [
                    Reaction(
                        sid=f"Flow_arli_li_{sid}",
                        name=f"arterial inflow liver {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*Qha*Car_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Car_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # shunted arterial flow
                    Reaction(
                        sid=f"Flow_arli_hv_{sid}",
                        name="flow arterial shunts",
                        formula=(f"f_shunts*Qha*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # (unshunted) portal flow
                    Reaction(
                        sid=f"Flow_po_li_{sid}",
                        name=f"outflow po {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*Qpo*Cpo_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Cpo_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # portal shunts
                    Reaction(
                        sid=f"Flow_po_hv_{sid}",
                        name="flow portal shunts",
                        formula=(f"f_shunts*Qpo*Cpo_{sid}", U.mmole_per_min),
                        equation=f"Cpo_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_li_hv_{sid}",
                        name=f"outflow liver {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*(Qpo+Qha)*Cli_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Cli_plasma_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_hv_ve_{sid}",
                        name=f"outflow hepatic vein {sname}",
                        formula=(f"Qh*Chv_{sid}", U.mmole_per_min),
                        equation=f"Chv_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )

# --------------------------------------------------------------------------------------------------
# Cleavage/metabolism
# --------------------------------------------------------------------------------------------------
_m.reactions.append(
    Reaction(
        sid="TIR2TM",
        name="proteolytic cleavage and beta-oxidation of tirzepatide (systemic clearance)",
        equation="Cve_tir -> Cve_tm",
        pars=[
            Parameter(
                "TIR2TM_k",
                **FITS.parameter("TIR2TM_k", unit=U.l_per_min),
                constant=True,
                sboTerm=SBO.KINETIC_CONSTANT,
                name="clearance of the cleavage of tirzepatide",
                notes="""
                The clearance at the reference body weight `BW_ref`, it scales
                with the body weight as the volumes do, so that the half-life
                does not depend on the body weight (about 5 days in lean and
                obese subjects). The cleavage takes place in the plasma and
                the tissues; with an exchange much faster than the elimination
                its location does not change the timecourses, it is lumped in
                the venous plasma.
                """,
            ),
        ],
        formula=("TIR2TM_k * BW/BW_ref * Cve_tir", U.mmole_per_min),
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        compartment="Vve",
    )
)

# --------------------------------------------------------------------------------------------------
# Total tirzepatide metabolites
# --------------------------------------------------------------------------------------------------
_m.species.extend(
    [
        Species(
            "Cve_tmtot",
            metaId="meta_Cve_tmtot",
            initialConcentration=0,
            compartment="Vve",
            substanceUnit=U.mmole,
            name="total tirzepatide (plasma)",
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species["tmtot"],
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "Cve_tmtot",
            "Cve_tir + Cve_tm",
            unit=U.mM,
            name="Sum of tirzepatide and tirzepatide metabolites",
            notes="""
        Used for comparison with total plasma radioactivity.
        """,
        ),
    ]
)

# --------------------------------------------------------------------------------------------------
# Dosing and application
# --------------------------------------------------------------------------------------------------
for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # dosing
    if "IVDOSE" in sdict:
        _m.parameters.extend(
            [
                Parameter(
                    f"IVDOSE_{sid}",
                    sdict["IVDOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"IV bolus dose {sid} [mg]",
                ),
                # iv kinetics after application
                Parameter(
                    f"ti_{sid}",
                    10,
                    U.second,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"injection time {sid} [s]",
                ),
                Parameter(
                    f"Ki_{sid}",
                    0.02,
                    U.per_min,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"Ki [1/min] injection {sid}",
                ),
                # continuous infusion
                Parameter(
                    f"Ri_{sid}",
                    0,
                    U.mg_per_min,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"Ri [mg/min] rate of infusion {sid}",
                ),
            ]
        )
        _m.rules.extend(
            [
                AssignmentRule(
                    f"Ki_{sid}",
                    f"0.693 dimensionless/ti_{sid} * 60 s_per_min",
                    U.per_min,
                    name="injection rate IV",
                    notes="""
                log(2) ~ 0.693 used for conversion of half-life injection time to
                injection rate.
                """,
                ),
            ]
        )
        _m.rate_rules.extend(
            [
                # injection of dose
                RateRule(
                    f"IVDOSE_{sid}", f"-iv_{sid}*Mr_{sid} + Ri_{sid}", U.mg_per_min
                )
            ]
        )

    if "SCDOSE" in sdict:
        # subcutaneous application: the dose is moved into the depot with the
        # fast rate Ksc_injection, so that a repeated dose (a change of
        # SCDOSE) adds to the rest of the earlier doses in the depot
        _m.parameters.extend(
            [
                Parameter(
                    f"SCDOSE_{sid}",
                    sdict["SCDOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"subcutaneous dose {sid} [mg]",
                ),
                Parameter(
                    f"SCDEPOT_{sid}",
                    0,
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"subcutaneous depot {sid} [mg]",
                ),
                Parameter(
                    f"Ksc_injection_{sid}",
                    100.0,
                    U.per_min,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"subcutaneous injection rate {sid}",
                ),
                Parameter(
                    f"Ksc_{sid}",
                    **FITS.parameter(f"Ksc_{sid}", unit=U.per_min),
                    sboTerm=SBO.KINETIC_CONSTANT,
                    name=f"subcutaneous absorption rate {sid}",
                ),
                Parameter(
                    f"Fsc_{sid}",
                    0.8,
                    U.dimensionless,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"subcutaneous bioavailability {sid}",
                    notes="""
                    The absolute bioavailability of a subcutaneous dose of
                    tirzepatide, 80 % (label, EMA assessment report). The rest
                    of the depot is degraded at the injection site to the
                    metabolites, which are excreted (Martin2024: 99 % of the
                    radiolabel recovered).
                    """,
                ),
            ]
        )
        _m.reactions.extend(
            [
                Reaction(
                    sid=f"sc_{sid}",
                    name=f"subcutaneous absorption {sname}",
                    formula=(
                        f"Fsc_{sid} * Ksc_{sid} * SCDEPOT_{sid}/Mr_{sid}",
                        U.mmole_per_min,
                    ),
                    equation=f"-> Cve_{sid}",
                    sboTerm=SBO.TRANSPORT_REACTION,
                    annotations=[(BQB.IS, "ncit/C38299")],
                    compartment="Vve",
                ),
                Reaction(
                    sid=f"sc_deg_{sid}",
                    name=f"subcutaneous degradation {sname}",
                    formula=(
                        f"(1 dimensionless - Fsc_{sid}) * Ksc_{sid} * SCDEPOT_{sid}/Mr_{sid}",
                        U.mmole_per_min,
                    ),
                    equation="-> Cve_tm",
                    sboTerm=SBO.BIOCHEMICAL_REACTION,
                    compartment="Vve",
                ),
            ]
        )
        _m.rate_rules.extend(
            [
                RateRule(
                    f"SCDOSE_{sid}",
                    f"-Ksc_injection_{sid}*SCDOSE_{sid}",
                    U.mg_per_min,
                ),
                RateRule(
                    f"SCDEPOT_{sid}",
                    f"Ksc_injection_{sid}*SCDOSE_{sid} - (sc_{sid} + sc_deg_{sid})*Mr_{sid}",
                    U.mg_per_min,
                ),
            ]
        )


model_body: Model = _m


if __name__ == "__main__":
    from pkdb_models.models.tirzepatide import MODEL_BASE_PATH

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_body.sid}.xml",
        model=model_body,
        sbml_level=3,
        sbml_version=2,
    )
