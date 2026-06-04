You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
So I have a CRM sync application where we process thousands of customer records sequentially, but we also have a live chat feature where our agents talk to premium leads. I want to optimize cost and latency for both workloads. What synchronous tiers should I use, what are the cost differences, and what happens if our live chat suddenly gets hit with huge spikes in traffic?

Please write your final complete answer to `output.txt` at the root of the workspace.
