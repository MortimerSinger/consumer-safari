#!/usr/bin/env python3
"""Build the April 24 branded email."""
import json, subprocess, time

DATE = "Friday, April 24, 2026"

BRIEF = (
    "Private label crossed $330B with 24% unit share. GLP-1 households are now $390/year "
    "lighter on groceries and 1 in 4 have switched stores since starting. Consumer megadeals "
    "came back in Q1 and PwC is telling CPG leaders to reshape, not resize. On AI: 78,557 "
    "tech layoffs in Q1 with half attributed to AI; Epoch/Ipsos found 1 in 5 workers saying "
    "AI has already taken over parts of their job; and agentic commerce is live with 50M U.S. "
    "users already transacting through agents."
)

KEY_NUMBERS = [
    {"label": "Private Label 2025", "value": "$330B", "change": "24% unit share, 23% dollar share", "direction": "up"},
    {"label": "GLP-1 Grocery Spend", "value": "-5 to -8%", "change": "$390/year lower per household", "direction": "down"},
    {"label": "Tech Layoffs Q1", "value": "78,557", "change": "47.9% attributed to AI", "direction": "up"},
    {"label": "Agentic Commerce", "value": "~50M", "change": "17% of U.S. consumers using AI agents", "direction": "up"},
]

CONSUMER_STORIES = [
    {"cat": "🥫 CPG & Food", "items": [
        {"h": "U.S. Private Label Sales Hit $330 Billion, 24% Unit Share",
         "s": "PLMA / Circana", "u": "https://www.plma.com/article/report-us-private-label-cpg-sales-reach-330-billion",
         "b": "Updated Circana figures put store brands at a 23% dollar share, with unit growth still outpacing national brands even as growth is expected to slow."},
        {"h": "GLP-1 Users Cut Grocery Spending 5-8%, Shift to Fresh and High-Protein",
         "s": "Supermarket News", "u": "https://www.supermarketnews.com/nonfood-pharmacy/glp-1-drugs-reshape-consumer-spending-eating-and-wellness-habits-report",
         "b": "GLP-1 households spend ~$390 less annually on groceries and show the biggest declines in chips, cookies, and sweet bakery; 70% research products digitally."},
        {"h": "1 in 4 GLP-1 Users Switched Grocery Stores Since Starting Medication",
         "s": "CivicScience", "u": "https://civicscience.com/glp-1-trends-by-civicscience-weight-loss-pills-dining-out-motivations-and-grocery-store-preferences/",
         "b": "Highest store-switching percentage since November 2025; fast-food dinner traffic down 6% among regular users."},
    ]},
    {"cat": "💼 M&A & Investments", "items": [
        {"h": "Consumer Megadeals Return in Q1 2026 After Multi-Year Drought",
         "s": "Reuters", "u": "https://www.reuters.com/business/finance/consumer-megadeals-make-rare-comeback-first-quarter-2026-04-03/",
         "b": "Q1 saw consumer megadeals rebound as rate cuts and LP pressure for distributions force activity. H2 2026 expected to see a significant uptick in consumer M&A."},
        {"h": "Consumer VC Bifurcates: Megafunds Flush, Seed Funding Down 31% YoY",
         "s": "Peony / Carta", "u": "https://www.peony.ink/blog/consumer-investors",
         "b": "L Catterton raised $11B, VMG Partners closed a $1B fund, CAVU closed $325M in February. Early-stage check availability is thinning fast."},
    ]},
    {"cat": "🏬 Retail", "items": [
        {"h": "Coresight: 8,270 U.S. Store Closures in 2025; 2026 Tracking Higher",
         "s": "MMCG / Coresight", "u": "https://www.mmcginvest.com/post/the-great-american-store-closure-tracker-2026-edition",
         "b": "GameStop accelerating to 727 U.S. closures in FY2025 with 430-500 more announced for early 2026. Store rationalization is now structural, not cyclical."},
        {"h": "7-Eleven to Close 645 Stores in FY2026; Apple Shuts 3 Mall Locations",
         "s": "Business Insider", "u": "https://www.businessinsider.com/stores-closing-in-2026-list",
         "b": "Seven & i Holdings confirms 645 North American closures through February 2027. Apple citing declining mall conditions."},
    ]},
]

