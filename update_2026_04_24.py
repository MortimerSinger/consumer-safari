#!/usr/bin/env python3
"""Update DATA in index.html for 2026-04-24 briefing."""
import re, json
from pathlib import Path

HTML_PATH = Path(__file__).parent / "index.html"
html = HTML_PATH.read_text()

m = re.search(r'const DATA = (\{.*?\});\s*\n', html, re.DOTALL)
data = json.loads(m.group(1))

# --- Rotate ---
prev_today = data.get("todayNews", [])
prev_ai_today = data.get("aiTodayNews", [])
week = data.get("weekNews", [])
ai_week = data.get("aiWeekNews", [])
month = data.get("monthNews", [])
ai_month = data.get("aiMonthNews", [])

week = prev_today + week
ai_week = prev_ai_today + ai_week
if len(week) > 10:
    overflow = week[10:]
    week = week[:10]
    month = overflow + month
if len(ai_week) > 10:
    overflow = ai_week[10:]
    ai_week = ai_week[:10]
    ai_month = overflow + ai_month
if len(month) > 18: month = month[:18]
if len(ai_month) > 18: ai_month = ai_month[:18]

# --- New todayNews (Consumer) ---
today_news = [
    {
        "category": "🥫 CPG & Food",
        "stories": [
            {
                "headline": "U.S. Private Label Sales Hit $330 Billion, 24% Unit Share",
                "source": "PLMA / Circana",
                "url": "https://www.plma.com/article/report-us-private-label-cpg-sales-reach-330-billion",
                "blurb": "Updated Circana figures put store brands at a 23% dollar share, with unit growth still outpacing national brands even as growth is expected to slow.",
                "tag": "Consumer",
            },
            {
                "headline": "GLP-1 Users Cut Grocery Spending 5-8%, Shift to Fresh and High-Protein",
                "source": "Supermarket News",
                "url": "https://www.supermarketnews.com/nonfood-pharmacy/glp-1-drugs-reshape-consumer-spending-eating-and-wellness-habits-report",
                "blurb": "GLP-1 households spend ~$390 less annually on groceries and show the biggest declines in chips, cookies, and sweet bakery; 70% research products digitally.",
                "tag": "Consumer",
            },
            {
                "headline": "CivicScience: 1 in 4 GLP-1 Users Switched Grocery Stores Since Starting Medication",
                "source": "CivicScience",
                "url": "https://civicscience.com/glp-1-trends-by-civicscience-weight-loss-pills-dining-out-motivations-and-grocery-store-preferences/",
                "blurb": "Highest store-switching percentage since November 2025; dining-out motivation also shifting, with fast-food dinner traffic down 6% among regular users.",
                "tag": "Consumer",
            },
        ],
    },
    {
        "category": "💼 M&A & Investments",
        "stories": [
            {
                "headline": "Consumer Megadeals Return in Q1 2026 After Multi-Year Drought",
                "source": "Reuters",
                "url": "https://www.reuters.com/business/finance/consumer-megadeals-make-rare-comeback-first-quarter-2026-04-03/",
                "blurb": "Q1 saw consumer megadeals rebound as rate cuts and LP pressure for distributions force activity; H2 2026 expected to see a significant uptick in consumer M&A.",
                "tag": "PE",
            },
            {
                "headline": "Capstone Partners: 2025 Consumer M&A Multiples Closed at 9.2x EV/EBITDA",
                "source": "Capstone Partners",
                "url": "https://www.capstonepartners.com/insights/reports-annual-consumer-ma-report/",
                "blurb": "Third consecutive year below the 10.5x historical median; strategic buyers paid lower multiples due to AI integration capex competing for capital.",
                "tag": "PE",
            },
            {
                "headline": "Consumer VC Bifurcates: Megafunds Flush, Seed Funding Down 31% YoY",
                "source": "Peony / Carta",
                "url": "https://www.peony.ink/blog/consumer-investors",
                "blurb": "L Catterton raised $11B, VMG Partners closed a $1B fund, CAVU closed $325M in February; early-stage check availability is thinning fast.",
                "tag": "PE",
            },
        ],
    },
    {
        "category": "🏬 Retail",
        "stories": [
            {
                "headline": "Coresight: 8,270 U.S. Store Closures in 2025; 2026 Tracking Higher",
                "source": "MMCG / Coresight Research",
                "url": "https://www.mmcginvest.com/post/the-great-american-store-closure-tracker-2026-edition",
                "blurb": "GameStop accelerating to 727 U.S. closures in FY2025 with 430-500 more announced for early 2026; store rationalization is now structural, not cyclical.",
                "tag": "Retail",
            },
            {
                "headline": "7-Eleven to Close 645 Stores in FY2026; Apple Shuts 3 Mall Locations",
                "source": "Business Insider",
                "url": "https://www.businessinsider.com/stores-closing-in-2026-list",
                "blurb": "Seven & i Holdings earnings document confirms the 645 North American closures through February 2027; Apple citing declining mall conditions in Connecticut, California, and Maryland.",
                "tag": "Retail",
            },
        ],
    },
]

