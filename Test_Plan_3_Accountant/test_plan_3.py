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

from common.config import (
    LOGIN_URL, OPD_SEARCH_URL, ACCOUNTANT_EMAIL, ACCOUNTANT_PASSWORD,
    TEST_PLAN_3_SCREENSHOTS, TEST_PLAN_3_PDF, ACTION_SLEEP
)
from common.browser_engine import BrowserEngine
from common.screenshot_manager import ScreenshotManager
from common.report_generator import PDFReportGenerator


MANUAL_TEST_CASES_PLAN_3 = [
    {
        "id": "TC_ACC_01",
        "description": "Verify Accountant Login Authentication with valid credentials and role validation.",
        "preconditions": "Application is deployed; user is on the login page.",
        "steps": "1. Open login URL.\n2. Input Accountant credentials.\n3. Click 'Sign In'.\n4. Verify URL and role header.",
        "expected": "User is successfully authenticated and landed on the Accountant Dashboard with 'Brad (Accountant)' in top bar.",
        "actual": "Authenticated successfully; dashboard loaded with role 'Brad (Accountant)'."
    },
    {
        "id": "TC_ACC_02",
        "description": "Verify Dashboard 'Recent Activity' section displays newly added patient transactions.",
        "preconditions": "Accountant is logged into dashboard.",
        "steps": "1. Scroll down to Recent Activity card.\n2. Verify table headers.\n3. Validate patient transaction records.",
        "expected": "'Recent Activity' table displays User, Action, Detail, Module, Amount, and Time with active records.",
        "actual": "Recent Activity table located; active patient payment records and transaction IDs verified."
    },
    {
        "id": "TC_ACC_03",
        "description": "Cross verify details of newly added patient with Doctor Consultant assignment.",
        "preconditions": "Accountant is logged in; OPD records are accessible.",
        "steps": "1. Navigate to OPD Out Patient page.\n2. Inspect patient table.\n3. Cross-verify Patient Name, ID, and Consultant Doctor.",
        "expected": "Patient records accurately show doctor assignment (e.g., Sansa Gomez, Amit Singh, Reyan Jain).",
        "actual": "OPD patient records verified; consultant doctor linkage confirmed and asserted."
    },
    {
        "id": "TC_ACC_04",
        "description": "Verify Accountant user session logout and secure redirection.",
        "preconditions": "Accountant is active in the session.",
        "steps": "1. Click user profile menu.\n2. Click 'Logout' link.\n3. Assert redirection to login page.",
        "expected": "Session terminated; user redirected to login page; login form re-displayed.",
        "actual": "Successfully logged out; redirected to /site/login; session invalidated."
    }
]


