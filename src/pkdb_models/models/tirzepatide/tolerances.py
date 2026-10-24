"""The tolerances of the integrator for the tirzepatide model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, drug: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the tirzepatide model.

    The species of tirzepatide and its metabolites have plasma concentrations
    down to about 1e-6 mM (5 ng/ml) at the end of the studies, and amounts
    down to 1e-9 mmole in the plasma of the organs after a dose of 0.25 mg;
    the doses and the subcutaneous depot (the targets of the rate rules) are
    milligrams.

    Args:
        value: tolerance of the targets of the rate rules, i.e. the doses.
        drug: tolerance of the species, of the amount and of the concentration
            [mmole, mM]; the tolerance of a concentration is multiplied by the
            volume of its compartment.

    Returns:
        The absolute tolerance per state.
    """
    return AbsoluteTolerance(amount=drug, concentration=drug, other=value)


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, drug=1e-16)
