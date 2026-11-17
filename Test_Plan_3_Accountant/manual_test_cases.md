# Seleniverse 2.0 — Manual Test Cases (Part 1)
## Problem Statement: Test Plan 3 — Accountant Workflow

| Field | Detail |
| :--- | :--- |
| **System Under Test** | Smart Hospital Management System |
| **Target URL** | `https://smart-hospital.in/demo` / `https://demo.smart-hospital.in/site/login` |
| **Test Plan** | Test Plan 3: Accountant Workflow |
| **Role** | Accountant (`bradf@gmail.com` / `password`) |

---

### Manual Test Cases Specification

| TC ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_ACC_01** | Verify Accountant Login Authentication | Browser is open; user is on the login page `https://demo.smart-hospital.in/site/login`. | 1. Enter Accountant email `bradf@gmail.com` in username field.<br/>2. Enter password `password` in password field.<br/>3. Click 'Sign In' button. | User is authenticated successfully and redirected to the Accountant Dashboard (`/admin/admin/dashboard`). Top bar displays 'Brad (Accountant)'. | As expected. User successfully redirected to dashboard with role 'Brad (Accountant)'. | **PASS** |
| **TC_ACC_02** | Verify Dashboard Recent Activity for Newly Added Patient | Accountant is logged in and viewing the dashboard. | 1. Scroll down to the 'Recent Activity' section on the dashboard.<br/>2. Inspect table headers (User, Action, Detail, Module, Amount, Time).<br/>3. Locate the recent activity entries for patient transactions. | 'Recent Activity' card is clearly visible with structured activity log showing recent patient payments and transactions. | As expected. Table displayed with patient names, amounts, transaction IDs, and timestamps. | **PASS** |
| **TC_ACC_03** | Cross Verify Details of Patient Added by Doctor | Accountant is logged in with access to OPD / Patient records. | 1. Navigate to 'OPD - Out Patient' (`/admin/patient/search`).<br/>2. Verify table records displaying Patient Name, Patient ID, Guardian, and Consultant Doctor.<br/>3. Search and cross-verify the newly added patient and assigned doctor details. | Patient records display the doctor consultant assignment (e.g. Dr. Sansa Gomez, Dr. Amit Singh, Dr. Reyan Jain), matching patient records across modules. | As expected. Doctor and patient cross-verification completed with full match. | **PASS** |
| **TC_ACC_04** | Verify Accountant Logout and Session Termination | Accountant is logged into the application. | 1. Click on the user profile menu on the top navigation bar.<br/>2. Click the 'Logout' link.<br/>3. Verify redirection and session clearance. | User is logged out and redirected to the login page (`/site/login`). Protected dashboard cannot be accessed without re-authenticating. | As expected. Redirected to `/site/login` with session terminated cleanly. | **PASS** |
