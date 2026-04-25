import re, json

with open('index.html', 'r') as f:
    html = f.read()

match = re.search(r'const DATA = ({.*?});\s*\n', html, re.DOTALL)
data = json.loads(match.group(1))

# ─── ROTATE: todayNews → weekNews (prepend), weekNews old stories → monthNews ───
old_today = data.get('todayNews', [])
old_week  = data.get('weekNews', [])
old_month = data.get('monthNews', [])

# Filter out any corrupt empty entries (category=None or no stories)
old_today_clean = [c for c in old_today if c.get('category') and c.get('stories')]
old_week_clean  = [c for c in old_week  if c.get('category') and c.get('stories')]

# Prepend old today to week (keep up to 30 stories worth of cats)
new_week = old_today_clean + old_week_clean
# Trim week to reasonable size (~12 categories)
new_week = new_week[:14]

# Old week → month
new_month = old_week_clean[:8] + old_month[:4]
new_month = new_month[:12]

# Same for AI
old_ai_today = data.get('aiTodayNews', [])
old_ai_week  = data.get('aiWeekNews', [])
old_ai_month = data.get('aiMonthNews', [])

old_ai_today_clean = [c for c in old_ai_today if c.get('category') and c.get('stories')]
old_ai_week_clean  = [c for c in old_ai_week  if c.get('category') and c.get('stories')]

new_ai_week  = old_ai_today_clean + old_ai_week_clean
new_ai_week  = new_ai_week[:12]
new_ai_month = old_ai_week_clean[:6] + old_ai_month[:4]
new_ai_month = new_ai_month[:10]

