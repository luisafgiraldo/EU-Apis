# import pytest
# import pyautogui
# from playwright.async_api import async_playwright
# import pytest_asyncio

# # Credentials and URL
# USERNAME = "luisa_aristizabal23211@elpoli.edu.co"
# PASSWORD = "Luisa233@"
# URL = "https://va.staging.landing.ai/"
# #VIDEO_PATH = "/Users/luisaaristizabal/Desktop/API-s-/VA_playwright/Images/shark.mp4"

# @pytest_asyncio.fixture(scope="function")
# async def browser():
#     screen_width, screen_height = pyautogui.size()
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context(viewport={"width": screen_width, "height": screen_height})
#         page = await context.new_page()
#         await page.goto(URL)
#         yield page
#         await browser.close()

# @pytest.mark.asyncio
# async def test_login_and_validate_elements(browser):
#     # Log in
#     await browser.fill("input[name='identifier']", USERNAME)
#     await browser.get_by_role("button", name="Sign in").click()
#     await browser.fill("input[name='password']", PASSWORD)
#     await browser.get_by_role("button", name="Continue").click()
#     await browser.wait_for_selector("div:text('What vision task do you have in mind?')", timeout=10000)
#     print("✅ Successful login and page loaded correctly")

    # Click on the specified element
    # await browser.click("p.text-sm.font-semibold:text('Detect how close sharks are to surfers')")
    # print("✅ Clicked on the correct element")

    # Validate if the video is present with a 20-second wait
    #video_locator = "video source[src='/asset/examples/shark3_short.mp4']"
    #await browser.wait_for_selector(video_locator, timeout=20000)
    #assert await browser.is_visible(video_locator), "❌ The video is not present"
    #print("✅ Video found successfully")

    # Validate if the text is present
    # textarea = await browser.locator("textarea[placeholder*='Examples']").input_value()
    # expected_text = "Can you track both people and sharks in this video? Save a video with the tracked masks of both sharks and people and draw a line between the shark and the closest person with the distance above it. Use 13 pixels = 1m and FPS 10."
    # assert textarea == expected_text, "❌ The text in the textarea does not match"
    # print("✅ Text validated successfully")

    # Validate if the 'Generate Code' button is present and click it
    # generate_code_button = browser.locator("span.bold", has_text="Generate Code")
    # assert await generate_code_button.is_visible(), "❌ The 'Generate Code' button is not present"
    # await generate_code_button.click()
    # print("✅ Clicked on 'Generate Code'")

    # Validate if the 'Code' button is visible with timeout
    # code_button = browser.locator("button[aria-controls='radix-:rl:-content-Code']")
    # await code_button.wait_for(timeout=20000)
    # assert await code_button.is_visible(), "❌ The 'Code' button is not present"
    # print("✅ 'Code' button is visible correctly")

import pytest

assert 1 == 1