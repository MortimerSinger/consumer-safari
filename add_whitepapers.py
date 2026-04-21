#!/usr/bin/env python3
"""
Script to add the White Papers tab to index.html
"""
import re
import json

FILE = '/home/user/workspace/morning-briefing/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"File loaded: {len(html)} chars")

# ============================================================
# STEP 1: Add tab button after Voices tab button
# ============================================================
OLD_TAB_BTN = '<button class="tab-btn" role="tab" aria-selected="false" aria-controls="panel-voices" data-tab="voices">Voices</button>'
NEW_TAB_BTN = OLD_TAB_BTN + '\n        <button class="tab-btn" role="tab" aria-selected="false" aria-controls="panel-whitepapers" data-tab="whitepapers">White Papers</button>'

assert OLD_TAB_BTN in html, "Could not find Voices tab button!"
html = html.replace(OLD_TAB_BTN, NEW_TAB_BTN, 1)
print("Step 1 done: Tab button added")

# ============================================================
# STEP 2: Add the White Papers section/panel after panel-voices
# ============================================================
OLD_PANEL_CLOSE = '''      <section class="tab-panel" id="panel-voices" role="tabpanel" aria-labelledby="tab-voices">
        <div class="search-results-panel" id="searchResults-voices"></div>
        <div class="section-label" style="margin-bottom:var(--space-2);">Voices</div>
        <div id="voicesContainer"></div>
      </section>
    </main>'''

NEW_PANEL = '''      <section class="tab-panel" id="panel-voices" role="tabpanel" aria-labelledby="tab-voices">
        <div class="search-results-panel" id="searchResults-voices"></div>
        <div class="section-label" style="margin-bottom:var(--space-2);">Voices</div>
        <div id="voicesContainer"></div>
      </section>

      <section class="tab-panel" id="panel-whitepapers" role="tabpanel" aria-labelledby="tab-whitepapers">
        <div class="section-header">WHITE PAPERS</div>
        <div id="whitepapersContainer"></div>
      </section>
    </main>'''

assert OLD_PANEL_CLOSE in html, "Could not find panel-voices closing section!"
html = html.replace(OLD_PANEL_CLOSE, NEW_PANEL, 1)
print("Step 2 done: White Papers panel added")

# ============================================================
# STEP 3: Add whitePapers data to DATA object
# ============================================================
white_papers_data = [
    {
        "title": "The Digital Recoil",
        "subtitle": "& The Analog Enthusiast Economy",
        "oneLine": "The brands compounding most reliably across consumer share five structural signatures. A new paper from Traub Capital.",
        "author": "Mortimer Singer, Managing Partner, Traub Capital Partners",
        "date": "April 2026",
        "sortDate": "2026-04-22",
        "slug": "digital-recoil",
        "landingUrl": "/white-papers/digital-recoil",
        "pdfUrl": "/digital-recoil.pdf",
        "thumb": "/digital-recoil-thumb.jpg",
        "series": "Consumer Signal Series · Paper No. 1"
    }
]

# Find and parse DATA object
m = re.search(r'(const DATA = )(\{.*?\})(;\s*\n)', html, re.DOTALL)
assert m, "Could not find DATA variable!"

data_prefix = m.group(1)
data_str = m.group(2)
data_suffix = m.group(3)

data = json.loads(data_str)
data['whitePapers'] = white_papers_data

new_data_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
html = html[:m.start()] + data_prefix + new_data_str + data_suffix + html[m.end():]
print(f"Step 3 done: whitePapers data added (DATA is now {len(new_data_str)} chars)")

# ============================================================
# STEP 4: Add CSS for white paper cards (insert before VOICES TAB CSS comment)
# ============================================================
VOICES_CSS_COMMENT = '''    /* ============================================================
       VOICES TAB
       ============================================================ */'''

WHITE_PAPERS_CSS = '''    /* ============================================================
       WHITE PAPERS TAB
       ============================================================ */
    .whitepaper-card {
      display: grid;
      grid-template-columns: 120px 1fr;
      gap: 20px;
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 16px;
      align-items: start;
    }
    @media (max-width: 540px) {
      .whitepaper-card { grid-template-columns: 80px 1fr; gap: 14px; padding: 16px; }
    }
    .whitepaper-thumb {
      width: 120px;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(109,40,217,0.15);
      display: block;
    }
    @media (max-width: 540px) { .whitepaper-thumb { width: 80px; } }
    .whitepaper-body {}
    .whitepaper-series {
      font-size: 11px;
      font-weight: 700;
      color: var(--color-accent);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    .whitepaper-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--color-text);
      line-height: 1.2;
      margin: 0 0 4px;
      letter-spacing: -0.01em;
    }
    .whitepaper-subtitle {
      font-size: 15px;
      font-style: normal;
      color: var(--color-text-muted);
      margin: 0 0 12px;
    }
    .whitepaper-oneline {
      font-size: 15px;
      line-height: 1.5;
      color: var(--color-text);
      margin: 0 0 10px;
    }
    .whitepaper-meta {
      font-size: 13px;
      color: var(--color-text-muted);
      margin-bottom: 16px;
    }
    .whitepaper-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }
    .whitepaper-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 8px;
      text-decoration: none;
      cursor: pointer;
      font-family: inherit;
      border: 1.5px solid transparent;
    }
    .whitepaper-btn.primary { background: var(--color-accent); color: white; }
    .whitepaper-btn.primary:hover { background: var(--color-accent-dark, #5B21B6); }
    .whitepaper-btn.secondary { background: transparent; color: var(--color-accent); border-color: var(--color-accent); }
    .whitepaper-btn.secondary:hover { background: var(--color-accent-tint, #F5F3FF); }

    /* ============================================================
       VOICES TAB
       ============================================================ */'''

