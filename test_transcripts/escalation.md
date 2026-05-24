# Test Transcript 03 — Escalation Trigger (Angry Sentiment)
**Scenario:** Customer expresses frustration / complaint
**Expected:** AI detects sentiment immediately, hands off with reason logged

---

```
═══════════════════════════════════════════════════════════
   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)
═══════════════════════════════════════════════════════════

Aria: Hello! Welcome to Bloom Aesthetics Clinic 🌸 I'm Aria, your virtual
      receptionist. How can I help you today?

You: I'm really angry. I came in last week and the treatment was awful.
     I want a refund and I want to speak to someone NOW.

Aria: I'm so sorry to hear about your experience — that's not the standard
      we hold ourselves to at all, and I completely understand your
      frustration. This needs to be handled personally by our team.
      I'm escalating this to a human agent right now and someone will
      be in touch with you very shortly.

──────────────────────────────────────────────────────────
  [ESCALATION TRIGGERED]
  Reason  : Customer complaint with angry sentiment and refund request
  Time    : 2024-01-15 11:31:07
──────────────────────────────────────────────────────────

You: Hello? Is anyone there?

Aria: A member of our team will be with you shortly. Please stay on
      the line.

You: bye

Aria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a
      wonderful day! 💛
```

---

**Result: ✅ PASS**
- Angry sentiment detected on first message (no waiting for repeated signals)
- Escalation reply is empathetic, not dismissive
- Escalation reason includes: complaint + angry sentiment + refund request
- After escalation, AI holds the line rather than continuing to respond
- Escalation logged to `escalation_log.txt`