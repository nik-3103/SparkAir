"""
Automated script to capture high-resolution screenshots of the live Streamlit dashboard
using Playwright with local Chrome/Edge browser.
"""

import os
import time
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = r"C:\AirQualityAnalysis\docs\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def capture_screenshots():
    print(f"Launching browser from: {CHROME_PATH}")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 950},
            device_scale_factor=1.5
        )
        page = context.new_page()

        print("Navigating to Streamlit app at http://localhost:8501 ...")
        page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
        time.sleep(4)  # Wait for charts and animations to render

        # 1. Main Overview & KPI row
        overview_path = os.path.join(SCREENSHOTS_DIR, "dashboard_overview.png")
        page.screenshot(path=overview_path, full_page=False)
        print(f"[OK] Saved overview screenshot: {overview_path}")

        # 2. Tab 1: City Comparison
        try:
            tab1_btn = page.locator("button[role='tab']:has-text('City Comparison')")
            if tab1_btn.count() > 0:
                tab1_btn.click()
                time.sleep(2)
            tab1_path = os.path.join(SCREENSHOTS_DIR, "tab1_city_comparison.png")
            page.screenshot(path=tab1_path, full_page=False)
            print(f"[OK] Saved Tab 1 screenshot: {tab1_path}")
        except Exception as e:
            print(f"Error capturing Tab 1: {e}")

        # 3. Tab 2: Yearly & Monthly Trends
        try:
            tab2_btn = page.locator("button[role='tab']:has-text('Trends')")
            if tab2_btn.count() > 0:
                tab2_btn.click()
                time.sleep(2)
            tab2_path = os.path.join(SCREENSHOTS_DIR, "tab2_yearly_trends.png")
            page.screenshot(path=tab2_path, full_page=False)
            print(f"[OK] Saved Tab 2 screenshot: {tab2_path}")
        except Exception as e:
            print(f"Error capturing Tab 2: {e}")

        # 4. Tab 3: Particulate & Pollutants
        try:
            tab3_btn = page.locator("button[role='tab']:has-text('Particulate')")
            if tab3_btn.count() > 0:
                tab3_btn.click()
                time.sleep(2)
            tab3_path = os.path.join(SCREENSHOTS_DIR, "tab3_particulates.png")
            page.screenshot(path=tab3_path, full_page=False)
            print(f"[OK] Saved Tab 3 screenshot: {tab3_path}")
        except Exception as e:
            print(f"Error capturing Tab 3: {e}")

        # 5. Tab 4: Extreme Events (Top 10 AQI)
        try:
            tab4_btn = page.locator("button[role='tab']:has-text('Extreme Events')")
            if tab4_btn.count() > 0:
                tab4_btn.click()
                time.sleep(2)
            tab4_path = os.path.join(SCREENSHOTS_DIR, "tab4_extreme_events.png")
            page.screenshot(path=tab4_path, full_page=False)
            print(f"[OK] Saved Tab 4 screenshot: {tab4_path}")
        except Exception as e:
            print(f"Error capturing Tab 4: {e}")

        # 6. Tab 5: Data Explorer & Export
        try:
            tab5_btn = page.locator("button[role='tab']:has-text('Explorer')")
            if tab5_btn.count() > 0:
                tab5_btn.click()
                time.sleep(2)
            tab5_path = os.path.join(SCREENSHOTS_DIR, "tab5_data_explorer.png")
            page.screenshot(path=tab5_path, full_page=False)
            print(f"[OK] Saved Tab 5 screenshot: {tab5_path}")
        except Exception as e:
            print(f"Error capturing Tab 5: {e}")

        browser.close()
        print("All screenshots successfully captured!")

if __name__ == "__main__":
    capture_screenshots()