assert VOICES_CSS_COMMENT in html, "Could not find VOICES TAB CSS comment!"
html = html.replace(VOICES_CSS_COMMENT, WHITE_PAPERS_CSS, 1)
print("Step 4 done: White Papers CSS added")

# ============================================================
# STEP 5: Add renderWhitePapers() JS function (insert after saveVoiceItem function)
# ============================================================
# Find saveVoiceItem function end and FEED FILTER comment
AFTER_SAVE_VOICE = '''    /* ============================================
       FEED FILTER (Consumer / AI / Both)
       ============================================ */'''

RENDER_WHITE_PAPERS_JS = '''    function renderWhitePapers() {
      var container = document.getElementById('whitepapersContainer');
      if (!container) return;
      var papers = DATA.whitePapers || [];
      if (papers.length === 0) {
        container.innerHTML = '<div style="padding:24px;text-align:center;color:var(--color-text-muted);">Papers coming soon.</div>';
        return;
      }
      papers = papers.slice().sort(function(a,b){
        return (b.sortDate || '').localeCompare(a.sortDate || '');
      });
      container.innerHTML = papers.map(function(p) {
        var isSaved = savedArticles.some(function(a){ return a.url === p.landingUrl; });
        var saveLabel = isSaved ? 'Saved' : 'Save';
        var saveClass = isSaved ? ' saved' : '';
        return '<div class="whitepaper-card">' +
          '<a href="' + escAttr(p.landingUrl) + '"><img class="whitepaper-thumb" src="' + escAttr(p.thumb) + '" alt="' + escAttr(p.title) + '"></a>' +
          '<div class="whitepaper-body">' +
            '<div class="whitepaper-series">' + escHtml(p.series || '') + '</div>' +
            '<h3 class="whitepaper-title">' + escHtml(p.title) + '</h3>' +
            (p.subtitle ? '<p class="whitepaper-subtitle">' + escHtml(p.subtitle) + '</p>' : '') +
            '<p class="whitepaper-oneline">' + escHtml(p.oneLine || '') + '</p>' +
            '<div class="whitepaper-meta">' + escHtml(p.author || '') + ' · ' + escHtml(p.date || '') + '</div>' +
            '<div class="whitepaper-actions">' +
              '<a class="whitepaper-btn primary" href="' + escAttr(p.landingUrl) + '">Read Paper \u2192</a>' +
              '<a class="whitepaper-btn secondary" href="' + escAttr(p.pdfUrl) + '" download>Download PDF</a>' +
              '<button class="whitepaper-btn secondary voice-save-btn' + saveClass + '" onclick="saveWhitePaper(this, \'' + escAttr(p.landingUrl).replace(/\x27/g, '\\x27') + '\', \'' + escAttr(p.title).replace(/\x27/g, '\\x27') + '\')">' + saveLabel + '</button>' +
            '</div>' +
          '</div>' +
        '</div>';
      }).join('');
    }

    function saveWhitePaper(btn, url, title) {
      if (typeof _saveArticle === 'function') {
        _saveArticle({ title: title, url: url, source: 'Traub Capital Partners', tag: 'White Paper', excerpt: 'TCP white paper' });
      } else if (typeof toggleBookmark === 'function') {
        toggleBookmark({ title: title, url: url, source: 'Traub Capital Partners', tag: 'White Paper' });
      }
      btn.textContent = 'Saved';
      btn.classList.add('saved');
    }

    /* ============================================
       FEED FILTER (Consumer / AI / Both)
       ============================================ */'''

assert AFTER_SAVE_VOICE in html, "Could not find FEED FILTER comment!"
html = html.replace(AFTER_SAVE_VOICE, RENDER_WHITE_PAPERS_JS, 1)
print("Step 5 done: renderWhitePapers() JS function added")

# ============================================================
# STEP 6: Wire tab into switchTab function
# ============================================================
# 6a: Add renderWhitePapers() call in switchTab
OLD_SWITCH = "      if (tabName === 'voices') { renderVoices(); }"
NEW_SWITCH = "      if (tabName === 'voices') { renderVoices(); }\n      if (tabName === 'whitepapers') { renderWhitePapers(); }"

assert OLD_SWITCH in html, "Could not find voices switchTab line!"
html = html.replace(OLD_SWITCH, NEW_SWITCH, 1)
print("Step 6a done: renderWhitePapers() call in switchTab added")

# 6b: Add 'whitepapers' to the valid array in handleHash (but NOT to showToggle feedToggleBar array)
OLD_VALID = "      const valid = ['forme', 'today', 'week', 'month', 'listen', 'deepread', 'deals', 'events', 'saved', 'voices'];"
NEW_VALID = "      const valid = ['forme', 'today', 'week', 'month', 'listen', 'deepread', 'deals', 'events', 'saved', 'voices', 'whitepapers'];"

assert OLD_VALID in html, "Could not find valid tabs array!"
html = html.replace(OLD_VALID, NEW_VALID, 1)
print("Step 6b done: 'whitepapers' added to valid tabs array")

# ============================================================
# Write out the modified file
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nAll done! File written: {len(html)} chars")
