# Honcho

The main project here is `compliance_dashboard/`, an MLRO Morning Brief for a Turks & Caicos Money Laundering Reporting Officer. It is a static page built by a Python script and published to GitHub Pages (`gh-pages`) by `.github/workflows/compliance-dashboard.yml` every weekday at 6am TCI time.

## Constraints
- **Standard library only, Python 3.9+.** It must run on a locked-down work PC, so don't add pip dependencies.
- Data lives in `compliance_dashboard/data/*.json` (FATF lists, news sources, calendar, checklist, ntfy topic). Code lives in `compliance_dashboard/dashboard/`.
- The published site is public. Never commit customer data, case notes or secrets. Checklist ticks stay in the browser's localStorage.
- Compliance facts (FATF lists, designations, regulator rules) must come from official sources, cited. Don't fill them in from memory.

## Commands (run from compliance_dashboard/)
- Tests: `python -m unittest discover -s tests`
- Offline build: `python run.py --offline --no-open`
- Full build: `python run.py --no-open`

## Skills
- `fatf-plenary-update`: refresh `fatf_lists.json` after each FATF plenary.
- `sanctions-match-triage`: work through a screening hit or a RE-SCREEN flag.
- `customer-risk-assessment`: risk-rate a customer and write the CDD/EDD file note.
- `sar-drafting`: draft a SAR narrative for the FIA and the MLRO's decision record.
- `mlro-board-report`: periodic MLRO report to the board.
- `regulatory-change-summary`: summarise a new notice, law or guidance and the actions it creates.

Never write customer or case details into this repo: it is public.
