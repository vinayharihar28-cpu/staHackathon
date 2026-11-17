# Seleniverse 2.0 — Software Testing Hackathon Report
## Smart Hospital Management System Automated Test Suite

> [!IMPORTANT]
> **Hackathon Deliverables Completed:**
> - **Architecture & Folder Separation:** Differentiated into `Test_Plan_3_Accountant/` and `Test_Plan_4_Pharmacist/` with dedicated test runners, manual test specs, screenshots folders, and PDF reports.
> - **Unified Master Runner:** [run_all.py](file:///d:/Education/SEM%205/Software%20Testing/Hacakthon/run_all.py) executes all 4 test cases across both test plans with 100% pass rate.
> - **Comprehensive Testing Methods Covered:** Browser commands, Selenium waits (explicit & implicit), page scrolling, mouse actions (ActionChains), keyboard actions, locators (ID, Name, XPath, CSS, Class, Tag, LinkText), loading elements, buttons, checkboxes, labels, lists/dropdowns (Select), textboxes, frames, and assertions.
> - **Visual Evidence & PDF Reporting:** High-resolution screenshots captured at every step, saved locally in numbered sequence, and embedded into formal PDF reports.

---

## 1. System Architecture & Folder Layout

```
d:\Education\SEM 5\Software Testing\Hacakthon\
│
├── common/                                      # Reusable Automation & Reporting Engine
│   ├── config.py                               # Application URLs, credentials, timeouts, paths
│   ├── browser_engine.py                       # Core Selenium engine wrapping commands, waits, locators, mouse/keyboard
│   ├── screenshot_manager.py                   # Automated screenshot capture & metadata logging
│   └── report_generator.py                     # ReportLab PDF generator (manual test tables, status badges, embedded images)
│
├── Test_Plan_3_Accountant/                      # Problem Statement 1: Accountant Workflow
│   ├── test_plan_3.py                          # Executable Selenium automation script for Test Plan 3
│   ├── manual_test_cases.md                    # Formal Manual Test Cases Specification (Part 1)
│   ├── screenshots/                            # Step-by-step screenshots captured during live execution
│   └── Test_Plan_3_Accountant_Report.pdf       # Generated PDF Report with Manual Test Cases & Evidence
│
├── Test_Plan_4_Pharmacist/                      # Problem Statement 2: Pharmacist Workflow
│   ├── test_plan_4.py                          # Executable Selenium automation script for Test Plan 4
│   ├── manual_test_cases.md                    # Formal Manual Test Cases Specification (Part 1)
│   ├── screenshots/                            # Step-by-step screenshots captured during live execution
│   └── Test_Plan_4_Pharmacist_Report.pdf       # Generated PDF Report with Manual Test Cases & Evidence
│
├── run_all.py                                  # Master Orchestrator: executes all 4 test cases for both test plans & builds Master PDF
├── Seleniverse_2.0_Final_Report.pdf            # Consolidated Master PDF Dossier
├── requirements.txt                            # Python dependencies (selenium, webdriver-manager, reportlab, pillow)
├── HACKATHON_REPORT.md                         # Detailed Hackathon Dossier
├── PRESENTATION_GUIDE.md                       # Presentation Slides & Defense Guide
└── README.md                                   # Comprehensive Project & Architectural Documentation
```

---

## 2. Testing Methods & UI Elements Implementation Matrix

| Category | Technique / UI Element | Implementation Details |
| :--- | :--- | :--- |
| **Browser Commands** | `get()`, `maximize_window()`, `set_window_size()`, `title`, `current_url`, `page_source`, `refresh()`, `back()`, `forward()`, `quit()` | Implemented in [browser_engine.py](file:///d:/Education/SEM%205/Software%20Testing/Hacakthon/common/browser_engine.py). Tested on every navigation and session tear-down. |
| **Selenium Waits** | Explicit Waits (`WebDriverWait`) with `visibility_of_element_located`, `presence_of_element_located`, `element_to_be_clickable`, `url_contains`; Implicit Waits (`implicitly_wait`) | Synchronizes transitions, page loads, and modal appearances without brittle delays. |
| **Page Scrolling** | Smooth viewport scrolling (`execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});")`) | Ensures targets (like Recent Activity and Payment Modal) are centered before interaction. |
| **Mouse Actions** | `ActionChains(driver)`: `move_to_element` (hover), `click()`, `context_click()` | Used for hovering on table cards, action icons, and clicking profile dropdowns. |
| **Keyboard Actions** | `Keys.CONTROL + "a"` + `Keys.BACKSPACE`, `send_keys()`, `Keys.ENTER`, `Keys.ESCAPE` | Cleans inputs before typing credentials and filters search boxes. |
| **Locators** | `By.ID`, `By.NAME`, `By.XPATH`, `By.CSS_SELECTOR`, `By.CLASS_NAME`, `By.TAG_NAME`, `By.LINK_TEXT`, `By.PARTIAL_LINK_TEXT` | Full demonstration across login fields, tables, modals, buttons, and navigation elements. |
| **Loading Elements** | Dynamic loading spinners, DataTables AJAX processing indicators | Synchronized via `wait_for_ajax_and_datatables()` to ensure table records are fully loaded. |
| **Form Controls** | Buttons, Checkboxes, Labels, Dropdowns (`Select`), Textboxes | Verified in login form, billing filters, payment mode selector, and invoice modals. |
| **Frames / Iframes** | Safe iframe context switching (`switch_to.frame`, `switch_to.default_content`) | Handles embedded frames gracefully if present on third-party integrations. |
| **Assertions** | Deep verification with failure messages | Asserts titles, URLs, table rows, user profiles, doctor-patient linkage, and bill calculations (`Net = Total - Discount + Tax`). |

---

## 3. Manual Test Cases (Part 1 Requirements)

### Test Plan 3: Accountant Workflow

| TC ID | Test Description | Pre-conditions | Test Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_ACC_01** | Verify Accountant Login Authentication | User is on login page `https://demo.smart-hospital.in/site/login` | 1. Enter email `bradf@gmail.com`<br/>2. Enter password `password`<br/>3. Click 'Sign In' | User is authenticated; redirected to dashboard (`/admin`); role displayed as 'Brad (Accountant)' | **PASS** |
| **TC_ACC_02** | Verify Dashboard Recent Activity for Newly Added Patient | Accountant is on dashboard | 1. Scroll to 'Recent Activity' card<br/>2. Verify table headers<br/>3. Inspect patient payment records | Recent Activity table renders with User, Action, Detail, Module, Amount, Time | **PASS** |
| **TC_ACC_03** | Cross Verify Details of Patient Added by Doctor | Accountant has access to OPD records | 1. Open OPD section (`/admin/patient/search`)<br/>2. Inspect patient table<br/>3. Cross-verify Patient Name, OPD No, and Consultant Doctor | Patient record (e.g. 'GANGA', OPD: 'OPDN7901') confirms linkage with Consultant Doctor (e.g. 'Amit Singh') | **PASS** |
| **TC_ACC_04** | Verify Accountant Logout and Session Termination | Accountant is logged in | 1. Click user profile signet<br/>2. Click 'Logout'<br/>3. Assert redirection to `/site/login` | User session is invalidated and redirected to login screen | **PASS** |

### Test Plan 4: Pharmacist Billing & Payment Validation

| TC ID | Test Description | Pre-conditions | Test Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_PHARM_01** | Verify Pharmacist Login Authentication | User is on login page | 1. Enter email `harry@gmail.com`<br/>2. Enter password `password`<br/>3. Click 'Sign In' | Pharmacist is authenticated and redirected to dashboard | **PASS** |
| **TC_PHARM_02** | View and Verify Pharmacy Billing Section | Pharmacist is logged in | 1. Navigate to `/admin/pharmacy/bill`<br/>2. Verify bill table headers<br/>3. Verify records | 100+ bill records rendered with columns: Bill No, Case ID, Patient, Doctor, Amount, Paid, Balance | **PASS** |
| **TC_PHARM_03** | View and Validate Payment Details for Latest Bill Payment | Pharmacist is on Pharmacy page | 1. Identify latest bill row (`PHARMAB620`)<br/>2. Click payment button (`a.add_payment`)<br/>3. Inspect modal fields, payment modes, and transactions | Payment modal displays Bill No, Patient Name, Net/Paid/Due amounts, Payment Modes (`Select`), and Transaction log | **PASS** |
| **TC_PHARM_04** | Verify Pharmacist Logout and Session Clearance | Pharmacist is logged in | 1. Click user profile signet<br/>2. Click 'Logout'<br/>3. Assert redirection to `/site/login` | Session is destroyed cleanly; user is back on login page | **PASS** |

---

## 4. Execution Evidence & Generated Reports

### Generated PDF Test Reports
- [Test_Plan_3_Accountant_Report.pdf](file:///d:/Education/SEM%205/Software%20Testing/Hacakthon/Test_Plan_3_Accountant/Test_Plan_3_Accountant_Report.pdf) (418 KB)
- [Test_Plan_4_Pharmacist_Report.pdf](file:///d:/Education/SEM%205/Software%20Testing/Hacakthon/Test_Plan_4_Pharmacist/Test_Plan_4_Pharmacist_Report.pdf) (449 KB)
- [Seleniverse_2.0_Final_Report.pdf](file:///d:/Education/SEM%205/Software%20Testing/Hacakthon/Seleniverse_2.0_Final_Report.pdf) (864 KB)

### Execution Output Summary
```
================================================================================
                         HACKATHON EXECUTION SUMMARY                    
================================================================================
Test Suite / Plan                        | Status         
--------------------------------------------------------------------------------
Test Plan 3 (Accountant)                 | [PASS] PASS
Test Plan 4 (Pharmacist)                 | [PASS] PASS
--------------------------------------------------------------------------------
Total Execution Time: 110.50 seconds
Pass Rate: 100% (8 / 8 tasks passed)
================================================================================
```

---

## 5. Quick Commands to Reproduce Execution

```powershell
# Run the complete test suite (both test plans) in live browser GUI:
python run_all.py

# Run in headless mode:
python run_all.py --headless

# Run Test Plan 3 individually:
python Test_Plan_3_Accountant/test_plan_3.py

# Run Test Plan 4 individually:
python Test_Plan_4_Pharmacist/test_plan_4.py
```
