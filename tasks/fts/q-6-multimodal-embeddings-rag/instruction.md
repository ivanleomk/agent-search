You are responsible for answering user questions about the Gemini API and Managed Agents.

A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!
The database contains two tables:
1. `docs`: A table containing the full content of each documentation page.
   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`
2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.
   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`

Based on the documentation, please answer the following question:
So I'm storing product images and descriptions to build a visual catalog search. If I use the new multimodal embedding model to encode these assets, do I still need to manually normalize the vectors if I decide to truncate them to a smaller size? Also, how can I configure a managed RAG store to handle these image searches instead of running a vector database myself?

Please write your final complete answer to `output.txt` at the root of the workspace.
