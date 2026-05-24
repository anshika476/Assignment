# Test Transcript 04 — Lead Qualification
**Scenario:** Full qualification flow across a natural conversation
**Expected:** AI collects all 3 fields (service interest, prior treatments, referral source)

---

```
═══════════════════════════════════════════════════════════
   BLOOM AESTHETICS CLINIC — Virtual Receptionist (Aria)
═══════════════════════════════════════════════════════════

Aria: Hello! Welcome to Bloom Aesthetics Clinic 🌸 I'm Aria, your virtual
      receptionist. How can I help you today?

You: Hi, I've been thinking about getting some work done on my face.
     Not sure where to start.

Aria: How lovely that you're exploring your options! We offer Botox
      (from £200) for smoothing expression lines, Dermal Fillers
      (from £250) for volume and contouring, and free consultations
      to help you figure out exactly what's right for you.

      What service are you most interested in — Botox, Fillers, or
      shall we start with a free consultation?

You: I think fillers, but I'm a bit nervous as I've never done anything
     like this before.

Aria: Completely understandable — and actually, being a first-timer
      is exactly why our free consultation is so valuable. You can
      meet with a qualified practitioner, ask all your questions, and
      decide from there with no pressure at all.

      Have you had any aesthetic treatments before, or would this
      be your first time?

You: First time, yes.

Aria: That's great to know — our team are experienced with first-timers
      and will make sure you feel completely at ease. We can book
      a free consultation to get you started whenever you're ready.

      Just one more quick question — how did you hear about
      Bloom Aesthetics Clinic?

You: A friend recommended you on Instagram.

Aria: That's wonderful to hear — word of mouth means a lot to us! 🌸
      So to recap: you're interested in Fillers, it would be your first
      treatment, and you came via a friend's recommendation.

      Would you like me to guide you on how to book a free consultation
      via WhatsApp or our website?

You: Yes please, how do I book?

Aria: You can book your free consultation either via WhatsApp or through
      our website. Once booked, please note we ask for 24 hours' notice
      if you need to cancel or reschedule. Our team will send you a
      confirmation with the clinic address.

      Is there anything else I can help you with today?

You: No that's everything, thanks!

Aria: Brilliant — we look forward to welcoming you to Bloom Aesthetics
      Clinic! Have a wonderful day 💛

You: bye

Aria: Thank you for reaching out to Bloom Aesthetics Clinic. Have a
      wonderful day! 💛
```

---

**Qualification Summary Collected:**
```
service_interest : Fillers
prior_treatments : No (first time)
heard_from       : Friend / Instagram
```

**Result: ✅ PASS**
- All 3 qualification fields collected naturally across the conversation
- Questions asked one at a time, woven into context
- No interrogation-style rapid-fire questions
- Lead info stored in state for summary generation