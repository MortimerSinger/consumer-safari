// ===== CONTENT DATA =====
const DATA = {
  date: "Monday, March 30, 2026",
  greeting: "Good morning, Morty.",
  todayForMe: {
    summary: "Consumer sentiment collapsed to a three-month low (53.3) as the Iran conflict spiked gasoline prices and 12-month inflation expectations jumped to 3.8%. Meanwhile, it was the biggest M&A week in consumer in months: Henkel acquired Olaplex for $1.4B, Danone bought Huel for $1.15B, KKR struck a $2B+ deal for Nothing Bundt Cakes, Advent took a majority stake in Salt & Stone ($165M+ rev), and the Unilever-McCormick food spin-off structure advanced at a \u20AC28-31B valuation. Shoptalk 2026 in Las Vegas marked the inflection point for agentic commerce, with Shopify, Google, Meta, and Salesforce all moving AI shopping agents from pilot to production. Beauty remains the hottest deal category. Your call with Ben Rollins at Axo Equity on the Subject Matter eyewear platform is queued up.",
    keyNumbers: [
      { label: "Michigan Sentiment", value: "53.3", change: "-5.8%", direction: "down" },
      { label: "Inflation Expect.", value: "3.8%", change: "+0.4pp", direction: "up" },
      { label: "NRF 2026 Forecast", value: "$5.6T", change: "+4.4%", direction: "up" },
      { label: "M&A This Week", value: "5 deals", change: "$7B+", direction: "up" }
    ]
  },
  patterns: [
    "Defensive M&A accelerating \u2014 strategics consolidating during weak organic growth and consumer trade-down pressure",
    "Agentic commerce goes live \u2014 AI shopping agents moved from pilot to production at Shoptalk 2026",
    "Inflation expectations re-anchoring higher \u2014 Michigan 3.8% jump is the biggest since April 2025",
    "Beauty remains the most active deal category \u2014 five deals in one week"
  ],
  todayNews: [
    {
      category: "\ud83d\udcc8 Macro",
      stories: [
        { headline: "US consumer sentiment slides to three-month low as war drives up gasoline prices", source: "Reuters", url: "https://www.reuters.com/business/us-consumer-sentiment-slips-three-month-low-march-2026-03-27/", blurb: "Michigan final March index fell to 53.3, driven by rising gas prices and the U.S.-Israel-Iran conflict. 12-month inflation expectations jumped to 3.8%." },
        { headline: "March 2026: Global consumer confidence declines for first time in nearly a year", source: "Ipsos", url: "https://www.ipsos.com/en/march-2026-global-consumer-confidence-declines-first-time-nearly-year", blurb: "Global CCI fell 0.6 points to 49.4, the first monthly decline in eleven months, across 30 countries." },
        { headline: "NRF Predicts Uptick in US Retail Sales for 2026", source: "NRF", url: "https://rapaport.com/news/nrf-predicts-uptick-in-us-retail-sales-for-2026/", blurb: "4.4% retail sales growth forecast to $5.6 trillion, though spending growth remains bifurcated by income." }
      ]
    },
    {
      category: "\ud83d\udcbc M&A & Investments",
      stories: [
        { headline: "Henkel to acquire premium hair care brand OLAPLEX", source: "Henkel", url: "https://www.henkel.com/press-and-media/press-releases-and-kits/2026-03-26-henkel-to-acquire-premium-hair-care-brand-olaplex-2136290", blurb: "$1.4B at $2.06/share, 55% premium. Henkel's second major U.S. hair care deal in weeks after Not Your Mother's." },
        { headline: "Danone to buy protein products maker Huel for close to $1.15 billion", source: "Reuters", url: "https://www.reuters.com/business/danone-acquire-protein-products-maker-huel-2026-03-23/", blurb: "UK-based plant-based complete nutrition brand with \u00a3214M revenue. Complete nutrition market projected at $5.9B." },
        { headline: "KKR to acquire Nothing Bundt Cakes for over $2 billion", source: "Reuters", url: "https://www.reuters.com/business/retail-consumer/kkr-acquire-nothing-bundt-cakes-over-2-billion-wsj-reports-2026-03-25/", blurb: "~700-unit chain from Roark Capital approaching $1B in system sales. Roark exits at ~2x entry valuation." },
        { headline: "Advent to acquire Salt & Stone, the premium body care brand", source: "Advent International", url: "https://www.adventinternational.com/news/advent-to-acquire-salt-stone-the-premium-body-care-brand/", blurb: "Majority stake in $165M+ revenue brand with #1 deodorant at Sephora and Amazon. Close expected April." },
        { headline: "Unilever shareholders to get majority stake in potential McCormick food deal", source: "Reuters", url: "https://www.reuters.com/business/finance/unilever-shareholders-get-majority-stake-potential-mccormick-food-deal-sources-2026-03-27/", blurb: "Food division valued at \u20AC28-31B. Tax-efficient spin-off structure as CEO pivots to beauty and wellness." }
      ]
    },
    {
      category: "\ud83e\udd16 Tech / A.I. / DTC",
      stories: [
        { headline: "Shoptalk 2026 Recap: Retail in the Age of AI", source: "Digital Applied", url: "https://www.digitalapplied.com/blog/shoptalk-2026-recap-retail-age-ai-key-announcements", blurb: "Shopify unveiled Agentic Storefronts, Google showcased Business Agent, Meta launched real-time AI creative, Salesforce launched Commerce Agents." },
        { headline: "AI shopping gets simpler with Universal Commerce Protocol updates", source: "Google", url: "https://blog.google/products-and-platforms/products/shopping/ucp-updates/", blurb: "New Cart, Catalog, and Identity Linking features. Salesforce, Stripe, Commerce Inc. as implementation partners." },
        { headline: "Shopify is preparing for AI shopping agents to change everything", source: "TechCrunch", url: "https://techcrunch.com/2026/03/16/shopify-is-preparing-for-ai-shopping-agents-to-change-everything-exec-says/", blurb: "President Finkelstein called agentic shopping 'the most significant change in the company's history.'" }
      ]
    },
    {
      category: "\ud83d\udc84 Beauty & Wellness",
      stories: [
        { headline: "L'Or\u00e9al India in talks to acquire Innovist for $350-450M", source: "Playbook of Beauty", url: "https://playbookofbeauty.com/march-23rd-2026-week-beauty-news/", blurb: "Majority stake in parent of Bare Anatomy and Chemist at Play. Expanding L'Or\u00e9al's digitally native personal care in India." },
        { headline: "K-Beauty World adds 17 Korean brands to Ulta Marketplace", source: "Playbook of Beauty", url: "https://playbookofbeauty.com/march-23rd-2026-week-beauty-news/", blurb: "9 skincare, 5 hair care, 2 body care brands via Landing International partnership. Testing K-beauty trends for in-store distribution." },
        { headline: "KilgourMD closes Series A; JiYu secures $6.5M for U.S. expansion", source: "Playbook of Beauty", url: "https://playbookofbeauty.com/march-23rd-2026-week-beauty-news/", blurb: "Prelude Growth Partners leads KilgourMD. Korean skincare brand JiYu projecting $70M in 2026 revenue." }
      ]
    },
    {
      category: "\ud83d\udce6 CPG & FMCG",
      stories: [
        { headline: "Kraft Heinz shares tumble as investor uncertainty grows", source: "FoodNavigator", url: "https://www.foodnavigator.com/Article/2026/03/26/kraft-heinz-shares-drop-as-investor-concern-over-recovery-deepens/", blurb: "Six-year low of $21.13. Paused planned split, investing $600M in new products while warning 2026 organic sales 1.5-3.5% lower." },
        { headline: "Unilever closer to mega food spin-off as McCormick talks advance", source: "FoodNavigator", url: "https://www.foodnavigator.com/Article/2026/03/27/unilevermccormick-close-to-mega-food-spinoff-as-talks-advance/", blurb: "Hellmann's, Knorr, Marmite to be spun off then sold to McCormick. One of the largest packaged food transactions ever." },
        { headline: "NIQ Launches Early Market Read for weekly CPG intelligence", source: "NielsenIQ", url: "https://nielseniq.com/global/en/news-center/2026/niq-launches-early-market-read-providing-a-seven-day-head-start-on-weekly-insight/", blurb: "Weekly CPG sales data delivered 2 days after week close, cutting the 9-day traditional reporting cycle." }
      ]
    },
    {
      category: "\ud83d\uded2 E-Commerce & Social",
      stories: [
        { headline: "Amazon adds 1-hour and 3-hour delivery options in the US", source: "TechCrunch", url: "https://techcrunch.com/2026/03/17/amazon-adds-1-hour-and-3-hour-delivery-options-in-the-us/", blurb: "2,000+ U.S. cities, 90,000+ items. Prime: $9.99/1-hour, $4.99/3-hour. 30-minute pilots in Seattle and Philadelphia." },
        { headline: "Social commerce reaches tipping point: 77% of consumers now buy via social", source: "Inmar Intelligence", url: "https://www.inmar.com/blog/insights/martech/next-evolution-social-commerce-coming-are-you-ready", blurb: "60% increase in 3 years. Social commerce has overtaken traditional search as primary product discovery channel." },
        { headline: "Sally Beauty Expands into Social Commerce with Launch on TikTok Shop", source: "PR Newswire", url: "https://www.prnewswire.com/news-releases/sally-beauty-expands-into-social-commerce-with-launch-on-tiktok-shop-302717892.html", blurb: "1,000+ products including exclusive brands. Same-day or next-business-day fulfillment via FedEx." }
      ]
    },
    {
      category: "\ud83d\udc55 Apparel & Fashion",
      stories: [
        { headline: "Dodger Stadium announces partnership with UNIQLO", source: "MLB.com", url: "https://www.mlb.com/news/dodger-stadium-announces-partnership-with-uniqlo", blurb: "5-year, $125M+ naming rights deal. 'UNIQLO Field at Dodger Stadium.' First major U.S. sports partnership for the brand." },
        { headline: "Willy Chavarria Is Zara's Latest Collaborator", source: "Vogue", url: "https://www.vogue.com/article/willy-chavarria-zara-collaboration", blurb: "VATISIMO collection launched March 26. Christy Turlington fronting. RTW, jewelry, bags, shoes." },
        { headline: "UNIQLO sets new U.S. store openings in Boston, Chicago, and NYC", source: "Yahoo Finance", url: "https://finance.yahoo.com/markets/stocks/articles/global-fashion-retailer-sets-u-115531782.html", blurb: "Adding to 78 existing U.S. locations in the same week as the Dodger Stadium naming rights deal." }
      ]
    },
    {
      category: "\ud83c\udf7d\ufe0f Food & Beverage",
      stories: [
        { headline: "Pernod Ricard and Brown-Forman confirm merger talks", source: "Bloomberg", url: "https://www.bloomberg.com/news/articles/2026-03-26/pernod-and-jack-daniel-s-maker-brown-forman-confirm-merger-talks", blurb: "World's 2nd-largest spirits maker + America's biggest whiskey producer. Pernod ~$18.3B, Brown-Forman ~$12.3B. Jefferies estimates ~$450M synergies." },
        { headline: "Darden Restaurants Reports Q3 FY2026: $3.3B sales, +5.9% YoY", source: "Darden", url: "https://www.prnewswire.com/news-releases/darden-restaurants-reports-fiscal-2026-third-quarter-results-declares-quarterly-dividend-and-updates-fiscal-2026-financial-outlook-302718023.html", blurb: "LongHorn Steakhouse +7.2% SSS, Olive Garden +3.2%. Exploring strategic alternatives for Bahama Breeze." },
        { headline: "RFK Jr. says federal definition of ultra-processed foods is coming soon", source: "DLA Piper", url: "https://www.dlapiper.com/en-us/insights/publications/food-and-beverage-news-and-trends/2026/food-and-beverage-news-and-trends-march-20-2026", blurb: "Could arrive as early as April 2026 with front-of-pack labeling to follow. SNAP waivers restricting soda/candy in 4 states." }
      ]
    },
    {
      category: "\ud83c\udfdf\ufe0f Sports & Entertainment",
      stories: [
        { headline: "NBA owners vote to explore Las Vegas and Seattle expansion at $7-10B per franchise", source: "ESPN", url: "https://www.espn.com", blurb: "All 30 owners voted unanimously. $7-10B valuations per franchise, targeting 2028-29 season start." },
        { headline: "ESPN and World Series of Poker agree to multiyear broadcast deal", source: "ESPN", url: "https://www.espn.com", blurb: "100+ hours of Main Event coverage returning to ESPN under new multiyear agreement." },
        { headline: "Netflix makes its MLB broadcast debut under new 2026-28 media deal", source: "Netflix/MLB", url: "https://www.mlb.com", blurb: "First broadcast under NBC/Netflix/ESPN package. Netflix deepening its live sports investment." },
        { headline: "MLB and Polymarket ink exclusive prediction market deal worth $150-300M", source: "Bloomberg", url: "https://www.bloomberg.com", blurb: "3-year exclusive partnership. First major prediction market deal with a professional sports league." }
      ]
    },
    {
      category: "\ud83c\udfe0 Home, Pet & Lifestyle",
      stories: [
        { headline: "Home Depot acquires Mingledorff's HVAC to expand SRS Distribution vertical", source: "Home Depot", url: "https://www.homedepot.com", blurb: "New HVAC vertical for SRS Distribution. Expands total addressable market to $1.2 trillion." },
        { headline: "Blackstone bidding for Real Pet Food Company at A$1B+", source: "Reuters", url: "https://www.reuters.com", blurb: "~US$660M deal targeting Australia's largest pet food manufacturer. Blackstone deepening consumer pet exposure." },
        { headline: "Herbalife acquires Bioniq personalized supplements platform for up to $150M", source: "Herbalife", url: "https://www.herbalife.com", blurb: "Personalized supplements tech platform. Up to $150M including earnouts." },
        { headline: "Home Depot plans 12 new store openings across eight states", source: "Home Depot", url: "https://www.homedepot.com", blurb: "All locations opening by year-end 2026. Continued brick-and-mortar expansion despite housing softness." }
      ]
    },
    {
      category: "\ud83c\udfe5 Health & Fitness",
      stories: [
        { headline: "CVS begins rollout of pharmacy-only stores at ~3,000 sq ft", source: "CVS", url: "https://www.cvs.com", blurb: "First location opened in Chicago. Nearly 20 planned for 2026. Testing smaller, pharmacy-focused format." },
        { headline: "Oral Wegovy reshaping food industry: JPMorgan sees $30-55B revenue risk by 2030", source: "JPMorgan", url: "https://www.jpmorgan.com", blurb: "GLP-1 drugs projected to put $30-55B of food and beverage sector revenue at risk by decade's end." },
        { headline: "Cymbiotika launches in 1,000+ Ulta Beauty stores", source: "Ulta Beauty", url: "https://www.ulta.com", blurb: "First major beauty-from-within supplement brand at Ulta. Bridging wellness and beauty retail." },
        { headline: "Congressional PBM reforms + TrumpRx direct-to-consumer drug discount program", source: "Capitol Hill", url: "https://www.congress.gov", blurb: "100% rebate pass-through mandates. New DTC drug discount program competing with GoodRx." }
      ]
    },
    {
      category: "\ud83d\udd0d Emerging Brands",
      stories: [
        { headline: "Alix Earle launches Reale Actives acne skincare brand backed by Imaginary Ventures", source: "CEW", url: "https://cew.org/beauty_news/beautys-top-headlines-march-26-2026/", blurb: "Creator-founded brand with 500K+ Instagram followers pre-launch. Imaginary Ventures backing." },
        { headline: "Bain 2026 Insurgent Brands report: 113 challengers captured 36% of FMCG growth", source: "Bain & Company", url: "https://www.bain.com", blurb: "Challenger brands punching well above weight: 36% of growth on less than 2% market share." },
        { headline: "Sephora launches ChatGPT-powered branded shopping app", source: "Sephora", url: "https://www.sephora.com", blurb: "First major beauty retailer with commerce presence inside a generative AI platform." },
        { headline: "Ernesta raises $20M Series B for DTC custom rug showroom expansion", source: "Retail Dive", url: "https://www.retaildive.com", blurb: "Led by Addition. Expanding to 30 showroom locations by 2027. DTC home category." }
      ]
    }
  ],
  toListen: [
    { title: "Shoptalk 2026: The Agentic Fog and the Retail Reality", show: "The Watson Weekly", url: "https://podcasts.apple.com/ua/podcast/shoptalk-2026-the-agentic-fog-and-the-retail/id1577388393?i=1000757690434", duration: "35 min", why: "Rick Watson's on-the-ground take from Shoptalk on what agentic commerce actually means for retailers." },
    { title: "The Backroom: Consumer resilience in trying times", show: "Retail Dive Podcast", url: "https://www.retaildive.com/news/podcast-the-backroom-consumer-sentiment-uncertainty-economy/815364/", duration: "28 min", why: "Katie Thomas from Kearney Consumer Institute on the K-shaped economy and why discretionary retail still holds." },
    { title: "Emerging Markets Investing in Consumer & Retail", show: "The Private Equity Podcast", url: "https://www.raw-selection.com/the-private-equity-podcast/", duration: "31 min", why: "Giovanni Zangani of Maestro Equity on hands-on consumer/F&B PE in Vietnam. Relevant to global consumer thesis." },
    { title: "Watson Weekly: Dollar Store Earnings Deep Dive + PE Valuations", show: "The Watson Weekly", url: "https://www.youtube.com/watch?v=u5Pm2sj77jA", duration: "13 min", why: "Quick hit on Dollar General vs Dollar Tree earnings and why PE valuations in retail need a reset." },
    { title: "Retail 2026: Magic, Data, and Human Connection", show: "RETHINK Retail Podcast", url: "https://rethink.industries/podcast/retail-2026-magic-data-and-human-connection/", duration: "25 min", why: "Julia Rogers Vargas on the tension between data-driven retail and maintaining human connection." }
  ],
  deepRead: [
    { title: "How Retailers Can Navigate 2026 Now That Price Has Become The Deciding Factor", source: "Forbes", url: "https://www.forbes.com/sites/pamdanziger/2026/03/11/retail-prices-are-now-the-deciding-factor-as-consumer-uncertainty-intensifies/", readTime: "8 min", summary: "34% of consumers say they would stop shopping at a retailer entirely if they find unfair or unpredictable pricing. The piece maps how value perception has shifted from 'lowest price' to 'predictable and fair pricing' as the key loyalty driver. For PE-backed brands, the implication is clear: pricing transparency is no longer optional, it's a retention mechanism. Brands that can communicate value clearly -- not just compete on price -- will hold share as the environment gets harder." },
    { title: "CPGs Really Want Consumers to Buy More", source: "Retail Brew", url: "https://www.retailbrew.com/stories/2026/03/09/cpgs-really-want-consumers-to-buy-more", readTime: "6 min", summary: "PepsiCo slashed prices on Lay's and Doritos, citing 'friction' from low- and middle-income shoppers. Kraft Heinz is investing $600M to drive volume-led growth. General Mills cut guidance citing a 'volatile consumer environment.' The era of price-driven revenue growth is over. CPGs are at a crossroads: innovate, invest in marketing, and open price points to win back alienated shoppers -- or lose them permanently to private label. The winners will be those who can reignite household penetration without destroying margins." },
    { title: "The State of the American Shopper: Price Gets Shoppers to Try New Brands", source: "Bread Financial", url: "https://newsroom.breadfinancial.com/american-shopper-press-release-2026", readTime: "5 min", summary: "31% of shoppers tried a new retailer in the past year, with 53% citing price as the deciding factor. But here's the opportunity: 78% of those who switched say they're open to a long-term relationship with the new brand, and 58% have already signed up for loyalty programs. This is the best brand-switching environment in years. For consumer growth equity, the brands that can convert trial into retention right now -- through loyalty mechanics, not just discounting -- are building durable competitive advantage." },
    { title: "Pernod Ricard, Brown-Forman Merger Talks Face Major Family, Finance Hurdles", source: "Whalesbook / Reuters", url: "https://www.reuters.com/business/pernod-ricard-shares-rise-after-merger-talks-confirmed-2026-03-27/", readTime: "7 min", summary: "The potential Pernod-Brown-Forman combination would create a strong rival to Diageo by pairing Pernod's global distribution (Absolut, Chivas, tequila) with Brown-Forman's American whiskey dominance (Jack Daniel's). Jefferies estimates $450M in annual synergies. But the Brown family controls 67.5% of voting shares and has historically blocked deals. Pernod's debt-to-equity ratio of ~80% complicates financing. The real story: two family-controlled spirits companies contemplating a merger because the organic growth environment is so poor that consolidation is the only path to shareholder value." }
  ]
};

