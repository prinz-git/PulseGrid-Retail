"""PulseGrid - Retail Analytics — Streamlit Cloud Entry Point.

This root entrypoint enables seamless deployment on Streamlit Community Cloud
(which defaults to looking for `streamlit_app.py` at the repository root)
while maintaining the modular dashboard structure inside `dashboard/`.
"""

from pathlib import Path
import runpy
import sys

# Resolve root and dashboard directories
REPO_ROOT = Path(__file__).resolve().parent
DASHBOARD_DIR = REPO_ROOT / "dashboard"

# Ensure both directories are on Python search path
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

# Launch the primary dashboard application
APP_PATH = DASHBOARD_DIR / "app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")

