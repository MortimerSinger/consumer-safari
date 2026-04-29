// /api/update-briefing.js
// Vercel Serverless Function — autonomous briefing data writer for Consumer Safari.
//
// PURPOSE:
//   Lets the cron submit a new daily briefing without needing the Supabase service-role key
//   in its sandbox. The function reads/writes Supabase server-side using its own env var.
//
// USAGE:
//   POST /api/update-briefing
//   Headers:
//     Authorization: Bearer <CRON_SECRET>
//     Content-Type: application/json
//
//   Body (mode "rotate" — recommended):
//     {
//       "mode": "rotate",
//       "date": "Wednesday, April 30, 2026",
//       "todayNews": [{category, stories:[{headline, source, url, blurb, tag}]}],
//       "aiTodayNews": [...],
//       "todayForMe": {summary, keyNumbers:[{label, value, change, direction}], patterns:[...]},
//       "deepRead": [...],          // optional, replaces existing
//       "aiDeepRead": [...],        // optional
//       "toListen": [...],          // optional
//       "aiListen": [...],          // optional
//       "voices": [...],            // optional
//       "newDeals": [...]           // optional, prepended to dealTracker (capped at 15)
//     }
//
//   In "rotate" mode the function:
//     1. Fetches current DATA from Supabase
//     2. Validates the new payload
//     3. Rotates current.todayNews → top of weekNews (trim to 10; overflow → monthNews, cap 30)
//        Same for aiTodayNews → aiWeekNews → aiMonthNews
//     4. Replaces todayNews / aiTodayNews / todayForMe with new ones
//     5. Replaces optional fields (deepRead, aiDeepRead, toListen, aiListen, voices) if provided
//     6. Prepends newDeals to dealTracker (capped at 15)
//     7. Preserves calendarEvents, whitePapers, greeting
//     8. Writes new row with is_current=true, clears prior is_current
//
//   Body (mode "full"):
//     Pass a complete DATA object exactly as the schema expects. The function validates and writes.
//
//   Optional: ?dry_run=1 → validates and computes the new DATA without writing.
//
// ENV VARS:
//   SUPABASE_SERVICE_ROLE_KEY — to read/write briefings
//   CRON_SECRET               — shared secret the cron sends in Authorization header
//
// SECURITY:
//   - Returns 401 on missing/wrong CRON_SECRET (masks endpoint existence)
//   - Validates against the same rules as briefing_schema.py
//   - On any failure, returns structured error JSON; never writes invalid data

const SUPABASE_URL = 'https://ugmirwqwlggdemwklcwi.supabase.co';

// ============================================
//  VALIDATION — mirrors briefing_schema.py
// ============================================

function validateBriefing(data) {
  const errors = [];

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return ['DATA must be an object'];
  }

  if (!data.date || typeof data.date !== 'string') {
    errors.push('date: required, non-empty string');
  }

  // Category-grouped feeds — todayNews and aiTodayNews are required
  for (const key of ['todayNews', 'aiTodayNews']) {
    const v = data[key];
    if (v === undefined || v === null) {
      errors.push(`${key}: required`);
      continue;
    }
    if (!Array.isArray(v)) {
      errors.push(`${key}: must be an array`);
      continue;
    }
    if (v.length === 0) {
      errors.push(`${key}: must have at least one category group`);
      continue;
    }
    validateGroups(v, key, errors);
  }

  // Optional category-grouped feeds
  for (const key of ['weekNews', 'aiWeekNews', 'monthNews', 'aiMonthNews']) {
    const v = data[key];
    if (v === undefined || v === null) continue;
    if (!Array.isArray(v)) {
      errors.push(`${key}: must be an array`);
      continue;
    }
    validateGroups(v, key, errors);
  }

  // todayForMe — must be an object
  const tfm = data.todayForMe;
  if (tfm === undefined || tfm === null) {
    errors.push('todayForMe: required');
  } else if (typeof tfm !== 'object' || Array.isArray(tfm)) {
    errors.push('todayForMe: MUST be an object with {summary, keyNumbers, patterns}, not a list');
  } else {
    if (!tfm.summary || typeof tfm.summary !== 'string') {
      errors.push('todayForMe.summary: required, non-empty string');
    }
    const kn = tfm.keyNumbers;
    if (!Array.isArray(kn) || kn.length === 0) {
      errors.push('todayForMe.keyNumbers: required, non-empty array');
    } else if (kn.length > 6) {
      errors.push('todayForMe.keyNumbers: max 6 items');
    } else {
      kn.forEach((n, i) => {
        if (!n || typeof n !== 'object') {
          errors.push(`todayForMe.keyNumbers[${i}]: must be an object`);
          return;
        }
        if (!n.label) errors.push(`todayForMe.keyNumbers[${i}].label: required`);
        if (!n.value) errors.push(`todayForMe.keyNumbers[${i}].value: required`);
        if (!n.change || typeof n.change !== 'string' || n.change.trim() === '') {
          errors.push(`todayForMe.keyNumbers[${i}].change: must be non-empty string (NEVER undefined/null)`);
        }
      });
    }
    if (tfm.patterns !== undefined && !Array.isArray(tfm.patterns)) {
      errors.push('todayForMe.patterns: must be an array');
    }
  }

  return errors;
}