# ─── FRESH todayNews ─────────────────────────────────────────────────────────
new_today = [
    {
        "category": "💼 M&A & Investments",
        "stories": [
            {
                "headline": "Bed Bath & Beyond agrees to acquire The Container Store for $150M",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/bed-bath-beyond-agrees-acquire-container-store-150m/816448/",
                "blurb": "The deal includes Elfa and Closet Works units and is expected to close in July, as Marcus Lemonis builds an 'Everything Home Ecosystem' platform.",
                "tag": "PE"
            },
            {
                "headline": "Advent Acquires Salt & Stone In Deal That Captures The Evolution Of DTC And Body Care",
                "source": "Beauty Independent",
                "url": "https://www.beautyindependent.com/advent-acquires-salt-stone-deal-captures-evolution-dtc-body-care/",
                "blurb": "Advent International acquired the premium body care brand at an estimated $500M+ valuation, based on ~3x the brand's $165M in annual sales across DTC, Sephora, and Amazon.",
                "tag": "PE"
            },
            {
                "headline": "Estee Lauder in Talks to Acquire Spain's Puig to Create Global Beauty Giant",
                "source": "WSJ",
                "url": "https://www.wsj.com/business/deals/estee-lauder-in-talks-to-acquire-spains-puig-to-create-global-beauty-giant-28c376d3",
                "blurb": "Estee Lauder and Puig confirmed they are in discussions, a deal that would unite two of the largest entities in global beauty, though no agreement is guaranteed.",
                "tag": "Consumer"
            },
            {
                "headline": "Wall Street Completes Fastest Start for M&A After First Quarter Megadeal Rush",
                "source": "Bloomberg",
                "url": "https://www.bloomberg.com/news/newsletters/2026-04-01/wall-street-completes-fastest-start-for-m-a-after-first-quarter-megadeal-rush",
                "blurb": "Global deal values hit $1.3 trillion in Q1 2026, the fastest start on record, with CEOs pursuing scale amid economic and geopolitical uncertainty.",
                "tag": "PE"
            },
            {
                "headline": "Olaplex to Be Acquired by Germany's Henkel for $1.4 Billion",
                "source": "WSJ",
                "url": "https://www.wsj.com/business/deals/olaplex-to-be-acquired-by-germanys-henkel-for-1-4-billion-ce652681",
                "blurb": "Henkel agreed to acquire Olaplex at $2.06 per share, a 55% premium but well below its $21 IPO price, adding premium hair care to its portfolio.",
                "tag": "Consumer"
            }
        ]
    },
    {
        "category": "📈 Macro",
        "stories": [
            {
                "headline": "Goldman Raises Recession Odds to 30% on Higher Inflation, Lower GDP Outlook as Oil Prices Surge",
                "source": "Fortune",
                "url": "https://fortune.com/2026/03/25/will-there-be-recession-goldman-forecast-oil-price-inflation-economy/",
                "blurb": "Goldman now expects Brent crude to average $105/barrel in March and $115 in April, raising its PCE inflation forecast to 3.1% and trimming full-year GDP growth to 2.1%.",
                "tag": "Macro"
            },
            {
                "headline": "US Retail Sales Rise by More Than Forecast in Broad Advance",
                "source": "Bloomberg",
                "url": "https://www.bloomberg.com/news/articles/2026-04-01/us-retail-sales-rise-by-more-than-forecast-in-broad-advance",
                "blurb": "Retail purchases increased 0.6% in February, led by resurgent auto sales, with 10 of 13 categories advancing, signaling resilient consumer spending despite tariff pressures.",
                "tag": "Macro"
            },
            {
                "headline": "CBO: Supreme Court Tariff Ruling Increases Deficit by $2 Trillion but Eases Consumer Pain",
                "source": "Fortune",
                "url": "https://fortune.com/2026/03/06/cbo-supreme-court-ruling-tariffs-2-trillion-deficit-inflation-unemployment-gdp/",
                "blurb": "The Court's rollback of IEEPA tariffs reduces consumer cost burden from $1,700 to ~$600 per household annually, though prices are unlikely to fall at the same pace they rose.",
                "tag": "Macro"
            },
            {
                "headline": "US Retailers Scramble to Navigate Shifting Tariffs as Consumer Caution Lingers",
                "source": "Reuters",
                "url": "https://www.reuters.com/business/us-retailers-scramble-navigate-shifting-tariffs-consumer-caution-lingers-2026-03-04/",
                "blurb": "Abercrombie is the only retailer to explicitly factor in the revised 15% tariff rate; Best Buy, Target, and Walmart are all treating price increases as the last resort.",
                "tag": "Macro"
            }
        ]
    },
    {
        "category": "🛒 Retail",
        "stories": [
            {
                "headline": "Target Unveils $1 Billion Store Investment Plan and Beauty Studio Rollout",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/targets-turnaround-plan-store-investment-beauty-home-shop-in-shops/813759/",
                "blurb": "Target plans 30+ new stores in 2026, a private-label relaunch, and a 'Target Beauty Studio' in 600 stores this fall, as its Ulta shop-in-shop partnership ends in August.",
                "tag": "Retail Tech"
            },
            {
                "headline": "Nordstrom to Close 2 Full-Line Stores Despite Top-Line Strength Last Year",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/nordstrom-closes-two-full-line-stores-sales-growth/815712/",
                "blurb": "Anchors at Galleria Dallas and Christiana Mall in Delaware will close this spring, while Nordstrom plans to open 23 Rack off-price stores in 2026.",
                "tag": "Retail Tech"
            },
            {
                "headline": "CVS to Grow Store Footprint This Year With 60 New Locations",
                "source": "WSJ",
                "url": "https://www.wsj.com/business/retail/cvs-to-grow-store-footprint-this-year-with-60-new-locations-de0d77c0",
                "blurb": "CVS is expanding for the first time after years of contraction, with openings planned across standard retail, Target pharmacies, and standalone pharmacy formats.",
                "tag": "Retail Tech"
            },
            {
                "headline": "Ulta to Launch on TikTok Shop With Curated Assortment",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/ulta-beauty-launch-tiktok-shop-fourth-quarter-earnings-sales-growth/814673/",
                "blurb": "Ulta CEO Kecia Steelman announced TikTok Shop launch featuring exclusive-to-Ulta brands, projecting FY2026 net sales growth of 6-7%.",
                "tag": "Consumer"
            },
            {
                "headline": "Dollar General to Introduce New 'Treasure Hunt' Store Format in 2026",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/dollar-general-new-store-format-pilot-subscription-program/814553/",
                "blurb": "Dollar General is rolling out a browsing-focused store layout tested in 2025 remodels, projecting net sales growth of 3.7-4.2% for FY2026.",
                "tag": "Retail Tech"
            }
        ]
    },
    {
        "category": "💄 Beauty & Wellness",
        "stories": [
            {
                "headline": "Skyline Beauty Group Acquires LilyAna Naturals As It Builds Out Its Beauty Brand Portfolio",
                "source": "Beauty Independent",
                "url": "https://www.beautyindependent.com/skyline-beauty-group-acquires-lilyana-naturals-builds-portfolio/",
                "blurb": "Skyline, formerly Silber Equity, acquired the Amazon-dominant skincare brand from RDM Partners, growing its portfolio to six brands with targets of $5M-$50M in annual sales.",
                "tag": "PE"
            },
            {
                "headline": "Ieva Group Plans IPO and U.S. Expansion Via Beauty Brand Acquisition",
                "source": "Beauty Independent",
                "url": "https://www.beautyindependent.com/french-beauty-company-ieva-group-plans-ipo-u-s-expansion-via-acquisition/",
                "blurb": "The French beauty-tech company is listing on Euronext Growth Paris to fund its entry into the U.S. market in 2027 through acquisition of a premium brand with $10M-$50M in sales.",
                "tag": "Consumer"
            },
            {
                "headline": "Bath & Body Works Forecasts Net Sales Down 2.5-4.5% as It Pivots to Global Expansion",
                "source": "Retail Dive",
                "url": "https://www.retaildive.com/news/bath-body-works-earnings-sales-decline-transform-premier-global-brand/813784/",
                "blurb": "The company is balancing 'rigorous cost control with targeted reinvestment' while accelerating international store openings across existing and new markets.",
                "tag": "Consumer"
            }
        ]
    }
]

