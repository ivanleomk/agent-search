# Conversational Multi-Hop Synthetic Questions

This file contains 10 natural, conversational evaluation questions generated from the Gemini API and Managed Agents documentation.

## Question 1

**Question:**
> Hey, I'm building a custom coding agent that needs to clone a private GitHub repository, install some dependencies, and run tests inside a secure sandbox. How can I safely pass my GitHub Personal Access Token to the agent without exposing it in the sandbox files or environment variables? Also, how can I make sure the agent only has outbound access to GitHub and PyPI, and what happens to the files we create after the session goes idle?

**Target Topics:**
Managed Agents Security, Agent Environments, Environment Lifecycle, Network Rules

**Ground Truth Answer:**
To safely pass your GitHub Personal Access Token (PAT) without exposing it in the sandbox environment variables or files, you should use the network transform feature within the environment's network allowlist. First, base64-encode your token in the format 'x-oauth-basic:YOUR_PAT'. Then, define a network rule for 'github.com' (or 'api.github.com') with a 'transform' block containing 'Authorization': 'Basic <YOUR_BASE64_TOKEN>'. The egress proxy will automatically inject this header on matching outbound requests. To restrict the network, set the 'network.allowlist' array to only contain the domains 'github.com' (and/or 'api.github.com') and 'pypi.org' with any needed wildcards. Once the session is done, the environment will automatically snapshot and stop after 15 minutes of inactivity (Idle state). The sandbox is kept for up to 7 days of being inactive (Offline state) before it is permanently deleted from the system, allowing you to resume by ID within that period.

---

## Question 2

**Question:**
> So I'm migrating my chatbot to the new version of the system. My app generates a markdown description and then creates an illustration graphic. How does the request configuration change under the new steps schema compared to the old outputs array, especially if I want to enforce an output JSON structure for the text and set specific aspect ratios and dimensions for the generated image?

**Target Topics:**
Interactions API Breaking Changes, Structured Outputs, Multimodal Generation

**Ground Truth Answer:**
In the new Interactions API schema, the legacy flat 'outputs' array is replaced by the 'steps' array, which organizes the timeline of the turn into structured steps (such as 'user_input', 'thought', and 'model_output'). To request both structured text and image generation in a single call, you must configure the top-level, polymorphic 'response_format' field as an array instead of using 'generation_config.response_mime_type' and 'generation_config.image_config' (which have both been removed). Your 'response_format' array should contain two entries: 1) A 'text' type entry specifying 'mime_type': 'application/json' and your defined 'schema' (e.g. using a Zod or Pydantic JSON schema). 2) An 'image' type entry specifying the 'mime_type' (like 'image/jpeg' or 'image/png'), 'aspect_ratio' (e.g., '16:9'), and 'image_size' (e.g., '2K' or '4K'). When the stream returns, the text will stream in 'step.delta' events with type 'text' under a 'model_output' step, and the image will arrive as base64-encoded data under a 'step.delta' event with type 'image'.

---

## Question 3

**Question:**
> I want to build an always-listening, real-time voice assistant using the Live API. What are the connection and session duration limits I need to plan around, how does the billing work for a long-running audio call, and will enabling Proactive Audio save me money on the new Gemini 3.1 models?

**Target Topics:**
Live API Session Management, Live API Billing, Proactive Audio

**Ground Truth Answer:**
Without compression, audio-only Live API sessions are limited to 15 minutes (2 minutes with video), and the physical WebSocket connection terminates after approximately 10 minutes. To bypass these limits, you must enable 'context_window_compression' (e.g., configuring a sliding window) and use 'session_resumption' to reconnect using a saved session handle within 2 hours of disconnection. Regarding billing, the Live API charges a compounding cost: on every turn (each user input and model response), you are billed for all accumulated tokens currently in the active context window, including historical audio tokens (which accumulate at roughly 25 tokens per second) at the standard audio input rate. If text transcription is enabled, you are additionally billed for the text tokens at standard output rates. Enabling Proactive Audio allows the model to decide not to respond to irrelevant inputs; when active, you are only billed for output tokens when the model actively replies (though input tokens are billed continuously while listening). However, Proactive Audio is not supported on Gemini 3.1 Flash Live (it requires Gemini 2.5), so it will not save you money on 3.1 models.

---

## Question 4

