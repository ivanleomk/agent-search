import os
import re
import sqlite3

def chunk_markdown(content):
    """
    Split markdown content into sections based on headers.
    Returns a list of dictionaries with 'heading' and 'content'.
    """
    lines = content.split("\n")
    sections = []
    current_heading = "Overview"
    current_lines = []

    for line in lines:
        match = re.match(r"^(#+)\s+(.+)$", line)
        if match:
            # Save the previous section if it has content
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines).strip()
                })
                current_lines = []
            current_heading = match.group(2).strip()
        else:
            current_lines.append(line)

    # Add the last section
    if current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines).strip()
        })

    return sections

def main():
    docs_dir = "/Users/ivanleo/Documents/coding/agent-search/gemini_docs"
    db_path = os.path.join(docs_dir, "docs.db")

    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create docs table for full-page documents
    print("Creating docs table...")
    cursor.execute("""
        CREATE TABLE docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE,
            title TEXT,
            content TEXT
        );
    """)

    # Create FTS5 virtual table
    print("Creating FTS5 virtual table...")
    cursor.execute("""
        CREATE VIRTUAL TABLE doc_search USING fts5(
            filename,
            title,
            heading,
            content,
            tokenize="porter unicode61"
        );
    """)

    # Walk through all markdown files in the docs directory
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".md"):
            filepath = os.path.join(docs_dir, filename)
            title = filename[:-3].replace("-", " ").title() # Clean file name as title
            
            print(f"Processing: {filename} -> {title}")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Insert full page into docs table
                cursor.execute(
                    "INSERT INTO docs(filename, title, content) VALUES (?, ?, ?)",
                    (filename, title, content)
                )

                # Chunk content by markdown headers
                sections = chunk_markdown(content)
                
                # Insert chunks into the virtual table
                for sec in sections:
                    if sec["content"]: # Skip empty sections
                        cursor.execute(
                            "INSERT INTO doc_search(filename, title, heading, content) VALUES (?, ?, ?, ?)",
                            (filename, title, sec["heading"], sec["content"])
                        )
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    conn.commit()
    
    # Run a quick test query to verify FTS is working
    print("\nRunning verification query for 'token'...")
    cursor.execute("""
        SELECT title, heading, snippet(doc_search, 2, '<b>', '</b>', '...', 10) 
        FROM doc_search 
        WHERE doc_search MATCH 'token' 
        LIMIT 3;
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Match in [{row[0]} -> {row[1]}]: {row[2]}")

    conn.close()
    print("\nSQLite FTS5 database generated successfully.")

if __name__ == "__main__":
    main()