AI_STORIES = [
    {"cat": "🤖 AI & Labor", "items": [
        {"h": "Tech Industry Shed 78,557 Jobs in Q1 2026, Nearly Half Attributed to AI",
         "s": "Tom's Hardware / Nikkei Asia", "u": "https://www.tomshardware.com/tech-industry/tech-industry-lays-off-nearly-80-000-employees-in-the-first-quarter-of-2026-almost-50-percent-of-affected-positions-cut-due-to-ai",
         "b": "37,638 cuts (47.9%) tied to AI and workflow automation. Cognizant CAIO warns the real productivity gain hasn't landed yet."},
        {"h": "1 in 5 Full-Time Workers Say AI Has Taken Over Parts of Their Job",
         "s": "Epoch AI / Ipsos", "u": "https://futureforwarded.substack.com/p/the-ai-labor-report-friday-9-april",
         "b": "Replacement (20%) outpaces creation (15%) by 5 points. Half of U.S. adults used AI at work last week, mostly via personal subscriptions."},
        {"h": "Snap Cuts 1,000 Jobs, Cancels 300 Openings; Stock Rises on AI Investment Pivot",
         "s": "Future Forwarded", "u": "https://futureforwarded.substack.com/p/the-ai-labor-report-monday-april",
         "b": "CEO Evan Spiegel announces $500M+ annual savings to fund AI infrastructure. Anthropic research shows hiring for ages 22-25 down 14% since ChatGPT launch."},
    ]},
    {"cat": "🛍️ AI & Commerce", "items": [
        {"h": "Agentic Commerce Now Live: 17% of Consumers Use AI Shopping Agents, ~50M U.S. Users",
         "s": "Codewave", "u": "https://codewave.com/insights/agentic-commerce-ai-shopping-agents/",
         "b": "Shopify, PayPal, Google, and Stripe building infrastructure for autonomous agent checkout. Walmart's Sparky is in production handling predictive reordering."},
        {"h": "Amazon 'Buy For Me' and OpenAI's Target/Instacart/DoorDash Deals Define the Default-Interface Fight",
         "s": "Modern Retail", "u": "https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/",
         "b": "Ralph Lauren and other luxury brands now launching their own AI assistants. The question is whose agent becomes the default interface, not whose cart processes the purchase."},
    ]},
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
    html = build_email()
    with open("/home/user/workspace/morning-briefing/email_2026_04_24.html", "w") as f:
        f.write(html)
    print(f"Wrote email HTML ({len(html)} chars)")

    # Send
    with open('/tmp/subs.json') as f: subs = json.load(f)
    ok = 0; fail = 0
    for i, r in enumerate(subs, 1):
        email = r['email']
        payload = {
            "from": "Consumer Safari <briefing@consumersafari.com>",
            "to": [email],
            "subject": "Consumer Safari Daily Brief -- April 24, 2026",
            "html": html,
        }
        result = subprocess.run(
            ['curl', '-s', '-X', 'POST', 'https://api.resend.com/emails',
             '-H', 'Authorization: Bearer <RESEND_API_KEY_ENV>',
             '-H', 'Content-Type: application/json',
             '-d', json.dumps(payload)],
            capture_output=True, text=True
        )
        try:
            resp = json.loads(result.stdout)
            if resp.get('id'): ok += 1
            else:
                fail += 1
                print(f"FAIL {email}: {result.stdout[:200]}")
        except Exception as e:
            fail += 1
            print(f"EXC {email}: {e}")
        if i % 10 == 0:
            print(f"{i}/{len(subs)} sent — ok={ok} fail={fail}")
        time.sleep(0.5)
    print(f"\nFinal: ok={ok} fail={fail} of {len(subs)}")
