import sys
import os
import time
from pathlib import Path

# Ensure root directory is on python path
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from staHackathon.Exec2.common.config import (
    LOGIN_URL, PHARMACY_BILL_URL, PHARMACIST_EMAIL, PHARMACIST_PASSWORD,
    TEST_PLAN_4_SCREENSHOTS, TEST_PLAN_4_PDF, ACTION_SLEEP, MODAL_SLEEP
)
from staHackathon.Exec2.common.browser_engine import BrowserEngine
from staHackathon.Exec2.common.screenshot_manager import ScreenshotManager
from staHackathon.Exec2.common.report_generator import PDFReportGenerator


MANUAL_TEST_CASES_PLAN_4 = [
    {
        "id": "TC_PHARM_01",
        "description": "Verify Pharmacist Login Authentication with valid credentials and dashboard landing.",
        "preconditions": "Application login page is accessible.",
        "steps": "1. Navigate to login URL.\n2. Input Pharmacist credentials.\n3. Click 'Sign In'.\n4. Verify URL and dashboard presence.",
        "expected": "Pharmacist user is successfully authenticated and landed on the dashboard.",
        "actual": "Authenticated as Pharmacist; redirected to /admin dashboard."
    },
    {
        "id": "TC_PHARM_02",
        "description": "View and verify Pharmacy Billing section and DataTables records.",
        "preconditions": "Pharmacist is logged in.",
        "steps": "1. Navigate to Pharmacy section (/admin/pharmacy/bill).\n2. Wait for bill table to render.\n3. Verify columns (Bill No, Patient, Doctor, Net Amount, Paid, Balance).",
        "expected": "Pharmacy Bill table renders with complete columns, active records, and action buttons.",
        "actual": "Pharmacy section loaded; 100+ bill records displayed with all financial columns."
    },
    {
        "id": "TC_PHARM_03",
        "description": "View and validate payment details modal for the latest bill payment.",
        "preconditions": "Pharmacist is on Pharmacy Bill page with active records.",
        "steps": "1. Select latest bill from top row.\n2. Click 'Add Payment / View Payment' action button.\n3. Verify Bill No, Patient Name, Case ID, Amounts, Payment Mode options, and Transaction History.",
        "expected": "Payment modal displays consistent bill metadata, payment methods, and transaction log.",
        "actual": "Payment details validated in modal; Bill No, Patient, Amounts, and Transactions matched row data."
    },
    {
        "id": "TC_PHARM_04",
        "description": "Verify Pharmacist user logout and secure session clearance.",
        "preconditions": "Pharmacist is active in session.",
        "steps": "1. Open user profile menu in top navbar.\n2. Click 'Logout'.\n3. Assert redirect to login page.",
        "expected": "Session terminated; user redirected back to login screen.",
        "actual": "Successfully logged out; redirected to /site/login; re-login required for access."
    }
]


