# Prompt Design — Closira / Bloom Aesthetics Clinic

---

## 1. Full System Prompt

The system prompt is built dynamically in `build_system_prompt()` inside `main.py`.
It has four sections injected at runtime:

1. **Persona** — Aria, a warm professional receptionist
2. **SOP data block** — the entire `sop.json` injected verbatim
3. **Qualification instruction** — which question to ask next, updated every turn
4. **Response schema** — exact JSON structure the model must return

The full template:

```
You are Aria, a warm and professional virtual receptionist for Bloom Aesthetics Clinic.

════════════ SOP DATA — YOUR ONLY SOURCE OF TRUTH ════════════
{sop_json}
══════════════════════════════════════════════════════════════

CORE RULES:
1. Answer ONLY using the SOP data above. Never invent prices, availability, or policies.
2. If a question is NOT answerable from the SOP, do NOT guess. Set escalate=true instead.
3. Escalate immediately for: complaints, medical questions, pricing negotiation,
   angry/frustrated sentiment, explicit human requests, or 2+ unanswered questions in a row.
4. Tone: warm, concise, professional. Suitable for a premium aesthetics clinic.
5. You MUST reply ONLY with valid JSON. No text outside the JSON block.

{qualification_instruction}

UNANSWERED QUESTIONS IN A ROW SO FAR: {unanswered_count}

ALWAYS respond with this JSON structure:
{
  "reply": "your message to the customer",
  "escalate": false,
  "escalation_reason": null,
  "answered_from_sop": true,
  "qualification_update": {
    "service_interest": null,
    "prior_treatments": null,
    "heard_from": null
  }
}
```

---

## 2. Key Design Decisions

### Why dynamic prompt rebuilding on every turn?
The system prompt is rebuilt before every API call so the model always has the
latest conversation state: how many questions it has asked, which lead fields are
still missing, and how many questions in a row have gone unanswered. This removes
the need for a separate stage-detection call.

### Why inject the full SOP as JSON?
JSON is structured, unambiguous, and easy for the model to parse. Using the raw
JSON rather than prose reduces the chance of the model misinterpreting nested
relationships (e.g. service name vs. price vs. description).

### Why force one qualification question per turn?
Asking multiple questions at once feels robotic and can overwhelm customers. By
telling the model exactly which single question to work in "when the conversation
allows", the qualification flow stays natural rather than feeling like a form.

---

## 3. Hallucination Prevention

Three layered safeguards:

**a) Explicit prohibition in the system prompt**
```
Answer ONLY using the SOP data above.
Never invent prices, availability, or policies.
```

**b) Grounding via full SOP injection**
The entire SOP is present in the context window. The model doesn't need to recall
anything from training data — every fact it needs is right there.

**c) Structured output with `answered_from_sop` flag**
The model is required to set `"answered_from_sop": false` whenever it cannot find
the answer in the SOP. The application code then increments `unanswered_count` and
triggers escalation after 2 consecutive gaps. This means out-of-scope questions
*automatically* cause escalation without relying on the model to self-identify
uncertainty in natural language.

---

## 4. Confidence-Based Escalation

Escalation is detected via the structured `"escalate": true` flag in the JSON
response, combined with two application-layer counters:

| Trigger | Detection Method |
|---|---|
| Out-of-scope question | `answered_from_sop: false` → increments counter → escalate at 2 |
| Angry sentiment | Model sets `escalate: true`, `escalation_reason: "angry sentiment"` |
| Explicit human request | Model sets `escalate: true`, `escalation_reason: "human requested"` |
| Complaint | Model sets `escalate: true`, `escalation_reason: "complaint"` |
| Medical question | Model sets `escalate: true`, `escalation_reason: "medical question"` |
| Pricing negotiation | Model sets `escalate: true`, `escalation_reason: "pricing negotiation"` |
| Parse failure | Application-layer catch → immediate escalation |

All escalation events are written to `escalation_log.txt` with:
- Timestamp
- Reason
- The exact customer message that triggered it

### Why JSON flags rather than regex or keyword matching?
Regex and keyword matching are brittle — "I'm not happy about this" vs
"This is unacceptable" vs "I'm furious" all express anger but share no keywords.
The model has genuine language understanding; asking it to emit a structured flag
is far more reliable than post-processing its natural language output.

---

## 5. Tone and Persona

**Persona name:** Aria — chosen to feel modern and friendly without being generic.

**Tone principles:**
- **Warm but not over-familiar** — suitable for a premium medical aesthetics clinic
- **Concise** — customers asking about treatments want quick, clear answers, not essays
- **Empathetic** — especially when escalating, the handoff message must not feel abrupt
- **Professional** — avoids slang or casual contractions like "gonna", "wanna"
- **No medical jargon** — the SOP itself is written in plain English; responses match this

**Escalation tone:**
When handing off, the model is implicitly guided (via the SOP `escalate_if` list
and the word "immediately") to produce a message that:
1. Acknowledges the customer's concern
2. Explains they're being connected to a human
3. Does not leave the customer feeling dismissed

Example output the model produces naturally:
> "I completely understand your concern, and I want to make sure you get the right
> support. I'm connecting you with a member of our team right now."

---

## 6. Multi-Stage State Management

Rather than hard-switching between separate prompts for each stage, a single
unified prompt handles all stages by dynamically injecting state context.
The application maintains:

```python
state = {
    "lead_info": { ... },          # collected qualification data
    "qualification_done": bool,    # drives qual instruction in prompt
    "qual_questions_asked": int,   # which question comes next
    "unanswered_count": int,       # escalation counter
    "escalated": bool,             # stops further AI calls post-escalation
    "conversation_history": []     # full message list sent to API every turn
}
```

This approach was chosen over stage-switching because:
- It handles natural conversation order (customer may volunteer lead info early)
- It avoids awkward stage boundary messages
- The prompt is simpler to debug — one template, not four