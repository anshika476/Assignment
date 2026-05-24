# Closira — AI Customer Support Workflow
**Bloom Aesthetics Clinic Demo** | Built with Python + Anthropic Claude API

---

## What It Does

A CLI-based AI receptionist that handles real customer conversations end-to-end:

| Stage | Behaviour |
|---|---|
| FAQ Answering | Answers questions strictly from `sop.json`. Never guesses. |
| Lead Qualification | Collects service interest, prior experience, and referral source naturally across the conversation. |
| Escalation Detection | Detects complaints, anger, medical questions, out-of-scope queries, and explicit human requests. Logs all escalations to `escalation_log.txt`. |
| Conversation Summary | Auto-generates a structured CRM-ready summary at session end. Saved to a timestamped `.txt` file. |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/closira-demo.git
cd closira-demo
```

### 2. Install dependencies
```bash
pip install anthropic
```

### 3. Set your API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```
Get a key at: https://console.anthropic.com

### 4. Run
```bash
python main.py
```

---

## Project Structure

```
closira-demo/
├── main.py                          # Core workflow script
├── sop.json                         # Clinic SOP data (AI's only knowledge source)
├── prompt_design.md                 # System prompt + design decisions
├── README.md                        # This file
├── escalation_log.txt               # Auto-created on first escalation
├── summary_YYYYMMDD_HHMMSS.txt      # Auto-created at session end
└── test_transcripts/
    ├── 01_in_sop_question.md
    ├── 02_out_of_scope.md
    ├── 03_escalation_trigger.md
    ├── 04_lead_qualification.md
    └── 05_conversation_summary.md
```

---

## How to End a Session
Type `exit`, `bye`, `goodbye`, or `quit`. The summary is generated automatically.

---

## Trade-offs & Known Limitations

- **No persistent memory** — each run is a fresh session. No database is used.
- **Single-turn qualification** — the bot asks one qualification question per turn to keep flow natural; this means collection takes several exchanges.
- **Escalation is terminal** — once escalated, the bot holds the line and doesn't continue answering. A production system would hand off to a live agent queue.
- **JSON output dependency** — the workflow relies on the model returning valid JSON every turn. A fallback escalation triggers if parsing fails, but this should be rare with Claude.
- **SOP is static** — the SOP is loaded once at startup. A production version would reload from a database on each session.

---

## Dependencies

- Python 3.8+
- `anthropic` — `pip install anthropic`

No other dependencies required.