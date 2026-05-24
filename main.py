import json
import os
from datetime import datetime
from groq import Groq


def load_sop(path: str = "sop.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)


def build_system_prompt(sop: dict, state: dict) -> str:
    sop_text = json.dumps(sop, indent=2)

    all_questions = [
        "What service are you most interested in? (e.g. Botox, Fillers, or a free Consultation)",
        "Have you had any aesthetic treatments before?",
        "How did you hear about Bloom Aesthetics Clinic?"
    ]
    asked = state["qual_questions_asked"]
    remaining_questions = all_questions[asked:]

    if state["qualification_done"]:
        qual_instruction = (
            "LEAD QUALIFICATION: Already complete. "
            f"Info collected: {json.dumps(state['lead_info'])}"
        )
    elif remaining_questions:
        next_q = remaining_questions[0]
        qual_instruction = (
            f"LEAD QUALIFICATION: You still need to collect some information. "
            f"When the conversation allows, naturally ask the customer: \"{next_q}\". "
            f"Ask only one qualification question per turn."
        )
    else:
        qual_instruction = "LEAD QUALIFICATION: All questions asked."

    return f"""You are Aria, a warm and professional virtual receptionist for Bloom Aesthetics Clinic.

SOP DATA - YOUR ONLY SOURCE OF TRUTH:
{sop_text}

CORE RULES:
1. Answer ONLY using the SOP data above. Never invent prices, availability, or policies.
2. If a question is NOT answerable from the SOP, do NOT guess. Set escalate=true instead.
3. Escalate for: complaints, medical questions, pricing negotiation, angry/frustrated sentiment,
   explicit human requests, or 2+ unanswered questions in a row.
4. Tone: warm, concise, professional. Suitable for a premium aesthetics clinic.
5. You MUST reply ONLY with valid JSON. No text outside the JSON block. No markdown fences.

{qual_instruction}

UNANSWERED QUESTIONS IN A ROW SO FAR: {state['unanswered_count']}

ALWAYS respond with this exact JSON structure (no extra keys, no extra text):
{{
  "reply": "your message to the customer",
  "escalate": false,
  "escalation_reason": null,
  "answered_from_sop": true,
  "qualification_update": {{
    "service_interest": null,
    "prior_treatments": null,
    "heard_from": null
  }}
}}

Field rules:
- "escalate": true if ANY escalation trigger is met
- "escalation_reason": short plain-English reason, or null
- "answered_from_sop": false if the question could not be answered from SOP data
- "qualification_update": fill in any field the customer just revealed; leave others null
"""


def log_escalation(reason: str, trigger_message: str):
    line = (
        f"\n{'='*55}\n"
        f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Reason    : {reason}\n"
        f"Trigger   : {trigger_message}\n"
    )
    with open("escalation_log.txt", "a") as f:
        f.write(line)


def parse_json_response(raw: str) -> dict:
    text = raw.strip()

    # Strip markdown fences
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            candidate = part.strip()
            if candidate.startswith("json"):
                candidate = candidate[4:].strip()
            if candidate.startswith("{"):
                text = candidate
                break

    # Try direct parse
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    # Find first {...} block anywhere in the response
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(raw[start:end])
        except json.JSONDecodeError:
            pass

    # Fallback: use raw text as reply so conversation keeps going
    clean_text = raw.strip().strip("`").strip()
    return {
        "reply": clean_text if clean_text else "I'm sorry, could you repeat that?",
        "escalate": False,
        "escalation_reason": None,
        "answered_from_sop": True,
        "qualification_update": {
            "service_interest": None,
            "prior_treatments": None,
            "heard_from": None
        }
    }


def call_groq(client: Groq, system_prompt: str, messages: list) -> str:
    groq_messages = [{"role": "system", "content": system_prompt}] + messages
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=groq_messages
    )
    return response.choices[0].message.content