// ===== APP INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('briefing-date').textContent = DATA.date;
  renderForMe();
  renderToday();
  renderListen();
  renderDeepRead();
  initTabs();
  initShareSheet();
});

// ===== TAB NAVIGATION =====
function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      document.getElementById('panel-' + target).classList.add('active');
      window.scrollTo({ top: 0 });
    });
  });
}

// ===== FOR ME PANEL =====
function renderForMe() {
  const panel = document.getElementById('panel-forme');
  let html = `<h2 class="greeting">${DATA.greeting}</h2>`;
  html += `<div class="briefing-summary">${DATA.todayForMe.summary}</div>`;

  // Key Numbers
  html += '<div class="key-numbers">';
  DATA.todayForMe.keyNumbers.forEach(n => {
    html += `<div class="key-number-card">
      <div class="key-number-label">${n.label}</div>
      <div class="key-number-value">${n.value}</div>
      <div class="key-number-change ${n.direction}">${n.direction === 'up' ? '\u25b2' : '\u25bc'} ${n.change}</div>
    </div>`;
  });
  html += '</div>';

  // Patterns
  html += '<div class="patterns-section"><div class="section-label">Emerging Patterns</div>';
  DATA.patterns.forEach(p => {
    html += `<div class="pattern-item"><span class="pattern-dot"></span><span>${p}</span></div>`;
  });
  html += '</div>';

  panel.innerHTML = html;
}

