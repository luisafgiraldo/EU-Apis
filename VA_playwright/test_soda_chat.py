import utils as u
import os
from datetime import datetime
import base64
from utils import browser, login
from playwright.sync_api import sync_playwright, expect

def test_soda_chats(browser):
    """Test example chats and validate responses."""
    # Log in
    page = u.login(browser)

    try:
        # Wait 5 sec after login
        page.wait_for_timeout(5000)

        # Scroll and click on 'Try VisionAgent'
        span_locator = page.locator("span:has-text('Try VisionAgent')")
        span_locator.scroll_into_view_if_needed()
        span_locator.click(force=True)
        print("✅ Scroll y clic en el span 'Try VisionAgent'")

        # Validate if login was successful
        page.wait_for_selector("div:text('What vision task do you have in mind?')", timeout=10000)
        print("✅ Successful login and page loaded correctly")

        # Scroll before clicking on the 3rd example
        page.locator("div[data-testid='prompt-examples-2']").scroll_into_view_if_needed()
        page.locator("div[data-testid='prompt-examples-2']").click(force=True)
        print("✅ Clicked on chat: Soda Can Counting and Inventory Status")

        # Validate if the image is visible
        page.wait_for_selector("img[src*='cola.jpeg']", timeout=30000)
        print("✅ Image is visible")

        # Validate if the textarea is visible
        page.wait_for_selector("textarea[placeholder*='Examples: Detect the dogs in the image, count the number of red cars in the video, identify the logos in the image.']", timeout=10000)
        print("✅ Textarea is visible")

        # Click on the 'Generate Code' button
        page.locator("button:has(span.bold:has-text('Generate Code'))").click(force=True)
        print("✅ Clicked on 'Generate Code'")

        # Validate if the 'Code' tab is visible
        page.wait_for_selector("button[role='tab'][aria-selected='true'][aria-controls*='Code']", timeout=10000)
        print("✅ Code' tab is visible")

        # Validate if the expected text is visible
        expected_text = '''Write a program that counts soda cans in an image. The program should output the count, draw bounding boxes around each detected can, and display the confidence score for each prediction. Additionally, calculate the inventory percentage based on a maximum capacity of 35 cans. If the inventory is below 50%, the program should output a status of "Needs Restocking." If the inventory is above 50%, it should output a status of "Healthy."'''
        page.wait_for_selector(f"p:text('{expected_text}')", timeout=10000)
        print("✅ Expected text is visible")

        # Validate if the 'Conversation' element is visible
        page.wait_for_selector("div:has-text('Conversation')", timeout=20000)
        print("✅ Conversation' element is visible")

        # Wait for 6 and a half minutes
        page.wait_for_timeout(390000)
        print("⏱️ Waited for 6 and a half minutes")

        # Validate if the 'Code Output' tab is visible
        page.wait_for_selector("button[role='tab'][aria-selected='true'][aria-controls*='Code Output']", timeout=20000)
        print("✅ 'Code Output' tab is visible")

        # Validate if the element containing 'import os' is visible
        page.wait_for_selector("div.view-line:has(span:has-text('import os'))", timeout=300000)
        assert page.is_visible("div.view-line:has(span:has-text('import os'))"), "❌ Error: The 'Code Output' content is not as expected."
        print("✅ Part of the 'Code Output' content validated successfully")

        # Validate if the new element is visible with the expected text
        page.wait_for_selector("div.w-full.flex-1.overflow-hidden.rounded-md.rounded-b-none.bg-blue-gray-900.p-2.pb-0", timeout=20000)
        assert page.is_visible("div.w-full.flex-1.overflow-hidden.rounded-md.rounded-b-none.bg-blue-gray-900.p-2.pb-0"), "❌ Error: The element is not visible."
        print("✅ Element is visible with the expected text")

        # Validate if the 'Deploy' button is visible
        page.wait_for_selector("button[data-testid='code-deploy-button']", timeout=10000)
        assert page.is_visible("button[data-testid='code-deploy-button']"), "❌ Error: The 'Deploy' button is not visible."
        print("✅ 'Deploy' button is visible")

        page.screenshot(path=os.path.join("VA_playwright", "CaptureImages", "captured_soda_chat.png"), full_page=True)
        print("📸 Screenshot saved successfully")

    except Exception as e:
        # Ruta y timestamp
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{timestamp}_test_soda_chats_failed.png"
        screenshot_dir = os.path.join("VA_playwright", "Failed test")
        screenshot_path = os.path.join(screenshot_dir, filename)

        # Solo crear carpeta si no existe
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Captura de pantalla
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"❌ Test failed. Screenshot saved at: {screenshot_path}")

        # Convertir imagen a base64
        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Crear archivo HTML con imagen y error
        html_content = f"""
        <html>
            <head><title>Test Failed Report</title></head>
            <body style="font-family:sans-serif;">
                <h2 style="color:red;">❌ Test Failed</h2>
                <p><strong>Test:</strong> test_soda_chats</p>
                <p><strong>Timestamp:</strong> {timestamp}</p>
                <p><strong>Error:</strong> {str(e)}</p>
                <h3>Screenshot:</h3>
                <img src="data:image/png;base64,{encoded_string}" alt="Failed Screenshot" style="max-width:100%;">
            </body>
        </html>
        """

        html_path = os.path.join(screenshot_dir, f"{timestamp}_test_soda_chats_report.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"📝 HTML report saved at: {html_path}")

        # Re-lanzar la excepción
        raise e
