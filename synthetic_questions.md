# Gemini API & Managed Agents: Synthetic Multi-Hop Evaluation Questions

This document presents a set of complex, multi-hop evaluation questions designed to test a model's ability to retrieve, synthesize, and reason over disparate sections of the Gemini API and Managed Agents documentation.

---

## Question 1: Managed Agents Setup, Sandboxing, and Search Grounding

### The Question
> "We want to deploy a custom managed agent using the Antigravity agent. Can you tell us:
> 1. What underlying model powers it?
> 2. How the Linux sandbox environment handles external resources (specifically file size limits and authentication/authorization config for private GitHub repos)?
> 3. When the agent uses the default Google Search tool, what structured metadata is returned to help us attribute sources, and how can we programmatically insert inline citations into the final text using the SDK response?"

### Target Pages & Chunks
* **Model definition:** `gemini_docs/antigravity-agent.md` (lines 1-10)
* **Sandbox limits & private repo auth:** `gemini_docs/agent-environment.md` (lines 263-305 and 378-419)
* **Google Search metadata & inline citation logic:** `gemini_docs/google-search.md` (lines 97-189)

### Ground Truth Answer
1. **Underlying Model:** The Antigravity agent is powered by **Gemini 3.5 Flash** (using the same harness as the Antigravity IDE).
2. **Environment Sandbox Limits & Auth:**
   * **Size Limits:** When mounting external sources, the Git repository limit is **500 MB**, Cloud Storage is **2 GB**, and inline file content is **1 MB per file** (up to a **2 MB total**).
   * **Private GitHub Repo Auth:** Access requires `Basic` authentication using a GitHub Personal Access Token (PAT). The username should be set to `x-oauth-basic` and the token is Base64 encoded as `x-oauth-basic:ghp_YourPATHere` to form the `Authorization: Basic <base64>` header, configured within the `network.allowlist` domain transforms block.
3. **Google Search Metadata & Citations:**
   * The API returns a `groundingMetadata` block containing `webSearchQueries` (the queries run), `groundingChunks` (URIs and titles of web sources), and `groundingSupports` (text segments linked to chunks by index).
   * **Inline Citation Implementation:** To insert citations (e.g. `[1](url)`), you must sort `groundingSupports` by the segment's `endIndex` in **descending order** (to avoid character shifting as you insert strings) and loop through the supports to append markdown links pointing to the URIs in `groundingChunks`.

### Why This Forces Multi-Hop Reasoning
* **Hop 1:** Find the core model powering Antigravity in the agent overview.
* **Hop 2:** Locate the environment sandbox specification to find file limits and Git repository size limits.
* **Hop 3:** Extract the specific Base64 format and domain transformation mapping needed to authenticate private Git checkouts.
* **Hop 4:** Jump to the search grounding docs to retrieve the structure of `groundingMetadata` and explain the reverse-sorting end-index insertion logic required to programmatically render citations.

---

## Question 2: Interactions API Server-Side History, Retention, and Compaction

### The Question
> "We are transitioning from the classic `generateContent` API to the new Interactions API. Can you explain:
> 1. What are the retention differences for stored interactions between the free and paid tiers?
> 2. Are there any features from the classic API—specifically regarding caching and batch tasks—that are not yet supported by the Interactions API?
> 3. In a long multi-turn session using a managed agent, how does the API automatically optimize context length to prevent token limit errors, and what parameters do we pass to continue both the conversation context and the sandbox state across turns?"

### Target Pages & Chunks
* **Tier Retention & API Limitations:** `gemini_docs/interactions-overview.md` (lines 93-115 and 151-164)
* **Context Compaction:** `gemini_docs/managed-agents-quickstart.md` (lines 112-116)
* **Multi-Turn parameters:** `gemini_docs/managed-agents-quickstart.md` (lines 61-111)

### Ground Truth Answer
1. **Retention differences:** Stored interactions (`store=true`) are retained for **55 days** on the Paid Tier, and **1 day** on the Free Tier.
2. **Unsupported classic features:** The **Batch API** and **explicit caching** are not yet available in the Interactions API (though server-side implicit caching is supported).
3. **Context Length Optimization & Turn Parameters:**
   * **Context Compaction:** The API features an automatic **context compaction** step that triggers at around **135k tokens** to prevent context rot.
   * **Multi-turn parameters:** To continue, you must pass two parameters in your `interactions.create` call:
     * `previous_interaction_id`: preserves the conversation history (inputs and outputs).
     * `environment`: takes the `environment_id` to reuse the existing Linux sandbox workspace/files.
     * Note: parameters like `tools` and `system_instruction` are interaction-scoped and must be re-specified on each turn.

### Why This Forces Multi-Hop Reasoning
* **Hop 1:** Retrieve storage/retention limits from the paid vs. free metadata sections.
* **Hop 2:** cross-reference the supported model/feature list to find what classic tools are missing in the Beta revision.
* **Hop 3:** Pull the token threshold value for context compaction from the Quickstart guide.
* **Hop 4:** Connect the state persistence parameters (conversation ID vs. environment ID) and highlight that system instructions must be re-sent on every turn since they are interaction-scoped.

