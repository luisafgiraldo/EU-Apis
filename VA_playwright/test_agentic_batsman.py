import env
import utils as u
from utils import browser

TOOL_NAME = "Agentic Object Detection"


def test_agentic_object_detection(browser):
    """Runs the test for all elements in env.ELEMENTS_OD in a for loop."""

    # Log in
    page = u.login(browser)

    # Navigate to the API
    u.navigate_tool(page, TOOL_NAME)

    # Iterate over each test element
    for element in env.ELEMENTS_OD:
        print(f"🔍 Testing with element: {element}")

        # Wait for the page to fully load before each interaction
        page.wait_for_load_state("networkidle")

        # Try clicking on the image
        try:
            img_selector = f"img[alt*='{element}']"
            page.wait_for_selector(img_selector, timeout=20000)
            u.click_image(page, element)
        except Exception as e:
            print(f"⚠️ image '{element}' not found: {e}")
            continue  # Skip to the next element in the list

        print("⏳ Waiting 50 seconds...")
        u.time_step(50)

        # Define the path of the captured image
        captured_image_path = env.CAPTURED_IMAGE_PATH.format(element.replace(" ", "_"))

        # Capture a screenshot of the SVG element
        svg_element = page.locator("svg.relative.size-full")
        svg_element.screenshot(path=captured_image_path)
        print(f"📸 Screenshot saved: {captured_image_path}")

        # Get the correct reference image
        reference_image_path = env.REFERENCES_OD.get(element)
        
        result = u.compare_images(captured_image_path, reference_image_path)
        print(result)
        if result:
            print("Entering")
            print("✅ Images match")
            # Option to delete the captured image
            u.remove_image(captured_image_path)
        else:
            print("❌ Images are different")
        # 🔄 Reload the browser after processing each image
        print("🔄 Reloading the page for the next element...")
        page.reload()
