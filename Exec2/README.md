# Seleniverse 2.0 — Software Testing Hackathon
## Hospital Management System Automated Test Suite & Compliance Dossier

### Target Application
- **Exploration Portal:** `https://smart-hospital.in/demo`
- **Application Portal:** `https://demo.smart-hospital.in/site/login`

---

## 1. Project Architecture & Folder Organization

This project differentiates the two problem statements into dedicated, self-contained modular folders while sharing a reusable common engine:

```
d:\Education\SEM 5\Software Testing\Hacakthon\
│
├── common/                                      # Reusable Automation & Reporting Engine
│   ├── __init__.py
│   ├── config.py                               # Centralized URLs, credentials, timeouts, paths
│   ├── browser_engine.py                       # Core Selenium engine wrapping browser commands, waits, locators, mouse/keyboard
│   ├── screenshot_manager.py                   # Automated screenshot capture & metadata logging
│   └── report_generator.py                     # ReportLab PDF generator (manual test tables, status badges, embedded images)
│
├── Test_Plan_3_Accountant/                      # Problem Statement 1: Accountant Workflow
│   ├── test_plan_3.py                          # Executable Selenium automation script for Test Plan 3
│   ├── manual_test_cases.md                    # Formal Manual Test Cases Specification (Part 1)
│   ├── screenshots/                            # Clean directory containing screenshots captured during execution
│   └── Test_Plan_3_Accountant_Report.pdf       # Generated PDF Report with Manual Test Cases & Screenshot Evidence
│
├── Test_Plan_4_Pharmacist/                      # Problem Statement 2: Pharmacist Workflow
│   ├── test_plan_4.py                          # Executable Selenium automation script for Test Plan 4
│   ├── manual_test_cases.md                    # Formal Manual Test Cases Specification (Part 1)
│   ├── screenshots/                            # Clean directory containing screenshots captured during execution
│   └── Test_Plan_4_Pharmacist_Report.pdf       # Generated PDF Report with Manual Test Cases & Screenshot Evidence
│
├── run_all.py                                  # Master Orchestrator: executes all 4 test cases for both test plans & builds Master PDF
├── Seleniverse_2.0_Master_Report.pdf           # Consolidated Master PDF Dossier
├── requirements.txt                            # Python dependencies (selenium, webdriver-manager, reportlab, pillow)
└── README.md                                   # Comprehensive Project & Architectural Documentation
```

---

## 2. Testing Methods & UI Elements Coverage Matrix

| Testing Method / Element | Implementation in Framework | Location / Method |
| :--- | :--- | :--- |
| **Browser Commands** | `driver.get()`, `driver.maximize_window()`, `driver.set_window_size()`, `driver.title`, `driver.current_url`, `driver.page_source`, `driver.refresh()`, `driver.back()`, `driver.quit()` | `common/browser_engine.py` |
| **Selenium Waits** | Explicit Waits with `WebDriverWait(driver, 15)` and `expected_conditions` (`visibility_of_element_located`, `presence_of_element_located`, `element_to_be_clickable`, `url_contains`, `invisibility_of_element_located`); Implicit Wait (`implicitly_wait(5)`) | `common/browser_engine.py` |
| **Page Scrolling** | Smooth scrolling into view center using `execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});")`, top and bottom scroll | `common/browser_engine.py:scroll_into_view` |
| **Mouse Actions** | Mouse hover (`move_to_element`), mouse click, double click, right click (`context_click`) using `ActionChains(driver)` | `common/browser_engine.py:hover, mouse_click` |
| **Keyboard Actions** | Clearing textboxes with `Keys.CONTROL + "a"` + `Keys.BACKSPACE`, typing with `send_keys()`, pressing `Keys.ENTER`, `Keys.ESCAPE` | `common/browser_engine.py:send_keys_with_keyboard` |
| **Web Element Locators** | Comprehensive demonstration of all standard Selenium locators: `By.ID` (`al-username`, `al-password`), `By.NAME` (`username`, `payment_mode`), `By.XPATH` (`//button[contains(text(), ...)]`), `By.CSS_SELECTOR` (`table.dash-tbl`, `button.lp-btn-submit`), `By.CLASS_NAME` (`tb-signet`, `lp-input`), `By.TAG_NAME` (`th`, `td`, `tr`, `h3`), `By.LINK_TEXT` / `By.PARTIAL_LINK_TEXT` (`Logout`, `Pharmacy`) | Utilized across all scripts |
| **Loading Elements Sync** | Dynamic loading spinner synchronization, DataTables AJAX processing wait, modal fade-in/fade-out synchronization | `common/browser_engine.py:wait_for_ajax_and_datatables` |
| **Buttons** | Sign In buttons, role demo selector buttons, payment modal buttons, view detail action buttons, modal dismiss buttons (`btn-close`, `data-bs-dismiss`) | Verified in both Test Plans |
| **Checkboxes** | Search filter checkboxes, table row selection checkboxes with `is_selected()` checking | `common/browser_engine.py:set_checkbox` |
| **Labels & Headings** | Page headings (`H: Recent Activity`, `H: Dashboard`), field labels (`BILL NO`, `PATIENT`, `CASE ID`), summary value labels | Validated with assertions |
| **Lists & Dropdowns** | `<select>` dropdown handling using Selenium `Select` class (`select_by_visible_text`, `select_by_value`, options extraction for Payment Modes: `Cash`, `Cheque`, `UPI`, `Online`, etc.) | Tested in Payment Modal |
| **Textboxes** | Username input, password input, search filter inputs, note textareas | Tested with keyboard commands |
| **Frames (Iframes)** | Safe iframe context switching with `driver.switch_to.frame()` and `driver.switch_to.default_content()` | `common/browser_engine.py:switch_to_frame_safely` |
| **Assertions** | Deep verification of page titles, URLs, table rows, user profiles, doctor-patient linkage, and bill calculations (`Net = Total - Discount + Tax`) | Validated at each critical step |

