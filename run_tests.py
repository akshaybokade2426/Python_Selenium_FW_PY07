import os
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path


def cleanup_old_reports(reports_root, days_to_keep=7):
    if not reports_root.exists():
        print("📂 Reports root not found. Skipping cleanup.")
        return

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    print(f"🧹 Checking for reports older than {cutoff_date.strftime('%Y-%m-%d')}...")

    # Categories: 'allure-results' and 'allure-report'
    for category in ["allure-results", "allure-report"]:
        category_path = reports_root / category
        if not category_path.exists():
            continue

        for folder in category_path.iterdir():
            if folder.is_dir():
                try:
                    # Ensure we are parsing just the folder name (e.g., '2026-03-01')
                    folder_date = datetime.strptime(folder.name, "%Y-%m-%d")

                    if folder_date < cutoff_date:
                        print(f"  🗑️ Deleting: {category}/{folder.name}")
                        shutil.rmtree(folder)
                except ValueError:
                    # This folder isn't named 'YYYY-MM-DD', ignore it safely
                    continue


def run_daily_tests():
    # 1. Setup Paths
    project_root = Path(__file__).parent
    reports_root = project_root / "reports"
    today = datetime.now().strftime("%Y-%m-%d")

    results_dir = reports_root / "allure-results" / today
    results_dir.mkdir(parents=True, exist_ok=True)

    # 2. Run Cleanup
    cleanup_old_reports(reports_root, days_to_keep=7)

    # 3. Add Environment Info (Allure Widget)
    env_file = results_dir / "environment.properties"
    with open(env_file, "w") as f:
        f.write(f"Date={today}\nBrowser=Chrome\nPython_Version=3.10\n")

    # 4. Execute Pytest
    print(f"🚀 Running tests for {today}...")
    pytest_cmd = ["pytest", "tests/", f"--alluredir={results_dir}"]
    subprocess.run(pytest_cmd)

    # 5. Serve Report
    print("📊 Opening Allure Report...")
    subprocess.run(["allure", "serve", str(results_dir)])


if __name__ == "__main__":
    run_daily_tests()