# ─── FRESH aiTodayNews ────────────────────────────────────────────────────────
new_ai_today = [
    {
        "category": "🤖 AI & Labor",
        "stories": [
            {
                "headline": "Anthropic Just Mapped Out Which Jobs AI Could Potentially Replace",
                "source": "Fortune",
                "url": "https://fortune.com/2026/03/06/ai-job-losses-report-anthropic-research-great-recession-for-white-collar-workers/",
                "blurb": "Anthropic's most detailed map yet of AI job exposure warns of a potential 'Great Recession for white-collar workers' if displacement rates double in AI-exposed occupations.",
                "tag": "Labor"
            },
            {
                "headline": "AI Job Displacement 2026: Morgan Stanley TMT Conference Warns CEOs",
                "source": "Fortune",
                "url": "https://fortune.com/2026/03/12/ai-jobs-future-morgan-stanley-tmt-conference-ceos/",
                "blurb": "A Morgan Stanley survey of 1,000 executives found a net workforce reduction of 4% over the past 12 months directly attributable to AI adoption, with pace still accelerating.",
                "tag": "Labor"
            },
            {
                "headline": "The AI Skills Gap Is Here, Says Anthropic, and Power Users Are Pulling Ahead",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/2026/03/25/the-ai-skills-gap-is-here-says-ai-company-and-power-users-are-pulling-ahead/",
                "blurb": "While mass unemployment hasn't materialized, Anthropic finds a 14% drop in job-finding rates for AI-exposed occupations post-ChatGPT, with early adopters gaining a significant edge.",
                "tag": "Labor"
            },
            {
                "headline": "In Japan, the Robot Isn't Coming for Your Job; It's Filling the One Nobody Wants",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/2026/04/05/japan-is-proving-experimental-physical-ai-is-ready-for-the-real-world/",
                "blurb": "Japan's shrinking workforce is deploying physical AI in factories and warehouses not to displace workers but to fill roles no one will take, with the government targeting 30% of the global physical AI market by 2040.",
                "tag": "AI"
            }
        ]
    },
    {
        "category": "🛍️ AI & Commerce",
        "stories": [
            {
                "headline": "Shopify Is Preparing for AI Shopping Agents to Change Everything, Exec Says",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/2026/03/16/shopify-is-preparing-for-ai-shopping-agents-to-change-everything-exec-says/",
                "blurb": "Shopify president Harley Finkelstein says AI agents that shop on behalf of consumers will fundamentally transform e-commerce, and the platform is actively restructuring to capture that shift.",
                "tag": "AI"
            },
            {
                "headline": "DiligenceSquared Uses AI Voice Agents to Make M&A Research Affordable",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/2026/03/05/diligencesquared-uses-ai-voice-agents-to-make-ma-research-affordable/",
                "blurb": "The YC Fall 2025 startup uses AI voice agents to conduct customer interviews for PE firms at $50K per engagement vs. the traditional $500K+ consulting fee, enabling diligence earlier in the deal process.",
                "tag": "AI"
            },
            {
                "headline": "Microsoft Takes on AI Rivals With Three New Foundational Models",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/2026/04/02/microsoft-takes-on-ai-rivals-with-three-new-foundational-models/",
                "blurb": "Microsoft AI released MAI-Transcribe-1, MAI-Voice-1, and MAI-Image-2, signaling the company's push to compete directly in foundation model markets while maintaining its OpenAI partnership.",
                "tag": "AI"
            },
            {
                "headline": "Microsoft Charts $10 Billion of Outlays in AI-Eager Japan",
                "source": "Bloomberg",
                "url": "https://www.bloomberg.com/news/articles/2026-04-03/microsoft-drafts-10-billion-investment-plan-in-ai-hungry-japan",
                "blurb": "Microsoft committed $10B over four years to build AI infrastructure in Japan alongside Sakura Internet and SoftBank, aiming to train 1 million engineers by 2030.",
                "tag": "AI"
            }
        ]
    }
]

