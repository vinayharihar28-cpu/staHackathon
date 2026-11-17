import time
from typing import List, Optional, Tuple, Union
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import sys
from pathlib import Path

# Ensure Exec2 directory is in sys.path
_base_dir = Path(__file__).resolve().parent.parent
if str(_base_dir) not in sys.path:
    sys.path.insert(0, str(_base_dir))

from common.config import DEFAULT_EXPLICIT_WAIT, IMPLICIT_WAIT, ACTION_SLEEP


class BrowserEngine:
    """
    Robust Browser Automation Engine implementing:
    - Standard browser commands (get, title, current_url, maximize, refresh, back, forward, quit)
    - Explicit and Implicit Selenium waits
    - Mouse actions (hover, click, double click, right click via ActionChains)
    - Keyboard actions (Keys.ENTER, Keys.TAB, Keys.CONTROL, Keys.BACKSPACE)
    - Web element locators (ID, NAME, XPATH, CSS_SELECTOR, CLASS_NAME, TAG_NAME, LINK_TEXT)
    - Dynamic loading elements synchronization
    - UI control handlers (buttons, checkboxes, labels, lists/dropdowns, textboxes, frames)
    - Smooth scrolling and JavaScript execution fallbacks
    """

    def __init__(self, headless: bool = False, window_width: int = 1920, window_height: int = 1080):
        self.headless = headless
        self.window_width = window_width
        self.window_height = window_height
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self._init_driver()

    def _init_driver(self):
        """Initializes ChromeDriver with optimized options."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        self.wait = WebDriverWait(self.driver, DEFAULT_EXPLICIT_WAIT)

    # ══════════════════════════════════════════════════════════════════
    # 1. BROWSER COMMANDS
    # ══════════════════════════════════════════════════════════════════
    def open_url(self, url: str):
        """Navigate to the specified URL (Browser Command)."""
        print(f"[BrowserEngine] Navigating to: {url}")
        self.driver.get(url)
        time.sleep(ACTION_SLEEP)

    def maximize_window(self):
        """Maximize the browser window (Browser Command)."""
        self.driver.maximize_window()

    def set_window_size(self, width: int, height: int):
        """Set specific browser window dimensions (Browser Command)."""
        self.driver.set_window_size(width, height)

    def get_title(self) -> str:
        """Retrieve current page title (Browser Command)."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Retrieve current browser URL (Browser Command)."""
        return self.driver.current_url

    def get_page_source(self) -> str:
        """Retrieve complete page DOM HTML (Browser Command)."""
        return self.driver.page_source

    def refresh(self):
        """Refresh current page (Browser Command)."""
        print("[BrowserEngine] Refreshing page...")
        self.driver.refresh()
        time.sleep(ACTION_SLEEP)

    def back(self):
        """Navigate back in browser history (Browser Command)."""
        print("[BrowserEngine] Navigating back...")
        self.driver.back()
        time.sleep(ACTION_SLEEP)

    def forward(self):
        """Navigate forward in browser history (Browser Command)."""
        print("[BrowserEngine] Navigating forward...")
        self.driver.forward()
        time.sleep(ACTION_SLEEP)

    def quit(self):
        """Close all windows and safely terminate driver session (Browser Command)."""
        if self.driver:
            print("[BrowserEngine] Terminating browser session.")
            self.driver.quit()
            self.driver = None

    # ══════════════════════════════════════════════════════════════════
    # 2. SELENIUM WAIT MECHANISMS & LOADING ELEMENTS
    # ══════════════════════════════════════════════════════════════════
    def wait_for_presence(self, by: By, value: str, timeout: int = DEFAULT_EXPLICIT_WAIT) -> WebElement:
        """Explicit wait for element presence in DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def wait_for_visibility(self, by: By, value: str, timeout: int = DEFAULT_EXPLICIT_WAIT) -> WebElement:
        """Explicit wait for element to become visible on page."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )

    def wait_for_clickable(self, by: By, value: str, timeout: int = DEFAULT_EXPLICIT_WAIT) -> WebElement:
        """Explicit wait for element to be clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def wait_for_url_contains(self, partial_url: str, timeout: int = DEFAULT_EXPLICIT_WAIT) -> bool:
        """Explicit wait until the URL contains the expected substring."""
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url)
        )

    def wait_for_invisibility(self, by: By, value: str, timeout: int = DEFAULT_EXPLICIT_WAIT) -> bool:
        """Wait until a loading spinner, overlay, or element becomes invisible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, value))
        )

    def wait_for_ajax_and_datatables(self, timeout: int = 10):
        """Wait for jQuery/DataTables processing indicators to finish."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return (typeof jQuery === 'undefined' || jQuery.active === 0);")
            )
        except Exception:
            pass
        time.sleep(1.0)

    # ══════════════════════════════════════════════════════════════════
    # 3. PAGE SCROLLING & SCRIPT EXECUTION
    # ══════════════════════════════════════════════════════════════════
    def execute_script(self, script: str, *args):
        """Execute custom JavaScript in the browser context."""
        return self.driver.execute_script(script, *args)

    def scroll_into_view(self, element: WebElement):
        """Scroll element smoothly into the viewport center."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
            element
        )
        time.sleep(1.0)

    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    # ══════════════════════════════════════════════════════════════════
    # 4. MOUSE ACTIONS (ActionChains)
    # ══════════════════════════════════════════════════════════════════
    def hover(self, element: WebElement):
        """Hover mouse over the element using ActionChains."""
        self.scroll_into_view(element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(0.5)

    def mouse_click(self, element: WebElement):
        """Perform mouse click using ActionChains."""
        self.scroll_into_view(element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
        time.sleep(ACTION_SLEEP)

    def double_click(self, element: WebElement):
        """Perform mouse double click using ActionChains."""
        self.scroll_into_view(element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).double_click().perform()
        time.sleep(ACTION_SLEEP)

    def context_click(self, element: WebElement):
        """Perform right click (context click) using ActionChains."""
        self.scroll_into_view(element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).context_click().perform()
        time.sleep(ACTION_SLEEP)

    # ══════════════════════════════════════════════════════════════════
    # 5. KEYBOARD ACTIONS
    # ══════════════════════════════════════════════════════════════════
    def send_keys_with_keyboard(self, element: WebElement, text: str, press_enter: bool = False):
        """Clear textbox using Ctrl+A + Backspace and type text using keyboard commands."""
        self.scroll_into_view(element)
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        time.sleep(0.3)
        element.send_keys(text)
        if press_enter:
            element.send_keys(Keys.ENTER)
        time.sleep(ACTION_SLEEP)

    def press_escape(self):
        """Send Escape key to close open popups or tooltips."""
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)

    # ══════════════════════════════════════════════════════════════════
    # 6. WEB ELEMENT LOCATORS & INTERACTION HELPERS
    # ══════════════════════════════════════════════════════════════════
    def find_element(self, by: By, value: str) -> WebElement:
        """Find single element using any locator strategy."""
        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Find multiple elements using any locator strategy."""
        return self.driver.find_elements(by, value)

    def click_button(self, by: By, value: str, use_js_fallback: bool = True) -> WebElement:
        """
        Locates button, scrolls into view, waits until clickable,
        and clicks with graceful JavaScript fallback.
        """
        elem = self.wait_for_clickable(by, value)
        self.scroll_into_view(elem)
        try:
            elem.click()
        except Exception:
            if use_js_fallback:
                print(f"[BrowserEngine] Standard click intercepted on ({by}, {value}), falling back to JS click.")
                self.driver.execute_script("arguments[0].click();", elem)
            else:
                raise
        time.sleep(ACTION_SLEEP)
        return elem

    def type_into_textbox(self, by: By, value: str, text: str, clear_first: bool = True) -> WebElement:
        """Locates textbox, clears contents, and types input string."""
        elem = self.wait_for_visibility(by, value)
        self.scroll_into_view(elem)
        if clear_first:
            elem.click()
            elem.send_keys(Keys.CONTROL + "a")
            elem.send_keys(Keys.BACKSPACE)
            elem.clear()
        elem.send_keys(text)
        time.sleep(1.0)
        return elem

    def get_label_or_text(self, by: By, value: str) -> str:
        """Retrieves text content from a label, heading, or element."""
        elem = self.wait_for_presence(by, value)
        return elem.text.strip()

    def set_checkbox(self, by: By, value: str, checked: bool = True) -> WebElement:
        """Checks or unchecks a checkbox element."""
        elem = self.wait_for_presence(by, value)
        self.scroll_into_view(elem)
        is_selected = elem.is_selected()
        if (checked and not is_selected) or (not checked and is_selected):
            try:
                elem.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elem)
            time.sleep(ACTION_SLEEP)
        return elem

    def select_dropdown_by_text(self, by: By, value: str, option_text: str):
        """Selects an option from a <select> element by visible text."""
        elem = self.wait_for_presence(by, value)
        self.scroll_into_view(elem)
        select = Select(elem)
        select.select_by_visible_text(option_text)
        time.sleep(ACTION_SLEEP)

    def select_dropdown_by_value(self, by: By, value: str, option_val: str):
        """Selects an option from a <select> element by value."""
        elem = self.wait_for_presence(by, value)
        self.scroll_into_view(elem)
        select = Select(elem)
        select.select_by_value(option_val)
        time.sleep(ACTION_SLEEP)

    def get_dropdown_options(self, by: By, value: str) -> List[str]:
        """Returns all option labels from a <select> dropdown list."""
        elem = self.wait_for_presence(by, value)
        select = Select(elem)
        return [opt.text.strip() for opt in select.options]

    # ══════════════════════════════════════════════════════════════════
    # 7. FRAMES (IFRAMES) HANDLING
    # ══════════════════════════════════════════════════════════════════
    def switch_to_frame_safely(self, frame_reference: Union[int, str, WebElement]) -> bool:
        """Switches to an iframe by index, name/id, or WebElement."""
        try:
            self.driver.switch_to.frame(frame_reference)
            return True
        except Exception as e:
            print(f"[BrowserEngine] Could not switch to frame: {e}")
            return False

    def switch_to_default_content(self):
        """Switches back from an iframe to the main document context."""
        self.driver.switch_to.default_content()
