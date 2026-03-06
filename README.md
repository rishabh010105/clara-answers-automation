# Clara Answers Automation Pipeline

Welcome to the Clara Answers zero-cost automation pipeline repository. This pipeline simulates the real-world operational challenge of taking messy conversational data (from Sales/Demo calls and Support/Onboarding calls) and reliably transforming it into production-ready configuration artifacts for the Retell AI Voice Agent.

## Overview and Data Flow

This repository contains:

1.  **Pipeline A (Demo -> v1)**: Ingests `account_demo.txt` -> Extracts `Account Memo JSON` -> Generates `Retell Agent Spec v1`.
2.  **Pipeline B (Onboarding -> v2)**: Ingests `account_onboarding.txt` and `Account Memo JSON v1` -> Generates updated `Account Memo JSON v2` -> Generates differential `changelog.md` -> Generates updated `Retell Agent Spec v2`.

### The Dataset

Five mock accounts with varying complexities are located in `dataset/demo/` and `dataset/onboarding/`. The mock dataset contains transcripts that include missing details in Pipeline A, which are clarified in Pipeline B:
- `Account1`: Fire & Safety Pros (Standard transfer and fallback logic)
- `Account2`: Aqua HVAC (Strict integration constraints regarding ServiceTrade)
- `Account3`: Rapid Electrical (Routing to multiple numbers with constraints)
- `Account4`: Peak Facilities (Strict emergency requirements)
- `Account5`: Elite Alarms (Tiered timeouts and backup routing)

## Architecture

The orchestrator (`scripts/pipeline.py`) acts as the core controller, processing the datasets locally and securely. The pipeline is built to be run on a daily cadence via an n8n scheduled workflow.

-   `extractor.py`: Parses transcripts using pattern-matching to extract the precise account configuration constraints (simulating a zero-cost local LLM model like Ollama for the sake of deterministic reproducibility across environments).
-   `prompter.py`: Uses the structured JSON logic from the extractor to build a perfectly hygienic system prompt template, fulfilling all prompt engineering requirements (business hours, after-hours, and transfer protocols).
-   `patcher.py`: Manages version control. It merges the extracted updates from onboarding directly over the v1 memo configuration, resolving unknowns, and building a clean differential Markdown update (`changelog.md`).
-   **Asana Simulator**: The pipeline simulates an API POST request by generating a mock Asana Task Track item per account to `outputs/tasks/` representing the required tracking item creation block.

## Setup Instructions

### Local Orchestrator (n8n Setup)

We provide an exported `workflows/n8n_workflow.json` to orchestrate this system on a CRON schedule without compromising local safety:

1. Start your local n8n instance via Docker: `docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n`
2. Navigate to `http://localhost:5678`.
3. Click "Import from File" and upload `workflows/n8n_workflow.json`.
4. The workflow utilizes the `Execute Command` node to trigger `python scripts/pipeline.py`, combining local zero-cost deterministic extraction with n8n orchestration.

### Local Execution (Zero-Cost Python Stack)

We chose a completely local Python-based execution over pure cloud tools like Zapier or Make due to the strict zero-cost limit. This eliminates free-tier usage caps, allows processing of all transcripts seamlessly, and does not require credit card verifications for APIs. 

1. Ensure Python 3.9+ is installed.
2. Clone this repository.
3. Open a terminal and run the core pipeline script:

```bash
python scripts/pipeline.py
```

### Outputs

After execution, examine the `outputs/` directory.

For each account, you will find:
```
outputs/
├── accounts/<account_id>/
│   ├── v1/
│   │   ├── agent_spec.json
│   │   └── memo.json
│   └── v2/
│       ├── agent_spec.json
│       ├── changelog.md
│       └── memo.json
└── tasks/
    └── <account_id>_task.json
```

### Using outputs with Retell

Once pipeline execution generates the `agent_spec.json`:

1.  Log in to the Retell dashboard (Free Tier).
2.  Navigate to "Create Agent".
3.  Select the **Voice** (e.g., 11labs-Rachel) as described in the JSON.
4.  Copy the `system_prompt` from the JSON into the "System Prompt" window.
5.  If transfer protocols require a physical integration to a telephony service, configure the custom Retell parameters using the routing rules defined inside the `memo.json` and agent tool placeholders (`transfer_call`).

## Known Limitations

-   The script relies on a deterministic `extractor.py` parsing function to avoid external API costs.
-   In a production environment (with API budgets), the `extractor.py` must be swapped to use an LLM provider such as OpenAI `gpt-4o-mini` via HTTP. The schema is built cleanly to easily drop the LLM in to output the Pydantic structured output directly.

## Improvements with Production Access

-   **Integrations**: Implement standard Webhook nodes to push `memo.json` directly into standard CRMs like ServiceTrade or Salesforce, preventing duplicate data entry.
-   **Audio Ingestion**: Run a local Whisper model to transcribe raw `.wav` or `.mp3` call recordings on the fly inside `pipeline.py`.