def generate_summary(client: Groq, state: dict) -> dict:
    convo_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}"
        for m in state["conversation_history"]
    )

    prompt = f"""You are summarising a completed customer support conversation for a clinic CRM.

CONVERSATION:
{convo_text}

LEAD INFO COLLECTED: {json.dumps(state['lead_info'])}
ESCALATION OCCURRED: {state['escalated']}
ESCALATION REASON: {state.get('escalation_reason') or 'None'}

Reply ONLY with valid JSON, no markdown fences:
{{
  "customer_intent": "one sentence describing what the customer wanted",
  "details_collected": {{
    "service_interest": "value or null",
    "prior_treatments": "value or null",
    "heard_from": "value or null"
  }},
  "sop_gaps": ["list any questions the AI could not answer from the SOP"],
  "escalation": {{
    "occurred": false,
    "reason": null
  }},
  "recommended_next_action": "what the human team should do next"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": "Reply only with valid JSON. No markdown."},
            {"role": "user", "content": prompt}
        ]
    )
    return parse_json_response(response.choices[0].message.content)


def print_summary(summary: dict):
    d = summary.get("details_collected", {})
    esc = summary.get("escalation", {})
    gaps = summary.get("sop_gaps", [])

    print(f"\n{'='*60}")
    print("  CONVERSATION SUMMARY")
    print(f"{'='*60}")
    print(f"\n  Customer Intent    : {summary.get('customer_intent', 'N/A')}")
    print(f"\n  Details Collected  :")
    print(f"    Service Interest : {d.get('service_interest') or 'Not collected'}")
    print(f"    Prior Treatments : {d.get('prior_treatments') or 'Not collected'}")
    print(f"    Heard From       : {d.get('heard_from') or 'Not collected'}")
    print(f"\n  SOP Gaps           : {', '.join(gaps) if gaps else 'None'}")
    if esc.get("occurred"):
        print(f"\n  Escalation         : YES — {esc.get('reason')}")
    else:
        print(f"\n  Escalation         : None")
    print(f"\n  Recommended Action : {summary.get('recommended_next_action', 'N/A')}")
    print(f"\n{'='*60}\n")

    filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"CONVERSATION SUMMARY — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write(f"Customer Intent    : {summary.get('customer_intent')}\n\n")
        f.write(f"Details Collected  :\n")
        f.write(f"  Service Interest : {d.get('service_interest')}\n")
        f.write(f"  Prior Treatments : {d.get('prior_treatments')}\n")
        f.write(f"  Heard From       : {d.get('heard_from')}\n\n")
        f.write(f"SOP Gaps           : {gaps}\n\n")
        f.write(f"Escalation         : {esc}\n\n")
        f.write(f"Recommended Action : {summary.get('recommended_next_action')}\n")
    print(f"  Summary saved to: {filename}\n")


def run():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("\n[ERROR] GROQ_API_KEY not set.")
        print("Set it with:  $env:GROQ_API_KEY='your_key_here'  (PowerShell)")
        print("Get a free key at: https://console.groq.com\n")
        return

    client = Groq(api_key=api_key)
    sop = load_sop()

    state = {
        "lead_info": {
            "service_interest": None,
            "prior_treatments": None,
            "heard_from": None
        },
        "qualification_done": False,
        "qual_questions_asked": 0,
        "unanswered_count": 0,
        "escalated": False,        # logged in summary — does NOT stop the bot
        "hard_escalation": False,  # only True for anger/complaint — stops the bot
        "escalation_reason": None,
        "conversation_history": []
    }

    print("\n" + "="*60)
    print("   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)")
    print("   Powered by Groq + LLaMA 3.3 70B")
    print("="*60)
    print("   Type 'exit' or 'bye' to end the conversation.\n")

    opening = (
        "Hello! Welcome to Bloom Aesthetics Clinic. "
        "I'm Aria, your virtual receptionist. "
        "How can I help you today?"
    )
    print(f"Aria: {opening}\n")
    state["conversation_history"].append({"role": "assistant", "content": opening})

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "bye", "goodbye", "quit"}:
            farewell = "Thank you for reaching out to Bloom Aesthetics Clinic. Have a wonderful day!"
            print(f"\nAria: {farewell}\n")
            state["conversation_history"].append({"role": "assistant", "content": farewell})
            break

        state["conversation_history"].append({"role": "user", "content": user_input})

        # Hard stop only for serious escalations (anger, complaint, explicit human request)
        if state["hard_escalation"]:
            holding = "A member of our team will be with you shortly. Please stay on the line."
            print(f"\nAria: {holding}\n")
            state["conversation_history"].append({"role": "assistant", "content": holding})
            continue

        system_prompt = build_system_prompt(sop, state)

        try:
            raw = call_groq(client, system_prompt, state["conversation_history"])
            parsed = parse_json_response(raw)

        except json.JSONDecodeError:
            # Parse error — log it but keep conversation going
            print("\nAria: I'm sorry, I didn't quite catch that. Could you rephrase?\n")
            log_escalation("JSON parse error (conversation continued)", user_input)
            continue

        except Exception as e:
            print(f"\n[API Error: {e}]\n")
            continue

        reply             = parsed.get("reply", "I'm sorry, could you repeat that?")
        escalate          = parsed.get("escalate", False)
        escalation_reason = parsed.get("escalation_reason") or ""
        answered_from_sop = parsed.get("answered_from_sop", True)
        qual_update       = parsed.get("qualification_update", {})

        if not answered_from_sop:
            state["unanswered_count"] += 1
        else:
            state["unanswered_count"] = 0

        for key in ("service_interest", "prior_treatments", "heard_from"):
            if qual_update.get(key):
                state["lead_info"][key] = qual_update[key]

        filled = sum(1 for v in state["lead_info"].values() if v is not None)
        state["qual_questions_asked"] = filled
        if filled >= 3:
            state["qualification_done"] = True

        if escalate:
            state["escalated"] = True
            state["escalation_reason"] = escalation_reason
            log_escalation(escalation_reason, user_input)

            # Serious triggers stop the bot; soft triggers just log and continue
            serious_keywords = ["angry", "complaint", "frustrated", "human", "refund", "legal", "medical", "abuse"]
            is_serious = any(w in escalation_reason.lower() for w in serious_keywords)

            if is_serious:
                state["hard_escalation"] = True

            print(f"\nAria: {reply}\n")
            print("─"*50)
            print(f"  [ESCALATION TRIGGERED]")
            print(f"  Reason     : {escalation_reason}")
            print(f"  Bot stops  : {'YES' if is_serious else 'NO — continuing conversation'}")
            print(f"  Time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("─"*50 + "\n")
        else:
            print(f"\nAria: {reply}\n")

        state["conversation_history"].append({"role": "assistant", "content": reply})

    if state["conversation_history"]:
        print("─"*60)
        print("  Generating session summary, please wait...")
        print("─"*60)
        try:
            summary = generate_summary(client, state)
            print_summary(summary)
        except Exception as e:
            print(f"\n[Error generating summary: {e}]\n")


if __name__ == "__main__":
    run()