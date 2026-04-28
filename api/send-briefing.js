// /api/send-briefing.js
// Vercel Serverless Function — autonomous email sender for Consumer Safari.
//
// USAGE:
//   POST /api/send-briefing
//   Headers:
//     Authorization: Bearer <CRON_SECRET>
//     Content-Type: application/json
//   Body: email_data JSON (same schema as build_email_template.py)
//   Optional: ?dry_run=1 → renders + validates only, does not send
//
// ENV VARS (set in Vercel Dashboard → Project → Settings → Environment Variables):
//   RESEND_API_KEY              — production Resend API key
//   SUPABASE_SERVICE_ROLE_KEY   — to fetch subscriber list
//   CRON_SECRET                 — shared secret the cron sends in Authorization header
//
// SECURITY:
//   - Requires Authorization: Bearer <CRON_SECRET>. Without it, returns 401.
//   - Returns 401 (not 403) on missing/wrong CRON_SECRET to avoid leaking endpoint existence.
//   - Sanity-checks rendered HTML for Python-dict debug strings before sending.
//   - On any failure, returns structured error JSON instead of silently succeeding.

const SUPABASE_URL = 'https://ugmirwqwlggdemwklcwi.supabase.co';

// ============================================
//  RENDERING — mirrors build_email_template.py
// ============================================

function renderKeyNumber(kn) {
  const arrow = kn.direction === 'down' ? '↓' : '↑';
  const color = kn.direction === 'down' ? '#DC2626' : '#059669';
  return `
<td width="50%" style="padding:10px;vertical-align:top;">
  <div style="background:#F9FAFB;border-radius:10px;padding:14px 16px;border:1px solid #E5E7EB;">
    <div style="font-size:11px;font-weight:600;color:#6B7280;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">${escapeHtml(kn.label)}</div>
    <div style="font-size:24px;font-weight:800;color:#111827;line-height:1.1;">${escapeHtml(kn.value)} <span style="color:${color};font-size:18px;">${arrow}</span></div>
    <div style="font-size:13px;color:#6B7280;margin-top:4px;">${escapeHtml(kn.change)}</div>
  </div>
</td>`;
}

function renderStory(item) {
  return `
<div style="margin-bottom:18px;">
  <a href="${escapeAttr(item.u)}" style="text-decoration:none;color:#111827;">
    <div style="font-size:19px;font-weight:700;color:#111827;line-height:1.25;margin-bottom:6px;">${escapeHtml(item.h)}</div>
  </a>
  <div style="font-size:13px;color:#6D28D9;font-weight:600;margin-bottom:6px;">${escapeHtml(item.s)}</div>
  <div style="font-size:17px;color:#374151;line-height:1.5;">${escapeHtml(item.b)}</div>
</div>`;
}

function renderCategory(group) {
  if (!group || typeof group !== 'object') {
    throw new Error(`Bad category group: ${JSON.stringify(group)}`);
  }
  if (typeof group.cat !== 'string') {
    throw new Error(`category 'cat' must be a string, got: ${typeof group.cat}`);
  }
  if (!Array.isArray(group.items)) {
    throw new Error(`category 'items' must be an array`);
  }
  const stories = group.items.map(renderStory).join('');
  return `
<div style="margin-bottom:28px;">
  <div style="font-size:14px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #EDE9FE;">${escapeHtml(group.cat)}</div>
  ${stories}
</div>`;
}

function renderBanner(banner) {
  if (!banner) return '';
  const palettes = {
    warning: { bg: '#FEF3C7', border: '#D97706', label: '#92400E', body: '#78350F' },
    info:    { bg: '#F5F3FF', border: '#6D28D9', label: '#6D28D9', body: '#1F2937' },
  };
  const p = palettes[banner.kind] || palettes.info;
  return `
<div style="background:${p.bg};border-left:4px solid ${p.border};padding:14px 18px;margin:0 0 20px 0;border-radius:4px;">
  <div style="font-size:12px;font-weight:700;color:${p.label};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">${escapeHtml(banner.title || '')}</div>
  <div style="font-size:15px;color:${p.body};line-height:1.5;">${escapeHtml(banner.body || '')}</div>
</div>`;
}

