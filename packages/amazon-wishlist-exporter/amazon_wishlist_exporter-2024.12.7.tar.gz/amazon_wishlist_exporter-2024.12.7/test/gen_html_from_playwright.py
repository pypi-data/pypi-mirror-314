import os
import re
from pathlib import Path

from amazon_wishlist_exporter.utils.locale_ import (
    get_currency_from_territory,
    get_territory_from_tld,
    tld_to_locale_mapping,
)
from playwright.sync_api import sync_playwright

working_dir = Path(__file__).resolve().parent
URL_FILE = working_dir / "urls.txt"
DOWNLOAD_DIR = working_dir / "testdata/html_playwright"
USER_DATA_DIR_PARENT = working_dir / ".playwright"

re_wishlist_parts = re.compile(r"\.amazon\.([a-z.]{2,})/.*?/wishlist.*/([A-Z0-9]{10,})[/?]?\b")


def read_urls():
    with open(URL_FILE, "r") as file:
        return [line.strip() for line in file.readlines() if not line.startswith("#")]


def process_wishlist_url(url, fmt_locale, wishlist_tld):
    with sync_playwright() as p:
        user_data_dir_locale = USER_DATA_DIR_PARENT / fmt_locale
        user_data_dir_locale.mkdir(parents=True, exist_ok=True)

        territory = get_territory_from_tld(wishlist_tld)
        currency = get_currency_from_territory(territory)

        cookies = [
            {
                "name": "lc-acbin",
                "value": fmt_locale,
                "domain": f".amazon.{wishlist_tld}",
                "path": "/",
                "httpOnly": False,
                "secure": False,
                "sameSite": "Lax",
            },
            {
                "name": "i18n-prefs",
                "value": currency,
                "domain": f".amazon.{wishlist_tld}",
                "path": "/",
                "httpOnly": False,
                "secure": False,
                "sameSite": "Lax",
            },
        ]

        # Persistence avoids anti-bot measures
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir_locale),
            channel="chrome",
            executable_path=os.getenv("CHROME_BINARY_PATH"),
            headless=False,
            no_viewport=True,
            args=[
                f"--lang={fmt_locale}",
                f"--accept-lang={fmt_locale}",
            ],
            locale=fmt_locale,
            permissions=["storage-access"],
            downloads_path=str(DOWNLOAD_DIR),
        )

        # Needed to get correct formatting on initial page load
        context.add_cookies(cookies)

        page = context.new_page()

        page.goto(url)

        page.wait_for_timeout(3000)

        # Close locale selector on some stores
        redir_span = page.locator("span.redir-dismiss-x")
        span_count = redir_span.count()
        if span_count > 0:
            redir_span.locator("a").click()

        # Initial setup for infinite scroll
        previous_count = -1
        unchanged_count = 0

        # Infinite scroll to load all items
        while unchanged_count < 3:
            # Wait for items to load and get current count
            items = page.query_selector_all(".g-item-sortable")
            current_count = len(items)

            # Check for end of list marker or unchanged count threshold
            end_of_list_marker = page.query_selector("#endOfListMarker")
            if end_of_list_marker or unchanged_count >= 3:
                break

            # If item count hasn't changed, increment unchanged count
            if current_count == previous_count:
                unchanged_count += 1
            else:
                unchanged_count = 0  # Reset counter if new items were loaded

            previous_count = current_count

            # Scroll to the last item to trigger loading of more content
            if items:
                items[-1].scroll_into_view_if_needed()

        # Capture the outer HTML of the wishlist content only
        wishlist_html = page.eval_on_selector("#wishlist-page", "element => element.outerHTML")

        # Generate filename
        host = page.url.split("/")[2]
        list_id = page.evaluate("document.getElementById('listId')?.value || 'unknown'")
        language = page.evaluate("navigator.language || 'en'")
        fmt_lang = language.replace("-", "_")
        filename = DOWNLOAD_DIR / f"{host}_{list_id}_{fmt_lang}.html"

        # Write the HTML to a file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(wishlist_html)

        print(f"Saved wishlist HTML to {filename}")

        # Close the browser after the download
        context.clear_cookies()
        context.close()


def process_urls(sample_wishlist_urls, locale_dict):
    for url in sample_wishlist_urls:
        wishlist_re_search = re.search(re_wishlist_parts, url)

        if wishlist_re_search:
            wishlist_tld = wishlist_re_search.group(1)
            wishlist_id = wishlist_re_search.group(2)
            base_url = f"https://www.amazon.{wishlist_tld}"

            # Get the locales based on the TLD
            locales = locale_dict.get(wishlist_tld, [])

            # Create formatted URLs for each locale
            for locale in locales:
                fmt_locale = locale.split("_")[0].lower() + "_" + locale.split("_")[1].upper()
                fmt_url = f"{base_url}/hz/wishlist/ls/{wishlist_id}?language={fmt_locale}&viewType=list"
                process_wishlist_url(fmt_url, fmt_locale, wishlist_tld)


process_urls(read_urls(), tld_to_locale_mapping)
