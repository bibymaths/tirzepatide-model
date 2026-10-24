"""LaTeX table of the studies of the tirzepatide model."""

from pathlib import Path

import pandas as pd


def create_latex_table(df: pd.DataFrame) -> str:
    """Transform DataFrame into LaTeX table."""
    # Preamble:
    latex_header = r"""
%\begin{landscape}
\begin{table}[ht!]
\centering
\label{tab:data_overview}
\tabcolsep=3.5pt\relax
\scriptsize
\begin{threeparttable}

\caption{\textbf{Overview of tirzepatide studies.}
This table includes key identifiers (\emph{Study}, \emph{PMID}, \emph{PK-DB ID}),
administration route (\emph{Route}),
dosing regimen (\emph{Dosing}) and dose (\emph{Dose}), and participant characteristics
(\emph{H} for healthy, \emph{RI} for renal impairment,
\emph{HI} for hepatic impairment, \emph{T2} for diabetes mellitus type 2).}

\begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}
  p{1.2cm}  % Study
  p{1.2cm}  % PubMed ID
  p{1.2cm}  % PK-DB ID
  p{0.6cm}  % Route
  p{1.2cm}  % Dosing
  p{1.2cm}  % Dose [mg]
  p{0.3cm}  % Healthy
  p{0.3cm}  % Ren. imp.
  p{0.3cm}  % Hep. imp.
  p{0.3cm}  % T2DM
}
\toprule
""".strip("\n")

    # Selecting needed columns
    df = df.loc[
        :,
        [
            "study",
            "pmid",
            "pkdb",
            "route",
            "dosing",
            "dose",
            "healthy",
            "renal impairment",
            "hepatic impairment",
            "t2dm",
        ],
    ].copy()

    # Renaming columns
    df = df.rename(
        columns={
            "study": "Study",
            "pmid": "PMID",
            "pkdb": "PK-DB ID",
            "route": "Route",
            "dosing": "Dosing",
            "dose": "Dose [mg]",
            "healthy": "H",
            "renal impairment": "RI",
            "hepatic impairment": "HI",
            "t2dm": "T2",
        }
    )
    # Remove pipe characters from "Dose [mg]" column
    if "Dose [mg]" in df.columns:
        df["Dose [mg]"] = df["Dose [mg]"].str.replace("|", ",", regex=False)

    # Convert True/False to checkmarks
    checkmark_columns = [
        "Co-administration",
        "Healthy",
        "Ren. imp.",
        "Hep. imp.",
        "T2DM",
    ]

    for col in checkmark_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: r"\checkmark" if str(x).strip().upper() == "TRUE" else ""
            )

    # Column headers row
    column_names = df.columns.tolist()
    column_headers = " & ".join([f"\\textbf{{{col}}}" for col in column_names]) + r" \\"

    # LaTeX body
    latex_body = f"{column_headers}\n\\midrule\n"

    for _, row in df.iterrows():
        values = list(row.astype(str).values)

        # pubmed urls
        pmid_col_index = 1
        values[pmid_col_index] = (
            f"\\href{{https://pubmed.ncbi.nlm.nih.gov/{values[pmid_col_index]}}}"
            f"{{{values[pmid_col_index]}}}"
            if values[pmid_col_index]
            else ""
        )

        # pkdb urls
        pkdb_col_index = 2
        values[pkdb_col_index] = (
            f"\\href{{https://identifiers.org/pkdb:{values[pkdb_col_index]}}}"
            f"{{{values[pkdb_col_index]}}}"
            if values[pkdb_col_index]
            else ""
        )

        row_str = " & ".join(v.replace("TRUE", r"\checkmark") for v in values) + r" \\"

        latex_body += row_str + "\n"

    latex_footer = r"""
\bottomrule
\end{tabular*}

\end{threeparttable}
\end{table}
%\end{landscape}
""".strip("\n")

    # Combine all parts
    return latex_header + "\n" + latex_body + latex_footer


if __name__ == "__main__":
    # Input and output file paths
    tsv_path = Path(__file__).parent / "tirzepatide_studies.tsv"
    latex_path = Path(__file__).parent / "tirzepatide_studies.tex"

    # Load TSV file
    df = pd.read_csv(tsv_path, sep="\t", header=1)

    # Replace NaN values with an empty string
    df = df.fillna("")

    # Create LaTeX string
    latex_str = create_latex_table(df)

    # Save LaTeX table to file
    with open(latex_path, "w") as f_tex:
        f_tex.write(latex_str)
