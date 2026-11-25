# reCAPTCHA v2 Solver for Python Playwright (CapMonster Cloud)

[![tests](https://github.com/CapMonsterCloud/python-playwright-recaptcha-v2-solver/actions/workflows/test.yml/badge.svg)](https://github.com/CapMonsterCloud/python-playwright-recaptcha-v2-solver/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Playwright 1.45+](https://img.shields.io/badge/Playwright-1.45%2B-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)

A minimal, runnable **Google reCAPTCHA v2 solver for Python Playwright**. It opens a page in Chromium, detects the sitekey, requests a token from the [CapMonster Cloud reCAPTCHA v2 solver](https://capmonster.cloud/en/recaptcha-v2/?utm_source=github&utm_medium=repo-example&utm_campaign=python-playwright-recaptcha-v2&utm_content=intro) through the official Python SDK (`capmonstercloudclient`), puts the token into the page and can submit the form. Use it as a starting point when your Playwright scripts hit the reCAPTCHA v2 checkbox on forms you test or automate.

## What this example does

1. Opens a page with a Google reCAPTCHA v2 widget in Chromium (Playwright for Python, async API).
2. Detects the sitekey automatically, from `data-sitekey` or from the widget iframe URL.
3. Sends a `RecaptchaV2Request` to CapMonster Cloud and waits for the `g-recaptcha-response` token.
4. Puts the token into the page, fires the site's `data-callback` and, optionally, clicks your submit button.

By default it runs against the public demo page `lessons.zennolab.com`, so you can see the full flow before pointing it at your own form.

## Requirements

- Python 3.9+
- A CapMonster Cloud API key (see [Get an API key](#get-an-api-key))
- Chromium for Playwright (installed by the command below)

## Quick start

```bash
git clone https://github.com/CapMonsterCloud/python-playwright-recaptcha-v2-solver.git
cd python-playwright-recaptcha-v2-solver
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

## reCAPTCHA v2 token basics

- The token is a `g-recaptcha-response` string. Put it into the hidden textarea or pass it to the widget callback.
- reCAPTCHA v2 tokens are single-use and short-lived. Request a new token for every submission and submit right away.
- Pass the same page URL and sitekey that the browser used, otherwise the token can be rejected on validation.

## Common errors

| Symptom | Cause and fix |
|---|---|
| `Executable doesn't exist at ...chromium...` | Browser binaries are not installed: run `python -m playwright install chromium`. |
| `GetTaskError: [ERROR_KEY_DOES_NOT_EXIST]` | Wrong or empty `CAPMONSTER_API_KEY`. Copy the key again without spaces. |
| `[ERROR_ZERO_BALANCE]` | Top up the account balance. |
| `TimeoutError` waiting for `iframe[src*='recaptcha']` | The widget loads after a click or scroll, or the page uses reCAPTCHA v3/Enterprise. Trigger the widget first or use the matching request type. |
| Form says the captcha is invalid | The token is older than ~120 seconds or was used twice. Inject it right after it is returned and submit once. |
| `callback fired: False` and the button stays disabled | The callback is registered through `grecaptcha.render({callback})`. Call that function name yourself after injection. |

## Get an API key

This example needs a CapMonster Cloud account and API key. Register and get the key on the [reCAPTCHA v2 solver page](https://capmonster.cloud/en/recaptcha-v2/?utm_source=github&utm_medium=repo-example&utm_campaign=python-playwright-recaptcha-v2&utm_content=cta). There you will also find pricing and the API description.

## Responsible use

Use this code only on websites you own or are explicitly allowed to test and automate, for example QA of your own forms. Follow the website's terms of service and applicable laws. Keep your API key private.

## Links

- Python SDK: [CapMonster Cloud Python SDK](https://github.com/CapMonsterCloud/capmonster-python-captcha-solver)
- reCAPTCHA v2 solving with CapMonster Cloud: [capmonster.cloud/en/recaptcha-v2](https://capmonster.cloud/en/recaptcha-v2/?utm_source=github&utm_medium=repo-example&utm_campaign=python-playwright-recaptcha-v2&utm_content=links)

reCAPTCHA is a trademark of Google LLC. CapMonster Cloud is not affiliated with or endorsed by Google.
