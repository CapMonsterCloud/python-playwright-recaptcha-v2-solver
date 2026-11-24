"""Solve reCAPTCHA v2 in a Playwright (Python) session with the CapMonster Cloud SDK.

Usage:
    export CAPMONSTER_API_KEY=your_key
    python examples/solve_recaptcha_v2.py                      # demo page
    python examples/solve_recaptcha_v2.py --url https://your-site/form --submit "button[type=submit]"
"""
from __future__ import annotations

import argparse
import asyncio
import time

from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2Request
from playwright.async_api import async_playwright

from recaptcha_helpers import (
    DEMO_URL,
    INJECT_TOKEN_JS,
    pick_sitekey,
    require_api_key,
    token_preview,
)


async def find_sitekey(page) -> str | None:
    widget = await page.query_selector("[data-sitekey]")
    data_sitekey = await widget.get_attribute("data-sitekey") if widget else None
    srcs = [frame.url for frame in page.frames]
    return pick_sitekey(data_sitekey, srcs)


async def run(url: str, submit_selector: str | None, headless: bool) -> str:
    api_key = require_api_key()
    client = CapMonsterClient(options=ClientOptions(api_key=api_key))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector("iframe[src*='recaptcha']", timeout=20_000)

        sitekey = await find_sitekey(page)
        if not sitekey:
            raise SystemExit("reCAPTCHA sitekey not found on the page.")
        print(f"sitekey: {sitekey}")

        user_agent = await page.evaluate("navigator.userAgent")
        started = time.monotonic()
        solution = await client.solve_captcha(
            RecaptchaV2Request(websiteUrl=page.url, websiteKey=sitekey, userAgent=user_agent)
        )
        token = solution["gRecaptchaResponse"]
        print(f"solved in {time.monotonic() - started:.1f}s: {token_preview(token)}")

        result = await page.evaluate(INJECT_TOKEN_JS, token)
        print(f"injected into {result['textareas']} textarea(s), callback fired: {result['callbackFired']}")

        if submit_selector:
            await page.click(submit_selector)
            await page.wait_for_load_state("domcontentloaded")
            print(f"submitted, now at {page.url}")

        await browser.close()
        return token


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", default=DEMO_URL, help="page with a reCAPTCHA v2 widget")
    parser.add_argument("--submit", default=None, help="CSS selector of the submit button")
    parser.add_argument("--headed", action="store_true", help="show the browser window")
    args = parser.parse_args()
    asyncio.run(run(args.url, args.submit, headless=not args.headed))


if __name__ == "__main__":
    main()
