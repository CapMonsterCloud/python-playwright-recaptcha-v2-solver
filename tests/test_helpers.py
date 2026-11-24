import pytest

from recaptcha_helpers import (
    INJECT_TOKEN_JS,
    pick_sitekey,
    require_api_key,
    sitekey_from_iframe_src,
    token_preview,
)

ANCHOR = (
    "https://www.google.com/recaptcha/api2/anchor?ar=1"
    "&k=6Lcg7CMUAAAAANphynKgn9YAgA4tQ2KI_iqRyTwd&co=aHR0cHM6&hl=en&size=normal"
)


def test_sitekey_from_anchor_iframe():
    assert sitekey_from_iframe_src(ANCHOR) == "6Lcg7CMUAAAAANphynKgn9YAgA4tQ2KI_iqRyTwd"


def test_non_recaptcha_iframe_is_ignored():
    assert sitekey_from_iframe_src("https://example.com/embed?k=abc") is None
    assert sitekey_from_iframe_src(None) is None


def test_data_attribute_wins_over_iframe():
    assert pick_sitekey(" explicit-key ", [ANCHOR]) == "explicit-key"
    assert pick_sitekey(None, ["about:blank", ANCHOR]).startswith("6Lcg7")
    assert pick_sitekey(None, ["about:blank"]) is None


def test_missing_api_key_exits_with_message():
    with pytest.raises(SystemExit, match="CAPMONSTER_API_KEY"):
        require_api_key({})
    assert require_api_key({"CAPMONSTER_API_KEY": " abc "}) == "abc"


def test_token_preview_hides_long_tokens():
    assert token_preview("short") == "short"
    assert token_preview("x" * 500).endswith("(500 chars)")


def test_injection_in_real_browser():
    """Runs the injection script in headless Chromium against a local page (no network, no API key)."""
    sync_api = pytest.importorskip("playwright.sync_api")
    html = """
      <form><div class="g-recaptcha" data-sitekey="k" data-callback="onOk"></div>
      <textarea name="g-recaptcha-response" style="display:none"></textarea></form>
      <script>window.got = null; function onOk(t){ window.got = t; }</script>
    """
    try:
        with sync_api.sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html)
            result = page.evaluate(INJECT_TOKEN_JS, "TOKEN123")
            assert result == {"textareas": 1, "callbackFired": True}
            assert page.evaluate("window.got") == "TOKEN123"
            assert page.input_value("textarea") == "TOKEN123"
            browser.close()
    except Exception as exc:  # browser binaries not installed
        if "Executable doesn't exist" in str(exc):
            pytest.skip("run `python -m playwright install chromium` to enable this test")
        raise
