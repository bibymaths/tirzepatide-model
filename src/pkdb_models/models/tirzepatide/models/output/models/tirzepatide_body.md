# Tirzepatide body model

Model `tirzepatide_body`, SBML Level 3 Version 2, read from tirzepatide\_body.xml, written by sbmlode 0.3.0.

Tirzepatide body model

Physiological based pharmacokinetic (PBPK) model of tirzepatide in Human.

Tirzepatide is given subcutaneously: the dose enters a depot, from which the fraction Fsc\_tir (the absolute bioavailability, 80 %) is absorbed into the venous plasma and the rest is degraded at the injection site to the metabolites. Tirzepatide is bound to albumin (99 %) and distributes with it into the interstitial space of the tissues (ftissue\_tir, Kp\_tir). It is eliminated by proteolytic cleavage of the peptide backbone and beta-oxidation of the C20 fatty diacid (TIR2TM), which scales with the body weight; tirzepatide itself is not excreted. The metabolites are excreted in the urine with a clearance relative to the glomerular filtration rate (kidney submodel) and in the bile (liver submodel), from where they reach the feces through an intestinal transit chain (intestine submodel).

The metabolites are one species counted in tirzepatide equivalents (the molecular weight of tirzepatide), which is what the measurements of the radiolabel are (ng-eq/ml, % of the dose). They keep the C20 fatty diacid and distribute into a slow tissue pool (ftissue\_tm, Kp\_tm), from which they return to the plasma and are excreted over weeks: tirzepatide is about 80 % of the radioactivity in plasma, while the excretion of the radiolabel lags behind the cleavage (Martin2024).

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
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{Vgulumen}$ | `Vgulumen` | gut lumen |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vint\_0}}$ | `GU__Vint_0` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vint\_1}}$ | `GU__Vint_1` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vint\_2}}$ | `GU__Vint_2` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vint\_3}}$ | `GU__Vint_3` | intestinal lumen (inner part of intestine) |  | l |  |
| $\mathrm{GU}_{\mathrm{\_Vint\_4}}$ | `GU__Vint_4` | intestinal lumen (inner part of intestine) |  | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cki}_{\mathrm{plasma\_tir}}$ | `Cki_plasma_tir` | tirzepatide (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_tir}}$ | `Cli_plasma_tir` | tirzepatide (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_tir}}$ | `Clu_plasma_tir` | tirzepatide (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_tir}}$ | `Cgu_plasma_tir` | tirzepatide (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_tir}}$ | `Cre_plasma_tir` | tirzepatide (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{tir}}$ | `Car_tir` | tirzepatide (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{tir}}$ | `Cve_tir` | tirzepatide (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{tir}}$ | `Cpo_tir` | tirzepatide (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{tir}}$ | `Chv_tir` | tirzepatide (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{tir}}$ | `Clu_tir` | tirzepatide (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{tir}}$ | `Cre_tir` | tirzepatide (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_tm}}$ | `Cki_plasma_tm` | tirzepatide metabolites (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_tm}}$ | `Cli_plasma_tm` | tirzepatide metabolites (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_tm}}$ | `Clu_plasma_tm` | tirzepatide metabolites (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_tm}}$ | `Cgu_plasma_tm` | tirzepatide metabolites (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_tm}}$ | `Cre_plasma_tm` | tirzepatide metabolites (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{tm}}$ | `Car_tm` | tirzepatide metabolites (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{tm}}$ | `Cve_tm` | tirzepatide metabolites (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{tm}}$ | `Cpo_tm` | tirzepatide metabolites (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{tm}}$ | `Chv_tm` | tirzepatide metabolites (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{tm}}$ | `Clu_tm` | tirzepatide metabolites (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{tm}}$ | `Cre_tm` | tirzepatide metabolites (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{tm}}$ | `Aurine_tm` | tirzepatide metabolites (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{tm}}$ | `Afeces_tm` | tirzepatide metabolites (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Clumen}_{\mathrm{tm}}$ | `Clumen_tm` | tirzepatide metabolites (lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{tmtot}}$ | `Cve_tmtot` | total tirzepatide (plasma) | $\mathrm{Vve}$ |  | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tm\_int\_0}}$ | `GU__tm_int_0` | tirzepatide metabolites (intestinal transit 0) | $\mathrm{GU}_{\mathrm{\_Vint\_0}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tm\_int\_1}}$ | `GU__tm_int_1` | tirzepatide metabolites (intestinal transit 1) | $\mathrm{GU}_{\mathrm{\_Vint\_1}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tm\_int\_2}}$ | `GU__tm_int_2` | tirzepatide metabolites (intestinal transit 2) | $\mathrm{GU}_{\mathrm{\_Vint\_2}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tm\_int\_3}}$ | `GU__tm_int_3` | tirzepatide metabolites (intestinal transit 3) | $\mathrm{GU}_{\mathrm{\_Vint\_3}}$ | $0$ | mmol/l | concentration |
| $\mathrm{GU}_{\mathrm{\_tm\_int\_4}}$ | `GU__tm_int_4` | tirzepatide metabolites (intestinal transit 4) | $\mathrm{GU}_{\mathrm{\_Vint\_4}}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{lumen}}$ | `f_lumen` | fraction lumen of intestine | $0.9$ | \- | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $170$ | cm | ✓ |
| $\mathrm{HR}$ | `HR` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{HRrest}$ | `HRrest` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{MAP}$ | `MAP` | mean arterial pressure \[mmHg\] | $100$ | (133.322 N)/m<sup>2</sup> | ✓ |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m^2\] |  | m<sup>2</sup> |  |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.548$ | ml/s/kg | ✓ |
| $f_{\mathrm{cardiac\_function}}$ | `f_cardiac_function` | heart function | $1$ | \- |  |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[L/hr\] |  | l/min |  |
| $\mathrm{COHRI}$ | `COHRI` | increase of cardiac output per heartbeat \[ml/min\*min\] | $150$ | ml | ✓ |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- |  |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgu}$ | `FVgu` | gut fractional tissue volume | $0.0171$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | Conversion factor min to hours | $1440$ | min/day | ✓ |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $76.3105006271061$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) |  | ml/min |  |
| $\mathrm{Mr}_{\mathrm{tir}}$ | `Mr_tir` | Molecular weight tir \[g/mole\] | $4813.527$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{tir}}$ | `ftissue_tir` | tissue distribution tir | $0.15$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{tir}}$ | `Kp_tir` | tissue/plasma partition coefficient tir | $0.0355471914083463$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{tm}}$ | `Mr_tm` | Molecular weight tm \[g/mole\] | $4813.527$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{tm}}$ | `ftissue_tm` | tissue distribution tm | $0.036$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{tm}}$ | `Kp_tm` | tissue/plasma partition coefficient tm | $0.146900300619077$ | \- | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{tir}}$ | `IVDOSE_tir` | IV bolus dose tir \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{tir}}$ | `ti_tir` | injection time tir \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{tir}}$ | `Ki_tir` | Ki \[1/min\] injection tir |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{tir}}$ | `Ri_tir` | Ri \[mg/min\] rate of infusion tir | $0$ | mg/min | ✓ |
| $\mathrm{SCDOSE}_{\mathrm{tir}}$ | `SCDOSE_tir` | subcutaneous dose tir \[mg\] | $0$ | mg |  |
| $\mathrm{SCDEPOT}_{\mathrm{tir}}$ | `SCDEPOT_tir` | subcutaneous depot tir \[mg\] | $0$ | mg |  |
| $\mathrm{Ksc}_{\mathrm{injection\_tir}}$ | `Ksc_injection_tir` | subcutaneous injection rate tir | $100$ | 1/min | ✓ |
| $\mathrm{Ksc}_{\mathrm{tir}}$ | `Ksc_tir` | subcutaneous absorption rate tir | $0.00142501769891145$ | 1/min | ✓ |
| $\mathrm{Fsc}_{\mathrm{tir}}$ | `Fsc_tir` | subcutaneous bioavailability tir | $0.8$ | \- | ✓ |
| $\mathrm{TIR2TM}_{\mathrm{k}}$ | `TIR2TM_k` | clearance of the cleavage of tirzepatide | $0.000633701021586756$ | l/min | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_TMEX\_f}}$ | `KI__TMEX_f` | renal clearance of the tirzepatide metabolites relative to the GFR | $0.0121644486427196$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{LI}_{\mathrm{\_TMBEX\_k}}$ | `LI__TMBEX_k` | rate of the biliary excretion of the tirzepatide metabolites | $0.000384446508207574$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_Vchain}}$ | `GU__Vchain` | volume of chain compartment | $0.1$ | l | ✓ |
| $\mathrm{GU}_{\mathrm{\_TMEXC\_k}}$ | `GU__TMEXC_k` | rate of the intestinal transit of the tirzepatide metabolites | $0.002$ | 1/min | ✓ |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Aurine}_{\mathrm{tm}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{tm}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgu} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{BSA} &= 0.024265 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.5378} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.3964} \\[1ex]
\mathrm{CO} &= f_{\mathrm{cardiac\_function}} \cdot \mathrm{BW} \cdot \mathrm{COBW} + \frac{\mathopen{}\left(\mathrm{HR} - \mathrm{HRrest}\right) \cdot \mathrm{COHRI}}{60} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgu} \\[1ex]
\mathrm{Vgulumen} &= f_{\mathrm{lumen}} \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Cve}_{\mathrm{tmtot}} &= \mathrm{Cve}_{\mathrm{tir}} + \mathrm{Cve}_{\mathrm{tm}} \\[1ex]
\mathrm{Ki}_{\mathrm{tir}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{tir}}} \cdot 60 \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vint\_0}} &= \mathrm{GU}_{\mathrm{\_Vchain}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vint\_1}} &= \mathrm{GU}_{\mathrm{\_Vchain}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vint\_2}} &= \mathrm{GU}_{\mathrm{\_Vchain}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vint\_3}} &= \mathrm{GU}_{\mathrm{\_Vchain}} \\[1ex]
\mathrm{GU}_{\mathrm{\_Vint\_4}} &= \mathrm{GU}_{\mathrm{\_Vchain}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{transport\_lu\_tir}}$ | `transport_lu_tir` | transport tirzepatide | $\mathrm{Clu}_{\mathrm{plasma\_tir}} \rightleftharpoons \mathrm{Clu}_{\mathrm{tir}}$ |
| $v_{\mathrm{transport\_re\_tir}}$ | `transport_re_tir` | transport tirzepatide | $\mathrm{Cre}_{\mathrm{plasma\_tir}} \rightleftharpoons \mathrm{Cre}_{\mathrm{tir}}$ |
| $v_{\mathrm{iv\_tir}}$ | `iv_tir` | iv tirzepatide | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_tir}}$ | `Flow_ar_ki_tir` | inflow kidney tirzepatide | $\mathrm{Car}_{\mathrm{tir}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_tir}}$ | `Flow_ki_ve_tir` | outflow kidney tirzepatide | $\mathrm{Cki}_{\mathrm{plasma\_tir}} \longrightarrow \mathrm{Cve}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_arli\_li\_tir}}$ | `Flow_arli_li_tir` | arterial inflow liver tirzepatide | $\mathrm{Car}_{\mathrm{tir}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_arli\_hv\_tir}}$ | `Flow_arli_hv_tir` | flow arterial shunts | $\mathrm{Car}_{\mathrm{tir}} \longrightarrow \mathrm{Chv}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_po\_li\_tir}}$ | `Flow_po_li_tir` | outflow po tirzepatide | $\mathrm{Cpo}_{\mathrm{tir}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_po\_hv\_tir}}$ | `Flow_po_hv_tir` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{tir}} \longrightarrow \mathrm{Chv}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_li\_hv\_tir}}$ | `Flow_li_hv_tir` | outflow liver tirzepatide | $\mathrm{Cli}_{\mathrm{plasma\_tir}} \longrightarrow \mathrm{Chv}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_tir}}$ | `Flow_hv_ve_tir` | outflow hepatic vein tirzepatide | $\mathrm{Chv}_{\mathrm{tir}} \longrightarrow \mathrm{Cve}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_tir}}$ | `Flow_ve_lu_tir` | inflow lung tirzepatide | $\mathrm{Cve}_{\mathrm{tir}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_tir}}$ | `Flow_lu_ar_tir` | outflow lung tirzepatide | $\mathrm{Clu}_{\mathrm{plasma\_tir}} \longrightarrow \mathrm{Car}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_tir}}$ | `Flow_ar_gu_tir` | inflow gut tirzepatide | $\mathrm{Car}_{\mathrm{tir}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_gu\_po\_tir}}$ | `Flow_gu_po_tir` | outflow gut tirzepatide | $\mathrm{Cgu}_{\mathrm{plasma\_tir}} \longrightarrow \mathrm{Cpo}_{\mathrm{tir}}$ |
| $v_{\mathrm{Flow\_ar\_re\_tir}}$ | `Flow_ar_re_tir` | inflow rest tirzepatide | $\mathrm{Car}_{\mathrm{tir}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_tir}}$ |
| $v_{\mathrm{Flow\_re\_ve\_tir}}$ | `Flow_re_ve_tir` | outflow rest tirzepatide | $\mathrm{Cre}_{\mathrm{plasma\_tir}} \longrightarrow \mathrm{Cve}_{\mathrm{tir}}$ |
| $v_{\mathrm{transport\_lu\_tm}}$ | `transport_lu_tm` | transport tirzepatide metabolites | $\mathrm{Clu}_{\mathrm{plasma\_tm}} \rightleftharpoons \mathrm{Clu}_{\mathrm{tm}}$ |
| $v_{\mathrm{transport\_re\_tm}}$ | `transport_re_tm` | transport tirzepatide metabolites | $\mathrm{Cre}_{\mathrm{plasma\_tm}} \rightleftharpoons \mathrm{Cre}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_ar\_ki\_tm}}$ | `Flow_ar_ki_tm` | inflow kidney tirzepatide metabolites | $\mathrm{Car}_{\mathrm{tm}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_ki\_ve\_tm}}$ | `Flow_ki_ve_tm` | outflow kidney tirzepatide metabolites | $\mathrm{Cki}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Cve}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_arli\_li\_tm}}$ | `Flow_arli_li_tm` | arterial inflow liver tirzepatide metabolites | $\mathrm{Car}_{\mathrm{tm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_arli\_hv\_tm}}$ | `Flow_arli_hv_tm` | flow arterial shunts | $\mathrm{Car}_{\mathrm{tm}} \longrightarrow \mathrm{Chv}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_po\_li\_tm}}$ | `Flow_po_li_tm` | outflow po tirzepatide metabolites | $\mathrm{Cpo}_{\mathrm{tm}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_po\_hv\_tm}}$ | `Flow_po_hv_tm` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{tm}} \longrightarrow \mathrm{Chv}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_li\_hv\_tm}}$ | `Flow_li_hv_tm` | outflow liver tirzepatide metabolites | $\mathrm{Cli}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Chv}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_hv\_ve\_tm}}$ | `Flow_hv_ve_tm` | outflow hepatic vein tirzepatide metabolites | $\mathrm{Chv}_{\mathrm{tm}} \longrightarrow \mathrm{Cve}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_ve\_lu\_tm}}$ | `Flow_ve_lu_tm` | inflow lung tirzepatide metabolites | $\mathrm{Cve}_{\mathrm{tm}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_lu\_ar\_tm}}$ | `Flow_lu_ar_tm` | outflow lung tirzepatide metabolites | $\mathrm{Clu}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Car}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_ar\_gu\_tm}}$ | `Flow_ar_gu_tm` | inflow gut tirzepatide metabolites | $\mathrm{Car}_{\mathrm{tm}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_gu\_po\_tm}}$ | `Flow_gu_po_tm` | outflow gut tirzepatide metabolites | $\mathrm{Cgu}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Cpo}_{\mathrm{tm}}$ |
| $v_{\mathrm{Flow\_ar\_re\_tm}}$ | `Flow_ar_re_tm` | inflow rest tirzepatide metabolites | $\mathrm{Car}_{\mathrm{tm}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_tm}}$ |
| $v_{\mathrm{Flow\_re\_ve\_tm}}$ | `Flow_re_ve_tm` | outflow rest tirzepatide metabolites | $\mathrm{Cre}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Cve}_{\mathrm{tm}}$ |
| $v_{\mathrm{TIR2TM}}$ | `TIR2TM` | proteolytic cleavage and beta-oxidation of tirzepatide (systemic clearance) | $\mathrm{Cve}_{\mathrm{tir}} \longrightarrow \mathrm{Cve}_{\mathrm{tm}}$ |
| $v_{\mathrm{sc\_tir}}$ | `sc_tir` | subcutaneous absorption tirzepatide | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{tir}}$ |
| $v_{\mathrm{sc\_deg\_tir}}$ | `sc_deg_tir` | subcutaneous degradation tirzepatide | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{tm}}$ |
| $v_{\mathrm{KI\_\_TMEX}}$ | `KI__TMEX` | renal excretion of the tirzepatide metabolites (TMEX) | $\mathrm{Cki}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Aurine}_{\mathrm{tm}}$ |
| $v_{\mathrm{LI\_\_TMBEX}}$ | `LI__TMBEX` | biliary excretion of the tirzepatide metabolites (TMBEX) | $\mathrm{Cli}_{\mathrm{plasma\_tm}} \longrightarrow \mathrm{Clumen}_{\mathrm{tm}}$ |
| $v_{\mathrm{GU\_\_tmEXC}}$ | `GU__tmEXC` | intestinal transit of the tirzepatide metabolites (lumen) | $\mathrm{Clumen}_{\mathrm{tm}} \longrightarrow \mathrm{GU}_{\mathrm{\_tm\_int\_0}}$ |
| $v_{\mathrm{GU\_\_tmEXC\_0}}$ | `GU__tmEXC_0` | intestinal transit of the tirzepatide metabolites 0 | $\mathrm{GU}_{\mathrm{\_tm\_int\_0}} \longrightarrow \mathrm{GU}_{\mathrm{\_tm\_int\_1}}$ |
| $v_{\mathrm{GU\_\_tmEXC\_1}}$ | `GU__tmEXC_1` | intestinal transit of the tirzepatide metabolites 1 | $\mathrm{GU}_{\mathrm{\_tm\_int\_1}} \longrightarrow \mathrm{GU}_{\mathrm{\_tm\_int\_2}}$ |
| $v_{\mathrm{GU\_\_tmEXC\_2}}$ | `GU__tmEXC_2` | intestinal transit of the tirzepatide metabolites 2 | $\mathrm{GU}_{\mathrm{\_tm\_int\_2}} \longrightarrow \mathrm{GU}_{\mathrm{\_tm\_int\_3}}$ |
| $v_{\mathrm{GU\_\_tmEXC\_3}}$ | `GU__tmEXC_3` | intestinal transit of the tirzepatide metabolites 3 | $\mathrm{GU}_{\mathrm{\_tm\_int\_3}} \longrightarrow \mathrm{GU}_{\mathrm{\_tm\_int\_4}}$ |
| $v_{\mathrm{GU\_\_tmEXC\_4}}$ | `GU__tmEXC_4` | intestinal transit of the tirzepatide metabolites 4 | $\mathrm{GU}_{\mathrm{\_tm\_int\_4}} \longrightarrow \mathrm{Afeces}_{\mathrm{tm}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_lu\_tir}} &= \frac{\mathrm{ftissue}_{\mathrm{tir}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_tir}} \cdot \mathrm{Kp}_{\mathrm{tir}} - \mathrm{Clu}_{\mathrm{tir}}\right) \\[1ex]
v_{\mathrm{transport\_re\_tir}} &= \frac{\mathrm{ftissue}_{\mathrm{tir}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_tir}} \cdot \mathrm{Kp}_{\mathrm{tir}} - \mathrm{Cre}_{\mathrm{tir}}\right) \\[1ex]
v_{\mathrm{iv\_tir}} &= \frac{\mathrm{Ki}_{\mathrm{tir}} \cdot \mathrm{IVDOSE}_{\mathrm{tir}}}{\mathrm{Mr}_{\mathrm{tir}}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_tir}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_tir}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_tir}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_tir}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_tir}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_tir}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_tir}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_tir}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_tir}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_tir}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_tir}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_tir}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_tir}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_tir}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_tir}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tir}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_tir}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_tir}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_tir}} \\[1ex]
v_{\mathrm{transport\_lu\_tm}} &= \frac{\mathrm{ftissue}_{\mathrm{tm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_tm}} \cdot \mathrm{Kp}_{\mathrm{tm}} - \mathrm{Clu}_{\mathrm{tm}}\right) \\[1ex]
v_{\mathrm{transport\_re\_tm}} &= \frac{\mathrm{ftissue}_{\mathrm{tm}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_tm}} \cdot \mathrm{Kp}_{\mathrm{tm}} - \mathrm{Cre}_{\mathrm{tm}}\right) \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_tm}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_tm}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_tm}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_tm}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_tm}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_tm}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_tm}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_tm}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_tm}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_tm}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_tm}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_tm}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_tm}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_tm}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{TIR2TM}} &= \frac{\mathrm{TIR2TM}_{\mathrm{k}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathrm{Cve}_{\mathrm{tir}} \\[1ex]
v_{\mathrm{sc\_tir}} &= \frac{\mathrm{Fsc}_{\mathrm{tir}} \cdot \mathrm{Ksc}_{\mathrm{tir}} \cdot \mathrm{SCDEPOT}_{\mathrm{tir}}}{\mathrm{Mr}_{\mathrm{tir}}} \\[1ex]
v_{\mathrm{sc\_deg\_tir}} &= \frac{\mathopen{}\left(1 - \mathrm{Fsc}_{\mathrm{tir}}\right) \cdot \mathrm{Ksc}_{\mathrm{tir}} \cdot \mathrm{SCDEPOT}_{\mathrm{tir}}}{\mathrm{Mr}_{\mathrm{tir}}} \\[1ex]
v_{\mathrm{KI\_\_TMEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{KI}_{\mathrm{\_TMEX\_f}} \cdot \mathrm{Cki}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{LI\_\_TMBEX}} &= \mathrm{LI}_{\mathrm{\_TMBEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{plasma\_tm}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{Vgulumen} \cdot \mathrm{Clumen}_{\mathrm{tm}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC\_0}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vint\_0}} \cdot \mathrm{GU}_{\mathrm{\_tm\_int\_0}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC\_1}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vint\_1}} \cdot \mathrm{GU}_{\mathrm{\_tm\_int\_1}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC\_2}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vint\_2}} \cdot \mathrm{GU}_{\mathrm{\_tm\_int\_2}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC\_3}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vint\_3}} \cdot \mathrm{GU}_{\mathrm{\_tm\_int\_3}} \\[1ex]
v_{\mathrm{GU\_\_tmEXC\_4}} &= \mathrm{GU}_{\mathrm{\_TMEXC\_k}} \cdot \mathrm{GU}_{\mathrm{\_Vint\_4}} \cdot \mathrm{GU}_{\mathrm{\_tm\_int\_4}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_tir}} - v_{\mathrm{Flow\_ki\_ve\_tir}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_tir}} + v_{\mathrm{Flow\_po\_li\_tir}} - v_{\mathrm{Flow\_li\_hv\_tir}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_tir}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_tir}} + v_{\mathrm{Flow\_ve\_lu\_tir}} - v_{\mathrm{Flow\_lu\_ar\_tir}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_tir}} - v_{\mathrm{Flow\_gu\_po\_tir}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_tir}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_tir}} + v_{\mathrm{Flow\_ar\_re\_tir}} - v_{\mathrm{Flow\_re\_ve\_tir}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_tir}} - v_{\mathrm{Flow\_arli\_li\_tir}} - v_{\mathrm{Flow\_arli\_hv\_tir}} + v_{\mathrm{Flow\_lu\_ar\_tir}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_tir}} - v_{\mathrm{Flow\_ar\_re\_tir}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_tir}} + v_{\mathrm{Flow\_ki\_ve\_tir}} + v_{\mathrm{Flow\_hv\_ve\_tir}} - v_{\mathrm{Flow\_ve\_lu\_tir}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_tir}} - v_{\mathrm{TIR2TM}} + v_{\mathrm{sc\_tir}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_tir}} - v_{\mathrm{Flow\_po\_hv\_tir}} + v_{\mathrm{Flow\_gu\_po\_tir}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_tir}} + v_{\mathrm{Flow\_po\_hv\_tir}} + v_{\mathrm{Flow\_li\_hv\_tir}} - v_{\mathrm{Flow\_hv\_ve\_tir}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_tir}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{tir}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_tir}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_tm}} - v_{\mathrm{Flow\_ki\_ve\_tm}} - v_{\mathrm{KI\_\_TMEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_tm}} + v_{\mathrm{Flow\_po\_li\_tm}} - v_{\mathrm{Flow\_li\_hv\_tm}} - v_{\mathrm{LI\_\_TMBEX}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_tm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_tm}} + v_{\mathrm{Flow\_ve\_lu\_tm}} - v_{\mathrm{Flow\_lu\_ar\_tm}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_tm}} - v_{\mathrm{Flow\_gu\_po\_tm}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_tm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_tm}} + v_{\mathrm{Flow\_ar\_re\_tm}} - v_{\mathrm{Flow\_re\_ve\_tm}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_ki\_tm}} - v_{\mathrm{Flow\_arli\_li\_tm}} - v_{\mathrm{Flow\_arli\_hv\_tm}} + v_{\mathrm{Flow\_lu\_ar\_tm}} \\
&\quad {} - v_{\mathrm{Flow\_ar\_gu\_tm}} - v_{\mathrm{Flow\_ar\_re\_tm}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{Flow\_ki\_ve\_tm}} + v_{\mathrm{Flow\_hv\_ve\_tm}} - v_{\mathrm{Flow\_ve\_lu\_tm}} + v_{\mathrm{Flow\_re\_ve\_tm}} \\
&\quad {} + v_{\mathrm{TIR2TM}} + v_{\mathrm{sc\_deg\_tir}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{Flow\_po\_li\_tm}} - v_{\mathrm{Flow\_po\_hv\_tm}} + v_{\mathrm{Flow\_gu\_po\_tm}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_tm}} + v_{\mathrm{Flow\_po\_hv\_tm}} + v_{\mathrm{Flow\_li\_hv\_tm}} - v_{\mathrm{Flow\_hv\_ve\_tm}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_tm}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_tm}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{tm}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_TMEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{tm}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_tmEXC\_4}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clumen}_{\mathrm{tm}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_TMBEX}} - v_{\mathrm{GU\_\_tmEXC}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tm\_int\_0}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_tmEXC}} - v_{\mathrm{GU\_\_tmEXC\_0}}}{\mathrm{GU}_{\mathrm{\_Vint\_0}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tm\_int\_1}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_tmEXC\_0}} - v_{\mathrm{GU\_\_tmEXC\_1}}}{\mathrm{GU}_{\mathrm{\_Vint\_1}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tm\_int\_2}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_tmEXC\_1}} - v_{\mathrm{GU\_\_tmEXC\_2}}}{\mathrm{GU}_{\mathrm{\_Vint\_2}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tm\_int\_3}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_tmEXC\_2}} - v_{\mathrm{GU\_\_tmEXC\_3}}}{\mathrm{GU}_{\mathrm{\_Vint\_3}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_tm\_int\_4}}}{\mathrm{d} t} &= \frac{v_{\mathrm{GU\_\_tmEXC\_3}} - v_{\mathrm{GU\_\_tmEXC\_4}}}{\mathrm{GU}_{\mathrm{\_Vint\_4}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{tir}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_tir}} \cdot \mathrm{Mr}_{\mathrm{tir}} + \mathrm{Ri}_{\mathrm{tir}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SCDOSE}_{\mathrm{tir}}}{\mathrm{d} t} &= -\mathrm{Ksc}_{\mathrm{injection\_tir}} \cdot \mathrm{SCDOSE}_{\mathrm{tir}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{SCDEPOT}_{\mathrm{tir}}}{\mathrm{d} t} &= \mathrm{Ksc}_{\mathrm{injection\_tir}} \cdot \mathrm{SCDOSE}_{\mathrm{tir}} - \mathopen{}\left(v_{\mathrm{sc\_tir}} + v_{\mathrm{sc\_deg\_tir}}\right) \cdot \mathrm{Mr}_{\mathrm{tir}} \qquad \text{(rate rule)}
\end{aligned}
$$
