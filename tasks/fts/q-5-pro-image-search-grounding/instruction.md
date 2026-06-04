You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
I'm looking to use Gemini 3 Pro Image to generate high-resolution visual assets. Can I use Google Search grounding with this model to fetch real-time weather information and reflect it in the graphic? If so, what metadata is returned in the API response, and what are the specific legal and UI requirements I must follow when displaying the grounded image to end-users?

Please write your final complete answer to `output.txt` at the root of the workspace.