# --- New aiTodayNews ---
ai_today_news = [
    {
        "category": "🤖 AI & Labor",
        "stories": [
            {
                "headline": "Tech Industry Shed 78,557 Jobs in Q1 2026, Nearly Half Attributed to AI",
                "source": "Tom's Hardware / Nikkei Asia",
                "url": "https://www.tomshardware.com/tech-industry/tech-industry-lays-off-nearly-80-000-employees-in-the-first-quarter-of-2026-almost-50-percent-of-affected-positions-cut-due-to-ai",
                "blurb": "37,638 cuts (47.9%) tied to AI and workflow automation; Cognizant CAIO warns the real productivity gain hasn't landed yet, meaning more disruption ahead.",
                "tag": "Labor",
            },
            {
                "headline": "Snap Cuts 1,000 Jobs, Cancels 300 Openings; Stock Rises on AI Investment Pivot",
                "source": "Future Forwarded",
                "url": "https://futureforwarded.substack.com/p/the-ai-labor-report-monday-april",
                "blurb": "CEO Evan Spiegel announces $500M+ annual savings to fund AI infrastructure; Anthropic research shows hiring into AI-exposed jobs for ages 22-25 fell 14% since ChatGPT launch.",
                "tag": "Labor",
            },
            {
                "headline": "Epoch AI / Ipsos: 1 in 5 Full-Time Workers Say AI Has Taken Over Parts of Their Job",
                "source": "Future Forwarded",
                "url": "https://futureforwarded.substack.com/p/the-ai-labor-report-friday-9-april",
                "blurb": "Replacement (20%) outpaces creation (15%) by 5 points; half of U.S. adults used AI at work last week, with most using personal subscriptions over employer tools.",
                "tag": "Labor",
            },
        ],
    },
    {
        "category": "🛍️ AI & Commerce",
        "stories": [
            {
                "headline": "Agentic Commerce Now Live: 17% of Consumers Use AI Shopping Agents, ~50M U.S. Users",
                "source": "Codewave",
                "url": "https://codewave.com/insights/agentic-commerce-ai-shopping-agents/",
                "blurb": "Shopify, PayPal, Google, and Stripe building infrastructure for autonomous agent checkout; Walmart's Sparky assistant now in production handling predictive reordering.",
                "tag": "Retail Tech",
            },
            {
                "headline": "Amazon 'Buy For Me' and OpenAI's Target/Instacart/DoorDash Deals Define the Default-Interface Fight",
                "source": "Modern Retail",
                "url": "https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/",
                "blurb": "Ralph Lauren and other luxury brands now launching their own AI assistants; the question is whose agent becomes the default shopping interface, not whose cart processes the purchase.",
                "tag": "Retail Tech",
            },
        ],
    },
]