**Question:**
> Hey, I'm building a market-mapping research tool and want to use the Deep Research agent, but I need to collaboratively approve and refine its research plan before it starts executing. Also, can I hook up my own custom database API as a tool for the agent to call? And roughly what kind of cost am I looking at per task run?

**Target Topics:**
Deep Research Agent, Collaborative Planning, Deep Research Tools, Agent Pricing

**Ground Truth Answer:**
To review and refine the research plan before execution, set 'collaborative_planning': true in your first 'interactions.create' call. The agent will return a proposed plan. You can iterate and refine the plan through a multi-turn conversation by passing the 'previous_interaction_id'. To execute the research, call the API again with 'collaborative_planning': false (or omit it) and 'background': true. Regarding custom tools, Deep Research does not support user-defined custom function calling directly, but you can connect remote Model Context Protocol (MCP) servers by passing the 'mcp_server' tool type with a URL and authentication headers, or use standard tools (Search, URL Context, Code Execution, and File Search). For pricing, you are charged on a pay-as-you-go basis for the underlying model's tokens (including cached tokens, which typically cover 50-70% of inputs) plus search query fees. A standard task run on 'deep-research-preview-04-2026' is estimated to cost between $1.00 and $3.00, while a comprehensive 'deep-research-max-preview-04-2026' run is estimated to cost between $3.00 and $7.00.

---

## Question 5

**Question:**
> I'm looking to use Gemini 3 Pro Image to generate high-resolution visual assets. Can I use Google Search grounding with this model to fetch real-time weather information and reflect it in the graphic? If so, what metadata is returned in the API response, and what are the specific legal and UI requirements I must follow when displaying the grounded image to end-users?

**Target Topics:**
Gemini 3 Pro Image, Search Grounding, Service Usage Requirements

**Ground Truth Answer:**
Yes, Gemini 3 Pro Image (gemini-3-pro-image) is a reasoning model that can use Google Search grounding to fetch real-time information and generate high-resolution images up to 4K. When grounding is active, the response returns 'groundingMetadata' containing 'webSearchQueries' (the executed queries), 'searchEntryPoint' (rendered HTML/CSS for search suggestions), 'groundingChunks' (web source URIs and titles used for context), and 'groundingSupports' (mapping text segments to chunks). When displaying these grounded results, you must strictly comply with Google's service requirements: 1) You must display the source attributions immediately following the grounded image, viewable within one user interaction. 2) You must attribute sources to Google Maps or Google Search without modifying the text (e.g., maintain capitalization, do not translate, use standard Roboto font, minimum 12sp size, and include the translate='no' attribute). 3) You must provide a direct, single-click link from the source preview or image to its containing web page without intermediate viewers or multi-click paths.

---

## Question 6

**Question:**
> So I'm storing product images and descriptions to build a visual catalog search. If I use the new multimodal embedding model to encode these assets, do I still need to manually normalize the vectors if I decide to truncate them to a smaller size? Also, how can I configure a managed RAG store to handle these image searches instead of running a vector database myself?

**Target Topics:**
Gemini Embedding 2, Vector Normalization, File Search (Managed RAG)

**Ground Truth Answer:**
No, you do not need to manually normalize the vectors when truncating. While the older 'gemini-embedding-001' required manual normalization for truncated sizes, the new 'gemini-embedding-2' automatically renormalizes truncated dimensions (e.g. 768 or 1536) when using the 'output_dimensionality' parameter. If you want to avoid running your own vector database, you can use the managed File Search tool. To handle images, first create a 'FileSearchStore' using 'client.file_search_stores.create()' and explicitly set the 'embedding_model' config to 'models/gemini-embedding-2' (this is required to enable multimodal RAG). Once created, you can directly upload PNG or JPEG images (up to 4K x 4K) to the store using 'upload_to_file_search_store' or import existing files. The service will handle chunking, embedding, and indexing. You can then query the store by enabling the 'file_search' tool in your 'generate_content' calls.

---

## Question 7

**Question:**
> I'm writing a Python service using the OpenAI library with Gemini 3.5 Flash. I need to implement multi-turn sequential function calling. How do thought signatures show up in the OpenAI compatibility layer, when are they validated, and is there any way to bypass validation if I need to inject mock histories for testing?

**Target Topics:**
Thought Signatures, OpenAI Compatibility, Troubleshooting Signatures

