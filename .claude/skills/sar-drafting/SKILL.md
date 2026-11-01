---
name: sar-drafting
description: Draft a suspicious activity report (SAR/STR) narrative for the Turks and Caicos FIA from an MLRO's case notes, or an internal decision note when not filing. Use when the user mentions a SAR, STR, suspicious activity or transaction report, an internal disclosure from staff, or asks whether something is reportable.
---

# SAR drafting

Turns case notes into a clear, factual SAR narrative and records the MLRO's decision.
The MLRO decides whether to file and files it through the FIA's own channel. Claude only drafts.

## Ground rules
- **Tipping off**: warn the user at the start not to tell the subject, or anyone outside need-to-know, that a report is being considered or has been made. Draft nothing addressed to the customer.
- **Confidentiality**: work only from what the user pastes. Never save case details in the repo, in files that sync elsewhere, or in a shared document, unless the user explicitly asks and the location is private.
- **Don't state the law from memory.** The reporting form, portal, deadlines and legal thresholds come from the current TCI FIA guidance and the Proceeds of Crime legislation and regulations. Ask the user to confirm or paste them if they matter.
- **Facts, not conclusions.** Describe what happened and why it's unusual. Don't allege a specific crime unless the facts show it, and mark anything uncertain as such.

## Steps
1. **Gather facts.** Ask for:
   - Subject details (individuals or entities, identifiers, the relationship with the firm)
   - Accounts and products involved
   - Transactions (dates, amounts, currency, counterparties, jurisdictions)
   - How it came to light (internal disclosure, monitoring alert, screening, adverse media)
   - The customer's explanation, if one was given before suspicion arose
   - Prior SARs on the same subject

   List any gaps and continue with what you have.
2. **Identify the grounds for suspicion.** Map the facts to recognised red flags and typologies, for example structuring, rapid movement of funds, mismatch with the customer profile, high-risk jurisdictions (check `compliance_dashboard/data/fatf_lists.json`), third-party payments, unexplained wealth, TF or PF indicators. Explain why each matters.
3. **Draft the narrative** in the 5 Ws order:
   - **Who** is involved
   - **What** activity
   - **When**: a chronological timeline
   - **Where**: accounts and jurisdictions
   - **Why** it's suspicious
   - **How** it was detected

   Then list the action taken (relationship restricted or exited, funds held) and supporting documents available on request. Keep it plain, chronological and self-contained, so a reader with no other context understands it.
4. **Consent or freezing questions.** If the firm wants to proceed with a transaction, or funds may be restrained, flag that the user must check the FIA's consent and defence procedure before acting.
5. **Decision record.** Produce a short internal note:
   - Date the internal disclosure was received
   - MLRO's assessment
   - Decision: file or don't file, with the reasons
   - Date filed and reference, left blank for the user to complete

   This note is needed whichever way the decision goes.

End the draft with: "Draft prepared with AI assistance. To be reviewed and submitted by the MLRO."
