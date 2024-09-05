import time
import json


def pytest_terminal_summary(terminalreporter, json_file="test_summary.json"):
    """
    collect test reuslt, then write it to json file
    """
    stats = terminalreporter.stats
    num_collected = terminalreporter._numcollected
    num_passed = len([i for i in stats.get("passed", []) if i.when != "teardown"])
    num_failed = len([i for i in stats.get("failed", []) if i.when != "teardown"])
    num_error = len([i for i in stats.get("error", []) if i.when != "teardown"])
    num_skipped = len([i for i in stats.get("skipped", []) if i.when != "teardown"])

    if num_collected > 0 and (num_collected - num_skipped) > 0:
        success_rate = (num_passed / (num_collected - num_skipped)) * 100
    else:
        success_rate = 0

    total_time_seconds = time.time() - terminalreporter._sessionstarttime

    summary_data = {
        "total": num_collected,
        "passed": num_passed,
        "failed": num_failed,
        "error": num_error,
        "skipped": num_skipped,
        "success_rate": f"{success_rate:.2f}%",
        "total_time_seconds": f"{total_time_seconds:.2f}s",
    }

    # write to file
    with open(json_file, "w") as file:
        json.dump(summary_data, file, indent=4)
