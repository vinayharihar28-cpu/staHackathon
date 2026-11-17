
def generate_report(results):

    print("\n")
    print("=" * 120)
    print("                 SELENIUM TEST EXECUTION REPORT")
    print("=" * 120)

    print("{:<25} {:<25} {:<15} {:<25} {:<15} {:<10}".format(
        "Test Scenario",
        "Steps",
        "Input Data",
        "Expected Output",
        "Actual Output",
        "Status"
    ))

    print("-" * 120)

    for result in results:
        print("{:<25} {:<25} {:<15} {:<25} {:<15} {:<10}".format(
            result[0][:24],
            result[1][:24],
            result[2][:14],
            result[3][:24],
            result[4][:14],
            result[5]
        ))

    passed = sum(1 for r in results if r[5] == "PASS")
    failed = sum(1 for r in results if r[5] == "FAIL")

    print("-" * 120)
    print("Total Test Cases :", len(results))
    print("Passed           :", passed)
    print("Failed           :", failed)

    print("=" * 120)
