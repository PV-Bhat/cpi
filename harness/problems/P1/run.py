from playwright.sync_api import sync_playwright
import os, time
from pathlib import Path

# 1. Add your invoice URLs here:
INVOICE_URLS = [
    "https://knvl.me/LULUHP/G4QoDlg",
    "https://knvl.me/LULUHP/NXFxYpb",
    "https://knvl.me/LULUHP/YEVkh2D",
    "https://knvl.me/LULUHP/3YnbiwN",
    "https://knvl.me/LULUHP/ixYfsnC",
    "https://knvl.me/LULUHP/LARz3wt",
    "https://knvl.me/LULUHP/SMAXNGh",
    "https://knvl.me/LULUHP/1Qzvylc",
    "https://knvl.me/LULUHP/jOysxJy",
    "https://knvl.me/LULUHP/INJvAqa",
    "https://knvl.me/LULUHP/Dikr1BG",
    "https://knvl.me/LULUHP/CHtwJVE",
    "https://knvl.me/LULUHP/HbpolhS",
    "https://knvl.me/LULUHP/hSW3C0T",
    "https://knvl.me/LULUHP/pVP9GZC",
    "https://knvl.me/LULUHP/i6L1fe0",
    "https://knvl.me/LULUHP/gHzxwQe",
    "https://knvl.me/LULUHP/WR0jpg7",
    "https://knvl.me/LULUHP/2TKn9j9",
    "https://knvl.me/LULUHP/JeRfQgh",
    "https://knvl.me/LULUHP/L290XK9",
    "https://knvl.me/LULUHP/TPODp3h",
    "https://knvl.me/LULUHP/sXR0w8u",
    "https://knvl.me/LULUHP/TausKB6",
    "https://knvl.me/LULUHP/m2ZemT4",
    "https://knvl.me/LULUHP/FhfcKcL",
]

SAVE_DIR = Path(os.getenv("SAVE_DIR", Path(__file__).resolve().parent / "invoices"))
SAVE_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    for i, url in enumerate(INVOICE_URLS, 1):
        filename = SAVE_DIR / f"invoice_{i}.pdf"
        if filename.exists():
            print(f"Already exists: {filename} (skipping)")
            continue

        print(f"Processing {url} ...")
        page.goto(url, timeout=60000)
        try:
            # Wait for the Download Invoice button to become enabled
            button = page.locator("button:has-text('Download Invoice')")
            button.wait_for(state="visible", timeout=15000)
            with page.expect_download() as download_info:
                button.click()
            download = download_info.value
            download.save_as(str(filename))
            print(f"Downloaded {filename}")
            time.sleep(2)  # Wait to avoid hitting server too fast
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
            continue

    print("\nAll done!")
    browser.close()