function validateGroups(arr, key, errors) {
  arr.forEach((group, i) => {
    if (!group || typeof group !== 'object' || Array.isArray(group)) {
      errors.push(`${key}[${i}]: each item must be an object`);
      return;
    }
    if (!group.category) {
      errors.push(`${key}[${i}]: missing required field 'category'`);
    }
    if (!('stories' in group)) {
      errors.push(`${key}[${i}]: missing required field 'stories'`);
    }
    if ('items' in group && !('stories' in group)) {
      errors.push(`${key}[${i}]: uses 'items' but renderer expects 'stories' (2026-04-25 bug)`);
    }
    if (Array.isArray(group.stories)) {
      group.stories.forEach((s, j) => {
        if (!s || typeof s !== 'object') {
          errors.push(`${key}[${i}].stories[${j}]: must be an object`);
          return;
        }
        if (!s.headline && !s.title) {
          errors.push(`${key}[${i}].stories[${j}]: missing 'headline'`);
        }
        if (!s.url) {
          errors.push(`${key}[${i}].stories[${j}]: missing 'url'`);
        }
      });
    }
  });
}

// ============================================
//  SUPABASE I/O
// ============================================

async function fetchCurrentData(serviceKey) {
  const url = `${SUPABASE_URL}/rest/v1/briefings?is_current=eq.true&select=data`;
  const res = await fetch(url, {
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
    },
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Supabase fetch failed: HTTP ${res.status} ${txt}`);
  }
  const rows = await res.json();
  if (!rows || rows.length === 0) return null;
  return rows[0].data || null;
}

async function clearCurrentFlag(serviceKey) {
  const url = `${SUPABASE_URL}/rest/v1/briefings?is_current=eq.true`;
  const res = await fetch(url, {
    method: 'PATCH',
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal',
    },
    body: JSON.stringify({ is_current: false }),
  });
  if (!res.ok && res.status !== 204) {
    const txt = await res.text();
    throw new Error(`Supabase clear-current failed: HTTP ${res.status} ${txt}`);
  }
}

async function insertNewBriefing(serviceKey, data) {
  const url = `${SUPABASE_URL}/rest/v1/briefings`;
  const row = {
    date: data.date,
    is_current: true,
    data: data,
  };
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal',
    },
    body: JSON.stringify(row),
  });
  if (!res.ok && res.status !== 201) {
    const txt = await res.text();
    throw new Error(`Supabase insert failed: HTTP ${res.status} ${txt}`);
  }
}

// ============================================
//  ROTATION LOGIC
// ============================================

function rotate(current, payload) {
  // Promote yesterday's todayNews -> weekNews; trim to 10; overflow -> monthNews (cap 30)
  const prevToday = (current && current.todayNews) || [];
  const prevAiToday = (current && current.aiTodayNews) || [];
  const prevWeek = (current && current.weekNews) || [];
  const prevAiWeek = (current && current.aiWeekNews) || [];
  const prevMonth = (current && current.monthNews) || [];
  const prevAiMonth = (current && current.aiMonthNews) || [];

  let newWeek = [...prevToday, ...prevWeek];
  const overflow = newWeek.slice(10);
  newWeek = newWeek.slice(0, 10);
  let newMonth = [...overflow, ...prevMonth].slice(0, 30);

  let newAiWeek = [...prevAiToday, ...prevAiWeek];
  const aiOverflow = newAiWeek.slice(10);
  newAiWeek = newAiWeek.slice(0, 10);
  let newAiMonth = [...aiOverflow, ...prevAiMonth].slice(0, 30);

  // dealTracker: prepend newDeals if provided, cap 15
  let dealTracker = (current && current.dealTracker) || [];
  if (Array.isArray(payload.newDeals) && payload.newDeals.length > 0) {
    dealTracker = [...payload.newDeals, ...dealTracker].slice(0, 15);
  }

  // Replace optional fields if explicitly provided in payload; else preserve from current
  const replaceIfProvided = (key) => (
    payload[key] !== undefined ? payload[key] : (current ? current[key] : undefined)
  );

  const merged = {
    date: payload.date,
    greeting: (current && current.greeting) || 'Welcome back, Morty',

    // New today
    todayNews: payload.todayNews,
    aiTodayNews: payload.aiTodayNews,
    todayForMe: payload.todayForMe,

    // Rotated week/month
    weekNews: newWeek,
    aiWeekNews: newAiWeek,
    monthNews: newMonth,
    aiMonthNews: newAiMonth,

    // Optional, replace-if-provided
    deepRead: replaceIfProvided('deepRead'),
    aiDeepRead: replaceIfProvided('aiDeepRead'),
    toListen: replaceIfProvided('toListen'),
    aiListen: replaceIfProvided('aiListen'),
    voices: replaceIfProvided('voices'),

    // Preserve from current
    dealTracker: dealTracker,
    calendarEvents: (current && current.calendarEvents) || [],
    whitePapers: (current && current.whitePapers) || [],
    keyNumbers: (current && current.keyNumbers) || [],
    patterns: (current && current.patterns) || [],
  };

  // Strip undefined to keep payload clean
  Object.keys(merged).forEach(k => {
    if (merged[k] === undefined) delete merged[k];
  });

  return merged;
}

// ============================================
//  HANDLER
// ============================================

export default async function handler(req, res) {
  // Method check
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed; use POST' });
  }

  // Auth check — return 401 to mask existence
  const cronSecret = process.env.CRON_SECRET;
  if (!cronSecret) {
    return res.status(500).json({ ok: false, error: 'CRON_SECRET not configured on server' });
  }
  const authHeader = req.headers.authorization || '';
  const expected = `Bearer ${cronSecret}`;
  if (authHeader !== expected) {
    return res.status(401).json({ ok: false, error: 'Unauthorized' });
  }

  // Env check
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!serviceKey) {
    return res.status(500).json({ ok: false, error: 'SUPABASE_SERVICE_ROLE_KEY not configured on server' });
  }

  // Parse body — Vercel auto-parses JSON when content-type is application/json
  let payload = req.body;
  if (typeof payload === 'string') {
    try {
      payload = JSON.parse(payload);
    } catch (e) {
      return res.status(400).json({ ok: false, error: 'Body is not valid JSON', detail: e.message });
    }
  }
  if (!payload || typeof payload !== 'object') {
    return res.status(400).json({ ok: false, error: 'Body must be a JSON object' });
  }

  const mode = payload.mode || 'rotate';
  const dryRun = req.query && (req.query.dry_run === '1' || req.query.dry_run === 'true');

  try {
    let finalData;

    if (mode === 'rotate') {
      // Validate the inputs first (only the keys we need)
      const inputErrors = [];
      if (!payload.date) inputErrors.push('date: required');
      if (!Array.isArray(payload.todayNews) || payload.todayNews.length === 0) {
        inputErrors.push('todayNews: required, non-empty array');
      }
      if (!Array.isArray(payload.aiTodayNews) || payload.aiTodayNews.length === 0) {
        inputErrors.push('aiTodayNews: required, non-empty array');
      }
      if (!payload.todayForMe || typeof payload.todayForMe !== 'object') {
        inputErrors.push('todayForMe: required object');
      }
      if (inputErrors.length > 0) {
        return res.status(400).json({ ok: false, error: 'Invalid rotate payload', detail: inputErrors });
      }

      const current = await fetchCurrentData(serviceKey);
      finalData = rotate(current, payload);
    } else if (mode === 'full') {
      finalData = payload;
    } else {
      return res.status(400).json({ ok: false, error: `Unknown mode: ${mode}` });
    }

    // Validate the final composed DATA before writing
    const errors = validateBriefing(finalData);
    if (errors.length > 0) {
      return res.status(400).json({ ok: false, error: 'Validation failed', detail: errors });
    }

    if (dryRun) {
      return res.status(200).json({
        ok: true,
        dry_run: true,
        date: finalData.date,
        mode: mode,
        weekNews_len: (finalData.weekNews || []).length,
        monthNews_len: (finalData.monthNews || []).length,
        deal_count: (finalData.dealTracker || []).length,
      });
    }

    // Write
    await clearCurrentFlag(serviceKey);
    await insertNewBriefing(serviceKey, finalData);

    return res.status(200).json({
      ok: true,
      date: finalData.date,
      mode: mode,
      weekNews_len: (finalData.weekNews || []).length,
      monthNews_len: (finalData.monthNews || []).length,
      deal_count: (finalData.dealTracker || []).length,
    });
  } catch (e) {
    return res.status(500).json({ ok: false, error: 'Internal error', detail: e.message });
  }
}