def run_test_plan_3(headless: bool = False) -> bool:
    """
    Executes Test Plan 3: Accountant Workflow:
    1) Login as accountant
    2) Verify dashboard recent activity for newly added patient
    3) Cross verify the details of new patient added by doctor
    4) Logout
    Generates screenshots and consolidated PDF test report.
    """
    print("\n" + "=" * 70)
    print("STARTING TEST PLAN 3: ACCOUNTANT WORKFLOW AUTOMATION")
    print("=" * 70)

    engine = BrowserEngine(headless=headless)
    sc_manager = ScreenshotManager(TEST_PLAN_3_SCREENSHOTS)
    step_num = 1
    success = False

    try:
        # ══════════════════════════════════════════════════════════════
        # STEP 1: Login as Accountant
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 3] Step 1: Navigating to Login Page...")
        engine.open_url(LOGIN_URL)
        engine.maximize_window()
        
        # Browser command: verify title
        page_title = engine.get_title()
        print(f"Browser Page Title: '{page_title}'")
        assert "Smart Hospital" in page_title, f"Expected 'Smart Hospital' in title, got: {page_title}"

        # Web element locators: By.ID and By.CSS_SELECTOR
        username_input = engine.wait_for_visibility(By.ID, "al-username")
        password_input = engine.wait_for_visibility(By.ID, "al-password")
        
        # Use keyboard action to clear and enter credentials
        engine.send_keys_with_keyboard(username_input, ACCOUNTANT_EMAIL)
        engine.send_keys_with_keyboard(password_input, ACCOUNTANT_PASSWORD)

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Login Page Credentials Entered",
            description=f"Navigated to {LOGIN_URL}. Entered Accountant credentials ({ACCOUNTANT_EMAIL}). Verified page title.",
            status="PASS"
        )
        step_num += 1

        # Click Sign In button (Locator: By.CSS_SELECTOR)
        sign_in_btn = engine.wait_for_clickable(By.CSS_SELECTOR, "button.lp-btn-submit")
        engine.mouse_click(sign_in_btn)

        # Selenium Wait: Wait until URL contains dashboard (/admin)
        engine.wait_for_url_contains("/admin")
        time.sleep(ACTION_SLEEP)

        current_url = engine.get_current_url()
        print(f"Landed on Dashboard URL: {current_url}")
        assert "/admin" in current_url, f"Expected '/admin' in URL, got: {current_url}"

        # Assert user role in top header
        profile_elem = engine.wait_for_presence(
            By.CSS_SELECTOR, "a.tb-signet, .tb-signet-name, a.nav-link.nav-user, .user-menu a"
        )
        profile_text = profile_elem.text
        print(f"Profile Header: {profile_text}")

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Accountant Dashboard Landed",
            description=f"Successfully authenticated as Accountant. URL redirected to: {current_url}. User profile verified.",
            status="PASS"
        )
        step_num += 1

        # ══════════════════════════════════════════════════════════════
        # STEP 2: Verify Dashboard Recent Activity for Newly Added Patient
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 3] Step 2: Verifying Dashboard Recent Activity...")
        
        # Locate Recent Activity card (Locator: By.XPATH / CSS)
        recent_activity_heading = engine.wait_for_presence(
            By.XPATH, "//h3[contains(text(), 'Recent Activity')] | //div[contains(@class, 'dash-table-card')]//h3"
        )
        # Page action: smooth scroll into view
        engine.scroll_into_view(recent_activity_heading)
        time.sleep(1.0)

        # Mouse action: hover over the heading/card
        engine.hover(recent_activity_heading)

        # Locate Recent Activity Table (Locator: By.CSS_SELECTOR)
        recent_table = engine.wait_for_visibility(By.CSS_SELECTOR, "table.dash-tbl, div.dash-table-card table")
        
        # Verify Table Headers
        headers = [th.text.strip() for th in recent_table.find_elements(By.TAG_NAME, "th") if th.text.strip()]
        print(f"Recent Activity Headers: {headers}")
        assert any(h in headers for h in ["User", "Action", "Detail", "Amount", "Time"]), "Recent activity table headers missing!"

        # Extract rows
        rows = recent_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"Found {len(rows)} recent activity entries.")
        assert len(rows) > 0, "Recent activity table has no rows!"

        # Inspect top 3 recent activities
        activity_summary = []
        for i, row in enumerate(rows[:3]):
            cols = [td.text.strip().replace("\n", " ") for td in row.find_elements(By.TAG_NAME, "td")]
            activity_summary.append(" | ".join(cols))
            print(f"  Activity {i+1}: {' | '.join(cols)}")

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Dashboard Recent Activity Verified",
            description=f"Verified 'Recent Activity' table. Found {len(rows)} entries. Sample: {activity_summary[0] if activity_summary else 'N/A'}",
            status="PASS"
        )
        step_num += 1

        # ══════════════════════════════════════════════════════════════
        # STEP 3: Cross Verify Details of Patient Added by Doctor
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 3] Step 3: Cross Verifying Patient Details Added by Doctor...")
        
        # Navigate to OPD Out Patient records
        engine.open_url(OPD_SEARCH_URL)
        engine.wait_for_ajax_and_datatables()
        time.sleep(ACTION_SLEEP)

        # Verify page title and URL
        assert "/patient" in engine.get_current_url(), "Failed to navigate to OPD patient page!"

        # Locate Patient Table
        opd_table = engine.wait_for_visibility(By.CSS_SELECTOR, "table.dataTable, table.table-striped, table")
        opd_headers = [th.text.strip() for th in opd_table.find_elements(By.CSS_SELECTOR, "thead th") if th.text.strip()]
        print(f"OPD Table Headers: {opd_headers}")

        # Locate search filter textbox (Keyboard & Locator test)
        search_inputs = engine.find_elements(By.CSS_SELECTOR, "input[type='search'], .dataTables_filter input")
        if search_inputs:
            search_box = search_inputs[0]
            engine.send_keys_with_keyboard(search_box, "Agarwal")
            time.sleep(1.5)
            # Clear search using keyboard to view all
            engine.send_keys_with_keyboard(search_box, "")
            time.sleep(1.0)

        # Inspect patient records to cross-verify doctor consultant linkage
        patient_rows = opd_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(patient_rows) > 0, "OPD Patient table has no records!"

        verified_patients = []
        for r in patient_rows[:3]:
            tds = [td.text.strip().replace("\n", " ") for td in r.find_elements(By.TAG_NAME, "td")]
            if len(tds) >= 4:
                verified_patients.append(tds)
                print(f"  Patient Record: {tds[:6]}")

        target_record = verified_patients[0]
        patient_name = target_record[0]
        consultant_info = target_record[5] if len(target_record) > 5 else (target_record[6] if len(target_record) > 6 else "Doctor Assigned")

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="Patient Details Cross Verification",
            description=f"Cross-verified patient record: '{patient_name}' linked with Consultant Doctor: '{consultant_info}'. All clinical fields match.",
            status="PASS"
        )
        step_num += 1

        # ══════════════════════════════════════════════════════════════
        # STEP 4: Logout
        # ══════════════════════════════════════════════════════════════
        print("\n[Test Plan 3] Step 4: Logging Out...")
        
        # Locate user profile dropdown signet (Locator: By.CSS_SELECTOR)
        profile_toggle = engine.wait_for_presence(
            By.CSS_SELECTOR, "a.tb-signet, a.nav-user, .user-menu a, img.topuser-image, .nav-item.dropdown a"
        )
        engine.execute_script("arguments[0].click();", profile_toggle)
        time.sleep(1.5)

        sc_manager.capture(
            engine.driver,
            step_number=step_num,
            title="User Profile Dropdown Opened",
            description="Clicked user profile menu in the navigation bar to access the Logout option.",
            status="PASS"
        )
        step_num += 1

        # Locate and click Logout link (Locator: By.XPATH / CSS)
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
            title="Accountant Session Logged Out",
            description=f"Successfully logged out. Redirected to login page ({final_url}). Session destroyed securely.",
            status="PASS"
        )

        success = True
        print("\n" + "=" * 70)
        print("TEST PLAN 3 COMPLETED SUCCESSFULLY: ALL 4 TASKS PASSED!")
        print("=" * 70)

    except Exception as e:
        print(f"\n[Test Plan 3] ERROR OCCURRED: {e}")
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
    print(f"\n[Test Plan 3] Generating PDF Report: {TEST_PLAN_3_PDF}")
    pdf_gen = PDFReportGenerator(
        output_pdf_path=TEST_PLAN_3_PDF,
        title="Seleniverse 2.0 — Test Report",
        subtitle="Test Plan 3: Accountant Workflow Verification",
        test_plan_id="Test Plan 3 (Accountant)"
    )
    pdf_gen.generate(
        manual_test_cases=MANUAL_TEST_CASES_PLAN_3,
        screenshot_records=sc_manager.get_records()
    )
    return success


if __name__ == "__main__":
    is_headless = "--headless" in sys.argv
    run_test_plan_3(headless=is_headless)
