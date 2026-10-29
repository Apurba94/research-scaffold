# research-scaffold

**Start every research project with a clean, reproducible structure: separated raw and
processed data, code package, results, documentation, data provenance table, CITATION.cff and a
sensible .gitignore, in one command.**

Part of the *Research Automation Toolkit*: 100 open tools for daily research work.

## Why

Projects that start as a folder of `analysis_final_v3.R` and `data_clean_NEW.xlsx` are hard to
reproduce, share or hand over to the next student. Community recommendations ("Good enough practices
in scientific computing", Wilson et al. 2017; Cookiecutter Data Science) converge on a simple layout.
Creating it should take seconds, not an afternoon.

## Features

- Templates: `basic`, `ml` (models, configs, runs), `paper` (manuscript sections)
- `data/raw` (immutable), `data/interim`, `data/processed`, `results/figures|tables`, `src/<package>`, `tests`, `docs`
- README with structure and reproduction steps, `docs/DATA.md` provenance table (source, licence, checksum)
- `CITATION.cff` with ORCID, licence identifier, `.gitignore` that keeps data and secrets out of git
- Never overwrites existing files (safe to run on an existing project); `--dry-run`; optional `git init`

## Usage

```bash
pip install .
research-scaffold "Soil microbes under drought" -a "Ada Lovelace" --orcid 0000-0002-1825-0097
research-scaffold "Protein language models" -a "Alan Turing" -t ml --git
research-scaffold "Review of X" -a "Jane Doe" -t paper --dry-run
```

## Testing

```bash
python -m unittest discover -s tests -t .
```

## License

MIT (c) JANIN A APURBA
