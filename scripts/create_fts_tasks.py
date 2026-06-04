import os
import shutil
import re

def main():
    grep_dir = "/Users/ivanleo/Documents/coding/agent-search/tasks/grep"
    fts_dir = "/Users/ivanleo/Documents/coding/agent-search/tasks/fts"
    db_source = "/Users/ivanleo/Documents/coding/agent-search/gemini_docs/docs.db"

    os.makedirs(fts_dir, exist_ok=True)

    slugs = [
        "q-1-managed-agents-security",
        "q-2-interactions-api-schema",
        "q-3-live-api-session-limits",
        "q-4-deep-research-planning-mcp",
        "q-5-pro-image-search-grounding",
        "q-6-multimodal-embeddings-rag",
        "q-7-openai-compatibility-thought-signatures",
        "q-8-ai-studio-android-build",
        "q-9-inference-tiers-flex-priority",
        "q-10-context-caching-video-tokens"
    ]

    fts_info = (
        "You are responsible for answering user questions about the Gemini API and Managed Agents.\n\n"
        "A pre-indexed SQLite database is available at `/docs/docs.db` containing the parsed and indexed contents of all documentation. "
        "You MUST use SQLite queries on `/docs/docs.db` to search the documentation using Python!\n"
        "The database contains two tables:\n"
        "1. `docs`: A table containing the full content of each documentation page.\n"
        "   Schema: `CREATE TABLE docs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, title TEXT, content TEXT);`\n"
        "2. `doc_search`: A virtual FTS5 table containing chunked sections of the documentation for full-text search.\n"
        "   Schema: `CREATE VIRTUAL TABLE doc_search USING fts5(filename, title, heading, content);`"
    )

    for slug in slugs:
        src_path = os.path.join(grep_dir, slug)
        dest_path = os.path.join(fts_dir, slug)

        if not os.path.exists(src_path):
            print(f"Skipping {slug} because grep directory does not exist.")
            continue

        print(f"Copying {slug} to {dest_path}...")
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(src_path, dest_path)

        # 1. Copy docs.db into environment/docs/
        dest_db_path = os.path.join(dest_path, "environment", "docs", "docs.db")
        print(f"  Copying docs.db to {dest_db_path}...")
        shutil.copy(db_source, dest_db_path)

        # Remove all raw markdown files from environment/docs/
        dest_docs_dir = os.path.join(dest_path, "environment", "docs")
        for filename in os.listdir(dest_docs_dir):
            if filename.endswith(".md"):
                os.remove(os.path.join(dest_docs_dir, filename))
        print("  Removed raw markdown files")

        # 2. Modify instruction.md to include the FTS information
        inst_path = os.path.join(dest_path, "instruction.md")
        if os.path.exists(inst_path):
            with open(inst_path, "r", encoding="utf-8") as f:
                inst_content = f.read()

            # Find the actual question part and preserve it
            # The standard instruction format starts with raw doc info and then says "Based on the documentation, please answer..."
            match = re.search(r"(Based on the documentation, please answer the following question:.*)", inst_content, re.DOTALL)
            if match:
                new_inst = fts_info + "\n\n" + match.group(1)
            else:
                # Fallback if pattern does not match
                new_inst = fts_info + "\n\n" + inst_content

            with open(inst_path, "w", encoding="utf-8") as f:
                f.write(new_inst)
            print("  Updated instruction.md")

        # 3. Modify task.toml to change name to ivanleo/fts-<slug>
        toml_path = os.path.join(dest_path, "task.toml")
        if os.path.exists(toml_path):
            with open(toml_path, "r", encoding="utf-8") as f:
                toml_content = f.read()

            new_toml_content = re.sub(
                r'name\s*=\s*"ivanleo/q-',
                'name = "ivanleo/fts-q-',
                toml_content
            )

            with open(toml_path, "w", encoding="utf-8") as f:
                f.write(new_toml_content)
            print("  Updated task.toml name")

    print("\nAll tasks successfully migrated to FTS format.")

if __name__ == "__main__":
    main()