**Ground Truth Answer:**
In the OpenAI compatibility layer, thought signatures are returned inside the 'tool_calls' array under the 'extra_content.google.thought_signature' field. Because the Gemini API is stateless, these encrypted thought signatures must be returned to the model in subsequent turns to preserve reasoning context. Validation is strictly enforced for all function calls in the current active turn: the first 'functionCall' part in each step of the active turn must contain its matching 'thought_signature' exactly as received, or the API will return a 400 validation error ('missing a thought_signature'). If you need to bypass this validation for testing (e.g., injecting mock histories or transfer traces from other models), you can set the thought signature field of your custom function call parts to a dummy signature value of either 'context_engineering_is_the_way_to_go' or 'skip_thought_signature_validator'.

---

## Question 8

**Question:**
> Hey, I've been prototyping a mobile-first app in Google AI Studio's Build Mode. If I switch the platform picker from Web to Android, can I still use the Workspace Google Sheets integration and Firebase authentication? Also, how do I actually get the app onto my phone to test it?

**Target Topics:**
AI Studio Build Mode, AI Studio Android Apps, WebUSB Installation

**Ground Truth Answer:**
No, if you switch the platform picker to Android in AI Studio, you cannot use Google Workspace integrations (like Google Sheets) or Firebase authentication. Full-stack features that require a server-side runtime, including Workspace APIs, Firebase database/auth, multiplayer, and secrets management, are strictly supported for Web apps only; Android apps in AI Studio are client-side only and use Jetpack Compose. To install and test the generated Android app on your physical phone, you do not need a local Android SDK or ADB installation. Instead, connect your phone to your computer with a USB cable, enable Developer Options and USB Debugging on your device, and click the 'Install on Device' button in the AI Studio preview panel. This will use WebUSB directly in your browser to transfer and install the APK on your device.

---

## Question 9

**Question:**
> So I have a CRM sync application where we process thousands of customer records sequentially, but we also have a live chat feature where our agents talk to premium leads. I want to optimize cost and latency for both workloads. What synchronous tiers should I use, what are the cost differences, and what happens if our live chat suddenly gets hit with huge spikes in traffic?

**Target Topics:**
Inference Tiers, Flex Inference, Priority Inference, Graceful Degradation

**Ground Truth Answer:**
For the sequential CRM sync, you should use the Flex inference tier by setting 'service_tier': 'flex' in your requests. It processes requests synchronously but runs on off-peak, sheddable capacity, offering a 50% discount compared to standard rates with a variable latency target of 1 to 15 minutes. For the live chat, you should use the Priority inference tier ('service_tier': 'priority') to route requests to premium, non-sheddable compute queues for ultra-low, sub-second latency, though it costs 75% to 100% more than standard rates. If your live chat experiences massive spikes in traffic that exceed your priority limits (which default to 0.3x your standard limit), the API will automatically and gracefully downgrade those overflow requests to Standard processing instead of failing with 429 or 503 errors. These downgraded requests are processed at standard speeds and billed at standard rates, protecting your application from outages.

---

## Question 10

**Question:**
> Wait, I'm building a video analysis tool where users upload an hour-long MP4 file and ask multiple sequential questions about it. I want to use explicit context caching to save on inputs. What is the default lifespan of the cache, how is the video converted to tokens to calculate the size of my cache, and how is the storage billed?

**Target Topics:**
Context Caching, Video Tokenization, Caching Billing

**Ground Truth Answer:**
When you create an explicit context cache using 'client.caches.create()', the cache has a default Time-to-Live (TTL) of 1 hour, though you can manually update its 'ttl' or 'expire_time' to adjust this. To calculate the token size of your video for caching, Gemini tokenizes video at a rate of 263 tokens per second at standard resolution, which consists of 258 tokens per frame (sampled at 1 FPS by default) plus 32 tokens per second for audio. Consequently, an hour of video (3600 seconds) translates to approximately 1,080,000 tokens (or ~230,400 tokens if using the 'low' media resolution setting, which reduces frame costs to 66 tokens/frame). For billing, you pay the standard caching rate to first index your video, and then you are billed for the storage duration based on the cached token count per hour (e.g., $1.00 per 1M tokens/hour on Gemini 3.5 Flash; $0.03 per 1M tokens/hour on Gemini 2.5 Flash). Subsequent queries that hit this cache are then billed at a 90% discount on input tokens.

---

