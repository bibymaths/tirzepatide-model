#set page(paper: "a4", margin: 2cm)
#set text(size: 10pt)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")
// a table longer than a page continues on the next page, its
// caption above it and its header repeated
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)

#align(center, text(size: 16pt, weight: "bold")[Tirzepatide PBPK model: fit PK])

= Methods: Tirzepatide PBPK model: fit PK

== Parameters and data

6 parameters were optimized: subcutaneous absorption rate tir (#raw("Ksc_tir")), clearance of the cleavage of tirzepatide (#raw("TIR2TM_k")), tissue\/plasma partition coefficient tir (#raw("Kp_tir")), tissue\/plasma partition coefficient tm (#raw("Kp_tm")), renal clearance of the tirzepatide metabolites relative to the GFR (#raw("KI__TMEX_f")) and rate of the biliary excretion of the tirzepatide metabolites (#raw("LI__TMBEX_k")).

A fit mapping is a curve of a study, the data and the observable of the model it is compared with. The fit has 27 fit mappings of training data with 268 data points, whose residuals enter the objective; 11 fit mappings of validation data with 97 data points, which were simulated and evaluated with the fitted parameters but not fitted; and 1 fit mapping of outliers with 14 data points, data the fit dropped as not usable, which were evaluated like the validation data so that the decision to drop them can be checked. The fit was set up and run with sbmlsim #cite(<Koenig2026_sbmlsim>).

== Objective function

The parameters were estimated by minimizing the objective function

$ F(arrow(p)) = 1/2 sum_k sum_i rho(w_(i,k) r_(i,k)(arrow(p))^2) $

where $k$ runs over the fit mappings of the training data and $i$ over their data points, $r_(i,k)$ is the residual, $w_(i,k) = w_k w^p_(i,k)$ the weight of the data point and $rho$ the loss function, applied to the squared weighted residual $z = w_(i,k) r_(i,k)^2$. The loss function is linear, $rho(z) = z$, i.e. a standard least squares problem.

The residuals are normalized by the mean $overline(y)_k$ of the data of their curve, which makes curves of different quantities and magnitudes comparable:

$ r_(i,k) = (y_(i,k) - f_k(x_(i,k), arrow(p))) / overline(y)_k $

The weight of curve $k$ is $w_k = n_k / N_k$, the weight $n_k$ of its fit mapping (the weight its fit mapping collection assigns, 1 by default, or, for a collection which uses the weights of its mappings, the weight of the mapping, by default the number of subjects of its data) divided by the number $N_k$ of its data points.

A data point is weighted with the inverse of its coefficient of variation, $w^p_(i,k) = |y_(i,k)| / sigma_(i,k)$, with $sigma_(i,k)$ the standard deviation of the data point, or its standard error for data without a standard deviation. An error of zero is missing, a missing error of a curve with errors is replaced by the largest error of the curve, and the data points of a curve without errors have the weight $w^p_(i,k) = 2$, the weight of a coefficient of variation of 0.5.

== Optimization

The optimizer searched the parameters in log10 space within their bounds; bounds, values and intervals are given in the units of the fit parameters, the units of the table of the parameters.

The objective was minimized in 3 runs with differential evolution #cite(<Storn1997>) of SciPy #cite(<Virtanen2020>) within the bounds of the parameters, with the strategy #raw("best1bin"), a population of 15 times the number of parameters, at most 1000 generations, the relative tolerance 0.01 of convergence, the recombination constant 0.7 and a mutation dithered between 0.5 and 1. The initial population of a run was drawn by latin hypercube sampling #cite(<McKay1979>), with a seed of every run derived from the seed 1234 of the fit. The best member of the final population was polished with the L-BFGS-B method of SciPy.

The convergence of the runs was assessed from the traces of their cost and the waterfall plot of their final costs, and the parameter set with the lowest cost was used.

The models were simulated with libRoadRunner #cite(<Welsh2023>) and its integrator CVODE #cite(<Hindmarsh2005>) with the relative tolerance $10^(-6)$ and the absolute tolerances $10^(-12)$ of an amount, $10^(-12)$ of a concentration and $10^(-6)$ of the other states, which for a species in a concentration is multiplied by the initial volume of its compartment. It ran with the variable step size of libRoadRunner, i.e. with an output at every step of the integrator. A data point at the time of a change after the start of a simulation, e.g. a dose or the reset of a collection, was compared with the state before the change, except the first data point of a curve with data at later times, which starts a collection and was compared with the state after the change.

== Goodness of fit

The goodness of fit is given per kind of data (training data, validation data and outliers) by metrics over its $n$ data points with the residuals $e_i = y_i - f(x_i, hat(arrow(p)))$ at the fitted parameters $hat(arrow(p))$, the mean squared error, its root and the root mean squared error normalized by the mean $overline(y)_(k(i))$ of the data of the curve of a point:

$ "MSE" = 1/n sum_(i=1)^n e_i^2, quad "RMSE" = sqrt("MSE"), quad "NRMSE" = sqrt(1/n sum_(i=1)^n (e_i / overline(y)_(k(i)))^2) $

The root mean square of the residuals of the objective, i.e. what the fit minimizes, and the coefficient of determination:

$ "RMSE"_w = sqrt(1/n sum_(i=1)^n rho(w_i r_i^2)), quad R^2 = 1 - (sum_i e_i^2) / (sum_i (y_i - overline(y))^2) $

The predictions of a non-linear model are no linear regression of the data, so $R^2$ can be negative: the prediction is worse than the mean of the data. The information criteria of Akaike #cite(<Akaike1974>) and Schwarz #cite(<Schwarz1978>) with the number $n_p$ of fitted parameters are those of a least squares fit with normally distributed residuals, up to an additive constant, so only differences between models fitted to the same data are meaningful:

$ "AIC" = n ln("MSE") + 2 n_p, quad "BIC" = n ln("MSE") + n_p ln(n) $

The percentage of the data points whose prediction $f_i = f(x_i, hat(arrow(p)))$ lies within twofold of the data is taken over the $n_(+)$ data points with positive data $y_i > 0$ and a positive prediction $f_i > 0$; the others have no ratio and are not counted, and a kind of data without such a point has no percentage:

$ P_2 = 100 / n_(+) abs(\{ i : 1/2 <= f_i / y_i <= 2 \}) $

The goodness of fit plot shows the predictions against the data on logarithmic axes, with the lines of twofold $f = 2y$ and $f = y/2$. The Bland-Altman plot #cite(<Bland1986>) shows the ratio of prediction and data as $d_i = log_10(f_i / y_i)$ against the geometric mean $sqrt(f_i y_i)$ for the data points with positive values, with the bias $overline(d)$ and the limits of agreement $overline(d) plus.minus 1.96 s_d$, with the sample standard deviation $s_d$ of $d_i$, of the training data; they are read as the fold factors $10^(overline(d))$ and $10^(overline(d) plus.minus 1.96 s_d)$.

== Identifiability

The identifiability of the parameters was analysed with the profile likelihood #cite(<Raue2009>) #cite(<Kreutz2013>). The profile of a parameter is the lowest objective with the parameter fixed:

$ "PL"(p_j) = min_(p_(l != j)) F(arrow(p)) $

At every point of a scan the other parameters were re-optimized from the previous point with the least squares optimizer of SciPy with the relative step 0.05. A scan ran from the optimum in both directions in the space of the optimizer, with steps in decades of the parameter, starting at 0.1. A step which raised the objective by more than 0.2 of the distance between the objective at the optimum and the threshold was reduced by the factor 2 and repeated, down to 0.01, and the step after one which raised it by less than that divided by the factor was enlarged by the factor, up to 1. A scan stopped at the threshold, at the bound of the parameter, at a point which failed or after 50 points.

The confidence intervals are the values at which the profile crosses the threshold of the likelihood ratio test

$ F_"thr" = F_"min" + chi^2_alpha ("df") / 2 $

with $F_"min"$ the lowest objective of the fit and of all profiles and $chi^2_alpha ("df")$ the quantile of the $chi^2$ distribution at the confidence level $alpha = 0.95$ with df \= 1 degrees of freedom, i.e. 1.92 above the lowest objective. The threshold has this confidence level if $F$ is the negative log-likelihood of the data up to a constant, i.e. if the weighted residuals are independent and normally distributed with unit variance; otherwise the level is approximate. A crossing is interpolated between two points of the profile, on the logarithm of a parameter on a logarithmic scale. A parameter is identifiable if its profile reaches the threshold within the scan on both sides of the optimum, i.e. its confidence interval is finite; practically non-identifiable towards the lower bound if its profile reaches the threshold above the optimum but not below it within the scan, which ends at the lower bound or after 50 points; practically non-identifiable towards the upper bound if its profile reaches the threshold below the optimum but not above it within the scan, which ends at the upper bound or after 50 points; practically non-identifiable if its profile reaches the threshold on neither side within the scans, which end at the bounds or after 50 points, and is not flat; and structurally non-identifiable if its profile is flat on both sides. A side of a profile is flat if it rises by less than 0.05 of the distance between the lowest objective and the threshold, and a profile with a point which failed or did not converge is not classified. The profile likelihood is preferred over the intervals of the Fisher information, its intervals are invariant under a transformation of the parameters and can be asymmetric #cite(<Wieland2021>).

The Fisher information is the local alternative to the profiles: it is the Gauss-Newton approximation of the curvature of the objective at the optimum, from the Jacobian $J$ of the weighted residuals of the training data with respect to the parameters $arrow(p)$ in the space of the optimizer, computed by central finite differences with the step $h_j = epsilon max(|p_j|, 1), space epsilon = 10^(-6)$ of the parameter $p_j$:

$ I = J^top J, quad "cov" = sigma^2 I^(-1), quad sigma^2 = (2 F) / (n - n_p) $

with the number $n$ of data points of the training data and the number $n_p$ of parameters. The information has rank 6 of 6, the number of its eigenvalues above $10^(-8)$ of the largest one, and the condition number 80.3; the covariance of an information of a lower rank is computed with the pseudo-inverse. The Wald intervals are $hat(p)_j plus.minus t_((1+alpha)/2, n-n_p) "SE"_j$ with the standard errors $"SE"_j = sqrt("cov"_(j j))$ at the confidence level $alpha = 0.95$, transformed back into the units of the fit parameters.

== Provenance

The fit PK\_20261019\_095941\_\_4f772 was run on 2026-10-19 07:59:43 UTC with sbmlsim 0.10.0 #cite(<Koenig2026_sbmlsim>), libRoadRunner 2.10.0 #cite(<Welsh2023>), SciPy 1.18.1 #cite(<Virtanen2020>), NumPy 2.5.3 #cite(<Harris2020>) and Python 3.14.4 (seed 1234). The models and data were those of commit #raw("fb9e8e7711413d5136b5b28358c9aac064a679f1") of #raw("/home/mkoenig/git/pkdb_models-tirzepatide"); their SHA-256 checksums are listed in #ref(<tab:checksums:PK_20261019_095941__4f772>).

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([File], [SHA-256]),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_Fig1_EMA.tsv"),
  raw("b1a047b99aad..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_Fig1_FDA.tsv"),
  raw("a042b543da05..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_Fig2_EMA.tsv"),
  raw("19ddc9b1fe40..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_Fig2_FDA.tsv"),
  raw("61691c652a05..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_Tab2.tsv"),
  raw("13f33757bc62..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_TabGroups.tsv"),
  raw("c0cfb71785c7..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_TabInterventions.tsv"),
  raw("80ac58364aa4..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Coskun2018/.Coskun2018_TabS2.tsv"),
  raw("e61e5f7c3338..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_Fig1.tsv"),
  raw("70f92205e91f..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_Fig3.tsv"),
  raw("91522d28ab1c..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_TabGroups.tsv"),
  raw("f0eefecbcf1d..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_TabInterventions.tsv"),
  raw("827a5deb5352..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_TabS1.tsv"),
  raw("5667e25a5afa..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_TabS2.tsv"),
  raw("bc8f84a9bbe7..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Feng2023/.Feng2023_TabS3.tsv"),
  raw("d49264b6c219..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_Fig1.tsv"),
  raw("2af0a9b7b3d8..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_Fig2.tsv"),
  raw("1b3d120266a9..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_Fig3.tsv"),
  raw("c0c72d337961..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_TabGroups.tsv"),
  raw("ccadd9674677..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_TabInterventions.tsv"),
  raw("9cde037b7db8..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Furihata2022/.Furihata2022_TabS1.tsv"),
  raw("2932849056c1..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Martin2024/.Martin2024_Fig3.tsv"),
  raw("a935c1bc427e..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Martin2024/.Martin2024_Fig4.tsv"),
  raw("63994fc7054e..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Martin2024/.Martin2024_Tab1.tsv"),
  raw("25d6d1ec8152..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Martin2024/.Martin2024_TabGroups.tsv"),
  raw("8dd3cbbf14d6..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Martin2024/.Martin2024_TabInterventions.tsv"),
  raw("983f30d70322..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_Fig2.tsv"),
  raw("5991b35ae8fc..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_Fig3A.tsv"),
  raw("4c32ac5a4224..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_Fig3B.tsv"),
  raw("808703e122a5..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_Fig3C.tsv"),
  raw("9f4028070965..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_Tab2.tsv"),
  raw("6d00deabb4b8..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_TabGroups.tsv"),
  raw("08f38c526bf6..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_TabIndividuals.tsv"),
  raw("f7c87fa574f4..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2021/.Urva2021_TabInterventions.tsv"),
  raw("56d0d60eda69..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Fig1.tsv"),
  raw("b41c87be5472..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Fig1A.tsv"),
  raw("7b18353ab307..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Fig2A.tsv"),
  raw("79bbc7c27de3..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Fig2B.tsv"),
  raw("7d2cc6850d49..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Fig2C.tsv"),
  raw("0aff4931a880..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_Tab2.tsv"),
  raw("1868aef062d0..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_TabGroups.tsv"),
  raw("0495c6afb5ca..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_TabIndividuals.tsv"),
  raw("eb8849cdba03..."),
  raw("pkdb_models/models/tirzepatide/data/tirzepatide/Urva2022/.Urva2022_TabInterventions.tsv"),
  raw("943873afec9e..."),
  raw("pkdb_models/models/tirzepatide/models/output/models/tirzepatide_body_flat.xml"),
  raw("45e44c8380d2..."),
  ),
  caption: [SHA-256 checksums of the models and data of the fit PK\_20261019\_095941\_\_4f772, their first 12 characters; the full checksums are in the provenance of the result (optimization\_result.json).],
) <tab:checksums:PK_20261019_095941__4f772>

