# Test Transcript 05 — Full Session + Conversation Summary
**Scenario:** Complete end-to-end session ending with a structured summary
**Expected:** Summary includes intent, details, SOP gaps, escalation status, next action

---

```
═══════════════════════════════════════════════════════════
   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)
═══════════════════════════════════════════════════════════

Aria: Hello! Welcome to Bloom Aesthetics Clinic 🌸 I'm Aria, your virtual
      receptionist. How can I help you today?

You: Hi, I want to know about Botox. How much is it and how long does it last?

Aria: Botox at Bloom Aesthetics Clinic starts from £200. Results typically
      last around 3 to 4 months, after which many clients choose to
      come back for a top-up.

      What service are you most interested in — shall I put you down
      for Botox, or would you like to explore a free consultation first?

You: Botox sounds right. Do you offer any payment plans?

Aria: I'm sorry, I don't have details on payment plans in my current
      information — that's something our team would be best placed to
      advise on. I'd recommend booking a free consultation where they
      can discuss this with you directly.

      Have you had any aesthetic treatments before?

You: Yes, I've had Botox done elsewhere before actually.

Aria: Great — so you already know what to expect! We'd love to have you
      experience Bloom Aesthetics Clinic. Our treatments are carried out
      by qualified and insured practitioners, and aftercare instructions
      are provided after every session.

      How did you hear about us, if you don't mind me asking?

You: I found you on Google.

Aria: Lovely — glad you found us! So you're interested in Botox, you've
      had it before, and you found us via Google. 

      To book, you can reach us via WhatsApp or our website. We ask for
      24 hours' notice if you need to cancel. Is there anything else
      I can help you with?

You: No that's all, bye

Aria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a
      wonderful day! 💛

──────────────────────────────────────────────────────────
  Generating session summary, please wait...
──────────────────────────────────────────────────────────

══════════════════════════════════════════════════════════
  CONVERSATION SUMMARY
══════════════════════════════════════════════════════════

  Customer Intent    : Enquiring about Botox pricing and availability;
                       ready to book, asked about payment plans.

  Details Collected  :
    Service Interest : Botox
    Prior Treatments : Yes — has had Botox at another clinic before
    Heard From       : Google search

  SOP Gaps           : Payment plan availability (not covered in SOP)

  Escalation         : None

  Recommended Action : Follow up via WhatsApp to confirm booking.
                       Human agent to address payment plan query.

══════════════════════════════════════════════════════════

  Summary saved to: summary_20240115_113022.txt
```

---

**Result: ✅ PASS**
- Full conversation handled from greeting to farewell
- SOP gap (payment plans) correctly identified and noted
- All 3 qualification fields collected
- Summary includes: intent, details, gap, no escalation, actionable next step
- Summary saved to timestamped file