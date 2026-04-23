#!/usr/bin/env python3
"""Update DATA in index.html for 2026-04-23 briefing."""
import re, json
from pathlib import Path

HTML_PATH = Path(__file__).parent / "index.html"
html = HTML_PATH.read_text()

m = re.search(r'const DATA = (\{.*?\});\s*\n', html, re.DOTALL)
data = json.loads(m.group(1))

# --- Rotate ---
# Move yesterday's todayNews to top of weekNews; trim weekNews to 10 groups; overflow to monthNews
prev_today = data.get("todayNews", [])
prev_ai_today = data.get("aiTodayNews", [])
week = data.get("weekNews", [])
ai_week = data.get("aiWeekNews", [])
month = data.get("monthNews", [])
ai_month = data.get("aiMonthNews", [])

# Prepend yesterday to week
week = prev_today + week
ai_week = prev_ai_today + ai_week

# Trim week to last 10 groups, overflow to month
if len(week) > 10:
    overflow = week[10:]
    week = week[:10]
    month = overflow + month
if len(ai_week) > 10:
    overflow = ai_week[10:]
    ai_week = ai_week[:10]
    ai_month = overflow + ai_month
if len(month) > 18:
    month = month[:18]
if len(ai_month) > 18:
    ai_month = ai_month[:18]

# --- New todayNews (Consumer) ---
today_news = [
    {
        "category": "📈 Macro",
        "stories": [
            {
                "headline": "Consumer sentiment hits record low, inflation fears rise amid Iran war",
                "source": "CNBC",
                "url": "https://www.cnbc.com/2026/04/10/consumer-sentiment-inflation-fears-iran-war.html",
                "blurb": "April sentiment index fell 10.7% MoM to 47.6 with 1-year inflation expectations at 4.8%; the steepest confidence drop since the 2022 energy shock.",
                "tag": "Macro",
            },
            {
                "headline": "March retail sales surge 1.7% MoM to $752.1B, beating +1.3% consensus",
                "source": "U.S. Census Bureau",
                "url": "https://www.census.gov/retail/sales.html",
                "blurb": "Nonstore retail +10.1% YoY leads the acceleration; foodservice +2.4% YoY remains steady despite softening broader sentiment.",
                "tag": "Macro",
            },
            {
                "headline": "Fed note: tariff pass-through added 3.1% to core goods PCE through February; full pass-through takes 5-9 months",
                "source": "Federal Reserve",
                "url": "https://www.federalreserve.gov/econres/notes/feds-notes/detecting-tariff-effects-on-consumer-prices-in-real-time-part-II-20260408.html",
                "blurb": "Tariff-driven prices are still working through the retail stack; retailers with inventory hedges have runway through summer before passing full costs.",
                "tag": "Macro",
            },
        ],
    },
    {
        "category": "💼 M&A & Investments",
        "stories": [
            {
                "headline": "Estée Lauder to acquire remaining stake in Forest Essentials, closing 2H 2026",
                "source": "The Estée Lauder Companies",
                "url": "https://www.elcompanies.com/en/news-and-media/newsroom/press-releases/2026/03-05-2026-054514302",
                "blurb": "ELC takes full control of the India-based luxury Ayurveda brand after years as minority investor; founder stays, Luxurious Ayurveda positioned for global scale.",
                "tag": "PE",
            },
            {
                "headline": "David Protein scales alt-fat capacity 5x; targets $300M+ 2026 revenue and CPG supply deals",
                "source": "AgFunderNews",
                "url": "https://agfundernews.com/exclusive-david-protein-scales-alt-fat-epg-capacity-eyes-cpg-deals-as-ceo-targets-300m-revenues-in-2026",
                "blurb": "RXBAR founder Peter Rahal's vehicle expands manufacturing post-Epogee acquisition; B2B partnerships become the next lane while lawsuits from prior EPG customers persist.",
                "tag": "Consumer",
            },
        ],
    },
    {
        "category": "🏬 Retail",
        "stories": [
            {
                "headline": "Over 2,000 U.S. retail stores and restaurants set to close in 2026",
                "source": "Business Insider",
                "url": "https://www.businessinsider.com/stores-closing-in-2026-list",
                "blurb": "7-Eleven, Macy's, Kroger, Saks Off 5th among the chains shrinking footprints; store economics and traffic patterns force rebalancing across mass, mid, and luxury.",
                "tag": "Retail",
            },
            {
                "headline": "Associated Wholesale Grocers adds 63 new private label items to help independents compete",
                "source": "Grocery Dive",
                "url": "https://www.grocerydive.com/news/associated-wholesale-grocers-expands-private-label/814724/",
                "blurb": "Data-driven selection including premium tiers; AWG follows the PLMA signal that store brands are now the margin engine across grocery.",
                "tag": "Retail",
            },
        ],
    },
    {
        "category": "🥫 CPG & Food",
        "stories": [
            {
                "headline": "U.S. private label hits $282.8B in 2025, +3.3% vs national brands +1.2%",
                "source": "PLMA / Circana",
                "url": "https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025",
                "blurb": "Store brands now hold 21.3% dollar share and 23.5% unit share; private label unit growth outpaces national brand unit growth 7th consecutive year.",
                "tag": "Consumer",
            },
        ],
    },
]

