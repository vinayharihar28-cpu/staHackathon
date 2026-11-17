# Seleniverse 2.0 — Manual Test Cases (Part 1)
## Problem Statement: Test Plan 4 — Pharmacist Workflow

| Field | Detail |
| :--- | :--- |
| **System Under Test** | Smart Hospital Management System |
| **Target URL** | `https://smart-hospital.in/demo` / `https://demo.smart-hospital.in/site/login` |
| **Test Plan** | Test Plan 4: Pharmacist Billing & Payment Validation |
| **Role** | Pharmacist (`harry@gmail.com` / `password`) |

---

### Manual Test Cases Specification

| TC ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_PHARM_01** | Verify Pharmacist Login Authentication | User is on the login page `https://demo.smart-hospital.in/site/login`. | 1. Enter Pharmacist email `harry@gmail.com` into username field.<br/>2. Enter password `password` into password field.<br/>3. Click 'Sign In' button. | User is authenticated successfully and redirected to the dashboard (`/admin/admin/dashboard`) with Pharmacist privileges. | As expected. Landed on dashboard with authenticated Pharmacist session. | **PASS** |
| **TC_PHARM_02** | View and Verify Pharmacy Billing Section | Pharmacist is logged in and on the dashboard. | 1. Click 'Pharmacy' link in the sidebar or navigate to `/admin/pharmacy/bill`.<br/>2. Wait for DataTables bill records to load.<br/>3. Verify table columns (Bill No, Case ID, Patient Name, Doctor, Net Amount, Paid Amount, Balance). | Pharmacy bill table loads completely with active records and appropriate action buttons (View, Add Payment, Print). | As expected. 100+ bill records loaded with all financial and patient metadata columns. | **PASS** |
| **TC_PHARM_03** | View and Validate Payment Details for Latest Bill Payment | Pharmacist is viewing the Pharmacy bill table. | 1. Locate the top (latest) bill record.<br/>2. Click the Payment / Add Payment action button (`a.add_payment`).<br/>3. In the popup modal, inspect and validate Bill No, Patient Name, Case ID, Net Amount, Paid Amount, Balance, Payment Mode list, and Transaction History. | Payment Details modal opens smoothly. All financial figures match the table row; transaction history reflects posted payments. | As expected. Modal displayed Bill No, Patient, Net/Paid/Balance figures, and Transaction History with full mathematical integrity. | **PASS** |
| **TC_PHARM_04** | Verify Pharmacist Logout and Session Clearance | Pharmacist is logged in to the application. | 1. Click user avatar / profile menu in the top right navbar.<br/>2. Click 'Logout' link.<br/>3. Verify redirection and session termination. | User is logged out and returned to the login screen (`/site/login`). Session is cleared. | As expected. Redirected to login page; subsequent requests require re-authentication. | **PASS** |
