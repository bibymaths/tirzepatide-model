"""Liver model for tirzepatide: the biliary excretion of its metabolites."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import (
    SBO,
)

from pkdb_models.models.tirzepatide.models import annotations, templates
from pkdb_models.models.tirzepatide.models.fits import FITS


class U(templates.U):
    """Units of the liver model."""


mid = "tirzepatide_liver"
version = 2

_m = Model(
    sid=mid,
    name="Model for the biliary excretion of the tirzepatide metabolites.",
    notes=f"""
    # Model for the biliary excretion of the tirzepatide metabolites

    The metabolites of tirzepatide are taken up from the plasma of the liver
    and excreted into the bile, i.e. into the intestinal lumen, in one step
    (`TMBEX`); the amounts in the hepatocytes and the bile are not resolved.
    Tirzepatide itself is not excreted in the bile (Martin2024: no intact
    tirzepatide in urine or feces).

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
        "Vli",
        value=1.5,
        unit=U.liter,
        name="liver",
        constant=True,
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
        port=True,
    ),
    Compartment(
        "Vlumen",
        # the value is replaced by the lumen of the whole-body model (comp)
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
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
        "tm_lumen",
        initialConcentration=0.0,
        name="tirzepatide metabolites (lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tm"],
        port=True,
    ),
]

_m.reactions = [
    Reaction(
        sid="TMBEX",
        name="biliary excretion of the tirzepatide metabolites (TMBEX)",
        equation="tm_ext -> tm_lumen",
        compartment="Vli",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "TMBEX_k",
                **FITS.parameter("LI__TMBEX_k", unit=U.per_min),
                name="rate of the biliary excretion of the tirzepatide metabolites",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""
                The biliary clearance of the metabolites is TMBEX_k times the
                volume of the liver.
                """,
            )
        ],
        formula=("TMBEX_k * Vli * tm_ext", U.mmole_per_min),
    ),
]


model_liver = _m


if __name__ == "__main__":
    from sbmlode import OdeSystem

    from pkdb_models.models.tirzepatide import MODEL_BASE_PATH

    results: FactoryResult = create_model(
        model=model_liver,
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_liver.sid}.md"
    ode_system = OdeSystem.from_sbml(results.sbml_path)
    ode_system.write(md_path)