function buildEmail(data) {
  const required = ['date', 'subject', 'brief', 'key_numbers', 'consumer_stories', 'ai_stories'];
  for (const k of required) {
    if (!(k in data)) throw new Error(`Missing required key: ${k}`);
  }

  // Render key numbers in 2x2 grid
  const knRows = [];
  for (let i = 0; i < data.key_numbers.length; i += 2) {
    const row = data.key_numbers.slice(i, i + 2).map(renderKeyNumber).join('');
    knRows.push(`<tr>${row}</tr>`);
  }
  const keyNumbersHtml = `<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:separate;margin:8px -10px 18px;">${knRows.join('')}</table>`;

  const consumerHtml = (data.consumer_stories || []).map(renderCategory).join('');
  const aiHtml = (data.ai_stories || []).map(renderCategory).join('');
  const bannerHtml = renderBanner(data.banner);

  return `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F9FAFB;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<div style="max-width:600px;margin:0 auto;background:#FFFFFF;padding:28px;">

  <div style="text-align:center;padding-bottom:20px;border-bottom:1px solid #E5E7EB;">
    <div style="font-size:28px;font-weight:900;color:#6D28D9;letter-spacing:2px;">CONSUMER SAFARI</div>
    <div style="font-size:12px;font-weight:600;color:#6B7280;letter-spacing:2px;margin-top:4px;">THE MORNING BRIEFING</div>
    <div style="font-size:14px;color:#6B7280;margin-top:12px;">${escapeHtml(data.date)}</div>
    <div style="font-size:14px;margin-top:8px;"><a href="https://www.consumersafari.com" style="color:#6D28D9;text-decoration:underline;font-weight:600;">To save articles and more, go to ConsumerSafari.com</a></div>
  </div>

  ${bannerHtml}

  <div style="background:#F5F3FF;border-left:4px solid #6D28D9;padding:18px 20px;margin:0 0 20px 0;border-radius:4px;">
    <div style="font-size:12px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">Your Brief</div>
    <div style="font-size:18px;color:#1F2937;line-height:1.55;">${escapeHtml(data.brief)}</div>
  </div>

  ${keyNumbersHtml}

  ${consumerHtml}

  <hr style="border:none;border-top:1px solid #E5E7EB;margin:32px 0;">
  <div style="font-size:16px;font-weight:700;color:#6D28D9;text-transform:uppercase;letter-spacing:1.5px;text-align:center;margin-bottom:24px;">AI &amp; TECHNOLOGY</div>

  ${aiHtml}

  <div style="text-align:center;margin-top:32px;padding:20px 0;">
    <a href="https://www.consumersafari.com" style="display:inline-block;background:#6D28D9;color:#FFFFFF;text-decoration:none;font-weight:700;padding:14px 32px;border-radius:8px;font-size:15px;">Read Full Briefing</a>
  </div>

  <div style="text-align:center;margin-top:28px;padding-top:20px;border-top:1px solid #E5E7EB;font-size:11px;color:#9CA3AF;letter-spacing:1px;text-transform:uppercase;">Powered by TCP Intelligence</div>

</div>
</body>
</html>`;
}

function sanityCheck(html) {
  // Catches the 2026-04-25 Python-dict-stringification bug.
  const forbidden = [
    "{'headline'", "{'category'", "'stories':", "'tag': '", "'blurb':",
    '{"headline"', '{"category"', '"stories":',
  ];
  for (const needle of forbidden) {
    if (html.includes(needle)) {
      throw new Error(`SANITY CHECK FAILED: rendered HTML contains debug string ${JSON.stringify(needle)}. Aborting send.`);
    }
  }
}

// ============================================
//  HELPERS
// ============================================

function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
function escapeAttr(s) { return escapeHtml(s); }

