import os
import json
import glob
from google import genai
from google.genai import types


def read_all_docs():
    print("Reading markdown documents...")
    doc_texts = []
    # Read all md files in gemini_docs/
    for filepath in glob.glob("gemini_docs/*.md"):
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            doc_texts.append(f"--- FILE: {filename} ---\n{content}\n")
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")

    print(f"Read {len(doc_texts)} documents.")
    return "\n".join(doc_texts)


def main():
    docs_context = read_all_docs()

    client = genai.Client()

    prompt = """
You are an expert evaluator designing a benchmark for RAG (Retrieval-Augmented Generation) and multi-hop reasoning over the Gemini API and Managed Agents documentation.

Based on the provided documentation contents, generate 10 highly natural, conversational, and complex multi-hop evaluation questions.

Each question must satisfy these requirements:
1. It MUST sound like a natural, casual user asking a real-world developer question (e.g. starting with "Hey, I was looking at...", "So I'm building...", "Wait, does this mean...").
2. It MUST NOT mention file names, section headers, or explicit paths in the documentation.
3. It MUST require combining facts from 3 to 4 distinct documents or feature areas (e.g., combining Managed Agents sandbox limits, Google Search grounding metadata structure, and pricing or thinking signatures) to answer fully.
4. It should force the model to perform "multi-hop" retrieval—grabbing different points and blending them together.

For each question, provide:
- The conversational question.
- The target topics/documents it spans.
- A comprehensive, extremely accurate 'ground_truth' answer based solely on the provided documentation.

Return the result as a raw JSON list of objects matching this schema:
[
  {
    "question": "The natural, conversational question string.",
    "target_topics": ["topic/document 1", "topic/document 2", ...],
    "ground_truth": "The detailed, complete ground-truth answer combining all the facts."
  }
]

Do not return any extra markdown styling around the JSON (no ```json code blocks), just return the raw JSON string.
"""

    print("Calling Gemini 3.5 Flash to generate questions...")
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=docs_context),
                    types.Part.from_text(text=prompt),
                ],
            )
        ],
        config=types.GenerateContentConfig(
            # Using JSON output format if possible
            response_mime_type="application/json"
        ),
    )

    try:
        raw_text = response.text.strip()
        # Parse JSON
        questions = json.loads(raw_text)

        # Save to JSON file
        json_output = "data/natural_synthetic_questions_2.json"
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2)
        print(f"Successfully saved JSON to {json_output}")

        # Save to Markdown file
        md_output = "data/natural_synthetic_questions.md"
        with open(md_output, "w", encoding="utf-8") as f:
            f.write("# Conversational Multi-Hop Synthetic Questions\n\n")
            f.write(
                "This file contains 10 natural, conversational evaluation questions generated from the Gemini API and Managed Agents documentation.\n\n"
            )
            for idx, q in enumerate(questions):
                f.write(f"## Question {idx + 1}\n\n")
                f.write(f"**Question:**\n> {q['question']}\n\n")
                f.write(f"**Target Topics:**\n{', '.join(q['target_topics'])}\n\n")
                f.write(f"**Ground Truth Answer:**\n{q['ground_truth']}\n\n")
                f.write("---\n\n")

        print(f"Successfully saved Markdown to {md_output}")

    except Exception as e:
        print("Error parsing response or writing files:", str(e))
        print("Raw response from model was:")
        print(response.text)


if __name__ == "__main__":
    main()
