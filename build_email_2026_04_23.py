#!/usr/bin/env python3
"""Build the April 23 branded email."""

DATE = "Thursday, April 23, 2026"

BRIEF = (
    "Sentiment hit a record low while retail sales surprised up. The anxious-but-spending "
    "consumer persists. Private label crossed $282.8B and now owns 23.5% of grocery units; "
    "David Protein is chasing $300M on the alt-fat rail; Estée Lauder takes full control of "
    "Forest Essentials. Modern Retail calls 2026 the shopping-agent war year, a San Francisco "
    "storefront is being run end-to-end by an Anthropic-powered agent, and Grant Thornton's PE "
    "survey shows a wide AI proof gap."
)

KEY_NUMBERS = [
    {"label": "March Retail Sales", "value": "+1.7%", "change": "Beat +1.3% consensus, $752.1B", "direction": "up"},
    {"label": "Sentiment Index", "value": "47.6", "change": "-10.7% MoM, record low", "direction": "down"},
    {"label": "Private Label 2025", "value": "$282.8B", "change": "+3.3% vs national brands +1.2%", "direction": "up"},
    {"label": "Tariff Core Goods Lift", "value": "+3.1%", "change": "Full pass-through 5-9 months", "direction": "up"},
]

CONSUMER_STORIES = [
    {
        "cat": "📈 Macro",
        "items": [
            {"h": "Consumer sentiment hits record low, inflation fears rise amid Iran war",
             "s": "CNBC", "u": "https://www.cnbc.com/2026/04/10/consumer-sentiment-inflation-fears-iran-war.html",
             "b": "April sentiment index fell 10.7% MoM to 47.6 with 1-year inflation expectations at 4.8%. Steepest confidence drop since the 2022 energy shock."},
            {"h": "March retail sales surge 1.7% MoM to $752.1B, beating +1.3% consensus",
             "s": "U.S. Census Bureau", "u": "https://www.census.gov/retail/sales.html",
             "b": "Nonstore retail +10.1% YoY leads; foodservice +2.4% YoY holds steady despite softening broader sentiment."},
            {"h": "Fed: tariff pass-through added 3.1% to core goods PCE through February",
             "s": "Federal Reserve", "u": "https://www.federalreserve.gov/econres/notes/feds-notes/detecting-tariff-effects-on-consumer-prices-in-real-time-part-II-20260408.html",
             "b": "Full tariff pass-through takes 5-9 months. Retailers with inventory hedges have summer runway before the margin hit."},
        ]
    },
    {
        "cat": "💼 M&A & Investments",
        "items": [
            {"h": "Estée Lauder to acquire remaining stake in Forest Essentials, closing 2H 2026",
             "s": "The Estée Lauder Companies", "u": "https://www.elcompanies.com/en/news-and-media/newsroom/press-releases/2026/03-05-2026-054514302",
             "b": "ELC takes full control of the India-based luxury Ayurveda brand after years as minority investor. Founder stays, global scale-up begins."},
            {"h": "David Protein scales alt-fat capacity 5x; targets $300M+ 2026 revenue",
             "s": "AgFunderNews", "u": "https://agfundernews.com/exclusive-david-protein-scales-alt-fat-epg-capacity-eyes-cpg-deals-as-ceo-targets-300m-revenues-in-2026",
             "b": "RXBAR founder Peter Rahal's vehicle expands post-Epogee acquisition; B2B partnerships become the next lane."},
        ]
    },
    {
        "cat": "🏬 Retail",
        "items": [
            {"h": "Over 2,000 U.S. retail stores and restaurants set to close in 2026",
             "s": "Business Insider", "u": "https://www.businessinsider.com/stores-closing-in-2026-list",
             "b": "7-Eleven, Macy's, Kroger, Saks Off 5th among the chains shrinking footprints. Store economics and traffic rebalance across mass, mid, and luxury."},
            {"h": "Associated Wholesale Grocers adds 63 new private label items for independents",
             "s": "Grocery Dive", "u": "https://www.grocerydive.com/news/associated-wholesale-grocers-expands-private-label/814724/",
             "b": "Data-driven selection including premium tiers. AWG follows the PLMA signal that store brands are the margin engine."},
        ]
    },
    {
        "cat": "🥫 CPG & Food",
        "items": [
            {"h": "U.S. private label hits $282.8B in 2025, +3.3% vs national brands +1.2%",
             "s": "PLMA / Circana", "u": "https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025",
             "b": "Store brands now hold 21.3% dollar share and 23.5% unit share. Private label unit growth outpaces national brands for the 7th consecutive year."},
        ]
    },
]

