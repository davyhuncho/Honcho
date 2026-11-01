---
name: customer-risk-assessment
description: Risk-rate a customer or prospective customer for AML/CFT and write the CDD/EDD file note. Use when the user (a TCI MLRO) asks to risk-assess, risk-rate or onboard a client, decide whether enhanced due diligence applies, review a periodic KYC refresh, or check a customer's country risk.
---

# Customer risk assessment

Produces a reasoned risk rating and a file note that an examiner could follow.
Claude proposes the rating. The MLRO or relationship owner decides it.

## Ground rules
- **Use the firm's own methodology first.** Ask whether the firm has a risk matrix or scoring model.
  If one exists, use its factors, weights and thresholds exactly, and suggest saving it as `references/firm-matrix.md` in this skill folder so it's used every time.
  If none exists, use the default factors below and label the result "indicative, default factors".
- **Ask only for the information needed.** Don't ask for ID document images or full files. Never write customer data into the repo, because the published dashboard is public.
- If a fact is unknown, record it as a gap. Don't guess it.
- Country status comes from `compliance_dashboard/data/fatf_lists.json` (black list, grey list, `other_lists` notes).
  Give its `as_of` date and remind the user to check the live FATF, UK and EU lists if that date is more than a few months old.
- Sanctions and PEP screening results come from the user's screening system. If there's a possible hit, switch to the `sanctions-match-triage` skill.

## Default factors
Rate each factor Low, Medium or High, and give a one-line reason.

1. **Customer**: type (individual, company, trust, foundation, partnership), ownership complexity, nominee arrangements, bearer shares, business type and sector (cash-intensive, gaming, real estate, virtual assets, MSB), length of relationship, adverse media.
2. **PEP status**: foreign or domestic PEP, family member or close associate, and when they left office.
3. **Geography**: nationality, residence, place of incorporation, countries of business, and the origin and destination of funds. Mark each against the FATF black and grey lists and the EU and UK high-risk lists, and note sanctions exposure.
4. **Product or service**: complexity, anonymity, cross-border transfers, ability to pool or layer funds.
5. **Delivery channel**: face to face, non-face-to-face, introducer or intermediary reliance.
6. **Source of funds and source of wealth**: whether they're plausible and evidenced, and whether they match the expected activity.

## Overall rating
- Any black-list nexus, a confirmed sanctions link, or the firm's own automatic "High" triggers makes the rating **High**. Black-list countries with "countermeasures" may mean the relationship should be declined or escalated, so say so.
- A foreign PEP or a grey-list nexus normally means **EDD**, unless the firm's methodology says otherwise.
- Otherwise weigh the factors and explain the result. Don't just average them.
- State the **review frequency** using the firm's policy, or ask for it.

## File note
Write it with these headings:

1. **Customer and relationship**: who they are and the purpose and intended nature of the relationship.
2. **Information relied on**: documents and sources, with dates.
3. **Factor table**: Factor | Rating | Reason.
4. **Overall rating and CDD level**: simplified, standard or enhanced.
5. **EDD measures required**, if any: senior management approval, source of wealth evidence, enhanced monitoring.
6. **Gaps and conditions** that must be cleared before onboarding.
7. **Next review date. Prepared by / approved by** (left blank for the user to fill in).

End with: "Prepared with AI assistance; reviewed and approved by: ________".
