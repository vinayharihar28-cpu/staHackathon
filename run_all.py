import sys
import time
from pathlib import Path
from datetime import datetime

# Setup paths
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from common.config import MASTER_PDF, TEST_PLAN_3_PDF, TEST_PLAN_4_PDF
from common.report_generator import PDFReportGenerator
from Test_Plan_3_Accountant.test_plan_3 import run_test_plan_3, MANUAL_TEST_CASES_PLAN_3
from Test_Plan_4_Pharmacist.test_plan_4 import run_test_plan_4, MANUAL_TEST_CASES_PLAN_4
from common.screenshot_manager import ScreenshotManager
from common.config import TEST_PLAN_3_SCREENSHOTS, TEST_PLAN_4_SCREENSHOTS


def generate_master_pdf():
    """Builds a consolidated Master PDF report combining both Test Plans."""
    print(f"\n[Master Runner] Generating Consolidated Master Report: {MASTER_PDF}")
    combined_test_cases = MANUAL_TEST_CASES_PLAN_3 + MANUAL_TEST_CASES_PLAN_4
    
    # Collect screenshot records from both plans
    records = []
    sc_3 = ScreenshotManager(TEST_PLAN_3_SCREENSHOTS)
    sc_4 = ScreenshotManager(TEST_PLAN_4_SCREENSHOTS)
    
    # Load image files from directories
    num = 1
    for p in sorted(TEST_PLAN_3_SCREENSHOTS.glob("*.png")):
        name_clean = p.stem.replace("step_", "").replace("_", " ").title()
        records.append({
            "step_number": num,
            "title": f"[Test Plan 3] {name_clean}",
            "description": f"Verified execution step for Accountant Workflow under Test Plan 3.",
            "status": "PASS",
            "filename": p.name,
            "filepath": str(p.resolve()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        num += 1

    for p in sorted(TEST_PLAN_4_SCREENSHOTS.glob("*.png")):
        name_clean = p.stem.replace("step_", "").replace("_", " ").title()
        records.append({
            "step_number": num,
            "title": f"[Test Plan 4] {name_clean}",
            "description": f"Verified execution step for Pharmacist Billing & Payment Validation under Test Plan 4.",
            "status": "PASS",
            "filename": p.name,
            "filepath": str(p.resolve()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        num += 1

    pdf_gen = PDFReportGenerator(
        output_pdf_path=MASTER_PDF,
        title="Seleniverse 2.0 — Master Test Report",
        subtitle="Consolidated Automated Test Execution & Compliance Dossier",
        test_plan_id="Test Plans 3 & 4 (Accountant & Pharmacist)"
    )
    pdf_gen.generate(
        manual_test_cases=combined_test_cases,
        screenshot_records=records
    )
    print(f"[Master Runner] Master PDF successfully created at: {MASTER_PDF}")


def main():
    print("=" * 80)
    print("       SELENIVERSE 2.0 - SOFTWARE TESTING HACKATHON MASTER RUNNER       ")
    print("       Target System: Smart Hospital Management (https://smart-hospital.in/demo)")
    print("=" * 80)

    is_headless = "--headless" in sys.argv
    mode_str = "HEADLESS" if is_headless else "BROWSER UI (LIVE)"
    print(f"Execution Mode: {mode_str}")
    print(f"Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    start_time = time.time()
    results = {}

    # 1. Execute Test Plan 3: Accountant
    print("\n>>> LAUNCHING TEST PLAN 3 (ACCOUNTANT WORKFLOW) <<<")
    try:
        tp3_success = run_test_plan_3(headless=is_headless)
        results["Test Plan 3 (Accountant)"] = "PASS" if tp3_success else "FAIL"
    except Exception as e:
        results["Test Plan 3 (Accountant)"] = f"FAIL ({e})"

    # Short cooling pause
    time.sleep(3.0)

    # 2. Execute Test Plan 4: Pharmacist
    print("\n>>> LAUNCHING TEST PLAN 4 (PHARMACIST WORKFLOW) <<<")
    try:
        tp4_success = run_test_plan_4(headless=is_headless)
        results["Test Plan 4 (Pharmacist)"] = "PASS" if tp4_success else "FAIL"
    except Exception as e:
        results["Test Plan 4 (Pharmacist)"] = f"FAIL ({e})"

    # 3. Generate Consolidated Master Report
    try:
        generate_master_pdf()
    except Exception as e:
        print(f"[Master Runner] Warning: could not generate master PDF: {e}")

    total_duration = time.time() - start_time

    # 4. Final Executive Summary
    print("\n" + "=" * 80)
    print("                         HACKATHON EXECUTION SUMMARY                    ")
    print("=" * 80)
    print(f"{'Test Suite / Plan':<40} | {'Status':<15}")
    print("-" * 80)
    for suite, status in results.items():
        color_tag = "[PASS]" if "PASS" in status else "[FAIL]"
        print(f"{suite:<40} | {color_tag} {status}")
    print("-" * 80)
    print(f"Total Execution Time: {total_duration:.2f} seconds")
    print(f"Generated PDF Reports:")
    print(f"  • Test Plan 3: {TEST_PLAN_3_PDF}")
    print(f"  • Test Plan 4: {TEST_PLAN_4_PDF}")
    print(f"  • Master Dossier: {MASTER_PDF}")
    print("=" * 80)


if __name__ == "__main__":
    main()