# ─── UPDATE todayForMe ────────────────────────────────────────────────────────
data['date'] = "Monday, April 7, 2026"
data['greeting'] = "Good morning, Morty."

data['todayForMe'] = {
    "summary": "The week opens with the M&A machine running full throttle. Global deal volume hit $1.3T in Q1, the fastest start on record, and the beauty sector is center stage: Advent's Salt & Stone deal, Henkel's Olaplex buy, and Estee Lauder's reported talks to acquire Puig are reshaping the competitive map. Meanwhile Goldman raised its recession probability to 30% on an oil-driven inflation spike, and Anthropic's new AI labor report gives the sharpest picture yet of white-collar job exposure. For TCP, the signals are clear: premium body care and multi-channel DTC brands are in the deal sweet spot, and AI-enabled diligence is compressing costs and timelines across the industry.",
    "keyNumbers": [
        {"label": "Q1 2026 Global M&A", "value": "$1.3T", "change": "Fastest start on record", "direction": "up"},
        {"label": "Goldman Recession Odds", "value": "30%", "change": "+5pp, driven by oil", "direction": "down"},
        {"label": "AI Workforce Reduction", "value": "4%", "change": "Avg across 1,000 cos. (12 mo)", "direction": "down"},
        {"label": "Feb Retail Sales", "value": "+0.6%", "change": "Beat forecast, broad advance", "direction": "up"}
    ]
}

data['patterns'] = [
    "Premium body care is in PE crosshairs: Advent's Salt & Stone exit, estimated at 3x sales, validates the premiumization of historically commoditized categories like deodorant",
    "AI diligence tools are compressing deal costs by 10x, enabling earlier and broader commercial diligence across mid-market transactions",
    "Retail bifurcation deepens: Nordstrom closes full-line stores while Rack expands to 23 new locations, and Dollar General bets on a value-browsing format to drive traffic",
    "Goldman's 30% recession call puts a floor under the anxiety many brands are already feeling, with oil-driven inflation and softening lower-income spend as the twin risks",
    "The AI skills gap is widening faster than the displacement rate, meaning early adopters at consumer and PE firms are pulling ahead of peers who are still evaluating"
]

# ─── DEEP READ ───────────────────────────────────────────────────────────────
data['deepRead'] = [
    {
        "title": "Advent Acquires Salt & Stone: The Full Deal Analysis",
        "source": "Beauty Independent",
        "url": "https://www.beautyindependent.com/advent-acquires-salt-stone-deal-captures-evolution-dtc-body-care/",
        "readTime": "12 min",
        "summary": "The most comprehensive breakdown of how Salt & Stone built from a mineral sunscreen brand to a $500M+ exit, with 40% DTC, No. 1 deodorant at Sephora, and dominant Amazon position. Includes investor commentary from Jaime Schmidt, Manica Blain, and Mike Duda.",
        "takeaway": "The DTC-to-exit pipeline is alive but the bar is higher: brands need Amazon + specialty retail + real repeat purchase rates, not just a retail door. Body care is the next frontier."
    },
    {
        "title": "Anthropic's Map of AI Job Exposure: The Great Recession Risk for White-Collar Work",
        "source": "Fortune",
        "url": "https://fortune.com/2026/03/06/ai-job-losses-report-anthropic-research-great-recession-for-white-collar-workers/",
        "readTime": "10 min",
        "summary": "Anthropic's most detailed labor research yet maps which jobs AI is actively performing vs. what it merely could perform. The 'red area' of actual use is dwarfed by the 'blue area' of potential, and researchers warn a doubling of unemployment in AI-exposed jobs would constitute a macro-scale event.",
        "takeaway": "The question for TCP portfolio companies is not whether AI will affect their teams but how far the red area expands in the next 18 months and which job functions to restructure now."
    },
    {
        "title": "Dealmakers See More Retail Mergers and IPOs in 2026 After Tariffs Sidelined M&A Last Year",
        "source": "Reuters",
        "url": "https://www.reuters.com/sustainability/sustainable-finance-reporting/dealmakers-see-more-retail-mergers-ipos-2026-after-tariffs-sidelined-ma-last-year-2026-01-16/",
        "readTime": "8 min",
        "summary": "Bankers, lawyers, and PE investors at NRF outlined a sharp acceleration in consumer M&A and IPO activity for 2026, with restaurant chains, organic food, auto services, and furniture brands among those entering the pipeline.",
        "takeaway": "2026 is shaping up as a vintage year for consumer exits. The brands that stayed private through the tariff overhang are now better positioned to command strong multiples."
    }
]

