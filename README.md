# Faking a Filesystem vs. Querying a Database: Why Local Grep Beat SQL Round-Trips in Agent Search

This repository contains the benchmark code, dataset, and results comparing a raw filesystem search setup (Grep) against a database-centric setup (SQLite FTS) across the Google Gemini API & Managed Agents documentation (~300k tokens of text over 94 documents).

## The Task & Architectures

We evaluated the performance of an agent (built with the Antigravity SDK) answering 10 complex, multi-hop retrieval questions under two architectures:

### 1. Grep Baseline Setup
* **Architecture:** The agent is given a local sandbox containing the raw markdown files (300k tokens of data). It searches and reads them using direct, native tools like directory listing, grep, and `view_file`.
* **Execution:** Fast, local, in-process file operations.

### 2. SQLite FTS Setup
* **Architecture:** Raw markdown files are deleted. All 300k tokens are pre-indexed into a SQLite database (`/docs/docs.db`) containing two tables:
  1. `docs`: Stores the full page text of each document.
  2. `doc_search`: A virtual FTS5 table containing chunked headings and content snippets.
* **Execution:** The agent must query the SQLite database by running Python script commands via `run_command`.

---

## Results

| Metric | Grep Baseline Run | SQLite FTS Run (Resumed) |
| :--- | :--- | :--- |
| **Mean Reward** | **0.800** (8/10 passed) | **0.700** (7/10 passed) |
| **Total Input Tokens** | **3.67M** | **5.86M** |
| **Total Cost (USD)** | **$2.45** | **$3.48** |
| **Harbor Hub Job Link** | [Job 18c065f1 (Grep)](https://hub.harborframework.com/jobs/18c065f1-d900-4d55-a201-69db4efbaebd) | [Job bc96451b (FTS)](https://hub.harborframework.com/jobs/bc96451b-ef7d-4e03-9c63-e669fe2aaa00) |
| **Harbor Hub Dataset** | [ivanleo/agent-search](https://hub.harborframework.com/datasets/ivanleo/agent-search) | [ivanleo/agent-search](https://hub.harborframework.com/datasets/ivanleo/agent-search) |

