You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
So I'm migrating my chatbot to the new version of the system. My app generates a markdown description and then creates an illustration graphic. How does the request configuration change under the new steps schema compared to the old outputs array, especially if I want to enforce an output JSON structure for the text and set specific aspect ratios and dimensions for the generated image?

Please write your final complete answer to `output.txt` at the root of the workspace.
