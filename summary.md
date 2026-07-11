# Autonomous Candidate Shortlisting Agent Network

An enterprise-ready, decentralized multi-agent candidate matchmaking and shortlisting pipeline built on the **Neuro SAN** (System of Agent Networks) framework and driven by the low-latency reasoning capabilities of **Google Gemini Flash**. 

This repository implements the **AAOSA (Adaptive Agent-Oriented Software Architecture)** protocol to dynamically parse inbound Job Descriptions (JDs), query a localized candidate data stream, and generate a meritocratic evaluation match matrix with comprehensive guardrails against LLM hallucinations and empty states.

---

## 1. Architectural Design & Topology

The application relies on a decentralized agent network where data propagates downstream via a shared conversation context log rather than rigid, hardcoded function parameters.


```

```
              [ ShortlistOrchestrator ] (Frontman Node)
                         │
                         ▼ (AAOSA Context Handoff)
              [ RecruitmentScreener ] (Sub-Agent Node)
                         │
                         ▼ (Deterministic Tool Loop)
               [ CandidateFilterTool ] (Python Coded Tool)

```

```

### Core Node Responsibilities
*   **`ShortlistOrchestrator` (The Frontman Node):** 
    *   Acts as the primary network entry point matching the framework's array constraints.
    *   Ingests raw text job specifications, orchestrates downstream sub-agent delegation, implements defensive empty-state validation filters, and compiles the final structured markdown overview dashboard.
*   **`RecruitmentScreener` (Sub-Agent Node):** 
    *   Isolates target core technical skills out of the workflow context.
    *   Invokes the deterministic data storage tools and performs analytical match-scoring metrics against returned applicant criteria.
*   **`CandidateFilterTool` (Python Coded Tool Node):** 
    *   Acts as the network's programmatic extension to access hardware or database frameworks natively.
    *   Maps AI-extracted criteria string fragments directly to local database queries.

---

## 2. Key Engineering Core Features

### 🛠️ AI-Driven Dynamic Data Querying
Instead of relying on hardcoded keyword index maps or static routing matrices, this architecture delegates criteria isolation directly to the model context layer. Gemini Flash dynamically extracts key architectural tools and technical stacks (e.g., `Kafka, Spark, Python`) from the user prompt and passes them as real-time parameters into the custom `CandidateFilterTool`, which queries rows dynamically using parameterized SQL matches.

### 🛡️ Guardrailed Zero-Match Logic & Safeguards
To eliminate the risk of LLMs attempting to parse empty arrays or hallucinating dummy candidate entities when database queries return zero intersections, the system features tight conditional checks:
1.  If the query layer returns an empty dataset, the `CandidateFilterTool` responds with an explicit fallback data footprint: `{"status": "empty", "matching_candidates": []}`.
2.  The `RecruitmentScreener` catches this token and outputs the literal string `NO_SUITABLE_CANDIDATES_FOUND`.
3.  The parent `ShortlistOrchestrator` flags this string, terminates further dashboard processing, and prints a user-friendly diagnostic alert warning: `NO MATCHING CANDIDATES FOUND...`

### ⚡ Reorder Optimization for Server Stability
Array positioning dictates topology routing inside Neuro SAN. Placing a python class-based `CodedTool` containing a `"class"` definition at index `0` of the `"tools"` array results in a fatal initialization crash (`Internal server error: No valid front man found`). This stable configuration solves the constraint by anchoring the pure LLM node (`ShortlistOrchestrator`) at the top position and sinking the Python utility tool to the bottom of the stack configuration.

---

## 3. Project File Structure

Ensure your project file system is laid out according to the following structure to guarantee accurate module import paths:

```text
├── coded_tools/candidate_filter.py      # Python module containing the CodedTool class
├── update_db.py               # Database initialization and mock data seeding script
├── candidates.db            # Local SQLite database file (generated after seed run)
└── registries/
    ├── manifest.hocon       # System server registration registry manifest map
    └── candidate_shortlist.hocon  # Core declarative multi-agent topology configuration

```

---

## 4. Setup & Quickstart Guide

Follow these procedural steps to initialize your local environment and run a verification pass inside the Neuro SAN Studio web UI client panel:

### Step 1: Scaffold and Install Dependencies

Ensure you have the required agent framework packages and runtime tools installed within your active python workspace:

```bash
pip install neuro-san-studio
ns init --providers google

```

### Step 2: Seed the Local Relational Database

Run the mock data initialization script to create the local SQLite engine layer and insert sample technical candidate rows containing background metrics and skill tags:

```bash
python update_db.py

```

### Step 3: Verify Local Database Rows

You can confirm that the database has successfully seeded by executing a quick standalone python check script:

```bash
python -c "import sqlite3; conn=sqlite3.connect('candidates.db'); print(conn.execute('SELECT id, skills FROM candidate_pool;').fetchall()); conn.close()"

```

### Step 4: Register the Network Config Manifest

Open your central `registries/manifest.hocon` file and declare your new custom shortlister layout array configuration block:

```

### Step 5: Start the Local Orchestration Server

Export your required Google Gemini platform credential token keys directly to your environment shell and launch the visualization engine:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
ns run

```

Open up your web browser and navigate to the visual designer workbench dashboard located at `http://127.0.0.1:4173/`. Select the **Candidate Shortlist Network** layout option from the dropdown menu interface to trigger operational prompt runs.

```