# --- Deep Read / AI Deep Read ---
deep_read = [
    {
        "title": "2026 Consumer M&A Outlook: Deals That Reshape, Not Just Resize",
        "source": "PwC",
        "url": "https://www.pwc.com/us/en/industries/consumer-markets/library/consumer-deals-outlook.html",
        "readTime": "16 min",
        "summary": "PwC frames 2026 as the year consumer CPG leaders break from legacy peers through portfolio reshaping, agentic commerce adoption, and megadeal activity; shifting consumer behavior is the forcing function.",
        "takeaway": "The 'reshape vs. resize' distinction is the strategic question for every consumer portfolio review this year. Reshape means exiting laggards and buying AI-native capability.",
    }
]
ai_deep_read = [
    {
        "title": "AI Labor Report: The Gallup Gap Between AI Use and AI Transformation",
        "source": "Future Forwarded",
        "url": "https://futureforwarded.substack.com/p/the-ai-labor-report-wednesday-april",
        "readTime": "12 min",
        "summary": "Half of U.S. workers use AI daily, but only 12% say AI has transformed how their organization operates; 89% of executives in NBER survey report no measurable productivity effect over three years. Manager engagement is the bottleneck.",
        "takeaway": "The AI productivity gap is not a model problem, it is a management problem. Companies that solve manager engagement will capture the gains that individual workers are already producing alone.",
    }
]

# --- To Listen / AI Listen ---
to_listen = [
    {
        "title": "The Restaurant M&A Reshaping: What's Changing in 2026",
        "show": "ICR (YouTube / Podcast)",
        "url": "https://icrinc.com/news-resources/forces-reshaping-restaurant-ma-2026/",
        "duration": "42 min",
        "why": "ICR restaurant M&A panel: quality of experience and service consistency are redefining brand value beyond price. Useful frame for any restaurant deal in Diana's pipeline.",
    }
]
ai_listen = [
    {
        "title": "AI Job Displacement Update — April 2026",
        "show": "YouTube",
        "url": "https://www.youtube.com/watch?v=CZ_34jztLbE",
        "duration": "28 min",
        "why": "The 'silent recession' thesis: 40-55% of entry-level white-collar roles eliminated or frozen by late 2027, with modeled data showing 200-300K positions quietly erased vs. the 54K visible headline.",
    }
]

# --- Voices (prepend new, keep existing) ---
new_voices = [
    {
        "author": "Future Forwarded",
        "handle": "futureforwarded",
        "platform": "Substack",
        "title": "The AI Labor Report — Wednesday, April 22, 2026",
        "url": "https://futureforwarded.substack.com/p/the-ai-labor-report-wednesday-april",
        "date": "Apr 22, 2026",
        "feedType": "ai",
    },
    {
        "author": "Sean Yu",
        "handle": "peonyink",
        "platform": "Substack",
        "title": "Top 15 Consumer Investors in 2026 (After 97% Fundings Shrink)",
        "url": "https://www.peony.ink/blog/consumer-investors",
        "date": "Apr 9, 2026",
        "feedType": "consumer",
    },
]
existing_voices = data.get("voices", []) or []
seen_urls = {v.get("url") for v in new_voices}
merged_voices = new_voices + [v for v in existing_voices if v.get("url") not in seen_urls]

