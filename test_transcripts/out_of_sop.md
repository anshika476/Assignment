# Test Transcript 02 — Out-of-Scope Question
**Scenario:** Customer asks something not present in the SOP
**Expected:** AI acknowledges the gap, does NOT guess, escalates after 2 unanswered

---

```
═══════════════════════════════════════════════════════════
   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)
═══════════════════════════════════════════════════════════

Aria: Hello! Welcome to Bloom Aesthetics Clinic 🌸 I'm Aria, your virtual
      receptionist. How can I help you today?

You: Do you offer laser hair removal?

Aria: I'm sorry, I don't have any information about laser hair removal
      in our current services. We specialise in Botox (from £200),
      Dermal Fillers (from £250), and free consultations. Would any
      of those be of interest to you?

You: What about chemical peels?

Aria: That's not something I'm able to confirm from the information
      I have available. I want to make sure you get accurate details
      rather than guessing — let me connect you with a member of our
      team who can answer that properly.

──────────────────────────────────────────────────────────
  [ESCALATION TRIGGERED]
  Reason  : 2 consecutive questions not answerable from SOP
  Time    : 2024-01-15 11:23:44
──────────────────────────────────────────────────────────

You: bye

Aria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a
      wonderful day! 💛
```

---

**Result: ✅ PASS**
- First out-of-scope question: AI acknowledged gap without guessing
- Second consecutive out-of-scope question: escalation triggered correctly
- No invented services or prices
- Escalation logged to `escalation_log.txt`