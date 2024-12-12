from ._mac import _trigger_excel_on_mac
from ._win import _trigger_excel_on_windows

import platform


def trigger_excel_save_on_app(filepath: str):
    """Trigger Excel to open and save a file using COM automation.

    Args:
        filepath: Path to the Excel file to save
    """
    system = platform.system()
    if system == "Windows":
        _trigger_excel_on_windows(filepath)
    elif system == "Darwin":  # MacOS
        _trigger_excel_on_mac(filepath)
