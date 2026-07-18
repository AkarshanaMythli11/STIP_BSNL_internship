# Project Report: Smart Telecom Infrastructure Planner (STIP)

**A Decision Support Web Application for Optimal Telecom Site Prioritization**

---

## 1. Introduction
### 1.1 Project Objective
The principal objective of the **Smart Telecom Infrastructure Planner (STIP)** is to develop an automated, data-driven decision support system (DSS) that assists telecommunication planning engineers (specifically aligned with BSNL operational standards) in identifying and ranking geographical circles requiring urgent network coverage expansion, technology upgrades, or backhaul fiber deployment.

### 1.2 Problem Statement
Telecommunication service providers face intense competition and constrained capital expenditure budgets. Deciding where to install new base transceiver stations (BTS), where to run fiber optic lines, and where to upgrade legacy networks (2G/3G) to modern high-speed technology (4G/5G) is a complex, multi-criteria decision problem. 

Historically, this planning was done manually or through spreadsheet manipulation. These methods:
1. Suffer from inconsistencies and human bias.
2. Cannot handle batch processing of massive regional datasets efficiently.
3. Lack standardized visual analytics dashboards to represent priorities at a glance.

### 1.3 Scope of the Project
STIP automates the ingestion, calculation, ranking, and visualization of circle parameters. By calculating a mathematically standardized **Telecom Infrastructure Priority Index (TIPI)**, the system categorizes areas into High, Medium, or Low priority. Key deliverables include:
- A secure Flask-based engineer portal.
- Single-circle registry and batch Excel file imports.
- Interactive Chart.js visual dashboard.
- Automatic recommended action generation.
- Dynamic PDF and Excel report generation.

---

## 2. Requirement Analysis & Specifications
### 2.1 Functional Requirements
1. **User Authentication**: Secure user credentials validation via SQLite. Only logged-in engineers can edit, view, delete, calculate, or export.
2. **Circle Management (CRUD)**: Create, Read, Update, and Delete individual area parameters (name, population, signal strength, distance, complaints, fiber availability, technology).
3. **Priority Index Engine**: Automatically calculate the TIPI score (0–100) using a multi-criteria weighted scoring algorithm.
4. **Batch Excel Upload**: Upload an Excel dataset containing multiple circle records. Automatically map columns, parse entries, compute index values, and save to database.
5. **Interactive Dashboard & Analytics**: Render analytical summaries and dynamic visualizations including doughnut distributions and population correlation plots.
6. **Report Export Module**: Export planning indexes and recommendation tables to formatted Excel worksheets and high-fidelity PDF documents.

### 2.2 Non-Functional Requirements
1. **Security**: Password hashing using secure crypto libraries (`Werkzeug`). Session verification on all dashboard operations.
2. **Performance**: Bulk imports must execute in sub-second times using fast vectorized Pandas parsing.
3. **Aesthetics & Usability**: Modern corporate dashboard with sliding navigation, high-contrast badges, and dynamic animations utilizing Inter and Outfit typography.

### 2.3 Software and Hardware Specifications
- **Operating System**: Platform independent (Windows, Linux, macOS)
- **Language & Framework**: Python 3.x, Flask
- **Database**: SQLite3
- **Data Science Packages**: Pandas, NumPy
- **Export Engines**: OpenPyXL, ReportLab
- **Frontend Stack**: HTML5, Vanilla CSS, FontAwesome, Chart.js

---

## 3. Mathematical Model: TIPI Score Formulation
The system calculates the **Telecom Infrastructure Priority Index (TIPI)**, which ranges from $0$ to $100$. The score is a weighted linear combination of normalized indicators:

$$\text{TIPI} = \sum_{i=1}^{n} w_i \cdot S_i$$

### 3.1 Indicators and Normalization Logic
Let $P$ be population, $S_g$ be signal strength (1-5), $D$ be distance (km), $N$ be network technology, $C$ be complaint count, $I_u$ be internet users %, and $F$ be fiber availability.

1. **Population Sub-score ($S_{\text{pop}}$)**: Measures potential subscriber impact.
   $$S_{\text{pop}} = \min\left(\frac{P}{50000}, 1\right) \times 100$$
2. **Signal Strength Sub-score ($S_{\text{sig}}$)**: Prioritizes areas with poor coverage.
   $$S_{\text{sig}} = \left(1 - \frac{S_g - 1}{4}\right) \times 100$$
3. **Distance Sub-score ($S_{\text{dist}}$)**: Prioritizes regions distant from existing cell sites.
   $$S_{\text{dist}} = \min\left(\frac{D}{10}, 1\right) \times 100$$
