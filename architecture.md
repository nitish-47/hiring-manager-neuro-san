# Architectural Specification: Autonomous Candidate Shortlisting Agent Network

## 1. Problem Statement & Objective
Enterprise recruitment pipelines struggle with massive influxes of unstructured candidate data (resumes, portfolios, text profiles) that require manual keyword matching or rely on rigid boolean filters. Traditional automated screening tools frequently suffer from:
*   **Contextual Blindness:** An inability to read beyond exact keyword matches to understand underlying technical experience and scale.
*   **Hallucination Risks:** Naive AI wrappers that confidently invent profile qualifications or mismatch candidate IDs when processing complex data fields.
*   **System Fragility:** Tight infrastructure coupling where altering a job profile requires rebuilding parsing logic.

### The Mission
This project addresses these challenges by establishing an **Autonomous Candidate Shortlisting Agent Network**. The core objective is to ingest an arbitrary text-based Job Description (JD), dynamically deduce critical technical requirements using language models, safely isolate and search a localized database layer, and present a meritocratic, ranked candidate match matrix—all while maintaining data integrity through strict empty-state validation loops.

---

## 2. The Agentic Advantage
This application moves away from traditional, procedural coding architectures where standard control structures dictate code execution paths. Instead, it deploys an **Agentic System** characterized by decentralized decision-making, natural language instruction mapping, and autonomous tool manipulation.


```

```text
   [ Input: Job Description Text ] ──> UI Entry
                  │
                  ▼
    ┌───────────────────────────┐
    │   ShortlistOrchestrator   │ <── [ LLM Agent: Context Handler ]
    └─────────────┬─────────────┘
                  │ (AAOSA Context Handoff Loop)
                  ▼
    ┌───────────────────────────┐
    │    RecruitmentScreener    │ <── [ LLM Agent: Evaluator & Strategist ]
    └─────────────┬─────────────┘
                  │ (Autonomous Tool Call)
                  ▼
    ┌───────────────────────────┐
    │   CandidateFilterTool     │ <── [ Python Coded Tool: Relational DB Bridge ]
    └─────────────┬─────────────┘
                  │ (Dynamic SQL Parameterization)
                  ▼
         [ SQLite Database ]

```

### Highlights of the Agentic Architecture:
1.  **Natural Language Contracts (AAOSA Protocol):** The system relies on the **Adaptive Agent-Oriented Software Architecture (AAOSA)** framework protocol. Rather than passing data via strict, brittle programmatic function signatures (e.g., `filter_resumes(id=1, skill="Java")`), agents communicate asynchronously by extending and interpreting a shared **Conversation Context Log**. 
2.  **Autonomous Tool Identification:** The `RecruitmentScreener` sub-agent acts as an active strategist. Upon reading the conversation history, it dynamically identifies the mandatory technical constraints, determines that it lacks internal data access, and autonomously generates a structured tool execution call payload targeting the database layers.
3.  **Dynamic Parameter Generation:** When the agent calls the database, it produces the search criteria strings entirely on the fly based on semantic evaluation. If given a Data Engineering JD, it extracts `"Kafka, PySpark"`; if given a Frontend JD, it derives `"TypeScript, React"`. The single downstream Python module satisfies both without hardcoded routing.

---

## 3. Node Specification & System Topologies

The agent network topology is declared in a unified, hierarchical `.hocon` format, configuring each node as a functional block within a `"tools"` array. The system positioning maps as follows:

### Node 1: `ShortlistOrchestrator` (The Frontman Network Master)
*   **Type:** Generative LLM Node (`gemini-3-flash`)
*   **Responsibility:** Intercepts the primary text stream payload, functions as the top-level coordinator across the network graph, and builds the final UI layout matrix.
*   **Agentic Strategy:** Implements defensive empty-state checkpoints. It evaluates the down-chain conversation logs for a specialized error token flag string. If caught, it truncates code parsing loops immediately to suppress AI hallucinations, returning a user-facing warning alert dashboard instead of an empty layout table.

### Node 2: `RecruitmentScreener` (The Analytical Sub-Agent)
*   **Type:** Generative LLM Node (`gemini-3-flash`)
*   **Responsibility:** Maps out competency criteria and handles internal tool loops.
*   **Agentic Strategy:** Processes raw requirements, triggers the underlying database tool layers using dynamically generated search keys, reads the text result payloads returned by the hardware execution pipeline, and derives a numerical percentage match score for each profile.

### Node 3: `CandidateFilterTool` (The Functional Coded Tool Bridge)
*   **Type:** Python Class Module (`candidate_filter.CandidateFilterTool`)
*   **Responsibility:** Provides the network boundary interface allowing the LLM agent network to interact deterministically with the filesystem.
*   **Implementation Strategy:** Inherits from Neuro SAN's `CodedTool` wrapper. It defines clear schema inspection methods (`name`, `description`, `parameters`) to bypass runtime object reflection bugs, catches text strings passed by the AI, parses them, and executes dynamic, parameterized SQL queries against the local `candidates.db` file.

---

## 4. Execution Journey & Data Propagation Lifecycle

1.  **Intake Processing:** The host user provides a search prompt string to the `ShortlistOrchestrator` entry point node.
2.  **Semantic Handoff:** The orchestrator writes the data to the conversation context map log and invokes the `RecruitmentScreener`.
3.  **Tool Call Serialization:** The screener evaluates the text payload, extracts required hard technical competencies, and writes out a JSON tool arguments packet.
4.  **Hardware Query Interception:** The Neuro SAN framework pauses the generative model stream, intercepts the JSON payload, instantiates the local `CandidateFilterTool` Python class, and triggers its `async_invoke` sequence.
5.  **Relational Database Fetch:** The Python code queries the SQLite database using dynamic `LIKE` conditions based on the AI's keywords. 
6.  **Safeguard Branching:**
    *   *Path A (Empty Pool):* The DB returns 0 rows. The tool returns `{"status": "empty"}`. The Screener appends the exact string token `NO_SUITABLE_CANDIDATES_FOUND` to the history log. The Orchestrator halts formatting loops and displays a clean warning alert.
    *   *Path B (Matches Found):* The DB returns profile text blocks. The Screener evaluates the matches against the JD, calculates scoring weights, and prints the candidate logs. The Orchestrator intercepts this and formats a neat markdown table listing Rank, Candidate ID, Match Score %, and Alignment details.

