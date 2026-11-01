---
name: fatf-plenary-update
description: Update the MLRO dashboard's FATF black and grey lists after a FATF plenary (February, June, October). Use when the user says a plenary has happened, the dashboard shows the red "new FATF statement" banner, or they ask to refresh, update or check compliance_dashboard/data/fatf_lists.json.
---

# FATF plenary update

Updates `compliance_dashboard/data/fatf_lists.json` from the official FATF statements and checks the result.
Accuracy matters more than speed: an MLRO relies on this file for country risk decisions.

## 1. Get the official statements

Find the three FATF pages for the plenary that just ended:
- "Jurisdictions under Increased Monitoring – <Month Year>" (grey list)
- "High-Risk Jurisdictions subject to a Call for Action – <Month Year>" (black list)
- "Outcomes FATF Plenary, <dates>"

The URLs usually follow the pattern of the current `sources` block, with the new month in place of the old one.
fatf-gafi.org often blocks automated fetches. If you can't read the pages, **stop and ask the user to paste the list of jurisdictions** from each page, or to confirm a regulator's notice that reproduces it (for example TCI FSC, the UK FCA or HM Treasury, or CFATF).
Never fill the lists from memory, news articles or guesswork.

## 2. Edit the file

Keep the existing shape:

- `black_list`: `{"country", "iso", "measure"}`, where `measure` is `"Countermeasures"` or `"Enhanced due diligence"`.
- `grey_list`: `{"country", "iso", "listed_since": "YYYY-MM"}`, sorted alphabetically.
  - For countries already listed, keep their `listed_since` value.
  - For new countries, use the plenary month.
- Add a new first entry to `history`: `{"date": "YYYY-MM-DD" (last plenary day), "label": "<Month Year> Plenary", "added": [...], "removed": [...]}`.
  Use exactly the same country spelling as in `grey_list`.
- Update `as_of` (the last plenary day), `as_of_label`, every URL in `sources`, and `next_plenary`.
  Only give dates for the next plenary if FATF has announced them. Otherwise keep the "not yet announced" note.
- Review the notes in `other_lists` (EU and UK high-risk lists). Tell the user these may need a separate update, because they change on their own timetable.

## 3. Check

Run these commands from `compliance_dashboard/`:

```bash
python -m unittest discover -s tests
python run.py --offline --no-open
```

`test_baseline_is_consistent` fails if the countries in the history entry don't match the lists.

## 4. Report

Show the user a short table of countries added and removed, with the source URL for each list, before committing.
Remind them that this data is a convenience copy and that the official FATF statement is the authority.
