import pytest
import env
import utils as u
from utils import browser

BASE_API_URL = "https://api.va.staging.landing.ai/v1/tools/"

# List of the tools
TOOLS = {
    "Florence2 Phrase Grounding": "florence2",
    "Countgd Counting": "text-to-object-detection",
    "IXC25 Image VQA": "internlm-xcomposer2",
    "OWLv2 Image": "text-to-object-detection",
    "IXC25 Temporal Localization": "video-temporal-localization",
    "Loca Visual Prompt Counting": "loca",
    "Loca Zero Shot Counting": "loca",
    "Florence-2 Roberta Vqa": "florence2-qa",
    "Depth Anything V2": "depth-anything-v2",
    "ViT NSFW Classification": "nsfw-classification",
    "Florence-2 Image Caption": "florence2",
    "Florence-2 Sam2 Image": "text-to-instance-segmentation",
    "Florence-2 Sam2 Video Tracking": "text-to-instance-segmentation",
    "Florence2 OCR": "florence2",
    "OWLv2 Video": "text-to-object-detection",
    "Qwen2 VL Images VQA": "image-to-text",
    "Qwen2 VL Video VQA": "image-to-text",
}

def test_validate_all_tools(browser):
    """Iterates over all tools, validates their API URL, and returns to the tools list."""

    # Step 1: Login to the platform
    page = u.login(browser)
    # 🕒 wait for 10 seconds after login
    print("🕒 Waiting 10 seconds after login...")
    page.wait_for_timeout(10000)

    # Step 2: Navigate directly to the demo page (sin Explore APIs ni View all APIs)
    demo_url = "https://va.staging.landing.ai/demo"
    print(f"🌐 Navigating to {demo_url}")
    page.goto(demo_url, wait_until="load")

    # Step 4: Wait for the tools list to load
    page.wait_for_selector("div.overflow-hidden.text-ellipsis.text-lg.font-semibold.text-gray-50", timeout=10000)

    for tool_name, endpoint in TOOLS.items():
        print(f"🔄 Validating tool: {tool_name}")

        # Step 5: Scroll until the tool is visible
        tool_button = page.locator(f"div.overflow-hidden.text-ellipsis.text-lg.font-semibold.text-gray-50:has-text('{tool_name}')")

        if not tool_button.is_visible():
            print(f"🔍 '{tool_name}' not immediately visible, scrolling...")
            for _ in range(10):  # Intenta hacer scroll hasta 10 veces
                page.mouse.wheel(0, 300)
                page.wait_for_timeout(1000)
                if tool_button.is_visible():
                    break

        # Verifica si se encontró la tool después de hacer scroll
        assert tool_button.is_visible(), f"❌ '{tool_name}' button not found after scrolling"
        
        tool_button.click()
        print(f"✅ Clicked on '{tool_name}'")

        # Step 6: 🕒 Wait for 5 seconds to allow all elements to load
        page.wait_for_timeout(5000)  

        # Step 7: Validate the API URL inside the tool
        expected_url = f"{BASE_API_URL}{endpoint}"
        api_url_element = page.locator(f"span.token:text('{expected_url}')")

        actual_url = api_url_element.text_content().strip('"') if api_url_element.is_visible() else None

        print(f"🔍 Expected Base URL: {expected_url}")
        print(f"🔍 Found URL on Page: {actual_url}")

        # Step 8: Fail the test if the URL does not match
        assert actual_url == expected_url, f"❌ URL mismatch! Expected: {expected_url}, but found: {actual_url}"
        print(f"✅ URL validated successfully for {tool_name}: {expected_url}")

        # Step 9: Return to the tools list using browser back function
        page.go_back()
        print("✅ Returned to the tools list using browser back")

        # Step 10: Wait for the tools list to load again before continuing
        page.wait_for_selector("div.overflow-hidden.text-ellipsis.text-lg.font-semibold.text-gray-50", timeout=10000)

    # Step 11: Close the browser after testing all tools
    browser.close()
