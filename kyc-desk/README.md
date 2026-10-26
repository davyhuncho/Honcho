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

## PEPs, risk changes, restrictions and exits

Use **Change risk status** on the client file for any change outside a periodic review. Every decision needs a reason and an approver, is written to the audit trail, and produces a decision note to print, sign and file behind the cover sheet. The risk rating and relationship status can't be changed through *Edit details*.

| Decision | What happens |
|---|---|
| **Mark as PEP** | Records the connection (PEP, family member or close associate), public function, country, type, start date, how it was identified and senior management approval. The rating goes to High, the review falls due 12 months after the last review (so it may be due at once), enhanced due diligence documents join the checklist and screening moves to every 6 months. Offers to start a refresh. |
| **Remove PEP status** | Records the date the person left office. The client stays High for the enhanced-measures period (12 months by default, set in Settings). When it ends, the worklist asks whether to lower the rating. |
| **Raise or lower rating** | Shows how the next review date moves. A current PEP, or a former PEP inside the enhanced-measures period, can't be lowered below High. |
| **Restrict / lift / exit / reinstate** | Sets the relationship status. Exiting cancels any refresh in progress. A restricted client with no review in progress stays on the worklist. |

At sign-off, a PEP must be confirmed as High and senior management approval to continue the relationship must be ticked. If services are restricted, the approver must choose whether to lift the restriction or keep it.

## Password protection

The first time the app opens, it offers to set a username and password. Once set:

- Every record and scan is encrypted on the computer (AES-256, with the key derived from your password using PBKDF2). Without the password or the recovery key, the stored data is unreadable, even to someone who copies the browser's files.
- You get a **recovery key** to print and keep in the office safe. It is the only way back in if the password is forgotten. Nobody, including the app's author, can recover the records without one of the two.
- The app locks after 10 idle minutes (adjustable) and after 5 wrong passwords it makes you wait before trying again.
- Backups saved while a password is set are encrypted too. Restoring one also restores the password and recovery key that were in use when it was saved.
- Printed pages, CSV exports and downloaded scans are not encrypted. Handle them like the paper files.

## Working with an assistant

Only the compliance officer uses the app. The assistant works on paper. The **Procedure** page sets out who does what, where files live and the first checks on documents received; print it and both sign it.

- **Work pack** (Outreach or Paper files page): pick the week's files, check them out to the assistant, and print a pack with each file's task, contact details, outstanding items and a hand-back slip.
- **Cover sheet**: now includes a contact record and a documents-received log for the assistant to fill in by hand. Reprint it after each update so paper and app agree.

## Weekly report

The **Weekly report** page prints a one-page summary for management: work done in the week (reviews completed and started, requests and reminders, documents received and verified, scans, screenings, risk decisions, escalations), the position at the end of the week compared with the previous report, completed reviews, risk decisions, overdue reviews, and your notes. Press **Record end-of-week position** each Friday so the next report can show the change. Client names can be hidden so the report shows client IDs only.

## Onboarding new clients

**Add client** asks whether this is a new client or an existing one. A new client goes through onboarding: request identification documents, verify, screen and assess risk, then **Accept or decline**. Accepting sets the first periodic review date. Declining records the reason and can open an internal suspicious activity report straight away. A PEP can't be accepted without senior management approval.

## Suspicious activity register

Confidential to the MLRO. Log each internal report, record your decision and reasoning (report or not), the date and reference of any report to the Financial Intelligence Agency, follow-up notes, and closure. Each record prints for the MLRO's separate confidential file. Nothing appears on the client's file, work packs or the weekly report. If you restrict a client's services, their file shows only "Restricted by the MLRO". The annual report shows totals only, and you can switch them off.

## Matters and source of funds

Each client file has a **Matters** panel for transactions: value, where the money comes from, whether evidence is verified, and whether it fits what you know about the client. Unverified source of funds and transactions that don't fit go on the worklist, and a mismatch can open an internal report pre-filled with the details.

## Training register

The **Training** page lists staff, their last AML/CFT training and when the refresher is due (every 12 months by default). Record a session once for everyone who attended. The register prints for inspections.

## Record retention and destruction

When a client is exited or declined, the end date is recorded and records are kept for 5 years by default (set in Settings). Check this against your legal requirement. The **Paper files** page shows which files can now be destroyed. A client with an open internal report, or one you place on hold, can't be destroyed. Recording a destruction deletes the digital record and scans and keeps a permanent line in the destruction log.

## Inspection pack and annual report

- **Inspection pack** (Clients page): pick files (all high risk, a random 10, or your own choice) and print an index plus, for each file, the cover sheet, the due diligence history, matters, audit trail and, if wanted, every decision note.
- **Reports → Annual**: the MLRO's annual report for senior management, covering the client base, reviews, client decisions, suspicious activity totals, matters, training and retention, with your commentary.

## Backups: USB drive and OneDrive or SharePoint

The app stays offline. It writes encrypted backups into two ordinary folders, and OneDrive uploads the second one by itself whenever the PC is online.

**Set up once (Edge or Chrome):**
1. Set a password in the app. Cloud backups are only allowed once records are encrypted.
2. On the encrypted USB drive, make a folder called `KYC Backups`.
3. In SharePoint, open the document library your firm wants to use and press **Sync** (or **Add shortcut to My files**), so it appears in File Explorer under your firm's name. Make a `KYC Backups` folder inside it.
4. In the app, go to **Settings → Backups** and choose each folder. Allow the browser to edit files when asked.

