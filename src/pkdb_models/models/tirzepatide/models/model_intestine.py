"""Intestine model for tirzepatide: the fecal excretion of its metabolites."""

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


class U(templates.U):
    """Units of the intestine model."""


_m = Model(
    "tirzepatide_intestine",
    name="Model for the fecal excretion of the tirzepatide metabolites",
    notes="""
    # Model for the fecal excretion of the tirzepatide metabolites

    The metabolites which the liver excretes into the intestinal lumen pass
    a transit chain of `n_chain` compartments into the feces, with the same
    rate `TMEXC_k` per step; the mean transit time is (1 + n_chain)/TMEXC_k.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
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
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
]

#: the number of compartments of the transit chain after the lumen
n_chain = 5

_m.parameters = [
    Parameter(
        "Vchain",
        0.1,
        unit=U.liter,
        name="volume of chain compartment",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
]

for k in range(n_chain):
    # compartments for chain
    _m.compartments.append(
        Compartment(
            f"Vint_{k}",
            "Vchain",
            name="intestinal lumen (inner part of intestine)",
            sboTerm=SBO.PHYSICAL_COMPARTMENT,
            unit=U.liter,
            annotations=annotations.compartments["gu_lumen"],
            constant=False,
        ),
    )


_m.species = [
    Species(
        "tm_lumen",
        initialConcentration=0.0,
        name="tirzepatide metabolites (intestinal lumen)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tm"],
        port=True,
    ),
    Species(
        "tm_feces",
        initialConcentration=0.0,
        name="tirzepatide metabolites (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["tm"],
        port=True,
    ),
]

for k in range(n_chain):
    # species for chain
    _m.species.append(
        Species(
            f"tm_int_{k}",
            initialConcentration=0.0,
            name=f"tirzepatide metabolites (intestinal transit {k})",
            compartment=f"Vint_{k}",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=False,
            sboTerm=SBO.SIMPLE_CHEMICAL,
            annotations=annotations.species["tm"],
        ),
    )


_m.reactions = [
    Reaction(
        sid="tmEXC",
        name="intestinal transit of the tirzepatide metabolites (lumen)",
        compartment="Vlumen",
        equation="tm_lumen -> tm_int_0",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "TMEXC_k",
                2.0e-3,
                unit=U.per_min,
                name="rate of the intestinal transit of the tirzepatide metabolites",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""
                The rate per step of the transit chain from the intestinal
                lumen into the feces; the mean transit time is
                (1 + n_chain)/TMEXC_k = 50 hr, the whole gut transit time of
                about 2 days. Not fitted: the cumulative recovery in the feces
                (Martin2024) does not identify it (profile likelihood flat
                over a mean transit of 12 hr to 5 days).
                """,
            ),
        ],
        formula=("TMEXC_k * Vlumen * tm_lumen", U.mmole_per_min),
    ),
]

for k in range(n_chain):
    # reactions for chain
    source = f"tm_int_{k}"
    target = f"tm_int_{k + 1}" if k < n_chain - 1 else "tm_feces"
    _m.reactions.append(
        Reaction(
            sid=f"tmEXC_{k}",
            name=f"intestinal transit of the tirzepatide metabolites {k}",
            compartment="Vlumen",
            equation=f"{source} -> {target}",
            sboTerm=SBO.TRANSPORT_REACTION,
            formula=(
                f"TMEXC_k * Vint_{k} * {source}",
                U.mmole_per_min,
            ),
        ),
    )


model_intestine = _m


if __name__ == "__main__":
    from sbmlode import OdeSystem

    from pkdb_models.models.tirzepatide import MODEL_BASE_PATH

    # SBML model
    results: FactoryResult = create_model(
        model=model_intestine,
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )

    # create differential equations
    md_path = MODEL_BASE_PATH / f"{model_intestine.sid}.md"
    ode_system = OdeSystem.from_sbml(results.sbml_path)
    ode_system.write(md_path)
