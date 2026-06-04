You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
Hey, I've been prototyping a mobile-first app in Google AI Studio's Build Mode. If I switch the platform picker from Web to Android, can I still use the Workspace Google Sheets integration and Firebase authentication? Also, how do I actually get the app onto my phone to test it?

Please write your final complete answer to `output.txt` at the root of the workspace.