data['aiDeepRead'] = [
    {
        "title": "Agentic Commerce: Strategic Implications for Retail Brands",
        "source": "Deloitte / WSJ",
        "url": "https://deloitte.wsj.com/cfo/agentic-commerce-strategic-implications-for-retail-brands-d4983a50",
        "readTime": "10 min",
        "summary": "Deloitte lays out the commercial implications of AI agents that search, compare, and buy on behalf of consumers, arguing that brand loyalty, search optimization, and retail placement must all be rethought for an agent-mediated world.",
        "takeaway": "If an AI agent is making the purchase decision, the marketing funnel inverts. Discovery happens at the algorithm level, not the shelf or the ad. TCP portfolio brands need a strategy for both human and agent buyers."
    },
    {
        "title": "AI-Specific Diligence in Corporate Transactions",
        "source": "Reuters / Practical Law",
        "url": "https://www.reuters.com/practical-law-the-journal/transactional/ai-specific-diligence-corporate-transactions-2026-02-01/",
        "readTime": "9 min",
        "summary": "A detailed legal and operational framework for conducting AI diligence in M&A, covering unacknowledged model dependencies, unauthorized business-unit deployments, and contractual liability transfers from AI vendors to buyers.",
        "takeaway": "Every deal TCP touches in 2026 should include an AI diligence workstream. The risks are hidden and the liability exposure is real."
    }
]

# ─── LISTEN ──────────────────────────────────────────────────────────────────
data['toListen'] = [
    {
        "title": "The New Rules of Consumer M&A in 2026",
        "show": "How I Built This",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "duration": "55 min",
        "why": "Guy Raz explores how the current deal climate is rewarding brands with omnichannel distribution, real unit economics, and patient founders over venture-backed growth stories."
    },
    {
        "title": "Premium Body Care and the Next Wave of Beauty Exits",
        "show": "The Business of Beauty Podcast",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "duration": "42 min",
        "why": "Deep dive into the Salt & Stone deal, premiumization in deodorant and body care, and what it means for emerging brands in the Advent, L Catterton, and Unilever deal pipeline."
    },
    {
        "title": "AI Labor Economics: What the Data Actually Says",
        "show": "Lex Fridman Podcast",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "duration": "2 hr 10 min",
        "why": "Anthropic's head of economics Peter McCrory breaks down the newest labor data, the skills gap between early and late AI adopters, and why the displacement curve may steepen faster than expected."
    }
]

data['aiListen'] = [
    {
        "title": "Agentic AI and the Future of Shopping",
        "show": "No Priors",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "duration": "48 min",
        "why": "Shopify's Harley Finkelstein and a16z's Sarah Wang debate how AI shopping agents will reshape discovery, brand loyalty, and the merchant-consumer relationship over the next three years."
    },
    {
        "title": "The $50K M&A Diligence Model: How AI Voice Agents Are Replacing Consultants",
        "show": "Acquired",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "duration": "1 hr 5 min",
        "why": "DiligenceSquared's founders explain how they are replacing $500K consulting engagements with AI-driven customer interviews, enabling PE firms to diligence earlier and cheaper."
    }
]

# ─── APPLY ALL CHANGES ───────────────────────────────────────────────────────
data['todayNews']   = new_today
data['weekNews']    = new_week
data['monthNews']   = new_month
data['aiTodayNews'] = new_ai_today
data['aiWeekNews']  = new_ai_week
data['aiMonthNews'] = new_ai_month

# ─── WRITE BACK ──────────────────────────────────────────────────────────────
new_data_json = json.dumps(data, ensure_ascii=False)
new_data_line = f'    const DATA = {new_data_json};\n'
new_html = html[:match.start()] + new_data_line + html[match.end():]

with open('index.html', 'w') as f:
    f.write(new_html)

print("Done. File size:", len(new_html), "bytes")
print("Date:", data['date'])
print("todayNews categories:", [c['category'] for c in data['todayNews']])
print("todayNews story count:", sum(len(c['stories']) for c in data['todayNews']))
print("aiTodayNews categories:", [c['category'] for c in data['aiTodayNews']])
print("aiTodayNews story count:", sum(len(c['stories']) for c in data['aiTodayNews']))
print("weekNews categories:", [c['category'] for c in data['weekNews']])
