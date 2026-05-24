# Test Transcript 01 — In-SOP Question
**Scenario:** Customer asks about Botox pricing (information present in SOP)
**Expected:** AI answers accurately from SOP only

---

```
═══════════════════════════════════════════════════════════
   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)
═══════════════════════════════════════════════════════════
   Type 'exit' or 'bye' to end the conversation.

Aria: Hello! Welcome to Bloom Aesthetics Clinic 🌸 I'm Aria, your virtual
      receptionist. How can I help you today?

You: Hi, how much does Botox cost?

Aria: Great question! Botox at Bloom Aesthetics Clinic starts from £200.
      It's used to smooth expression lines, and results typically last
      around 3 to 4 months. Would you like to book a free consultation
      to discuss your goals with one of our practitioners?

You: What about fillers?

Aria: Dermal fillers start from £250. They're great for adding volume,
      lip enhancement, and facial contouring — with results lasting
      anywhere from 6 to 12 months. We also offer a free consultation
      if you'd like to explore which treatment suits you best!

You: Are you open on weekends?

Aria: We're open Monday to Saturday, 9am to 7pm. We're closed on Sundays.
      What service are you most interested in — Botox, Fillers, or
      a free Consultation?

You: bye

Aria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a
      wonderful day! 💛
```

---

**Result: ✅ PASS**
- Botox price (£200) answered correctly from SOP
- Filler price (£250) answered correctly from SOP
- Opening hours answered correctly from SOP
- No hallucinated information
- Qualification question naturally woven in