**Every day:** press **Back up and lock** in the sidebar when you step away or finish. Each backup writes the encrypted records, any new scans, a copy of the app and restore instructions into a `KYC Refresh Desk backups` folder in each location. The app also backs up before locking itself after being idle, if the folders were already allowed that session. The newest 10 backups are kept, plus one per month for a year.

**To restore** on any computer: open `KYC Refresh Desk.html` from the backup folder in Edge or Chrome, choose **Settings → Restore from a backup folder**, pick the backup, then sign in with the password or recovery key.

**Every 3 months:** test a restore on another computer, or in a Guest window of Edge or Chrome, and record it under **Record a restore test**. The annual report lists backups and restore tests.

The app also asks the browser to protect its storage from being cleared when the disk is nearly full, and Settings shows whether that is in force. If folder backups aren't available (another browser), backups are saved as downloads instead.

## Excel export: the fail-safe copy

**Export to Excel** (Settings, the Reports page, or the reminder on the Overview) saves every record except the scans into one workbook: clients, documents, connected parties, risk assessments, decisions, PEPs, reviews, screening, outreach, matters, the full audit trail, training and retention. It opens on an **Overview** sheet with the key figures (risk mix, overdue and due reviews, documents verified and scanned) and a linked list of the sheets. Every other sheet is a named Excel table (for example `tblClients`), so filters, sorting and **Insert → PivotTable** work straight away and pick up new rows on refresh. Risk ratings, statuses and overdue reviews are colour-coded, headers and client names stay in view while scrolling, every row carries the client ID, dates are real Excel dates, and each sheet prints landscape to the page width. The suspicious activity register is included only if you tick it.

It can be read without the app or its password, so if the app ever fails, the records are still there. Run it weekly (the Overview reminds you after 7 days). If a USB backup folder is set, a copy is also saved there, keeping the newest 12. The workbook itself is **not encrypted**: keep it on the encrypted USB drive, or protect it in Excel with *File → Info → Protect Workbook → Encrypt with Password*. With 2,000 clients the workbook is about 4 MB.

## Firm logo

In **Settings → Firm and people**, choose **Add logo** and pick the firm's own logo file (PNG or JPEG, ideally with a transparent or white background). It appears in the sidebar, on the sign-in screen, at the top of printed letters, cover sheets, decision notes, work packs and reports, and on the Excel overview. The app never fetches it from the internet: it is stored with the records and included in backups. A copy is also kept unencrypted on the computer so the sign-in screen can show it; a logo is not confidential.

## Moving from paper

1. Put your existing client register into a spreadsheet and save it as CSV. Columns: `name, type, risk, pep, country, last_review, contact, email, phone, address, file_ref, file_location`. Only `name` is required.
2. In **Settings**, choose *Import clients from CSV* and tick *Remove the sample clients first*.
3. Work through the files cabinet by cabinet. For each client, record what is on paper and print the cover sheet for the front of the file.
4. Scan documents as you handle them. The *Paper files* page tracks the backlog.

## Running fully offline

`index.html` makes no internet connections. It also carries an offline lock (a Content Security Policy), so the browser refuses any attempt by the page to send data anywhere, even if the computer is online.

**On a Mac or PC**

1. Copy `index.html` to the computer, ideally from a USB stick. Put it in a folder that is not synced to iCloud, OneDrive or Dropbox, such as a new folder in your home folder.
2. Open it in Google Chrome or Microsoft Edge. Bookmark it and always open it the same way: the records belong to that browser and that file location. If you move or rename the file, the app starts empty, and you restore from a backup.
3. Turn on disk encryption (FileVault on a Mac, BitLocker on Windows) and use a strong login password with a short auto-lock.
4. Save backups to an encrypted USB drive. On a Mac, avoid Desktop and Documents if *iCloud Drive → Desktop & Documents Folders* is turned on, because those folders upload to iCloud.

**Phones and more than one device**

- Each device keeps its own separate records. Nothing syncs, because nothing is sent over a network. Treat one computer as the system of record.
- To move records between devices without the cloud, save a backup and transfer it by USB or AirDrop, then *Restore from backup* on the other device. A restore replaces everything on the receiving device.
- Phone browsers do not reliably run apps opened from local files. Running this on a phone needs it packaged as an installed app.

## Keeping data safe

- Records and scans are stored in the browser on the computer where the app is opened. Use one computer and one browser for it.
- Back up daily to the USB drive and the cloud folder (see *Backups* above). Clearing browser data deletes everything that hasn't been backed up.
- Backups saved as downloads are one **records** file plus **scan** files holding only the scans added since the last download backup. Keep every file, and restore by choosing the records file together with all the scan files.

## Capacity

Tested with 2,000 clients carrying several years of audit history (13 MB of records). Records and scans are stored in the browser's IndexedDB database, which has no practical size limit; records saved by earlier versions move there automatically on first open. Long lists show 200 rows at a time, and searching filters all clients. Large photos are reduced to 2,200 pixels on the long side when attached, which keeps them legible while saving space. PDFs are kept as they are.
- The document lists, review cycles and risk weights are starting defaults. Check them against your firm's AML/CFT policy and the current Turks and Caicos AML/PTF Regulations and Code before relying on them.
- The app ships with 24 fictional sample clients for trying the workflow. Remove them before you enter real data.