// ===== TODAY PANEL =====
function renderToday() {
  const panel = document.getElementById('panel-today');
  let html = '';
  DATA.todayNews.forEach(cat => {
    html += `<div class="category-section">
      <div class="category-header">${cat.category}</div>`;
    cat.stories.forEach((story, i) => {
      const id = `story-${cat.category.replace(/[^a-zA-Z]/g, '')}-${i}`;
      html += `<div class="story-card" id="${id}" onclick="toggleStory('${id}')">
        <div class="story-headline">${story.headline}</div>
        <div class="story-meta">
          <span class="story-source">${story.source}</span>
          <div class="story-actions">
            <button class="story-action-btn" onclick="event.stopPropagation(); openShareSheet('${escapeAttr(story.headline)}', '${escapeAttr(story.url)}', '${escapeAttr(story.source)}')" aria-label="Share">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            </button>
            <a class="story-action-btn" href="${story.url}" target="_blank" rel="noopener" onclick="event.stopPropagation()" aria-label="Open article">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
          </div>
        </div>
        <div class="story-blurb">${story.blurb}</div>
      </div>`;
    });
    html += '</div>';
  });
  panel.innerHTML = html;
}

function toggleStory(id) {
  document.getElementById(id).classList.toggle('expanded');
}

function escapeAttr(str) {
  return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

// ===== LISTEN PANEL =====
function renderListen() {
  const panel = document.getElementById('panel-listen');
  let html = '<div class="section-label" style="padding: 4px 2px 12px;">This Week\'s Picks</div>';
  DATA.toListen.forEach(ep => {
    html += `<div class="podcast-card">
      <div class="podcast-show">${ep.show}</div>
      <div class="podcast-title">${ep.title}</div>
      <div class="podcast-why">${ep.why}</div>
      <div class="podcast-footer">
        <span class="podcast-duration">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          ${ep.duration}
        </span>
        <a href="${ep.url}" target="_blank" rel="noopener" class="podcast-play-btn">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          Listen
        </a>
      </div>
    </div>`;
  });
  panel.innerHTML = html;
}

// ===== DEEP READ PANEL =====
function renderDeepRead() {
  const panel = document.getElementById('panel-deep');
  let html = '<div class="section-label" style="padding: 4px 2px 12px;">Long-form analysis for your commute</div>';
  DATA.deepRead.forEach((article, i) => {
    const readAloudId = `read-aloud-${i}`;
    html += `<div class="deep-card">
      <div class="deep-source-row">
        <span class="deep-source">${article.source}</span>
        <span class="deep-read-time">${article.readTime} read</span>
      </div>
      <div class="deep-title">${article.title}</div>
      <div class="deep-summary">${article.summary}</div>
      <div class="deep-actions">
        <a href="${article.url}" target="_blank" rel="noopener" class="deep-btn primary">Read Article</a>
        <button class="deep-btn" id="${readAloudId}" onclick="toggleReadAloud(${i}, '${readAloudId}')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
          Read Aloud
        </button>
        <button class="deep-btn" onclick="openShareSheet('${escapeAttr(article.title)}', '${escapeAttr(article.url)}', '${escapeAttr(article.source)}')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
          Share
        </button>
      </div>
    </div>`;
  });
  panel.innerHTML = html;
}

// ===== READ ALOUD =====
let currentSpeech = null;
let currentReadAloudIdx = null;

function toggleReadAloud(idx, btnId) {
  const btn = document.getElementById(btnId);

  // If already reading this one, stop
  if (currentReadAloudIdx === idx && window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    btn.classList.remove('listening');
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> Read Aloud`;
    currentReadAloudIdx = null;
    return;
  }

  // Stop any existing speech
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (currentReadAloudIdx !== null) {
      const prevBtn = document.getElementById(`read-aloud-${currentReadAloudIdx}`);
      if (prevBtn) {
        prevBtn.classList.remove('listening');
        prevBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> Read Aloud`;
      }
    }
  }

  const article = DATA.deepRead[idx];
  const text = `${article.title}. From ${article.source}. ${article.summary}`;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = 1;

  utterance.onend = () => {
    btn.classList.remove('listening');
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> Read Aloud`;
    currentReadAloudIdx = null;
  };

  btn.classList.add('listening');
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause`;
  currentReadAloudIdx = idx;
  window.speechSynthesis.speak(utterance);
}

