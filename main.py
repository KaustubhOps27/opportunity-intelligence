import requests
from bs4 import BeautifulSoup
import json
import ollama

from scoring import calculate_score, get_priority
from research import get_research_evidence


def scrape_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    return text[:15000]


def analyze_company(company, domain, website_text, research_evidence):

    prompt = f"""
You are a B2B SaaS opportunity research analyst working for Brandhero,
a conversion-focused UI/UX company.

Brandhero primarily helps B2B technology and SaaS companies improve
their website, product experience, positioning, and conversion.

Your job is NOT to simply summarize the company.

Your job is to identify observable signals that suggest the company
may have a timely opportunity for Brandhero.

Analyze ONLY the evidence provided below.

Company: {company}
Domain: {domain}

Website evidence:
{website_text}

External research evidence:
{json.dumps(research_evidence, indent=2)}


EVALUATE THESE SIX OPPORTUNITY SIGNALS:

1. weak_website_positioning
2. major_product_website_change
3. category_repositioning
4. recent_funding
5. senior_marketing_brand_hire
6. active_design_brand_growth_hiring


IMPORTANT EVIDENCE RULES:

- Do NOT invent facts.
- Do NOT use outside knowledge.
- If the provided evidence does not support a signal, mark detected as false.
- Only mark a signal as true when there is observable supporting evidence.
- Every detected signal MUST contain a short explanation of the evidence.
- Do not assume that a company needs a redesign simply because it is a SaaS company.
- Do not assume funding, hiring, or product changes unless the evidence explicitly supports them.
- Confidence represents confidence in the interpretation of the evidence,
  NOT confidence that the company will buy Brandhero services.
- When evidence is weak or ambiguous, prefer detected=false.


SIGNAL-SPECIFIC GUIDANCE:

weak_website_positioning:
Look for unclear, generic, confusing, or inconsistent messaging about
what the company does, who it serves, or its value proposition.

IMPORTANT:
You are analyzing scraped text, not visually inspecting the rendered website.
Do NOT make claims about colors, visual hierarchy, spacing, typography,
or visual quality unless the evidence explicitly contains those details.


major_product_website_change:
Look for evidence of a significant product launch, major feature launch,
new product direction, new platform, or substantial website/product change.
- Product names or feature names alone are NOT evidence of a major product change.
- Words such as "New", "AI", "Pulse", "Inbox", "platform", or "product"
  do NOT automatically indicate a recent launch.
- The evidence must explicitly indicate a launch, announcement, release,
  redesign, new version, or meaningful product direction change.
- If the website only presents a product or feature without indicating
  that it is new or recent, mark detected=false.
Do NOT treat ordinary product features as proof of a major product change.

If there is no evidence that the change is recent or significant,
mark detected=false.


category_repositioning:
Look for language suggesting the company is changing how it positions itself,
such as moving into a broader category, targeting a new market, changing
its value proposition, or describing itself in a substantially different way.

Generic positioning language alone is NOT enough to prove recent repositioning.

If there is no evidence of a meaningful change, mark detected=false.


recent_funding:
Only detect this if the provided evidence explicitly mentions a funding,
investment, financing, or fundraising event.

The funding evidence should come from the external research evidence,
not assumptions from company size or website content.


senior_marketing_brand_hire:
Only detect this if the provided evidence explicitly indicates a recent
senior marketing, brand, growth, or similar leadership hire.


active_design_brand_growth_hiring:
Only detect this if the provided evidence explicitly indicates active hiring
for design, brand, growth, marketing, UX, or related roles.


IMPORTANT:
For signals involving CHANGE or RECENCY, the evidence must support
that the event is recent or represents a meaningful change.

If evidence is only a possible indication, mark detected=false.


BRANDHERO BUSINESS INTERPRETATION:

After evaluating the signals, provide:

website_observations:
Describe useful observations about the company's messaging, positioning,
product claims, navigation/content structure, and conversion-related messaging.

Do not make unsupported visual design claims.


likely_need:
Identify the SPECIFIC UI/UX, website, conversion, positioning, or product
experience opportunity that Brandhero could potentially help with.

The need MUST be connected to an observed signal.

Do NOT write generic statements such as:
"they need better tools"
"they need better workflows"
"they need to improve user experience"


relevant_stakeholder:
Identify the most relevant BUYER or DECISION-MAKER role for this opportunity.

Prefer roles such as:
Founder
CEO
CMO
VP Marketing
Head of Marketing
Head of Brand
Head of Growth
VP Product
Head of Product
Product Marketing

Do NOT use generic teams such as "product development team".


personalised_outreach_angle:
Write ONE concise outreach angle explaining why Brandhero would have
a reason to contact this company NOW.

The outreach angle must be based ONLY on detected signals and evidence.

Do not claim that the company definitely needs Brandhero.
Do not invent a specific problem that the evidence does not support.


RETURN ONLY VALID JSON.

Do not write:
"Here is the JSON output:"
Do not use markdown code fences.
Do not repeat the JSON.
Return exactly ONE JSON object.

Required format:

{{
    "signals": {{
        "weak_website_positioning": {{
            "detected": false,
            "evidence": "",
            "source_url": "{domain}",
            "confidence": 0.0
        }},
        "major_product_website_change": {{
            "detected": false,
            "evidence": "",
            "source_url": "",
            "confidence": 0.0
        }},
        "category_repositioning": {{
            "detected": false,
            "evidence": "",
            "source_url": "",
            "confidence": 0.0
        }},
        "recent_funding": {{
            "detected": false,
            "evidence": "",
            "source_url": "",
            "confidence": 0.0
        }},
        "senior_marketing_brand_hire": {{
            "detected": false,
            "evidence": "",
            "source_url": "",
            "confidence": 0.0
        }},
        "active_design_brand_growth_hiring": {{
            "detected": false,
            "evidence": "",
            "source_url": "",
            "confidence": 0.0
        }}
    }},
    "website_observations": "",
    "likely_need": "",
    "relevant_stakeholder": "",
    "personalised_outreach_angle": ""
}}
"""

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise B2B opportunity intelligence analyst. "
                    "Never invent evidence. Return exactly one valid JSON object "
                    "and nothing else."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    content = response["message"]["content"].strip()

    print("\nRAW LLM RESPONSE:\n")
    print(content)

    
    content = content.replace("```json", "")
    content = content.replace("```", "")
    content = content.strip()

    
    decoder = json.JSONDecoder()

    try:
        result, end_index = decoder.raw_decode(content)
        return result

    except json.JSONDecodeError:

        
        start = content.find("{")

        if start == -1:
            raise ValueError(
                "Llama did not return a JSON object.\n"
                f"Raw response:\n{content}"
            )

        try:
            result, end_index = decoder.raw_decode(content[start:])
            return result

        except json.JSONDecodeError:
            raise ValueError(
                "Could not extract valid JSON from Llama response.\n"
                f"Raw response:\n{content}"
            )


#main

company = "Vanta"
domain = "vanta.com"

print("Scraping website...")

website_text = scrape_website(domain)

print("Website scraped successfully.")
print("Characters:", len(website_text))


#external research

research_evidence = get_research_evidence(company)


#llm analysis

print("\nAnalyzing company...\n")

result = analyze_company(
    company,
    domain,
    website_text,
    research_evidence
)


#scoring

signals = result["signals"]

score = calculate_score(signals)
priority = get_priority(score)

result["opportunity_score"] = score
result["priority"] = priority


#output

print("\nFINAL STRUCTURED RESULT:\n")
print(json.dumps(result, indent=4))

print("\n-------------------------")
print("OPPORTUNITY SCORE:", score)
print("PRIORITY:", priority)
print("-------------------------")