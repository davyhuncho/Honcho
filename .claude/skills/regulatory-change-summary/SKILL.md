---
name: regulatory-change-summary
description: Summarise a new AML/CFT or sanctions development (a TCI FSC or FIA notice, legislation or regulation change, FATF publication, OFSI/OFAC guidance, CFATF report) and explain what it means for a TCI regulated firm. Use when the user shares or links a regulatory notice, consultation, guidance or law change and asks what changed, whether it affects them, or what to do.
---

# Regulatory change summary

Gives the MLRO a short, sourced brief on one regulatory development and the actions it creates.

## Ground rules
- **Work from the source text.** Read the document the user provides or links.
  If you can't open it (some regulator sites block automated access), ask the user to paste the relevant parts.
  Never summarise a regulation from memory or from news coverage alone.
- Quote the section or paragraph number for every point of substance.
- Separate what the document **says** from your **interpretation**, and label the interpretation.
- This is not legal advice. Flag points where external counsel or the regulator should be consulted.

## Brief format
1. **What it is**: issuer, title, date, status (consultation, final, in force on a date), and link.
2. **What changed**: bullet points, each with a section reference. Compare with the previous position where the document shows it.
3. **Who it applies to**: say whether the user's firm type is in scope. If you don't know their sector, ask.
4. **Key dates**: in-force date, transition periods, consultation deadline.
   Offer to add them to `compliance_dashboard/data/calendar.json` (tag "Regulatory"), which makes them appear on the morning brief.
5. **Impact and actions**: the policies, procedures, risk assessment, systems, training and customer populations affected. Give each a suggested owner and priority.
6. **Open questions**: points that are unclear in the text.

## Hand-offs
- **Policy gaps**: if the regulatory-legal plugin is installed, offer to run its `policy-diff` skill to compare the change against the firm's policy library, and `policy-redraft` to draft fixes.
- **FATF list changes**: use the `fatf-plenary-update` skill.
- **New sanctions designations that need re-screening**: use the `sanctions-match-triage` skill.
- **Board reporting**: keep the brief short enough to paste into the regulatory section of the `mlro-board-report` skill's output.
