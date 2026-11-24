✅ CapMonster.Cloud — Fast, Reliable CAPTCHA Solving for Automation & Scraping

[![CapMonster Cloud](https://help.zennolab.com/upload/u/02/020538b7c128.png)](https://capmonster.cloud/en/?utm_source=github-dw&utm_campaign=python-playwright-recaptcha-v2)

If you are tired of wasting time solving endless CAPTCHAs during scraping, automation, or testing — we’ve got a solution for you.  
Meet CapMonster.Cloud — the AI-powered CAPTCHA solving service trusted by thousands of users worldwide. 🚀

--

🔥 **Why users love CapMonster.Cloud**
  
💡 Very high success rates (up to 99%)  
⚡ Super fast solving times  
💲 Affordable transparent pricing (pay per 1,000 CAPTCHAs)  
🔌 Easy integration via API + browser extensions  
⭐ Excellent reviews on TrustPilot, SourceForge, SaaSHub, AlternativeTo

--

🔗 **Useful Links**

💲 [Pricing & Supported CAPTCHA Types (25+ types supported)](https://capmonster.cloud/en?utm_source=github-dw&utm_campaign=python-playwright-recaptcha-v2#new-plans)  
📘 [API Documentation](https://docs.capmonster.cloud/?utm_source=github-dw&utm_campaign=python-playwright-recaptcha-v2)  
💡 Main Website → [capmonster.cloud](https://capmonster.cloud/en/?utm_source=github-dw&utm_campaign=python-playwright-recaptcha-v2)  
⭐ Reviews → [TrustPilot](https://www.trustpilot.com/review/capmonster.cloud)

---

# reCAPTCHA v2 Solver for Python Playwright (Google reCAPTCHA) with CapMonster Cloud

A minimal, runnable **Python reCAPTCHA v2 solver** for **Playwright**: it solves the Google reCAPTCHA v2 checkbox inside a Playwright for Python session using the official CapMonster Cloud Python SDK (`capmonstercloudclient`). Use it as a starting point when your Playwright scripts hit Google reCAPTCHA on forms you test or automate.

## What this example does

1. Opens a page with a Google reCAPTCHA v2 widget in Chromium (Playwright for Python, async API).
2. Detects the sitekey automatically, from `data-sitekey` or from the widget iframe URL.
3. Sends a `RecaptchaV2Request` to CapMonster Cloud and waits for the `g-recaptcha-response` token.
4. Puts the token into the page, fires the site's `data-callback` and, optionally, clicks your submit button.

By default it runs against the public demo page `lessons.zennolab.com`, so you can see the full flow before pointing it at your own form.

## Requirements

- Python 3.9+
- A CapMonster Cloud API key (from your account dashboard)
- Chromium for Playwright (installed by the command below)

## Quick start

```bash
git clone https://github.com/CapMonsterCloud/python-playwright-recaptcha-v2-capmonster.git
cd python-playwright-recaptcha-v2-capmonster
pip install -r requirements.txt
python -m playwright install chromium

export CAPMONSTER_API_KEY=your_key        # Windows: set CAPMONSTER_API_KEY=your_key
python examples/solve_recaptcha_v2.py --headed

# your own page
python examples/solve_recaptcha_v2.py --url https://your-site.example/form --submit "button[type=submit]"
```

Run the tests (no API key or network needed):

```bash
pytest -q
```

## How it works

- **Sitekey without guessing.** Playwright exposes every frame, so the script reads the `k=` query parameter from the reCAPTCHA anchor iframe when the page renders the widget from JavaScript and has no `data-sitekey` attribute.
- **Same browser fingerprint.** The page's real `navigator.userAgent` is passed to the task. A token produced for a matching User-Agent is accepted more reliably than one produced for a generic one.
- **Token delivery the way Google does it.** `INJECT_TOKEN_JS` fills every `textarea[name="g-recaptcha-response"]` (some pages render more than one) and calls the function named in `data-callback`. Many modern forms enable the submit button only from that callback, so filling the textarea alone is not enough.
- **Secrets stay out of logs.** Only the first 32 characters of the token are printed.

## Common errors

| Symptom | Cause and fix |
|---|---|
| `Executable doesn't exist at ...chromium...` | Browser binaries are not installed: run `python -m playwright install chromium`. |
| `GetTaskError: [ERROR_KEY_DOES_NOT_EXIST]` | Wrong or empty `CAPMONSTER_API_KEY`. Copy the key again without spaces. |
| `[ERROR_ZERO_BALANCE]` | Top up the account balance. |
| `TimeoutError` waiting for `iframe[src*='recaptcha']` | The widget loads after a click or scroll, or the page uses reCAPTCHA v3/Enterprise. Trigger the widget first or use the matching request type. |
| Form says the captcha is invalid | The token is older than ~120 seconds or was used twice. Inject it right after it is returned and submit once. |
| `callback fired: False` and the button stays disabled | The callback is registered through `grecaptcha.render({callback})`. Call that function name yourself after injection. |

## Responsible use

Use this code only on websites you own or are explicitly allowed to test and automate, for example QA of your own forms. Follow the website's terms of service and applicable laws. Keep your API key private.

## Links

- Python SDK: [CapMonster Cloud Python SDK](https://github.com/CapMonsterCloud/capmonster-python-captcha-solver)
- reCAPTCHA v2 solving with CapMonster Cloud: [capmonster.cloud/en/recaptcha-v2](https://capmonster.cloud/en/recaptcha-v2/?utm_source=github&utm_medium=repo-example&utm_campaign=python-playwright-recaptcha-v2)
