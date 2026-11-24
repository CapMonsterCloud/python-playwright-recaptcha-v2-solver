"""Small, browser-independent helpers used by solve_recaptcha_v2.py.

Kept separate so they can be unit-tested without a browser or an API key.
"""
from __future__ import annotations

import os
from urllib.parse import parse_qs, urlparse

DEMO_URL = "https://lessons.zennolab.com/captchas/recaptcha/v2_simple.php?level=high"

# Runs inside the page: puts the token where Google's widget would put it and
# fires the site's own callback (if the widget was rendered with one).
INJECT_TOKEN_JS = """
(token) => {
  const areas = document.querySelectorAll('textarea[name="g-recaptcha-response"]');
  areas.forEach((el) => { el.style.display = 'block'; el.value = token; el.innerHTML = token; });

  let fired = false;
  const widget = document.querySelector('.g-recaptcha[data-callback]');
  if (widget) {
    const fn = window[widget.getAttribute('data-callback')];
    if (typeof fn === 'function') { fn(token); fired = true; }
  }
  return { textareas: areas.length, callbackFired: fired };
}
"""


def sitekey_from_iframe_src(src: str | None) -> str | None:
    """Extract the sitekey from a reCAPTCHA anchor iframe URL (the `k` query parameter)."""
    if not src or "recaptcha" not in src:
        return None
    values = parse_qs(urlparse(src).query).get("k")
    return values[0] if values else None


def pick_sitekey(data_sitekey: str | None, iframe_srcs: list[str]) -> str | None:
    """Prefer an explicit data-sitekey attribute, then fall back to the widget iframe."""
    if data_sitekey:
        return data_sitekey.strip()
    for src in iframe_srcs:
        key = sitekey_from_iframe_src(src)
        if key:
            return key
    return None


def require_api_key(env: dict | None = None) -> str:
    """Read CAPMONSTER_API_KEY or exit with a readable message."""
    env = os.environ if env is None else env
    key = (env.get("CAPMONSTER_API_KEY") or "").strip()
    if not key:
        raise SystemExit(
            "CAPMONSTER_API_KEY is not set. Export it first, e.g. "
            "export CAPMONSTER_API_KEY=your_key"
        )
    return key


def token_preview(token: str, size: int = 32) -> str:
    """Never print full tokens to logs."""
    return token if len(token) <= size else f"{token[:size]}... ({len(token)} chars)"
