import os
from pathlib import Path

# Project Roots & Directories
BASE_DIR = Path(__file__).resolve().parent.parent
COMMON_DIR = BASE_DIR / "common"

TEST_PLAN_3_DIR = BASE_DIR / "Test_Plan_3_Accountant"
TEST_PLAN_3_SCREENSHOTS = TEST_PLAN_3_DIR / "screenshots"
TEST_PLAN_3_PDF = TEST_PLAN_3_DIR / "Test_Plan_3_Accountant_Report.pdf"

TEST_PLAN_4_DIR = BASE_DIR / "Test_Plan_4_Pharmacist"
TEST_PLAN_4_SCREENSHOTS = TEST_PLAN_4_DIR / "screenshots"
TEST_PLAN_4_PDF = TEST_PLAN_4_DIR / "Test_Plan_4_Pharmacist_Report.pdf"

MASTER_PDF = BASE_DIR / "Seleniverse_2.0_Master_Report.pdf"

# Application URLs
APP_EXPLORE_URL = "https://smart-hospital.in/demo"
LOGIN_URL = "https://demo.smart-hospital.in/site/login"
DASHBOARD_URL = "https://demo.smart-hospital.in/admin/admin/dashboard"
OPD_SEARCH_URL = "https://demo.smart-hospital.in/admin/patient/search"
PATIENT_SEARCH_URL = "https://demo.smart-hospital.in/admin/admin/search"
PHARMACY_BILL_URL = "https://demo.smart-hospital.in/admin/pharmacy/bill"
LOGOUT_URL = "https://demo.smart-hospital.in/site/logout"

# Credentials
ACCOUNTANT_EMAIL = "bradf@gmail.com"
ACCOUNTANT_PASSWORD = "password"
ACCOUNTANT_ROLE_NAME = "Accountant"

PHARMACIST_EMAIL = "harry@gmail.com"
PHARMACIST_PASSWORD = "password"
PHARMACIST_ROLE_NAME = "Pharmacist"

DOCTOR_EMAIL = "sonia@gmail.com"
DOCTOR_PASSWORD = "password"

# Automation Delays & Timeouts
DEFAULT_EXPLICIT_WAIT = 15  # seconds for WebDriverWait
IMPLICIT_WAIT = 5          # seconds for standard element lookup
ACTION_SLEEP = 2.5          # seconds for visible interactions and reliable screenshots
MODAL_SLEEP = 3.0           # seconds for smooth modal animations
