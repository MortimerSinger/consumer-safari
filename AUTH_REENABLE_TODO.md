# Re-enable Google Sign-in After Supabase Pro Upgrade

**Status:** Google sign-in hidden 2026-05-07. Magic-link is the only flow.
**Why:** Default Supabase OAuth redirect shows scary `ugmirwqwlggdemwklcwi.supabase.co` URL on Google's sign-in screen, looking like a phishing site to users.
**Fix:** Custom auth domain (Supabase Pro feature, ~$25/mo).

## Steps After Upgrade

### 1. Configure custom auth domain in Supabase
- Supabase Dashboard → Project Settings → Custom Domains
- Add: `auth.consumersafari.com`
- Supabase provides a CNAME target

### 2. Add DNS record
- In your DNS provider (where consumersafari.com is managed)
- Add CNAME: `auth` → `<supabase-target>.supabase.co`
- Wait for verification (~5-30 min)

### 3. Update Google Cloud OAuth credentials
- Google Cloud Console → APIs & Services → Credentials
- Find the OAuth 2.0 Client ID for Consumer Safari
- Edit "Authorized redirect URIs"
- Replace: `https://ugmirwqwlggdemwklcwi.supabase.co/auth/v1/callback`
- With:    `https://auth.consumersafari.com/auth/v1/callback`
- Keep the Vercel redirect (`https://www.consumersafari.com`) in "Authorized JavaScript origins"

### 4. Re-enable UI in index.html
Search for: `<!-- Google sign-in hidden 2026-05-07`
Restore the four sections I removed:
- Landing gate sign-in button + in-app browser banner + OR divider (after `<p class="gate-tagline">`, before `<div id="gateMagicSection">`)
- Header `#authSignInBtn` (change `onclick` from `showSignInModal()` back to `signInWithGoogle()`, restore Google SVG icon)
- Saved-tab sign-in banner button (restore Google SVG, change onclick back)
- Sign-in modal Google button + OR divider (between `<p>...sign-in link.</p>` and `<div style="display:flex;gap:8px;">`)

The `signInWithGoogle()` function in the JS is preserved (line ~4335) — no function changes needed.

### 5. Test
- Sign out
- Click "Sign in with Google"
- Verify Google's OAuth screen says "to continue to **auth.consumersafari.com**" (not supabase.co)

## Reference (for me)
- 4 hidden locations have HTML comments with date 2026-05-07 marking the change
- `signInWithGoogle()` function definition retained for easy revert
- Magic-link flow handles 100% of sign-in until then