= Results: Tirzepatide PBPK model: fit PK

== Parameters

#figure(
  table(
  columns: 6,
  align: (left, left, right, left, right, left,),
  table.header([Parameter], [Description], [Value \[95% CI\]], [Unit], [Bounds], [Identifiable]),
  raw("Ksc_tir"),
  [subcutaneous absorption rate tir],
  [0.00143 \[0.00107, 0.00198\]],
  [1\/min],
  [\[0.0002, 0.01\]],
  [yes],
  raw("TIR2TM_k"),
  [clearance of the cleavage of tirzepatide],
  [0.000634 \[0.000584, 0.00069\]],
  [l\/min],
  [\[0.0002, 0.003\]],
  [yes],
  raw("Kp_tir"),
  [tissue\/plasma partition coefficient tir],
  [0.0355 \[0.0243, 0.0487\]],
  [dimensionless],
  [\[0.005, 0.5\]],
  [yes],
  raw("Kp_tm"),
  [tissue\/plasma partition coefficient tm],
  [0.147 \[LB, 6.62\]],
  [dimensionless],
  [\[0.01, 10\]],
  [no (LB)],
  raw("KI__TMEX_f"),
  [renal clearance of the tirzepatide metabolites relative to the GFR],
  [0.0122 \[0.0052, 0.352\]],
  [dimensionless],
  [\[0.0001, 1\]],
  [yes],
  raw("LI__TMBEX_k"),
  [rate of the biliary excretion of the tirzepatide metabolites],
  [0.000384 \[0.000161, UB\]],
  [1\/min],
  [\[1e-06, 0.01\]],
  [no (UB)],
  ),
  caption: [Parameters of the fit PK\_20261019\_095941\_\_4f772, the parameter set PK\_20261019\_095941\_\_4f772\_0, cost 13.6, with their bounds in the optimization. The 95% confidence intervals are those of the profile likelihood, LB and UB an interval which is open towards the lower or the upper bound, and the Wald intervals of the Fisher information for a parameter without a profile. Identifiable is the classification of the profile: yes, no (LB) or no (UB) if the profile does not reach the threshold towards the lower or the upper bound, no if it reaches it on neither side, structural if it is flat.],
) <tab:parameters:PK_20261019_095941__4f772>