async function fetchSubscribers(serviceKey) {
  const r = await fetch(
    `${SUPABASE_URL}/rest/v1/email_preferences?daily_digest=eq.true&select=email`,
    { headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` } }
  );
  if (!r.ok) throw new Error(`Supabase subscribers fetch failed: ${r.status}`);
  return await r.json();
}

async function sendOne(to, subject, html, resendKey) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${resendKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'Consumer Safari <briefing@consumersafari.com>',
      to: [to],
      subject,
      html,
    }),
  });
  const body = await r.text();
  let parsed = null;
  try { parsed = JSON.parse(body); } catch { /* keep as text */ }
  return { ok: r.ok && parsed && parsed.id, status: r.status, body: parsed || body };
}

// ============================================
//  HANDLER
// ============================================

export default async function handler(req, res) {
  // Method check
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed. Use POST.' });
    return;
  }

  // Auth check — return 401 to mask endpoint existence
  const auth = req.headers.authorization || req.headers.Authorization || '';
  const expected = `Bearer ${process.env.CRON_SECRET}`;
  if (!process.env.CRON_SECRET || auth !== expected) {
    res.status(401).json({ error: 'Unauthorized.' });
    return;
  }

  // Required env vars
  if (!process.env.RESEND_API_KEY) {
    res.status(500).json({ error: 'Server misconfiguration: RESEND_API_KEY not set.' });
    return;
  }
  if (!process.env.SUPABASE_SERVICE_ROLE_KEY) {
    res.status(500).json({ error: 'Server misconfiguration: SUPABASE_SERVICE_ROLE_KEY not set.' });
    return;
  }

  // Parse body
  let data;
  try {
    data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  } catch (e) {
    res.status(400).json({ error: `Invalid JSON: ${e.message}` });
    return;
  }
  if (!data || typeof data !== 'object') {
    res.status(400).json({ error: 'Body must be a JSON object.' });
    return;
  }

  // Render + sanity check
  let html;
  try {
    html = buildEmail(data);
    sanityCheck(html);
  } catch (e) {
    res.status(400).json({ error: e.message });
    return;
  }

  // Optional dry-run: validate, render, return preview, do not send
  const dryRun = String(req.query.dry_run || '0') === '1';
  if (dryRun) {
    res.status(200).json({
      ok: true,
      dry_run: true,
      html_length: html.length,
      subject: data.subject,
      preview: html.slice(0, 500),
    });
    return;
  }

  // Optional single-recipient test (?to=email@x.com bypasses Supabase fetch)
  const testTo = (req.query.to || '').toString().trim();

  // Resolve recipients
  let recipients;
  if (testTo) {
    recipients = [{ email: testTo }];
  } else {
    try {
      recipients = await fetchSubscribers(process.env.SUPABASE_SERVICE_ROLE_KEY);
    } catch (e) {
      res.status(502).json({ error: `Subscribers fetch failed: ${e.message}` });
      return;
    }
  }
  if (!Array.isArray(recipients) || recipients.length === 0) {
    res.status(200).json({ ok: true, sent: 0, failed: 0, note: 'No subscribers found.' });
    return;
  }

  // Send sequentially with light pacing to avoid Resend rate limits
  let sent = 0;
  let failed = 0;
  const failures = [];
  for (const r of recipients) {
    const result = await sendOne(r.email, data.subject, html, process.env.RESEND_API_KEY);
    if (result.ok) {
      sent++;
    } else {
      failed++;
      failures.push({ email: r.email, status: result.status, body: result.body });
    }
    // ~120ms gap; well under Resend's 10/sec limit
    await new Promise(resolve => setTimeout(resolve, 120));
  }

  res.status(200).json({
    ok: failed === 0,
    sent,
    failed,
    total: recipients.length,
    test: !!testTo,
    failures: failures.slice(0, 5),
  });
}

// Vercel function config — give it room to send 38+ emails sequentially
export const config = {
  maxDuration: 60, // seconds
};
