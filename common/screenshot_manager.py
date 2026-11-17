import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from selenium import webdriver


class ScreenshotManager:
    """
    Manages capturing, organizing, and cataloging screenshots for automated test execution.
    Produces metadata for embedding in automated PDF test reports.
    """

    def __init__(self, target_dir: Path):
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.records: List[Dict[str, Any]] = []

    def capture(
        self,
        driver: webdriver.Chrome,
        step_number: int,
        title: str,
        description: str,
        status: str = "PASS"
    ) -> Dict[str, Any]:
        """
        Captures a high-resolution screenshot from the current browser state,
        saves it in the designated folder with clean numbering, and records metadata.
        """
        # Ensure DOM has finished rendering
        time.sleep(1.0)
        
        # Clean title for filename
        sanitized_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title).strip("_")
        filename = f"step_{step_number:02d}_{sanitized_title.lower()}.png"
        filepath = self.target_dir / filename

        # Capture screenshot
        driver.save_screenshot(str(filepath))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "step_number": step_number,
            "title": title,
            "description": description,
            "status": status.upper(),
            "filename": filename,
            "filepath": str(filepath.resolve()),
            "timestamp": timestamp
        }

        self.records.append(record)
        print(f"[ScreenshotManager] Captured Step {step_number:02d} [{status}]: {title} -> {filename}")
        return record

    def get_records(self) -> List[Dict[str, Any]]:
        """Returns the chronological list of all captured screenshot records."""
        return self.records

    def export_summary(self, json_path: Path):
        """Exports screenshot metadata as a JSON file."""
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)