== Data

#figure(
  table(
  columns: 5,
  align: (left, right, right, right, right,),
  table.header([Study], [Training], [Validation], [Outlier], [Total]),
  [Coskun2018],
  [10 (84)],
  [4 (27)],
  [-],
  [14 (111)],
  [Feng2023],
  [6 (40)],
  [-],
  [-],
  [6 (40)],
  [Furihata2022],
  [6 (39)],
  [-],
  [-],
  [6 (39)],
  [Martin2024],
  [3 (85)],
  [-],
  [1 (14)],
  [4 (99)],
  [Urva2021],
  [1 (10)],
  [4 (40)],
  [-],
  [5 (50)],
  [Urva2022],
  [1 (10)],
  [3 (30)],
  [-],
  [4 (40)],
  [Total],
  [27 (268)],
  [11 (97)],
  [1 (14)],
  [39 (379)],
  ),
  caption: [Data of the fit PK\_20261019\_095941\_\_4f772: the number of fit mappings and, in parentheses, of data points per study and kind. The training data enters the cost, the validation data and the outliers are evaluated only.],
) <tab:data:PK_20261019_095941__4f772>

== Goodness of fit

#figure(
  table(
  columns: 11,
  align: (left, right, right, right, right, right, right, right, right, right, right,),
  table.header([Kind], [n], [cost], [MSE], [RMSE], [NRMSE], [RMSE\_w], [R²], [2-fold \[%\]], [AIC], [BIC]),
  [training],
  [268],
  [13.6],
  [2.03e-10],
  [1.42e-05],
  [0.152],
  [0.318],
  [0.987],
  [98.4],
  [-5969.8],
  [-5948.2],
  [validation],
  [97],
  [-],
  [3.88e-10],
  [1.97e-05],
  [0.263],
  [0.526],
  [0.863],
  [96.6],
  [-2089.9],
  [-2074.5],
  [outlier],
  [14],
  [-],
  [6.46e-10],
  [2.54e-05],
  [0.543],
  [0.834],
  [0.333],
  [92.9],
  [-284.2],
  [-280.4],
  ),
  caption: [Goodness of fit of the fit PK\_20261019\_095941\_\_4f772 per kind of data, the parameter set PK\_20261019\_095941\_\_4f772\_0. The cost is defined on the training data only, 2-fold is the percentage of the data points with a positive value and prediction whose prediction is within twofold of the data.],
) <tab:metrics:PK_20261019_095941__4f772>

