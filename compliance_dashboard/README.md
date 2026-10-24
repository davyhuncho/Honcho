# MLRO Morning Brief

A one-page compliance dashboard for a Money Laundering Reporting Officer in the Turks and Caicos Islands.
Open it each morning to see:

- **FATF black and grey lists**: the current jurisdictions, how long each has been listed, what changed at recent plenaries, and a countdown to the next plenary. Every list entry, "listed since" date and plenary change was checked against FATF statements and FATF-sourced regulator notices on 24 Oct 2026. Each run also checks fatf-gafi.org and shows a red banner when a newer statement has been published.
- **Country risk lookup**: type a country (aliases like "BVI", "DRC" and "North Korea" work) to see its FATF status, plus quick links to the UK, OFAC and EU sanctions search tools.
- **News**, in four groups: Turks & Caicos and the Caribbean, FATF, Sanctions (UK OFSI, UK sanctions list, OFAC, UN), and AML/CFT (enforcement, FinCEN, FCA, typologies, TF/PF). Stories published since your last visit are marked **NEW**. Stories that mention your watch terms (TCI, Caribbean, BVI, CFATF and so on) are tagged, and a filter can show only those.
- **Today's routine**: a daily MLRO checklist. Ticks reset each day and you can add your own tasks.
- **Key dates**: FATF plenaries and your own deadlines.
- **Quick links**: TCI FSC, FIA Ordinance, MLRO guideline, sanctions lists, FATF, CFATF, Egmont, Wolfsberg.

On your phone, it installs as a Home Screen app and can send you a morning notification (see **On your iPhone**).

It needs only Python 3.9 or newer. There is nothing to install, so it runs on a locked-down work PC.

## Run it

```bash
cd compliance_dashboard
python run.py            # fetch everything, build output/index.html, open it in your browser
python run.py --serve    # or keep it running at http://localhost:8765 and refresh hourly
python run.py --offline  # FATF lists and checklist only, with no network
```

On Windows, use `py run.py`. If a source is down, the dashboard shows the last copy it fetched, marked "cached".

### Have it ready every morning

- **Windows Task Scheduler**: create a daily task at 7:30am that runs `py C:\path\to\compliance_dashboard\run.py --no-open`, then bookmark `output\index.html`.
- **GitHub Pages (no PC needed)**: `.github/workflows/compliance-dashboard.yml` rebuilds the page at 6am TCI time every weekday and publishes it. To enable it, go to repo Settings → Pages → Source and choose "GitHub Actions". You can also trigger a run by hand from the Actions tab. Note that the Pages site is public unless your GitHub plan supports private Pages. The page holds only public information; checklist ticks stay in your browser.

## On your iPhone

### 1. Home Screen app
After the GitHub Pages site is switched on (above), it lives at `https://<your-github-username>.github.io/Honcho/`.

1. Open that address in **Safari** on your iPhone.
2. Tap the **Share** button (square with an arrow), then **Add to Home Screen**, then **Add**.

You now have an **MLRO Brief** icon that opens the dashboard full-screen like an app. If you have no signal, it shows the last brief you opened.

### 2. Morning push notification
Every weekday at 6am TCI time, the rebuild can send you a notification like:

> **MLRO Brief - Mon 26 Oct**
> FATF plenary in 2 days.
> 2 new on your watch list (TCI, Caribbean, BVI...):
> - …

It is high priority if FATF has published new lists. Tap it to open the brief. Setup takes about 3 minutes:

1. Install the free **ntfy** app from the App Store.
2. Pick a private topic name that nobody could guess, e.g. `mlro-brief-7f3k9q2x`. (ntfy topics work like a password: anyone who knows the name can read them. The messages only contain public news headlines.)
3. In the ntfy app, tap **+** and subscribe to that topic name.
4. On GitHub, open the repo **Settings → Secrets and variables → Actions → New repository secret**. Set the name to `NTFY_TOPIC` and the value to your topic name.
5. Test it: **Actions** tab → **Compliance dashboard** → **Run workflow**. The notification should arrive within about a minute.

To use it from your own PC instead, set `NTFY_TOPIC` (and optionally `DASHBOARD_URL`) and run `python run.py --notify`.

Note: on iPhone, tapping a notification opens the brief in Safari rather than in the Home Screen app. That is an Apple restriction.

## Keep it current (5 minutes, three times a year)

After each FATF plenary (February, June and October), the red banner will tell you a new statement exists. Edit `data/fatf_lists.json`:

1. Update `grey_list` / `black_list` from the official statements, using the links in the banner.
2. Add an entry at the top of `history` with the countries added and removed.
3. Update `as_of`, `as_of_label`, `sources` and `next_plenary`.

Run `python -m unittest discover -s tests` to check that the file is consistent.

## Customise

| File | What it controls |
|---|---|
| `data/sources.json` | News feeds (any RSS/Atom URL or Google News search), watch terms, quick links |
| `data/calendar.json` | Key dates. Add your Board reports, regulatory returns, audits and training, plus future FATF/CFATF plenaries once they are announced |
| `data/checklist.json` | Daily routine items |
| `data/fatf_lists.json` | FATF lists and change history |

> This tool collects public information for convenience and is not legal advice. Before acting on it,
> check the official FATF, sanctions authority and TCI FSC / FIA publications.
