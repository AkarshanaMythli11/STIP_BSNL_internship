# 📡 Smart Telecom Infrastructure Planner (STIP)

> A professional, web-based Decision Support System for Telecom Engineers to identify and prioritize areas requiring network infrastructure upgrades — built as an operational planning tool aligned with BSNL standards.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Render-46E3B7?style=for-the-badge)](https://stip-bsnl-internship.onrender.com)

> 🌐 **Live App:** [https://stip-bsnl-internship.onrender.com](https://stip-bsnl-internship.onrender.com)
> 
> ⚠️ *Hosted on Render free tier — the server may take ~30 seconds to wake up on first visit after inactivity.*

---

## 🔍 Abstract

The rapid growth of telecommunication services has increased the demand for efficient planning and optimal utilization of network infrastructure. Telecom service providers face challenges in deciding which geographical areas should be prioritized for network expansion or infrastructure upgrades due to limited resources and increasing customer demands.

**STIP** automates this decision-making process by computing a **Telecom Infrastructure Priority Index (TIPI)** for each registered circle using a multi-criteria weighted scoring algorithm. The system ranks areas from highest to lowest priority and generates detailed reports and visual analytics to support engineering decisions.

---

## 🌐 Website Architecture

```
Home (Landing Page)
   │
   ▼
Login (Engineer Portal)
   │
   ▼
Dashboard
   │
   ├── Add Area            (Single-circle registration form)
   ├── View Areas          (Searchable/filterable table + Edit/Delete/View modal)
   ├── Rankings            (Sorted TIPI list + BSNL Recommendations)
   ├── Analytics           (4 Chart.js graphs)
   ├── Reports             (Excel + PDF downloads + Print Manager)
   └── Logout
```

---

## 📐 TIPI Score Formula

The **Telecom Infrastructure Priority Index (TIPI)** ranges from 0–100:

```
TIPI = 0.20×Signal + 0.20×Complaints + 0.15×Population + 0.15×Distance + 0.15×NetworkType + 0.10×Fiber + 0.05×InternetUsers
```

| Category | TIPI Threshold | Recommended Action |
|---|---|---|
| 🔴 High Priority | TIPI ≥ 75 | Immediate Fiber + 5G BTS Installation |
| 🟡 Medium Priority | 45 ≤ TIPI < 75 | Scheduled 4G LTE Upgrade |
| 🟢 Low Priority | TIPI < 45 | Routine Preventive Maintenance |

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| Database | SQLite3 |
| Data Processing | Pandas |
| Report Generation | OpenPyXL (Excel), ReportLab (PDF) |
| Frontend | HTML5, Vanilla CSS, Chart.js |
| Icons | FontAwesome 6 |
| Typography | Google Fonts (Inter, Outfit) |

---

## 📁 Project Structure

```
stip/
│
├── app.py                    # Flask backend (routes, TIPI engine, file upload, exports)
├── db_init.py                # SQLite schema creator + default data seeder
├── verify_stip.py            # Automated test suite (4 unit tests)
├── requirements.txt          # Python dependencies
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css         # Custom BSNL-branded CSS design system
│
├── templates/
│   ├── base.html             # Shared layout (sidebar, header, footer)
│   ├── index.html            # Landing page
│   ├── login.html            # Standalone login card
│   ├── dashboard.html        # Metrics + Excel upload + quick nav
│   ├── add_area.html         # Add/Edit area form
│   ├── view_area.html        # Table view + search filter + detail modal
│   ├── ranking.html          # Ranked list + BSNL recommendations
│   ├── analytics.html        # 4 Chart.js interactive graphs
│   └── report.html           # Export panel + print preview
│
├── uploads/                  # Temporary Excel uploads (auto-created, git-ignored)
├── reports/                  # Generated PDF/Excel output (auto-created, git-ignored)
│
├── stip_project_report.md    # Software Engineering Project Report
└── stip_research_paper.md    # IEEE-style Publication-Ready Research Paper
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/stip.git
cd stip
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Initialize the Database
This creates `database.db`, the admin user, and seeds 12 mock telecom circles:
```bash
python db_init.py
```

### Step 4 — Run the Application
```bash
python app.py
```

### Step 5 — Open in Browser
Navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔐 Default Login Credentials

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `admin123` |

---

## 📊 Key Features

- ✅ **Secure Login** — Session-based authentication with hashed passwords
- ✅ **Area Management** — Full CRUD for telecom circle records
- ✅ **TIPI Engine** — Automated weighted scoring calculation
- ✅ **Batch Excel Import** — Upload `.xlsx` files with multiple circles for bulk calculation
- ✅ **Template Download** — Pre-formatted Excel template to guide user uploads
- ✅ **Interactive Analytics** — Bar chart, Doughnut, Pie, and Scatter plots (Chart.js)
- ✅ **Priority Rankings** — Full ranked list with engineering recommendations
- ✅ **PDF Export** — Professional multi-page PDF with headers, footers, and color-coded tables (ReportLab)
- ✅ **Excel Export** — Color-coded, formatted spreadsheet download (OpenPyXL)
- ✅ **Print Manager** — Print-ready view with automatic sidebar suppression

---

## 🧪 Running Tests

```bash
python verify_stip.py
```

**Test Results (Expected):**
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.3s

OK
```

---

## 📄 Documentation

| Document | Description |
|---|---|
| [stip_project_report.md](stip_project_report.md) | Full Software Engineering Project Report (SRS, Architecture, DB Schema, Testing) |
| [stip_research_paper.md](stip_research_paper.md) | IEEE-format Research Paper (Abstract, Literature Review, Methodology, Results) |

---

## 🚀 Deployment

This project is **live on Render.com** (free tier):

| | |
|---|---|
| 🌐 **Live URL** | [https://stip-bsnl-internship.onrender.com](https://stip-bsnl-internship.onrender.com) |
| ☁️ **Platform** | [Render.com](https://render.com) |
| 🐍 **Runtime** | Python 3.11 + Gunicorn |
| 🗄️ **Database** | SQLite3 |
| 🔁 **Auto-deploy** | Enabled — pushes to `master` deploy automatically |

### Notes
- Free tier servers **sleep after 15 min of inactivity** — first request may take ~30s to wake up
- SQLite database resets on each new deploy (no persistent disk on free tier)
- `SECRET_KEY` is set via Render environment variable (not hardcoded)

---

## 👨‍💻 Author

Developed as part of a Telecom Engineering research project aligned with **BSNL infrastructure planning standards**.

---

## 📜 License

This project is for academic and educational use.
