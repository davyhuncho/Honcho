---
name: mlro-board-report
description: Prepare the MLRO's periodic (quarterly or annual) AML/CFT report to the board or senior management. Use when the user asks for an MLRO report, board report, compliance report, annual AML report or management information pack.
---

# MLRO board report

Builds a board-ready report from the dashboard's data plus figures the user provides.
Every number must have a source. Claude never makes up statistics.

## 1. Agree the scope
Ask for:
- The reporting period
- The audience (board, audit committee, senior management)
- The firm's existing report template, if any. If there is one, follow its headings exactly, and suggest saving it as `references/template.md` in this skill folder.

## 2. Gather inputs
From the repo:
- **FATF**: `compliance_dashboard/data/fatf_lists.json`. Take each `history` entry dated within the period, plus the current black and grey lists and the `other_lists` notes. Flag any listed jurisdiction where the firm has customers. You'll need to ask the user which ones.
- **Key dates**: `compliance_dashboard/data/calendar.json`, for plenaries, deadlines, audits and training in or after the period.
- **Sanctions**: the dashboard keeps only the last 30 days of UK and OFAC changes, on the published brief at https://davyhuncho.github.io/Honcho/. For longer periods, ask the user for the number of re-screens and hits, or summarise only what's available and say so.

From the user (record "not provided" for anything missing):
- Number of customers by risk rating, and new high-risk or PEP relationships approved
- Internal disclosures received, SARs filed, and average time to decide. Give counts only, with no case details.
- Sanctions screening alerts, true matches, and assets frozen or reported
- Training completed (percentage of staff, and topics)
- Audit, regulator inspection or FSC findings and their remediation status
- Policy and procedure updates, and risk assessment refreshes
- Resourcing, systems issues and incidents

## 3. Write the report
Use these headings:

1. **Executive summary**: three to five key messages and decisions or approvals the board must make.
2. **Regulatory and threat environment**: FATF plenary outcomes, sanctions developments, TCI/FSC/FIA changes (the `regulatory-change-summary` skill output can feed this).
3. **Customer risk profile**: tables and short commentary.
4. **Suspicious activity reporting**: statistics and themes, with no identifying details.
5. **Sanctions compliance.**
6. **Training and awareness.**
7. **Assurance**: audit, monitoring and inspections, with open actions shown as owner, due date and RAG status.
8. **Policies, procedures and the business-wide risk assessment.**
9. **Resources and systems.**
10. **Priorities for next period.**
11. **Matters for board decision.**

Keep it concise: board readers want what changed, what's at risk and what you need from them.
Put tables in an appendix.
Offer the output as a doc (shareable and editable) or a Word file if the user names that format.
End with "Prepared by the MLRO with AI assistance; figures as provided by [sources]".
