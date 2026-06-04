.PHONY: run-fts run-grep run-fts-q1 regenerate-db regenerate-tasks

run-fts:
	./.venv/bin/harbor run --env docker -n 3 -p tasks/fts -a antigravity-sdk -m gemini-3.5-flash --ve GEMINI_API_KEY=$$GEMINI_API_KEY

run-grep:
	./.venv/bin/harbor run --env docker -n 3 -p tasks/grep -a antigravity-sdk -m gemini-3.5-flash --ve GEMINI_API_KEY=$$GEMINI_API_KEY

run-fts-q1:
	./.venv/bin/harbor run --env docker -p tasks/fts/q-1-managed-agents-security -a antigravity-sdk -m gemini-3.5-flash --ve GEMINI_API_KEY=$$GEMINI_API_KEY

regenerate-db:
	./.venv/bin/python scripts/generate_sqlite_docs.py

regenerate-tasks:
	./.venv/bin/python scripts/create_fts_tasks.py