== Figures

#figure(
  image("plots/traces.svg", width: 100%),
  caption: [Cost of the optimizers over their steps, fit PK\_20261019\_095941\_\_4f772. The cost of every optimization run over its steps. Runs which end at the same cost found the same optimum; a run which stops much higher is stuck in a local minimum.],
) <fig:traces:PK_20261019_095941__4f772>

#figure(
  image("plots/waterfall.svg", width: 100%),
  caption: [Cost of the optimization runs, ordered, fit PK\_20261019\_095941\_\_4f772. The final cost of the runs, ordered. A flat plateau at the left is the global optimum found repeatedly, which is the evidence that the multistart converged; steps to the right are local minima.],
) <fig:waterfall:PK_20261019_095941__4f772>

#figure(
  image("plots/goodness_of_fit.svg", width: 100%),
  caption: [Prediction against the measured data points, per kind of fit mapping, with the agreement of the training data, the lines of twofold and the metrics of the panel, fit PK\_20261019\_095941\_\_4f772. Within twofold of the data are 248 of the 252 training data points (98.4%), 86 of the 89 validation data points (96.6%) and 13 of the 14 outlier data points (92.9%); only the data points with a positive value and prediction are counted. Prediction against measurement, one point per data point, with a panel per kind of fit mapping. The points scatter around the diagonal when the model describes the data; a systematic deviation from it is a systematic error of the model. The band is the agreement of the training data, i.e. the same band the Bland-Altman plot draws, here as lines parallel to the diagonal. The dark red dotted lines are twofold, prediction \= 2 x measurement and prediction \= measurement \/ 2; the caption states the points between them of every kind. A point which is zero or negative is not drawn on the logarithmic axes and not counted, the title of a panel then states the points drawn of all. The validation panel shows how the fit describes data it was not fitted on, the outlier panel the data the fit dropped. The box of a panel carries its R², its normalized RMSE, the RMSE of the residuals of the cost, its fold errors GMFE and AFE and the percentages of its points within twofold and within two standard deviations of the data.],
) <fig:goodness_of_fit:PK_20261019_095941__4f772>