# --- todayForMe ---
today_for_me = {
    "greeting": "Morty",
    "summary": "Private label crossed $330B with 24% unit share. GLP-1 households are now $390/year lighter on groceries and 1 in 4 have switched stores since starting. Consumer megadeals came back in Q1 and PwC is telling CPG leaders to reshape, not resize. On AI: 78,557 tech layoffs in Q1 with half attributed to AI; Epoch/Ipsos found 1 in 5 workers saying AI has already taken over parts of their job; and agentic commerce is live with 50M U.S. users already transacting through agents.",
    "keyNumbers": [
        {"label": "Private Label 2025", "value": "$330B", "change": "24% unit share, 23% dollar share", "direction": "up"},
        {"label": "GLP-1 Grocery Spend", "value": "-5% to -8%", "change": "$390/year lower per household", "direction": "down"},
        {"label": "Tech Layoffs Q1", "value": "78,557", "change": "47.9% attributed to AI displacement", "direction": "up"},
        {"label": "Agentic Commerce", "value": "~50M", "change": "17% of U.S. consumers using AI shopping agents", "direction": "up"},
    ],
    "patterns": [
        {
            "title": "Private label is now a structural category, not a cycle",
            "detail": "Store brands crossed $330B and 24% unit share. The cycle trigger was inflation, but the structural driver is now capability (premium tiers, data-driven assortment, supply chain parity). National brands lose a point of share per year structurally.",
        },
        {
            "title": "GLP-1s are redrawing grocery basket composition, not just volume",
            "detail": "The basket shift is more important than the $390 spend cut. Fresh and high-protein up, processed snacks down 10%, sweet bakery down 9%. For any CPG portfolio review, GLP-1 exposure is now a category-level risk variable, not a scenario.",
        },
        {
            "title": "Consumer M&A dam breaks in H2 2026",
            "detail": "Capstone's 9.2x multiple is a floor, not a ceiling. LP distribution pressure, rate cuts, and the Q1 megadeal return all point to H2 being the cleanest deal window in three years. Diana's pipeline should be loaded by June.",
        },
        {
            "title": "AI is absorbing the entry-level on-ramp, not just tasks",
            "detail": "Anthropic found hiring for AI-exposed jobs for ages 22-25 down 14% since ChatGPT launch. The headline unemployment rate hides it because experienced workers stay employed. This is the pattern worth tracking for any consumer brand whose customer acquisition depends on Gen Z household formation.",
        },
        {
            "title": "Agentic commerce is no longer a pilot",
            "detail": "50M U.S. users already transact through AI agents. Walmart's Sparky is in production, Amazon's Buy For Me is live, OpenAI's retailer stack spans Target/Instacart/DoorDash. The brands that don't expose structured catalogs and machine-readable policy will be invisible to the new demand layer by Q4.",
        },
    ],
}

# --- Compose ---
data["date"] = "Friday, April 24, 2026"
data["todayNews"] = today_news
data["aiTodayNews"] = ai_today_news
data["weekNews"] = week
data["aiWeekNews"] = ai_week
data["monthNews"] = month
data["aiMonthNews"] = ai_month
data["deepRead"] = deep_read
data["aiDeepRead"] = ai_deep_read
data["toListen"] = to_listen
data["aiListen"] = ai_listen
data["voices"] = merged_voices
data["todayForMe"] = today_for_me

# --- Validation ---
assert all(isinstance(c, dict) and "category" in c for c in data["todayNews"])
assert all(isinstance(c, dict) and "category" in c for c in data["aiTodayNews"])
for group in data["todayNews"] + data["aiTodayNews"]:
    for s in group["stories"]:
        assert "headline" in s, f"missing headline: {s}"
        assert "source" in s and "url" in s
assert all(kn.get("change") for kn in data["todayForMe"]["keyNumbers"])

# --- Serialize ---
new_data_json = json.dumps(data, ensure_ascii=False, indent=None, separators=(',', ':'))
new_html = re.sub(r'const DATA = \{.*?\};\s*\n', f'const DATA = {new_data_json};\n', html, count=1, flags=re.DOTALL)
HTML_PATH.write_text(new_html)
print(f"Updated DATA. todayNews: {len(data['todayNews'])} groups / {sum(len(g['stories']) for g in data['todayNews'])} stories; aiTodayNews: {len(data['aiTodayNews'])} groups / {sum(len(g['stories']) for g in data['aiTodayNews'])} stories; voices: {len(merged_voices)}")
