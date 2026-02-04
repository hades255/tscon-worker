"""
Check whether Hubstaff tracking (timer) is on or off using Hubstaff CLI.
Requires Hubstaff desktop app with Scripted Control enabled (Always allow).
See: https://support.hubstaff.com/what-is-scripted-control/
"""
import json
import os
import subprocess
import sys

# Default Hubstaff CLI path on Windows
HUBSTAFF_CLI_DIR = os.environ.get("HUBSTAFF_CLI_DIR", r"C:\Program Files\Hubstaff")
HUBSTAFF_CLI = os.path.join(HUBSTAFF_CLI_DIR, "HubstaffClient.exe")


def get_hubstaff_status(autostart=False):
    """
    Run HubstaffCLI status and return parsed JSON, or None if CLI missing/failed.
    If autostart=True, adds --autostart so the app starts if not running.
    """
    if not os.path.isfile(HUBSTAFF_CLI):
        return None
    try:
        cmd = [HUBSTAFF_CLI, "status"]
        if autostart:
            cmd.append("--autostart")
        out = subprocess.run(
            cmd,
            cwd=HUBSTAFF_CLI_DIR,
            capture_output=True,
            text=True,
            timeout=15,
        )
        if out.returncode != 0:
            return None
        return json.loads(out.stdout.strip()) if out.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def is_hubstaff_tracking_on(autostart=False):
    """
    Return True if Hubstaff timer is actively tracking, False if not or unknown.
    """
    data = get_hubstaff_status(autostart=autostart)
    if data is None:
        return False
    return data.get("tracking") is True


def main():
    data = get_hubstaff_status(autostart=False)
    if data is None:
        print("Hubstaff CLI not found or status failed. Check install path and Scripted Control.")
        print("Default path:", HUBSTAFF_CLI)
        sys.exit(1)
    tracking = data.get("tracking", False)
    print("Tracking:", "ON" if tracking else "OFF")
    if "active_project" in data and data["active_project"]:
        print("Active project:", data.get("active_project"))
    sys.exit(0 if tracking else 2)


if __name__ == "__main__":
    main()
