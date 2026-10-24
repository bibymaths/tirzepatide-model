# Model for the biliary excretion of the tirzepatide metabolites.

Model `tirzepatide_liver`, SBML Level 3 Version 2, read from tirzepatide\_liver.xml, written by sbmlode 0.3.0.

Model for the biliary excretion of the tirzepatide metabolites

The metabolites of tirzepatide are taken up from the plasma of the liver and excreted into the bile, i.e. into the intestinal lumen, in one step (TMBEX); the amounts in the hepatocytes and the bile are not resolved. Tirzepatide itself is not excreted in the bile (Martin2024: no intact tirzepatide in urine or feces).

version 2

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vext}$ | `Vext` | plasma | $1.5$ | l | ✓ |
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{tm}_{\mathrm{ext}}$ | `tm_ext` | tirzepatide metabolites (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{lumen}}$ | `tm_lumen` | tirzepatide metabolites (lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{TMBEX}_{\mathrm{k}}$ | `TMBEX_k` | rate of the biliary excretion of the tirzepatide metabolites | $0.000384446508207574$ | 1/min | ✓ |

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{TMBEX}}$ | `TMBEX` | biliary excretion of the tirzepatide metabolites (TMBEX) | $\mathrm{tm}_{\mathrm{ext}} \longrightarrow \mathrm{tm}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{TMBEX}} &= \mathrm{TMBEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{tm}_{\mathrm{ext}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{TMBEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{TMBEX}}}{\mathrm{Vlumen}}
\end{aligned}
$$
