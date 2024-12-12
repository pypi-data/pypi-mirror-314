import gc
import platform
from contextlib import contextmanager
from pathlib import Path
import struct

IS_WINDOWS = False
if platform.system() == "Windows":
    import win32api
    import win32com.client
    from pywintypes import com_error as COMError  # pylint: disable=no-name-in-module
    import win32com

    IS_WINDOWS = True


def _to_unsigned(val):
    return struct.unpack("L", struct.pack("l", val))[0]


@contextmanager
def catch_com_error():
    """Try to convert COM errors to human-readable format."""
    try:
        yield
    except COMError as err:  # pylint: disable=no-member
        if err.excepinfo:
            try:
                msg = win32api.FormatMessage(_to_unsigned(err.excepinfo[5]))
            except Exception:  # pylint: disable=broad-except
                msg = err.excepinfo[2]
        else:
            try:
                msg = win32api.FormatMessage(_to_unsigned(err.hresult))
            except Exception:  # pylint: disable=broad-except
                msg = err.strerror
        raise RuntimeError(msg) from err


def _trigger_excel_on_windows(filepath: str):
    """Trigger Excel to open and save a file using COM interface.

    Args:
        filepath: Path to the Excel file to save
    """
    if IS_WINDOWS:
        xlApp = None
        xlBook = None
        print("Triggering Excel save on Windows Excel app")
        with catch_com_error():
            try:
                # Try to connect to an existing Excel instance first
                try:
                    xlApp = win32com.client.GetObject(Class="Excel.Application")
                    was_running = True
                except:
                    # If no existing instance, create a new one
                    xlApp = win32com.client.gencache.EnsureDispatch("Excel.Application")
                    was_running = False

                # Store original visibility state
                original_visible = xlApp.Visible
                original_alerts = xlApp.DisplayAlerts

                # Set visibility and alerts
                xlApp.Visible = False
                xlApp.DisplayAlerts = False

                abs_path = str(Path(filepath).resolve())
                xlBook = xlApp.Workbooks.Open(abs_path)
                if xlBook is None:
                    raise RuntimeError(f"Failed to open workbook: {abs_path}")
                xlBook.Save()
            finally:
                if xlBook is not None:
                    xlBook.Close(SaveChanges=False)
                    xlBook = None
                    gc.collect()
                if xlApp is not None:
                    # Restore original states
                    xlApp.DisplayAlerts = original_alerts
                    xlApp.Visible = original_visible
                    # Only quit Excel if we started it
                    if not was_running:
                        xlApp.Quit()
