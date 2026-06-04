You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
I'm writing a Python service using the OpenAI library with Gemini 3.5 Flash. I need to implement multi-turn sequential function calling. How do thought signatures show up in the OpenAI compatibility layer, when are they validated, and is there any way to bypass validation if I need to inject mock histories for testing?

Please write your final complete answer to `output.txt` at the root of the workspace.
