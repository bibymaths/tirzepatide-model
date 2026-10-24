"""Annotations of the tirzepatide models: the species.

The compartments are the shared ones of `pkpdsim.annotations`.
"""

from pkpdsim.annotations import compartments
from sbmlutils.metadata import (
    BQB,
)

__all__ = ["compartments", "species"]

species = {
    "tir": [  # tirzepatide
        (BQB.IS, "chebi/CHEBI:194186"),
        (BQB.IS, "ncit/C174817"),
        (BQB.IS, "pubchem.compound/163285897"),
        (BQB.IS, "inchikey/BTSOGEDATSQOAF-SMAAHMJQSA-N"),
    ],
    "tm": [  # tirzepatide metabolites
    ],
    "tmtot": [  # tirzepatide + tirzepatide metabolites
    ],
}
