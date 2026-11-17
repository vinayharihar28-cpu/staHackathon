
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

from report import generate_report


URL = "https://demo.smart-hospital.in/site/login"

os.makedirs("screenshots", exist_ok=True)

results = []


def test_plan_3():

    driver = webdriver.Chrome()

    try:

        # 1. Login as accountant
        driver.get(URL)
        time.sleep(2)

        driver.save_screenshot("screenshots/01_login_page.png")

        driver.find_element(By.XPATH, "//button[normalize-space()='Accountant']").click()
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(4)

        driver.save_screenshot("screenshots/02_dashboard.png")

        results.append([
            "Accountant Login",
            "Select Accountant and login",
            "Accountant",
            "Dashboard opens",
            "Dashboard opened",
            "PASS"
        ])


        # 2. Get a patient from Recent Activity
        patient = driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'dash-table-card')]"
            "[.//h3[normalize-space()='Recent Activity']]"
            "//tbody/tr[.//strong[contains(., '(Patient)')]][1]//strong"
        ).text.replace(" (Patient)", "")

        assert patient, "No patient was found in Recent Activity"

        driver.save_screenshot("screenshots/03_recent_activity.png")

        results.append([
            "Find Patient",
            "Read patient from Recent Activity",
            "Dashboard",
            "Patient name displayed",
            patient,
            "PASS"
        ])


        # 3. Cross-check patient details in Patient List
        driver.find_element(
            By.XPATH,
            "//a[.//span[normalize-space()='Patient']]"
        ).click()

        time.sleep(3)

        driver.save_screenshot("screenshots/04_patient_list.png")

        search = driver.find_element(
            By.CSS_SELECTOR,
            "table.ajaxlist ~ * input[type='search'], "
            "div.dataTables_wrapper input[type='search']"
        )

        search.send_keys(patient)
        time.sleep(2)

        row = driver.find_element(
            By.XPATH,
            "//table[contains(@class, 'ajaxlist')]//tbody/tr"
            "[contains(., \"%s\")]" % patient
        )

        details = row.find_elements(By.TAG_NAME, "td")

        assert len(details) >= 5 and all(
            cell.text.strip() for cell in details[1:5]
        )

        driver.save_screenshot("screenshots/05_patient_details.png")

        results.append([
            "Verify Patient",
            "Search in Patient List",
            patient,
            "Patient details displayed",
            "Details verified",
            "PASS"
        ])


        # 4. Logout
        driver.find_element(By.CSS_SELECTOR, "a.tb-signet").click()

        driver.save_screenshot("screenshots/06_profile_menu.png")

        driver.find_element(
            By.XPATH,
            "//a[normalize-space()='Logout']"
        ).click()

        time.sleep(2)

        driver.save_screenshot("screenshots/07_logout.png")

        results.append([
            "Logout",
            "Click Logout",
            "Logout option",
            "User logged out",
            "Logout successful",
            "PASS"
        ])

        print("Test Plan 3 completed")


    except Exception as e:

        driver.save_screenshot("screenshots/error.png")

        results.append([
            "Test Plan 3",
            "Execution interrupted",
            "Current test data",
            "All steps completed",
            str(e),
            "FAIL"
        ])

        print("Test failed:", e)


    finally:

        driver.quit()

        # Generate report using report.py
        generate_report(results)


if __name__ == "__main__":
    test_plan_3()