---

## Question 3: Customizing Agents, Custom Skills, and Deep Research

### The Question
> "We want to build a custom agent. 
> 1. What is the functional difference between customizing the Antigravity agent inline versus saving it as a registered agent?
> 2. How do we structure a custom skill folder in our workspace so the runtime correctly registers and loads it?
> 3. If we decide to use the Deep Research agent instead of a general custom agent, what are the three specific model IDs we can use, and can we mix a standard Gemini model with the Deep Research agent in the same conversation? If so, how do we link them?"

### Target Pages & Chunks
* **Inline vs Saved & Skill Folder Structure:** `gemini_docs/custom-agents.md` (lines 1-12 and 107-126)
* **Deep Research Model IDs & Mixing:** `gemini_docs/interactions-overview.md` (lines 120-139)

### Ground Truth Answer
1. **Inline vs. Saved Customization:** Inline customization passes instructions, tools, and sources directly in the `interactions.create` call without any pre-registration. Saving a configuration registers it as a managed agent that is permanently stored and invoked by a unique agent ID.
2. **Skill Folder Structure:** Skills must be placed in a directory structured as `.agents/skills/<skill-name>/` containing a `SKILL.md` file. The `SKILL.md` file must begin with YAML frontmatter containing metadata (e.g. `name: <skill-name>`) followed by the Markdown instructions describing how to use the skill.
3. **Deep Research & Model Mixing:**
   * **Model IDs:** The three model IDs for Deep Research are:
     * `deep-research-pro-preview-12-2025`
     * `deep-research-preview-04-2026`
     * `deep-research-max-preview-04-2026`
   * **Mixing:** Yes, you can mix standard Gemini models and Deep Research within a single conversation. You link them by passing the `previous_interaction_id` of the Deep Research step into the subsequent model interaction (or vice versa), allowing the server to retrieve the shared history.

### Why This Forces Multi-Hop Reasoning
* **Hop 1:** Retrieve Custom Agent definition types (inline vs. registered).
* **Hop 2:** Extract the exact folder syntax (`.agents/skills/`) and internal file metadata required for skill loading.
* **Hop 3:** Search model IDs in the table of supported models for the Interactions API to find the three Deep Research revisions.
* **Hop 4:** Connect the state persistence logic to explain model mixing in the same multi-turn session.

---

## Question 4: Gemini Thinking, Budgets, and Thought Signatures

### The Question
> "We want to leverage Gemini's reasoning capabilities. 
> 1. In Python, how do we configure a dynamic thinking level for Gemini 3.5 Flash versus a specific token budget for Gemini 2.5 Flash, and can thinking be fully disabled for Gemini 3.1 Pro?
> 2. What are 'thought signatures', why are they returned, and what are the rules when passing them back to the model?
> 3. How do we retrieve the reasoning thoughts in the output candidates of the response?"

### Target Pages & Chunks
* **Thinking Level, Budgets, and Disabling:** `gemini_docs/thinking.md` (lines 369-382 and 487-510)
* **Thought Signatures:** `gemini_docs/thinking.md` (lines 618-639)
* **Retrieving thoughts:** `gemini_docs/thinking.md` (lines 96-139)

### Ground Truth Answer
1. **Thinking Settings:**
   * **Gemini 3.5 Flash:** Set `thinking_level` in `ThinkingConfig` to a level like `"low"`, `"medium"`, `"high"`, or `"minimal"`. Dynamic thinking is turned on by default (equivalent to `"high"` or `"medium"` depending on model complexity).
   * **Gemini 2.5 Flash:** Set `thinking_budget` in `ThinkingConfig` to a specific token count (e.g. `1024` or up to `24576`). Setting `thinking_budget = -1` turns on dynamic thinking. Set `thinking_budget = 0` to fully disable thinking.
   * **Gemini 3.1 Pro:** No, you **cannot** fully disable thinking for Gemini 3.1 Pro. The lowest setting is `minimal` (which doesn't guarantee thinking is off, though it minimizes it).
2. **Thought Signatures:** 
   * Thought signatures are encrypted representations of the model's internal thought process. They are returned because the Gemini API is stateless; they maintain the context of the model's reasoning process across turns.
   * **Rules:** You must always pass the entire response with all signatures back to the model in subsequent turns (especially for function calling). Do not concatenate parts containing signatures together, and do not merge a signature part with a non-signature part.
3. **Retrieving Thoughts:** In your configuration, set `include_thoughts=True` (under `thinking_config`). When you receive the response, iterate through the `parts` of the candidate. Check if `part.thought` is `True` to access the reasoning text.

### Why This Forces Multi-Hop Reasoning
* **Hop 1:** Differentiate between the newer `thinkingLevel` parameters and the older `thinkingBudget` settings for Gemini 3 vs. 2.5.
* **Hop 2:** Extract the specific constraints for disabling thinking on Pro models.
* **Hop 3:** Connect the stateless nature of the API to the usage rules for thought signatures to prevent context breaking.
* **Hop 4:** Outline the exact configuration parameters (`include_thoughts`) and response field inspection logic (`part.thought`) to capture reasoning output.
