"""Kidney model for tirzepatide."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import (
    SBO,
)

from pkdb_models.models.tirzepatide.models import annotations, templates
from pkdb_models.models.tirzepatide.models.fits import FITS


class U(templates.U):
    """Units of the kidney model."""

    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


mid = "tirzepatide_kidney"
version = 1

_m = Model(
    sid=mid,
    name="Model for the renal excretion of the tirzepatide metabolites.",
    notes=f"""
    Model for the renal excretion of the tirzepatide metabolites.

    Tirzepatide is not excreted in the urine; its metabolites are filtered
    with a clearance relative to the glomerular filtration rate (GFR), which
    scales with the renal function.

    **version** {version}
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        value=1.5,
        unit=U.liter,
        name="plasma",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["plasma"],
        port=True,
    ),
    Compartment(
        "Vki",
        value=0.3,  # 0.4 % of bodyweight
        unit=U.liter,
        name="kidney",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
        port=True,
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = [
    Species(
        "tm_ext",
        name="tirzepatide metabolites (plasma)",
        initialConcentration=0.0,
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,  # this is a concentration
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tm"],
        port=True,
    ),
    Species(
        "tm_urine",
        name="tirzepatide metabolites (urine)",
        initialConcentration=0.0,
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tm"],
        port=True,
    ),
]

_m.parameters.extend(
    [
        Parameter(
            "f_renal_function",
            name="renal function",
            value=1.0,
            unit=U.dimensionless,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            >1.0: increased kidney function
            1.0: normal kidney function (healthy control)
            <1.0: decreased kidney function

            Renal function relative to the healthy glomerular filtration rate
            GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
            clearance or eGFR of X ml/min is the renal function X/101.
            """,
        ),
        Parameter(
            "GFR_base",
            101,
            U.ml_per_min,
            name="glomerular filtration rate (healthy)",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            port=True,
        ),
        Parameter(
            "TMEX_f",
            **FITS.parameter("KI__TMEX_f", unit=U.dimensionless),
            name="renal clearance of the tirzepatide metabolites relative to the GFR",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
            The renal clearance of the metabolites of tirzepatide is TMEX_f
            times the GFR. The metabolites carry the C20 fatty diacid and the
            linker of tirzepatide and are largely bound to albumin, so that
            their clearance is a small fraction of the GFR. Tirzepatide itself
            is not excreted in the urine (Martin2024: no intact tirzepatide in
            urine or feces).
            """,
        ),
    ]
)

_m.rules.append(
    AssignmentRule(
        "GFR",
        "f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
)

_m.reactions = [
    Reaction(
        sid="TMEX",
        name="renal excretion of the tirzepatide metabolites (TMEX)",
        equation="tm_ext -> tm_urine",
        compartment="Vki",
        sboTerm=SBO.TRANSPORT_REACTION,
        # [ml/min] * [l/ml] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * TMEX_f * tm_ext",
            U.mmole_per_min,
        ),
    ),
]

model_kidney = _m


if __name__ == "__main__":
    from sbmlode import OdeSystem

    from pkdb_models.models.tirzepatide import MODEL_BASE_PATH

    # SBML model
    results: FactoryResult = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_kidney.sid}.md"
    ode_system = OdeSystem.from_sbml(results.sbml_path)
    ode_system.write(md_path)