#figure(
  image("plots/bland_altman.svg", width: 100%),
  caption: [Agreement of prediction and measurement as a ratio, per kind of fit mapping, with the agreement of the training data and the agreement of the panel, fit PK\_20261019\_095941\_\_4f772. The ratio of prediction and measurement over the geometric mean of the two, i.e. the goodness of fit with the diagonal turned into the horizontal. The band is the same, the bias and the limits of agreement #raw("bias ± 1.96 SD") of the training data as fold factors. A bias away from 1 is a systematic over- or underprediction, wide limits are a large scatter, and a trend over the mean is a model which describes the large or the small values better. The box of a panel carries the bias and the SD of its own points as fold factors and the share of them inside the limits of agreement of the training data.],
) <fig:bland_altman:PK_20261019_095941__4f772>

#figure(
  image("plots/profiles.svg", width: 100%),
  caption: [Profile likelihood of every parameter: the cost with the parameter fixed and the other parameters optimized, the threshold of the confidence level and the confidence interval, fit PK\_20261019\_095941\_\_4f772. One profile per parameter. A profile which crosses the dashed threshold on both sides gives a finite confidence interval; one which stays below it up to a bound is practically non-identifiable; a flat profile is structurally non-identifiable, the parameter is compensated by the others.],
) <fig:profiles:PK_20261019_095941__4f772>

== Provenance

#figure(
  table(
  columns: 2,
  align: (left, left,),
  table.header([Item], [Value]),
  [Fit],
  raw("PK_20261019_095941__4f772"),
  [Created],
  [2026-10-19 07:59:43 UTC],
  [Seed],
  [1234],
  [Python],
  [3.14.4],
  [sbmlsim],
  [0.10.0],
  [libRoadRunner],
  [2.10.0],
  [SciPy],
  [1.18.1],
  [NumPy],
  [2.5.3],
  [Repository],
  raw("/home/mkoenig/git/pkdb_models-tirzepatide"),
  [Commit],
  raw("fb9e8e7711413d5136b5b28358c9aac064a679f1"),
  [Uncommitted changes],
  [no],
  ),
  caption: [Provenance of the fit PK\_20261019\_095941\_\_4f772: the versions it ran with and the revision of its models and data; the SHA-256 checksums of the models and data are listed in #ref(<tab:checksums:PK_20261019_095941__4f772>).],
) <tab:provenance:PK_20261019_095941__4f772>

#bibliography("references.bib", style: "references.csl")
