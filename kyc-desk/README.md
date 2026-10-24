# KYC Refresh Desk

A single-file app for running periodic KYC reviews (refreshes and remediation) at a paper-based firm. The paper file stays the record. The app is the register and tracker that sits next to it.

**To use it:** download `index.html` and open it in Chrome or Edge. It needs no installation or internet connection, and nothing is sent anywhere.

## What it does

| Area | Purpose |
|---|---|
| **Overview** | Overdue reviews, reviews due in the next 90 days, chasers due, ID expiries, scanning progress, and a prioritised worklist for the day. |
| **Clients** | The client register: risk rating, last and next review, refresh stage, document completeness and paper file location. |
| **Client file** | Document checklist (status, received date, expiry, on paper, scanned, attached scan), connected parties, risk assessment, screening, outreach and audit trail. |
| **Refresh pipeline** | Every open review by stage: *Due → Awaiting client → Verify documents → Screening & risk → MLRO sign-off*. |
| **Outreach** | Who you are waiting on, how long, and when to send a reminder or escalate. Drafts request, reminder and final-notice letters. |
| **Paper files** | Where each physical file is, who has it checked out, and how much is scanned. Prints a cover-sheet checklist for the front of each file. |
| **Settings** | Review cycles, chase timings, firm and approver names, backups and CSV import. |

## The process it follows

1. **Schedule.** The next review date comes from the risk rating: by default every 12 months for high risk, 24 for medium and 36 for low. A review shows as due 90 days ahead. Trigger events, such as an expired ID, stale screening or a new owner, show up on the worklist too.
2. **Request.** *Start refresh* pre-selects what to ask for: documents renewed at every review, plus anything missing, expired, or expiring before the next cycle. It then drafts the request letter.
3. **Chase.** By default, a first reminder goes at 14 days, a final notice at 30, and the file goes to the MLRO at 60 days, with the option to restrict services.
4. **Receive and file.** As documents arrive, put the certified copy on the paper file, tick *On paper*, scan it, tick *Scan* and attach the scan.
5. **Verify.** The review can't move on until every required document and connected party is verified.
6. **Screen and re-rate.** Record sanctions, PEP and adverse media screening, then update the risk assessment.
7. **Sign off.** The MLRO or approver confirms the risk rating, which sets the next review date. Every step is written to the client's audit trail.

## Moving from paper

1. Put your existing client register into a spreadsheet and save it as CSV. Columns: `name, type, risk, pep, country, last_review, contact, email, phone, address, file_ref, file_location`. Only `name` is required.
2. In **Settings**, choose *Import clients from CSV* and tick *Remove the sample clients first*.
3. Work through the files cabinet by cabinet. For each client, record what is on paper and print the cover sheet for the front of the file.
4. Scan documents as you handle them. The *Paper files* page tracks the backlog.

## Keeping data safe

- Records and scans are stored in the browser on the computer where the app is opened. Use one computer and one browser for it.
- Use *Save backup file* in Settings regularly, and store the backup where your firm keeps compliance records. Clearing browser data deletes everything that hasn't been backed up.
- The document lists, review cycles and risk weights are starting defaults. Check them against your firm's AML/CFT policy and the current Turks and Caicos AML/PTF Regulations and Code before relying on them.
- The app ships with 24 fictional sample clients for trying the workflow. Remove them before you enter real data.