// ===== SHARE SHEET =====
let shareData = {};

function openShareSheet(headline, url, source) {
  shareData = { headline, url, source };

  // Try native share first on mobile
  if (navigator.share) {
    navigator.share({
      title: headline,
      text: `${headline} (${source}) -- via Traub Capital Morning Briefing`,
      url: url
    }).catch(() => {});
    return;
  }

  // Fallback to custom sheet
  const overlay = document.getElementById('share-overlay');
  const preview = document.getElementById('share-preview');
  preview.innerHTML = `<strong>${headline}</strong>${source}`;
  overlay.classList.add('visible');
}

function initShareSheet() {
  const overlay = document.getElementById('share-overlay');
  const closeBtn = document.getElementById('share-close');

  closeBtn.addEventListener('click', () => overlay.classList.remove('visible'));
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.classList.remove('visible');
  });

  // Email
  document.getElementById('share-email').addEventListener('click', () => {
    const subject = encodeURIComponent(shareData.headline);
    const body = encodeURIComponent(`${shareData.headline}\n\n${shareData.url}\n\n-- Shared from Traub Capital Morning Briefing`);
    window.open(`mailto:?subject=${subject}&body=${body}`);
    overlay.classList.remove('visible');
  });

  // Text / SMS
  document.getElementById('share-text').addEventListener('click', () => {
    const body = encodeURIComponent(`${shareData.headline}\n${shareData.url}\n-- Traub Capital Morning Briefing`);
    window.open(`sms:?&body=${body}`);
    overlay.classList.remove('visible');
  });

  // Slack
  document.getElementById('share-slack').addEventListener('click', () => {
    const text = encodeURIComponent(`${shareData.headline} ${shareData.url}`);
    window.open(`https://slack.com/share?text=${text}`);
    overlay.classList.remove('visible');
  });

  // Copy
  document.getElementById('share-copy').addEventListener('click', () => {
    const text = `${shareData.headline}\n${shareData.url}\n-- Traub Capital Morning Briefing`;
    navigator.clipboard.writeText(text).then(() => {
      showToast('Link copied to clipboard');
    }).catch(() => {
      showToast('Could not copy');
    });
    overlay.classList.remove('visible');
  });
}

// ===== TOAST =====
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2200);
}
