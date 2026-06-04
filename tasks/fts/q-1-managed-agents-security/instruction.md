You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
Hey, I'm building a custom coding agent that needs to clone a private GitHub repository, install some dependencies, and run tests inside a secure sandbox. How can I safely pass my GitHub Personal Access Token to the agent without exposing it in the sandbox files or environment variables? Also, how can I make sure the agent only has outbound access to GitHub and PyPI, and what happens to the files we create after the session goes idle?

Please write your final complete answer to `output.txt` at the root of the workspace.