4. **Network Type Sub-score ($S_{\text{net}}$)**: Legacy technologies receive higher priority to trigger modernization.
   - $2\text{G} \rightarrow 100$
   - $3\text{G} \rightarrow 75$
   - $4\text{G} \rightarrow 40$
   - $5\text{G} \rightarrow 10$
5. **Complaints Sub-score ($S_{\text{comp}}$)**: Prioritizes regions with poor customer satisfaction.
   $$S_{\text{comp}} = \min\left(\frac{C}{100}, 1\right) \times 100$$
6. **Internet Users Sub-score ($S_{\text{user}}$)**: Direct percentage maps to score ($S_{\text{user}} = I_u$).
7. **Fiber Sub-score ($S_{\text{fib}}$)**:
   - Fiber = "No" $\rightarrow 100$
   - Fiber = "Yes" $\rightarrow 0$

### 3.2 Weight Allocations
$$\text{TIPI} = 0.20 \cdot S_{\text{sig}} + 0.20 \cdot S_{\text{comp}} + 0.15 \cdot S_{\text{pop}} + 0.15 \cdot S_{\text{dist}} + 0.15 \cdot S_{\text{net}} + 0.10 \cdot S_{\text{fib}} + 0.05 \cdot S_{\text{user}}$$

---

## 4. Database Architecture
STIP utilizes a relational database to store circle parameters and login credentials.

### 4.1 Schema Definition
1. **`users` table**:
   - `id`: INTEGER, Primary Key, Auto-increment
   - `username`: TEXT, Unique, Not Null
   - `password`: TEXT, Hashed string, Not Null

2. **`areas` table**:
   - `id`: INTEGER, Primary Key, Auto-increment
   - `name`: TEXT, Not Null (Circle circle identification name)
   - `population`: INTEGER, Not Null
   - `signal_strength`: INTEGER, Not Null (Scale 1-5)
   - `distance`: REAL, Not Null (in km)
   - `internet_users`: INTEGER, Not Null (0-100)
   - `complaints`: INTEGER, Not Null
   - `fiber`: TEXT, Not Null ("Yes" or "No")
   - `network_type`: TEXT, Not Null ("2G", "3G", "4G", "5G")
   - `priority_score`: REAL, Calculated score (0.00 - 100.00)
   - `category`: TEXT, Class label ("High", "Medium", "Low")
   - `created_at`: TIMESTAMP, Defaults to current time

---

## 5. System Design & Routing Workflow
The backend is structured into modular routes:

```
[User Request] 
      │
      ├── GET /index ──────────► [Renders Landing Page]
      ├── POST /login ─────────► [Validates Session]
      │
      (Authenticated Session Required)
      │
      ├── GET /dashboard ──────► [Renders Analytics Cards & Upload Panel]
      ├── POST /upload ────────► [Parses Excel via Pandas -> Saves DB]
      ├── GET /view ───────────► [Displays Circle Grid & Filter Panel]
      ├── POST /calculate ─────► [Triggers DB Batch recalculation Engine]
      ├── GET /ranking ────────► [Generates Ranked recommendations]
      ├── GET /analytics ──────► [Chart.js initializes API payloads]
      └── GET /report/pdf ─────► [Compiles ReportLab story and streams PDF]
```

---

## 6. Implementation Highlights
- **Vectorized Ingestion**: Using `pandas.read_excel`, columns are cleaned and mapping is case-insensitive. A sample template is provided, preventing user input schema crashes.
- **Custom PDF Canvas Flow**: The `NumberedCanvas` subclass tracks total document page counts dynamically, adding headers and "Page X of Y" footers automatically to report pages.
- **Dynamic BSNL Recommendations**: Standard operating procedures are simulated. For instance, high priority paired with 2G/3G and no fiber generates: *"CRITICAL: Deploy fiber backhaul & replace legacy BTS with multi-sector 5G node immediately."*

---

## 7. System Testing & Verification
The system was verified against boundary cases:
1. **Auth Test**: Attempting to access `/dashboard` without cookies redirected to `/login` with flash alert message.
2. **Formula Boundary Test**: An area with population=1,000,000, signal=1, distance=25km, complaints=450, fiber=No, tech=2G, users=90 resulted in maximum index score $\approx 99.5$, marked as High Priority.
3. **Robust Excel Parsing**: Uploading sheets with missing optional cells or altered column casings (e.g., "SIGNAL") successfully resolved to correct table fields.

---

## 8. Conclusion & Future Scope
The developed system demonstrates how database integration and automated linear mathematical modeling can replace legacy telecom circle analysis tools. STIP provides planning engineers with immediate data-driven priorities, eliminating manual bias.

**Future Enhancements include**:
1. Integration of Google Maps APIs to render circle points geographically.
2. Real-time API connections with cell site health monitoring tools.
3. Predictive forecasting of user growth using machine learning algorithms.