---

## 3. Detailed Test Plans Specification & Verification

### Test Plan 3: Accountant Workflow
1. **Login as Accountant:**
   - Navigates to `https://demo.smart-hospital.in/site/login`
   - Inputs Accountant credentials (`bradf@gmail.com` / `password`) using keyboard actions
   - Submits form; asserts URL contains `/admin` and profile signet displays `Brad (Accountant)`
2. **Verify Dashboard Recent Activity for Newly Added Patient:**
   - Smooth-scrolls to the `Recent Activity` card
   - Asserts table visibility and headers (`User`, `Action`, `Detail`, `Module`, `Amount`, `Time`)
   - Verifies active patient transactions (e.g. `posted bill payment`, amounts, transaction IDs)
3. **Cross Verify Details of New Patient Added by Doctor:**
   - Navigates to OPD Out Patient records (`/admin/patient/search`)
   - Locates the active OPD DataTables view (`table.opd_ajaxlist, #DataTables_Table_1`)
   - Extracts and verifies Patient Name (e.g. `GANGA`), OPD No (`OPDN7901`), Case ID (`7945`), and Consultant Doctor assignment (`Dr. Amit Singh (9009)`)
4. **Logout:**
   - Opens user profile dropdown menu (`a.tb-signet`)
   - Clicks `Logout` (`/site/logout`); asserts redirection to `/site/login`

### Test Plan 4: Pharmacist Billing & Payment Validation
1. **Login as Pharmacist:**
   - Navigates to `https://demo.smart-hospital.in/site/login`
   - Inputs Pharmacist credentials (`harry@gmail.com` / `password`)
   - Submits form; asserts URL contains `/admin` and Pharmacist role is active
2. **View Pharmacy Section:**
   - Navigates to `/admin/pharmacy/bill`
   - Verifies billing DataTables headers (`Bill No`, `Case ID`, `Date`, `Patient Name`, `Doctor Name`, `Amount ($)`, `Paid Amount ($)`, `Balance Amount ($)`)
   - Asserts 100+ pharmacy bill records exist
3. **View Payment Details for Latest Bill Payment and Validate:**
   - Identifies latest bill payment row (`PHARMAB620`, Case ID `7490`, Patient `Rachel Priest`)
   - Clicks payment button (`a.add_payment`) to open `#addPaymentModal`
   - Validates Bill No, Patient Name, Net Amount ($309.96), Paid Amount ($250.00), Due Amount ($59.96)
   - Inspects Payment Mode dropdown (`Cash`, `Cheque`, `UPI`, `Online`, etc.) using `Select`
   - Verifies Transaction History table
   - Inspects full bill invoice breakdown modal (`#viewModal`)
4. **Logout:**
   - Opens user profile dropdown menu
   - Clicks `Logout`; asserts redirection to `/site/login`

---

## 4. How to Run the Test Suite

### Prerequisites
Install the required Python dependencies:
```powershell
pip install -r requirements.txt
```

### Running the Entire Hackathon Suite (Master Runner)
Runs Test Plan 3 and Test Plan 4 sequentially, captures all screenshots, validates assertions, and produces all 3 PDF reports:
```powershell
# Run with visible Chrome browser UI:
python run_all.py

# Run in headless mode:
python run_all.py --headless
```

### Running Test Plan 3 Individually
```powershell
python Test_Plan_3_Accountant/test_plan_3.py
# Or headless:
python Test_Plan_3_Accountant/test_plan_3.py --headless
```

### Running Test Plan 4 Individually
```powershell
python Test_Plan_4_Pharmacist/test_plan_4.py
# Or headless:
python Test_Plan_4_Pharmacist/test_plan_4.py --headless
```

---

## 5. Generated Artifacts & Reports

1. **Test Plan 3 Report:**
   `Test_Plan_3_Accountant/Test_Plan_3_Accountant_Report.pdf`
2. **Test Plan 4 Report:**
   `Test_Plan_4_Pharmacist/Test_Plan_4_Pharmacist_Report.pdf`
3. **Consolidated Master Dossier:**
   `Seleniverse_2.0_Master_Report.pdf`
4. **Screenshots Directories:**
   - `Test_Plan_3_Accountant/screenshots/`
   - `Test_Plan_4_Pharmacist/screenshots/`
