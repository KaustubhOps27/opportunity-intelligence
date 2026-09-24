# B2B Opportunity Intelligence System

## 1. Objective

The objective of this POC is to identify B2B SaaS companies that are unusually likely to need Brandhero's services **now**, rather than treating every company as an equal lead.

The system combines observable company signals, website/business observations, structured LLM analysis, and deterministic scoring to produce an actionable opportunity assessment.

---

## 2. Intelligence Framework

I selected six signals based on their potential connection to Brandhero's conversion-focused UI/UX, website, and positioning work.

| Signal | Weight | Why it matters |
|---|---:|---|
| Weak Website / Unclear Positioning | 25 | Direct indication of a potential conversion or messaging problem |
| Major Product / Website Change | 20 | Major changes can create a need to rethink UX and messaging |
| Category Repositioning | 20 | New positioning can require a new brand/product story |
| Recent Funding | 15 | Funding can create pressure to scale GTM and conversion |
| New Senior Marketing / Brand Hire | 10 | May indicate a new growth or positioning mandate |
| Active Design / Brand / Growth Hiring | 10 | Shows investment in brand, UX, or growth |

### Scoring

The LLM identifies and structures signals, but the final opportunity score is calculated using fixed business weights.

- **60–100:** HIGH
- **35–59:** MEDIUM
- **0–34:** LOW

Signals are only awarded when supporting evidence is present.

---

## 3. System Architecture

```text
Company Domain
      ↓
Website Scraping + External Research
      ↓
Raw Evidence
      ↓
Llama 3.1 8B
      ↓
Structured Signals
      ↓
Deterministic Scoring
      ↓
Opportunity Score + Priority
      ↓
Likely Need + Stakeholder + Outreach Angle
```

### Technology Used

- Python
- Requests
- BeautifulSoup
- Ollama
- Llama 3.1 8B
- Deterministic Python scoring
- Manual external research for the POC

---

## 4. Output

For each company, the system produces a structured opportunity assessment containing:

- **Observable Signals** — six opportunity signals identified by the LLM from the available website and external research evidence.
- **Supporting Evidence** — evidence and source information associated with each detected signal.
- **Website Observations** — observations derived from the scraped website content.
- **Likely Business Need** — the potential Brandhero opportunity inferred from the detected signals.
- **Relevant Stakeholder** — the decision-maker most relevant to the identified opportunity.
- **Personalised Outreach Angle** — a concise outreach direction based on the detected signals and business need.
- **Opportunity Score** — calculated deterministically using predefined business weights.
- **Priority** — derived from the opportunity score using fixed thresholds.

The LLM is responsible for interpreting the available evidence and generating the qualitative intelligence, while the final opportunity score and priority are calculated independently using deterministic Python logic.

For this POC, the structured JSON output was manually transferred into the accompanying Google Sheet for the five-company evaluation. In a production version, this final reporting step can be automated using the Google Sheets API, allowing each company's structured output to flow directly into the prospecting sheet.

---

## 5. Five-Company Test

The POC was tested on five real B2B SaaS companies.

| Company | Score | Priority |
|---|---:|---|
| Linear | 55 | MEDIUM |
| Intercom | 55 | MEDIUM |
| Ramp | 65 | HIGH |
| Gong | 55 | MEDIUM |
| Vanta | 55 | MEDIUM |

### Key observations

**Ramp** produced the strongest opportunity signal combination, including a major product launch, category evolution, recent funding, and product design hiring.

**Gong** was intentionally treated more conservatively because ARR growth is not the same as funding. This highlighted the importance of validating evidence rather than blindly trusting an LLM classification.

The purpose of the test was not to maximise scores, but to distinguish companies based on observable evidence.

---

## 6. What Breaks First at 500 Companies?

External research and evidence collection would become the first bottleneck.

Website scraping is relatively straightforward, but funding, hiring, product launches, and repositioning signals are distributed across different sources and formats. Maintaining reliable and recent evidence at scale would be harder than the scoring itself.

---

## 7. What Information Couldn't Be Reliably Obtained?

I couldn't reliably obtain consistent external information for every company from a single source.

Hiring and company-change signals often required cross-checking. I also avoided making visual UX or design-quality claims from scraped website text alone because text-only scraping cannot reliably establish visual design quality.

---

## 8. What Did I Deliberately Keep Manual?

I kept external research collection manual in this POC because I wanted to prioritise evidence quality over building a fragile multi-source scraping system.

This also made it easier to verify the evidence behind each signal during the three-hour practical.

---

## 9. What I Would Build With Another Week

With another week, I would:

1. Automate external evidence collection.
2. Add timestamps and source reliability for every signal.
3. Batch-process companies instead of running them individually.
4. Improve signal validation and recency checks.
5. Add confidence and evidence-quality checks.
6. Introduce a human-review queue for low-confidence or conflicting signals.
7. Improve failure handling and logging.

The goal would be to make the system reliable at scale without allowing the LLM to become the final decision-maker.

---

## 10. Key Technical / Business Decision

The most important decision was separating **LLM interpretation from deterministic scoring**.

The LLM is useful for interpreting messy evidence and converting it into structured signals. However, the final opportunity score is calculated using fixed business weights.

This makes the scoring more transparent, predictable, and easier to audit.

---

## 11. Limitations

This is a POC rather than a production system.

The biggest limitation is the external research layer. The current implementation relies partly on manually supplied research evidence instead of building a complete multi-source data acquisition pipeline.

The system also depends on the quality and recency of the evidence provided to it. In a production version, each signal would need explicit timestamps, source validation, and stronger evidence checks.
