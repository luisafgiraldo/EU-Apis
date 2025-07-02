import os
import pytest
import env
import time
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import pyautogui

@pytest.fixture(scope="function")
def browser():
    screen_width, screen_height = pyautogui.size()  # Get screen size
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": screen_width, "height": screen_height})
        yield context
        browser.close()


def compare_images(img1_path, img2_path):
    """Compares two images and checks if they are similar within a threshold."""
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")
    diff = ImageChops.difference(img1, img2)
    diff_bbox = diff.getbbox()
    return diff_bbox is None  # Returns True if there are no significant differences


def login(browser):
    """Performs login and returns the loaded page."""
    page = browser.new_page()
    page.goto(env.URL, timeout=60000)

    # Perform login
    page.fill("input[name='identifier']", env.USERNAME)
    page.get_by_role("button", name="Sign in").click()
    page.fill("input[name='password']", env.PASSWORD)
    page.get_by_role("button", name="Continue").click()
    print("✅ Successful login")
    
    return page  # Return the page to reuse it

def navigate_to_explore_apis(page):
    """Navigates to the 'Explore APIs' section after login."""
    page.wait_for_selector("div:text('What vision task do you have in mind?')", timeout=10000)
    page.get_by_role("button", name="Explore APIs").click()
    print("✅ Clicked on 'Explore APIs'")
    

def navigate_tool(page, tool):
    """Navigates to the 'Agentic Object Detection' option."""
# Espera el div con el texto del nombre del tool (ya no es <p>, ahora es <div class="text-2xl font-semibold">)
    page.wait_for_selector(f"div.text-2xl.font-semibold:text('{tool}')", timeout=10000)

    # Hace clic sobre la tarjeta completa que contiene ese título
    tool_card = page.locator(f"div:has(div.text-2xl.font-semibold:text('{tool}'))").first
    tool_card.click()

    print(f"✅ Clicked on '{tool}'")

    # Confirmamos que el nombre aparece en la vista que carga
    page.wait_for_selector(f"div:text('{tool}')", timeout=10000)
    print(f"✅ Successful validation: '{tool}' is visible")

def click_image(page, element_name):
    """Clicks on the image of the specified element."""
    page.wait_for_selector(f"div.relative.flex.size-full img[alt='{element_name}']", timeout=10000)
    page.locator(f"div.relative.flex.size-full img[alt='{element_name}']").click(force=True)
    print(f"✅ Clicked on the {element_name}")

    # Wait for the PromptTips element to appear
    page.wait_for_selector("div[data-sentry-component='PromptTips']", timeout=10000)
    print("✅ PromptTips element is visible")

    # Click the green button
    page.wait_for_selector("button.bg-green-500")
    page.locator("button.bg-green-500").click()
    print("✅ Click en botón verde")

def time_step(iterator : int):
    return time.sleep(iterator)


def remove_image(image_path):
    """Removes an image if the user confirms."""
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"✅ File deleted: {image_path}")
    else:
        print(f"⚠️ File does not exist: {image_path}")

