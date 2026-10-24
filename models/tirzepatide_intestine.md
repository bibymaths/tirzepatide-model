# Model for the fecal excretion of the tirzepatide metabolites

Model `tirzepatide_intestine`, SBML Level 3 Version 2, read from tirzepatide\_intestine.xml, written by sbmlode 0.3.0.

Model for the fecal excretion of the tirzepatide metabolites

The metabolites which the liver excretes into the intestinal lumen pass a transit chain of n\_chain compartments into the feces, with the same rate TMEXC\_k per step; the mean transit time is (1 + n\_chain)/TMEXC\_k.

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
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vint}_{0}$ | `Vint_0` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{Vint}_{1}$ | `Vint_1` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{Vint}_{2}$ | `Vint_2` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{Vint}_{3}$ | `Vint_3` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{Vint}_{4}$ | `Vint_4` | intestinal lumen (inner part of intestine) |  | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{tm}_{\mathrm{lumen}}$ | `tm_lumen` | tirzepatide metabolites (intestinal lumen) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{feces}}$ | `tm_feces` | tirzepatide metabolites (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{tm}_{\mathrm{int\_0}}$ | `tm_int_0` | tirzepatide metabolites (intestinal transit 0) | $\mathrm{Vint}_{0}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{int\_1}}$ | `tm_int_1` | tirzepatide metabolites (intestinal transit 1) | $\mathrm{Vint}_{1}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{int\_2}}$ | `tm_int_2` | tirzepatide metabolites (intestinal transit 2) | $\mathrm{Vint}_{2}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{int\_3}}$ | `tm_int_3` | tirzepatide metabolites (intestinal transit 3) | $\mathrm{Vint}_{3}$ | $0$ | mmol/l | concentration |
| $\mathrm{tm}_{\mathrm{int\_4}}$ | `tm_int_4` | tirzepatide metabolites (intestinal transit 4) | $\mathrm{Vint}_{4}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vchain}$ | `Vchain` | volume of chain compartment | $0.1$ | l | ✓ |
| $\mathrm{TMEXC}_{\mathrm{k}}$ | `TMEXC_k` | rate of the intestinal transit of the tirzepatide metabolites | $0.002$ | 1/min | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{tm}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{Vint}_{0} &= \mathrm{Vchain} \\[1ex]
\mathrm{Vint}_{1} &= \mathrm{Vchain} \\[1ex]
\mathrm{Vint}_{2} &= \mathrm{Vchain} \\[1ex]
\mathrm{Vint}_{3} &= \mathrm{Vchain} \\[1ex]
\mathrm{Vint}_{4} &= \mathrm{Vchain}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{tmEXC}}$ | `tmEXC` | intestinal transit of the tirzepatide metabolites (lumen) | $\mathrm{tm}_{\mathrm{lumen}} \longrightarrow \mathrm{tm}_{\mathrm{int\_0}}$ |
| $v_{\mathrm{tmEXC\_0}}$ | `tmEXC_0` | intestinal transit of the tirzepatide metabolites 0 | $\mathrm{tm}_{\mathrm{int\_0}} \longrightarrow \mathrm{tm}_{\mathrm{int\_1}}$ |
| $v_{\mathrm{tmEXC\_1}}$ | `tmEXC_1` | intestinal transit of the tirzepatide metabolites 1 | $\mathrm{tm}_{\mathrm{int\_1}} \longrightarrow \mathrm{tm}_{\mathrm{int\_2}}$ |
| $v_{\mathrm{tmEXC\_2}}$ | `tmEXC_2` | intestinal transit of the tirzepatide metabolites 2 | $\mathrm{tm}_{\mathrm{int\_2}} \longrightarrow \mathrm{tm}_{\mathrm{int\_3}}$ |
| $v_{\mathrm{tmEXC\_3}}$ | `tmEXC_3` | intestinal transit of the tirzepatide metabolites 3 | $\mathrm{tm}_{\mathrm{int\_3}} \longrightarrow \mathrm{tm}_{\mathrm{int\_4}}$ |
| $v_{\mathrm{tmEXC\_4}}$ | `tmEXC_4` | intestinal transit of the tirzepatide metabolites 4 | $\mathrm{tm}_{\mathrm{int\_4}} \longrightarrow \mathrm{tm}_{\mathrm{feces}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{tmEXC}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{tm}_{\mathrm{lumen}} \\[1ex]
v_{\mathrm{tmEXC\_0}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vint}_{0} \cdot \mathrm{tm}_{\mathrm{int\_0}} \\[1ex]
v_{\mathrm{tmEXC\_1}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vint}_{1} \cdot \mathrm{tm}_{\mathrm{int\_1}} \\[1ex]
v_{\mathrm{tmEXC\_2}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vint}_{2} \cdot \mathrm{tm}_{\mathrm{int\_2}} \\[1ex]
v_{\mathrm{tmEXC\_3}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vint}_{3} \cdot \mathrm{tm}_{\mathrm{int\_3}} \\[1ex]
v_{\mathrm{tmEXC\_4}} &= \mathrm{TMEXC}_{\mathrm{k}} \cdot \mathrm{Vint}_{4} \cdot \mathrm{tm}_{\mathrm{int\_4}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{tmEXC}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{tmEXC\_4}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{int\_0}}}{\mathrm{d} t} &= \frac{v_{\mathrm{tmEXC}} - v_{\mathrm{tmEXC\_0}}}{\mathrm{Vint}_{0}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{int\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{tmEXC\_0}} - v_{\mathrm{tmEXC\_1}}}{\mathrm{Vint}_{1}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{int\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{tmEXC\_1}} - v_{\mathrm{tmEXC\_2}}}{\mathrm{Vint}_{2}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{int\_3}}}{\mathrm{d} t} &= \frac{v_{\mathrm{tmEXC\_2}} - v_{\mathrm{tmEXC\_3}}}{\mathrm{Vint}_{3}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{tm}_{\mathrm{int\_4}}}{\mathrm{d} t} &= \frac{v_{\mathrm{tmEXC\_3}} - v_{\mathrm{tmEXC\_4}}}{\mathrm{Vint}_{4}}
\end{aligned}
$$