# --- New aiTodayNews ---
ai_today_news = [
    {
        "category": "🛍️ AI & Commerce",
        "stories": [
            {
                "headline": "AI shopping agent wars define 2026: platforms fight to become the default shopping interface",
                "source": "Modern Retail",
                "url": "https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/",
                "blurb": "Amazon, OpenAI, and fashion-agent startups push conversational discovery and in-flow checkout; the question is who owns the attention layer, not the cart.",
                "tag": "Retail Tech",
            },
        ],
    },
    {
        "category": "🤖 AI & Labor",
        "stories": [
            {
                "headline": "Anthropic-powered AI agent runs a San Francisco storefront: posts jobs, interviews, hires staff",
                "source": "ABC News",
                "url": "https://abcnews.com/video/132290329/",
                "blurb": "First visible production case of AI agents making retail labor decisions end-to-end; the line between 'assisting' and 'managing' just moved.",
                "tag": "Labor",
            },
        ],
    },
    {
        "category": "💼 AI & PE",
        "stories": [
            {
                "headline": "Grant Thornton survey: private equity reports heavy AI use, limited revenue lift, weak governance",
                "source": "Grant Thornton",
                "url": "https://www.grantthornton.com/insights/survey-reports/private-equity/2026/private-equity-insights-2026-ai-impact-survey-report",
                "blurb": "The Feb-Mar 2026 AI Impact Survey finds the PE proof gap wide open: intent and experimentation are high, measurable outcomes and governance readiness are not.",
                "tag": "PE",
            },
        ],
    },
]

# --- Deep Read / AI Deep Read ---
deep_read = [
    {
        "title": "Detecting Tariff Effects on Consumer Prices in Real Time – Part II",
        "source": "Federal Reserve FEDS Notes",
        "url": "https://www.federalreserve.gov/econres/notes/feds-notes/detecting-tariff-effects-on-consumer-prices-in-real-time-part-II-20260408.html",
        "readTime": "14 min",
        "summary": "Board economists track tariff pass-through into PCE inflation using Trade Partner Inflation methodology; core goods +3.1% tariff effect through Feb 2026 with 5-9 months to full pass-through.",
        "takeaway": "Retailers with forward-bought inventory still have summer runway; the back-to-school season is where margin compression shows up in earnings.",
    }
]
ai_deep_read = [
    {
        "title": "AI Impact Survey Report 2026 – Private Equity",
        "source": "Grant Thornton",
        "url": "https://www.grantthornton.com/insights/survey-reports/private-equity/2026/private-equity-insights-2026-ai-impact-survey-report",
        "readTime": "18 min",
        "summary": "PE firms report broad AI deployment including autonomous agents in due diligence and portfolio management, but weak outcome measurement and light governance frameworks create proof-of-value pressure.",
        "takeaway": "AI due diligence is table stakes; the differentiation is governance and measurable portfolio lift, not tool adoption.",
    }
]

# --- To Listen / AI Listen ---
to_listen = [
    {
        "title": "From $7K To 10,000 Stores. The Protein Pints Playbook.",
        "show": "YouTube",
        "url": "https://www.youtube.com/watch?v=r4MJe6pjjNg",
        "duration": "32 min",
        "why": "Founder playbook for protein-forward frozen scaling; timed to Expo West 2026 and the broader protein-snack wave.",
    }
]
ai_listen = [
    {
        "title": "AI, Agentic Commerce & Retail Media's Next Power Shift",
        "show": "Retail Media Breakfast Club (YouTube)",
        "url": "https://www.youtube.com/watch?v=UGoMEsruakE",
        "duration": "10 min",
        "why": "Shoptalk 2026 floor pulse check on agentic commerce and retail media power shifts; practitioner tempo, not analyst commentary.",
    }
]