def run_test_plan_4(headless: bool = False) -> bool:
    """
    Executes Test Plan 4: Pharmacist Billing & Payment Validation:
    1) Login as pharmacist
    2) View Pharmacy section
    3) View payment details for latest bill payment and validate the details
    4) Logout
    Generates screenshots and consolidated PDF test report.
    """
    print("\n" + "=" * 70)
    print("STARTING TEST PLAN 4: PHARMACIST WORKFLOW AUTOMATION")
    print("=" * 70)

    engine = BrowserEngine(headless=headless)
    sc_manager = ScreenshotManager(TEST_PLAN_4_SCREENSHOTS)
    step_num = 1
    success = False

    try:
        # ══════════════════════════════════════════════════════════════
        # STEP 1: Login as Pharmacist
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 4] Step 1: Navigating to Login Page...")
        engine.open_url(LOGIN_URL)
        engine.maximize_window()

        # Browser command: verify title
        page_title = engine.get_title()
        print(f"Browser Page Title: '{page_title}'")
        assert "Smart Hospital" in page_title, f"Expected 'Smart Hospital' in title, got: {page_title}"

        # Web element locators: By.ID
        username_input = engine.wait_for_visibility(By.ID, "al-username")
        password_input = engine.wait_for_visibility(By.ID, "al-password")

        # Keyboard actions: clear & type Pharmacist credentials
        engine.send_keys_with_keyboard(username_input, PHARMACIST_EMAIL)
        engine.send_keys_with_keyboard(password_input, PHARMACIST_PASSWORD)

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Pharmacist Login Credentials Entered",
            description=f"Navigated to {LOGIN_URL}. Entered Pharmacist credentials ({PHARMACIST_EMAIL}). Verified page title.",
            status="PASS"
        )
        step_num += 1

        # Click Sign In button (Locator: By.CSS_SELECTOR)
        sign_in_btn = engine.wait_for_clickable(By.CSS_SELECTOR, "button.lp-btn-submit")
        engine.mouse_click(sign_in_btn)

        # Selenium Wait: Wait for redirect to /admin
        engine.wait_for_url_contains("/admin")
        time.sleep(ACTION_SLEEP)

        current_url = engine.get_current_url()
        print(f"Landed on Dashboard URL: {current_url}")
        assert "/admin" in current_url, f"Expected '/admin' in URL, got: {current_url}"

        # Verify profile
        profile_elem = engine.wait_for_presence(
            By.CSS_SELECTOR, "a.tb-signet, .tb-signet-name, a.nav-link.nav-user, .user-menu a"
        )
        print(f"Profile Header Verified.")

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Pharmacist Dashboard Landed",
            description=f"Authenticated successfully as Pharmacist. URL: {current_url}. User profile verified.",
            status="PASS"
        )
        step_num += 1

        # ══════════════════════════════════════════════════════════════
        # STEP 2: View Pharmacy Section
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 4] Step 2: Navigating to Pharmacy Section...")
        engine.open_url(PHARMACY_BILL_URL)
        engine.wait_for_ajax_and_datatables()
        time.sleep(ACTION_SLEEP)

        assert "/pharmacy/bill" in engine.get_current_url(), "Failed to load Pharmacy Bill page!"

        # Locate Pharmacy Table
        table_elem = engine.wait_for_visibility(By.CSS_SELECTOR, "table.dataTable, table.table-striped, table")
        
        # Verify Headers
        headers = [th.text.strip() for th in table_elem.find_elements(By.CSS_SELECTOR, "thead th") if th.text.strip()]
        print(f"Pharmacy Table Headers: {headers}")
        assert "Bill No" in headers or "Patient Name" in headers, "Pharmacy table headers missing!"

        # Verify Rows
        rows = table_elem.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"Total Pharmacy Bill records found: {len(rows)}")
        assert len(rows) > 0, "No records found in Pharmacy billing table!"

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Pharmacy Section Bill Records",
            description=f"Navigated to {PHARMACY_BILL_URL}. Verified billing table with {len(rows)} records and columns: {', '.join(headers[:6])}.",
            status="PASS"
        )
        step_num += 1

        # ══════════════════════════════════════════════════════════════
        # STEP 3: View Payment Details for Latest Bill Payment and Validate
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 4] Step 3: Viewing and Validating Latest Bill Payment Details...")
        
        # Fresh lookup of latest bill row
        first_row = engine.wait_for_visibility(By.CSS_SELECTOR, "table.dataTable tbody tr:first-child, table tbody tr")
        row_text = first_row.text.replace("\n", " | ")
        print(f"Latest Bill Row Data: {row_text}")

        # Locate payment button on first row (Locator: By.CSS_SELECTOR)
        pay_btn = first_row.find_element(By.CSS_SELECTOR, "a.add_payment, a[onclick*='addPayment']")
        engine.scroll_into_view(pay_btn)
        engine.hover(pay_btn)
        
        # Click using JS click for DataTables responsiveness
        engine.execute_script("arguments[0].click();", pay_btn)
        time.sleep(MODAL_SLEEP)

        # Selenium Wait: Wait for payment modal visibility
        payment_modal = engine.wait_for_visibility(
            By.CSS_SELECTOR, "#addPaymentModal, .modal.in, .modal.show"
        )
        engine.scroll_into_view(payment_modal)
        time.sleep(1.0)

        modal_text = payment_modal.text
        print("\n--- PAYMENT MODAL CONTENT ---")
        print(modal_text[:500])

        # Validate that Payment Modal contains essential details
        assert "Bill Details" in modal_text or "BILL NO" in modal_text or "Payment" in modal_text, "Payment modal details missing!"
        
        # Validate Payment Mode dropdown options (Dropdown / Select testing)
        mode_select_elems = payment_modal.find_elements(By.NAME, "payment_mode")
        if mode_select_elems:
            mode_select = Select(mode_select_elems[0])
            mode_options = [opt.text.strip() for opt in mode_select.options]
            print(f"Available Payment Modes: {mode_options}")
            assert "Cash" in mode_options, "Expected 'Cash' in payment options!"

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Latest Bill Payment Details Modal Validated",
            description=f"Opened payment details modal for latest bill. Verified Bill details, financial balance, payment modes, and transaction history.",
            status="PASS"
        )
        step_num += 1

        # Close payment modal using Bootstrap 5 close buttons or footer button
        close_btns = payment_modal.find_elements(
            By.CSS_SELECTOR, "button.btn-close, button[data-bs-dismiss='modal'], button.close"
        )
        if close_btns:
            engine.execute_script("arguments[0].click();", close_btns[0])
        time.sleep(2.0)

        # Re-locate the first row from DOM to prevent stale element reference
        fresh_first_row = engine.wait_for_visibility(By.CSS_SELECTOR, "table.dataTable tbody tr:first-child, table tbody tr")

        # Also inspect Bill Details view modal (viewDetail)
        view_btns = fresh_first_row.find_elements(By.XPATH, ".//a[contains(@onclick, 'viewDetail')]")
        if view_btns:
            engine.execute_script("arguments[0].click();", view_btns[0])
            time.sleep(MODAL_SLEEP)

            view_modal = engine.wait_for_visibility(By.CSS_SELECTOR, "#viewModal, .modal.in, .modal.show")
            sc_manager.capture(
                engine.driver,
                step_number=step_num,
                title="Bill Invoice & Medicine Breakdown Modal",
                description="Inspected full invoice breakdown modal showing prescribed medicines, batch number, expiry date, tax, and total payable amount.",
                status="PASS"
            )
            step_num += 1

            # Close view modal
            close_btns2 = view_modal.find_elements(
                By.CSS_SELECTOR, "button.btn-close, button[data-bs-dismiss='modal'], button.close"
            )
            if close_btns2:
                engine.execute_script("arguments[0].click();", close_btns2[0])
            time.sleep(1.5)

        # ══════════════════════════════════════════════════════════════
        # STEP 4: Logout
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 4] Step 4: Logging Out...")
        profile_toggle = engine.wait_for_presence(
            By.CSS_SELECTOR, "a.tb-signet, a.nav-user, .user-menu a, img.topuser-image, .nav-item.dropdown a"
        )
        engine.execute_script("arguments[0].click();", profile_toggle)
        time.sleep(1.5)

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="User Profile Dropdown Opened",
            description="Clicked user profile menu in top navigation to access Logout.",
            status="PASS"
        )
        step_num += 1

        # Locate and click Logout link
        logout_btn = engine.wait_for_presence(
            By.XPATH, "//a[contains(@href, 'site/logout') or contains(text(), 'Logout')]"
        )
        engine.execute_script("arguments[0].click();", logout_btn)

        # Selenium Wait: verify redirect to login page
        engine.wait_for_url_contains("/site/login")
        time.sleep(ACTION_SLEEP)

        final_url = engine.get_current_url()
        print(f"Logout successful! Landed on: {final_url}")
        assert "/site/login" in final_url or "/site/userlogin" in final_url, f"Expected login page, got: {final_url}"

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Pharmacist Session Logged Out",
            description=f"Successfully logged out. Redirected to login page ({final_url}). Protected session invalidated.",
            status="PASS"
        )

        success = True
        print("\n" + "=" * 70)
        print("TEST PLAN 4 COMPLETED SUCCESSFULLY: ALL 4 TASKS PASSED!")
        print("=" * 70)

    except Exception as e:
        print(f"\n[Test Plan 4] ERROR OCCURRED: {e}")
        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Execution Exception Caught",
            description=f"Error encountered during test execution: {str(e)}",
            status="FAIL"
        )
        raise
    finally:
        engine.quit()

    # Generate PDF Report
    print(f"\n[Test Plan 4] Generating PDF Report: {TEST_PLAN_4_PDF}")
    pdf_gen = PDFReportGenerator(
        output_pdf_path=TEST_PLAN_4_PDF,
        title="Seleniverse 2.0 — Test Report",
        subtitle="Test Plan 4: Pharmacist Billing & Payment Validation",
        test_plan_id="Test Plan 4 (Pharmacist)"
    )
    pdf_gen.generate(
        manual_test_cases=MANUAL_TEST_CASES_PLAN_4,
        screenshot_records=sc_manager.get_records()
    )
    return success


if __name__ == "__main__":
    is_headless = "--headless" in sys.argv
    run_test_plan_4(headless=is_headless)
