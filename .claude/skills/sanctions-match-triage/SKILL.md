---
name: sanctions-match-triage
description: Structured triage of a possible sanctions or PEP screening match, or a re-screen after new UK/OFAC designations. Use when the user (a TCI MLRO) mentions a screening alert, a name hit, a "RE-SCREEN" flag on the morning brief, a new designation that may affect a client, or asks whether a match is a false positive.
---

# Sanctions match triage

Helps the MLRO work through a possible match so that both the decision and the reasons for it are recorded.
Claude helps with analysis and drafting. The MLRO makes the decision.

## Ground rules
- **Use official sources only** to confirm a designation: the UK Sanctions List (FCDO) / OFSI Consolidated List, the OFAC SDN search, or the UN list.
  Quote the list entry (name, aliases, DOB, nationality, regime, date designated, ID numbers) and give its URL.
  If you can't reach the source, say so and ask the user to paste the entry. Never rely on memory or news reports for designation details.
- **Data minimisation**: ask only for the identifiers needed to compare. Don't ask for full customer files.
- **Tipping off**: warn the user not to tell the customer about the review or any report.
- This is not legal advice. Point the user to the current TCI FSC / FIA guidance and the Order in Council that applies, which sets the competent authority and reporting route.

## Steps

1. **Collect the alert.** Get the customer identifiers (full name, aliases, DOB, nationality, address, ID numbers, entity registration) and the list entry that matched.
2. **Compare field by field.** Build a table with columns Field | Customer | List entry | Match / Mismatch / Unknown.
   Treat transliteration, name order and partial names carefully. A name match alone is not a true match.
3. **Classify:**
   - **False positive**: a strong identifier contradicts the list entry (DOB, nationality or ID number). Record which one.
   - **Possible match**: no contradiction, but not enough data to confirm. List the information needed to resolve it.
   - **Likely true match**: several strong identifiers agree.
   - For entities, also check ownership and control (50% ownership rules for UK/OFAC and aggregation), and say what ownership information is missing.
4. **Next actions:**
   - **Likely true match**: don't deal with the funds or economic resources. Escalate to the MLRO/board as policy requires. Prepare the frozen-asset / breach report for the competent authority. Consider a SAR to the TCI FIA.
     Ask the user to confirm current reporting deadlines and forms from official guidance, and don't state deadlines from memory.
   - **Possible match**: pause the activity pending information, and draft the request for information without tipping off.
   - **False positive**: record the reason so the same alert can be closed quickly next time.
5. **Write the file note.** Produce a dated note: alert source, list and entry, comparison table, classification, rationale, actions, reviewer. It must be good enough for a regulator's file review.

## Re-screen after new designations

When the morning brief shows **RE-SCREEN**, list the new names, regimes and programmes from the brief. Help the user run them against the customer base export they provide, then triage each hit with the steps above.