# --- Voices (prepend 2 new, keep existing roster) ---
new_voices = [
    {
        "author": "Philip Lempert",
        "handle": "phillempert",
        "platform": "Substack",
        "title": "They Changed Your Food. Now You're Changing It Back.",
        "url": "https://phillempert.substack.com/p/they-changed-your-food-now-youre",
        "date": "Apr 6, 2026",
        "feedType": "consumer",
    },
    {
        "author": "Jason Averbook",
        "handle": "jasonaverbook",
        "platform": "Substack",
        "title": "What the March 2026 AI Jobs Data Actually Tells Us",
        "url": "https://jasonaverbook.substack.com/p/what-the-march-2026-ai-jobs-data",
        "date": "Mar 26, 2026",
        "feedType": "ai",
    },
]
existing_voices = data.get("voices", []) or []
# Dedupe by url
seen_urls = {v.get("url") for v in new_voices}
merged_voices = new_voices + [v for v in existing_voices if v.get("url") not in seen_urls]

# --- todayForMe ---
today_for_me = {
    "greeting": "Morty",
    "summary": "Sentiment hit a record low while retail sales surprised up — the split persists. Private label crossed $282.8B and now owns 23.5% of grocery units; David Protein is chasing $300M on the alt-fat rail; Estée Lauder takes full control of Forest Essentials. On AI: Modern Retail frames 2026 as the shopping-agent war year, a San Francisco storefront is being run end-to-end by an Anthropic-powered agent, and Grant Thornton's PE survey shows a yawning proof gap between AI use and AI results.",
    "keyNumbers": [
        {
            "label": "March Retail Sales",
            "value": "+1.7%",
            "change": "Beat +1.3% consensus, $752.1B level",
            "direction": "up",
        },
        {
            "label": "Sentiment Index",
            "value": "47.6",
            "change": "-10.7% MoM, record low",
            "direction": "down",
        },
        {
            "label": "Private Label 2025",
            "value": "$282.8B",
            "change": "+3.3% vs national brands +1.2%",
            "direction": "up",
        },
        {
            "label": "Tariff Core Goods Lift",
            "value": "+3.1%",
            "change": "Fed: full pass-through 5-9 months",
            "direction": "up",
        },
    ],
    "patterns": [
        {
            "title": "The confidence-spending split widened",
            "detail": "Sentiment at a record low coexists with retail sales beating consensus by 40 bps. The consumer is anxious but still spending on essentials and protein-forward categories; discretionary discretionary trading will be the Q2 tell.",
        },
        {
            "title": "Private label is now the structural margin engine",
            "detail": "Store brands at 23.5% unit share crossed a psychological line. AWG adding 63 new items including premium tier confirms the 'worth it' frame: consumers trade down on commodity, up on functional, and private label is playing both lanes.",
        },
        {
            "title": "Alt-fat and alt-protein are the new moats",
            "detail": "David Protein's 5x capacity expansion to hit $300M and chase B2B partnerships mirrors what whey did in 2015. The ingredient layer is where the next wave of food M&A will concentrate.",
        },
        {
            "title": "Agentic commerce is becoming an attention war, not a transaction war",
            "detail": "Modern Retail's 2026 frame is right: the question is not who processes the purchase but who owns the discovery moment. Amazon, OpenAI, and fashion-agent startups are fighting for the same consumer attention window.",
        },
        {
            "title": "PE has an AI proof gap",
            "detail": "Grant Thornton shows heavy deployment, limited results, thin governance. The firms that quantify AI lift at the portfolio level first will win the next fundraising cycle.",
        },
    ],
}

# --- Compose updated data ---
data["date"] = "Thursday, April 23, 2026"
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
assert all(kn.get("change") for kn in data["todayForMe"]["keyNumbers"]), "keyNumbers change cannot be empty"

# --- Serialize and replace ---
new_data_json = json.dumps(data, ensure_ascii=False, indent=None, separators=(',', ':'))
# Replace in HTML
new_html = re.sub(r'const DATA = \{.*?\};\s*\n', f'const DATA = {new_data_json};\n', html, count=1, flags=re.DOTALL)
HTML_PATH.write_text(new_html)
print(f"Updated DATA. todayNews: {len(data['todayNews'])} groups / {sum(len(g['stories']) for g in data['todayNews'])} stories; aiTodayNews: {len(data['aiTodayNews'])} groups / {sum(len(g['stories']) for g in data['aiTodayNews'])} stories; voices: {len(merged_voices)}")
