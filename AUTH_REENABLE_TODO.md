# Re-enable Google Sign-in After Supabase Pro Upgrade

**Status:** ✅ COMPLETE 2026-05-11. Google sign-in restored with custom auth domain `auth.consumersafari.com`.
**Why:** Default Supabase OAuth redirect was showing scary `ugmirwqwlggdemwklcwi.supabase.co` URL on Google's sign-in screen.
**Fix:** Custom auth domain (Supabase Pro $25/mo + Custom Domain add-on $10/mo).

## What happened
1. May 7: Hid Google sign-in UI, shipped magic-link-only as interim fix
2. May 7-11: Magic-link served all sign-ins cleanly (no conversion data captured)
3. May 11: Upgraded to Supabase Pro, activated `auth.consumersafari.com`, updated Google Cloud OAuth, restored UI
4. May 11 9:58am ET: Verified working in production

## Bug encountered (for future reference)
Squarespace silently failed to propagate the `_acme-challenge` TXT record on initial save. The UI showed the record as saved, but the authoritative Google Domains nameservers returned NXDOMAIN. Edit operations on existing TXT records also did not propagate. **Fix: delete the record and recreate it from scratch** — then it propagated within seconds.

## To re-enable original state (if ever needed)
1. Delete `auth.consumersafari.com` in Supabase → Settings → General → Custom Domains
2. Remove $10 Custom Domain add-on in Supabase → Add-ons
3. Update Google Cloud OAuth redirect URI back to `https://ugmirwqwlggdemwklcwi.supabase.co/auth/v1/callback`
4. Delete CNAME and `_acme-challenge.auth` TXT records from Squarespace DNS

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