AI_STORIES = [
    {
        "cat": "🛍️ AI & Commerce",
        "items": [
            {"h": "AI shopping agent wars define 2026: platforms fight to become the default shopping interface",
             "s": "Modern Retail", "u": "https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/",
             "b": "Amazon, OpenAI, and fashion-agent startups push conversational discovery and in-flow checkout. The question is who owns attention, not the cart."},
        ]
    },
    {
        "cat": "🤖 AI & Labor",
        "items": [
            {"h": "Anthropic-powered AI agent runs a San Francisco storefront: posts jobs, interviews, hires",
             "s": "ABC News", "u": "https://abcnews.com/video/132290329/",
             "b": "First visible production case of AI agents making retail labor decisions end-to-end. The line between 'assisting' and 'managing' just moved."},
        ]
    },
    {
        "cat": "💼 AI & PE",
        "items": [
            {"h": "Grant Thornton: private equity reports heavy AI use, limited revenue lift, weak governance",
             "s": "Grant Thornton", "u": "https://www.grantthornton.com/insights/survey-reports/private-equity/2026/private-equity-insights-2026-ai-impact-survey-report",
             "b": "The AI proof gap in PE is wide open. Intent and experimentation are high; measurable outcomes and governance readiness are not."},
        ]
    },
]


def render_key_number(kn):
    arrow = "↑" if kn["direction"] == "up" else "↓"
    color = "#059669" if kn["direction"] == "up" else "#DC2626"
    return f'''
<td width="50%" style="padding:10px;vertical-align:top;">
  <div style="background:#F9FAFB;border-radius:10px;padding:14px 16px;border:1px solid #E5E7EB;">
    <div style="font-size:11px;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">{kn["label"]}</div>
    <div style="font-size:24px;font-weight:800;color:#111827;line-height:1.1;">{kn["value"]} <span style="color:{color};font-size:18px;">{arrow}</span></div>
    <div style="font-size:13px;color:#6B7280;margin-top:4px;">{kn["change"]}</div>
  </div>
</td>'''


def render_story(item):
    return f'''
<div style="margin-bottom:18px;">
  <a href="{item['u']}" style="text-decoration:none;color:#111827;">
    <div style="font-size:19px;font-weight:700;color:#111827;line-height:1.25;margin-bottom:6px;">{item['h']}</div>
  </a>
  <div style="font-size:13px;color:#6D28D9;font-weight:600;margin-bottom:6px;">{item['s']}</div>
  <div style="font-size:17px;color:#374151;line-height:1.5;">{item['b']}</div>
</div>'''


def render_category(group):
    stories_html = "".join(render_story(i) for i in group["items"])
    return f'''
<div style="margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #EDE9FE;">{group["cat"]}</div>
  {stories_html}
</div>'''


def build_email():
    key_pairs = []
    for i in range(0, len(KEY_NUMBERS), 2):
        row = "".join(render_key_number(kn) for kn in KEY_NUMBERS[i:i+2])
        key_pairs.append(f'<tr>{row}</tr>')
    key_numbers_html = f'<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:separate;margin:8px -10px 18px;">{"".join(key_pairs)}</table>'

    consumer_html = "".join(render_category(g) for g in CONSUMER_STORIES)
    ai_html = "".join(render_category(g) for g in AI_STORIES)

    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F9FAFB;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<div style="max-width:600px;margin:0 auto;background:#FFFFFF;padding:28px;">

  <div style="text-align:center;padding-bottom:20px;border-bottom:1px solid #E5E7EB;">
    <div style="font-size:28px;font-weight:900;color:#6D28D9;letter-spacing:2px;">CONSUMER SAFARI</div>
    <div style="font-size:12px;font-weight:600;color:#6B7280;letter-spacing:2px;margin-top:4px;">THE MORNING BRIEFING</div>
    <div style="font-size:14px;color:#6B7280;margin-top:12px;">{DATE}</div>
    <div style="font-size:14px;margin-top:8px;"><a href="https://www.consumersafari.com" style="color:#6D28D9;text-decoration:underline;font-weight:600;">To save articles and more, go to ConsumerSafari.com</a></div>
  </div>

  <div style="background:#F5F3FF;border-left:4px solid #6D28D9;padding:18px 20px;margin:24px 0;border-radius:4px;">
    <div style="font-size:12px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Your Brief</div>
    <div style="font-size:18px;color:#1F2937;line-height:1.55;">{BRIEF}</div>
  </div>

  {key_numbers_html}

  {consumer_html}

  <hr style="border:none;border-top:1px solid #E5E7EB;margin:32px 0;">
  <div style="font-size:16px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;text-align:center;margin-bottom:24px;">AI &amp; TECHNOLOGY</div>

  {ai_html}

  <div style="text-align:center;margin-top:32px;padding:20px 0;">
    <a href="https://www.consumersafari.com" style="display:inline-block;background:#6D28D9;color:#FFFFFF;text-decoration:none;font-weight:700;padding:14px 32px;border-radius:8px;font-size:15px;">Read Full Briefing</a>
  </div>

  <div style="text-align:center;margin-top:28px;padding-top:20px;border-top:1px solid #E5E7EB;font-size:11px;color:#9CA3AF;letter-spacing:1px;text-transform:uppercase;">Powered by TCP Intelligence</div>

</div>
</body>
</html>'''
    return html


if __name__ == "__main__":
    import sys
    html = build_email()
    with open("/home/user/workspace/morning-briefing/email_2026_04_23.html", "w") as f:
        f.write(html)
    print(f"Wrote email HTML ({len(html)} chars)")
