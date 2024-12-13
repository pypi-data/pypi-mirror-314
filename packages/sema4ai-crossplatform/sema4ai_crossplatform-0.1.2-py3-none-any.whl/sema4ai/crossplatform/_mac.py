from pathlib import Path
import platform
import subprocess
import logging

IS_MAC = platform.system() == "Darwin"

logger = logging.getLogger(__name__)

def _trigger_excel_on_mac(filepath: str) -> bool:
    """Trigger Excel to open and save a file using AppleScript.

    Args:
        filepath: Path to the Excel file to save

    Returns:
        True if the operation was successful, False otherwise
    """
    result = False
    if IS_MAC:
        logger.info("Triggering Excel save on MacOS Excel app")
        # Convert to absolute path
        abs_path = str(Path(filepath).resolve())

        # Updated script to check if Excel is installed
        launch_script = """
            tell application "System Events"
                set excelExists to exists application process "Microsoft Excel"
                if not excelExists then
                    try
                        tell application "Microsoft Excel"
                            launch
                            set visible to false
                        end tell
                        -- Wait for process to appear
                        set startTime to current date
                        repeat until exists application process "Microsoft Excel"
                            delay 0.5
                            if (current date) - startTime > 10 then
                                error "Excel process did not start within 10 seconds"
                            end if
                        end repeat
                    on error
                        return false
                    end try
                end if
                return true
            end tell
        """

        # Run the launch script and check if Excel exists
        try:
            launch_result = subprocess.run(
                ["osascript", "-e", launch_script],
                capture_output=True,
                text=True,
                check=False,
            )
            logger.debug(f"Launch result: {launch_result.stdout}")
            if launch_result.returncode != 0 or "false" in launch_result.stdout.lower():
                logger.warning("Microsoft Excel is not installed or cannot be launched")
                return False

            # Modify the save script to keep Excel invisible
            apple_script = f"""
            tell application "Microsoft Excel"
                set was_running to running
                set was_visible to visible
                set visible to false
                set display alerts to false

                try
                    open "{abs_path}"
                    save active workbook
                    close active workbook saving no

                    -- Restore previous visibility only if Excel was already running
                    if was_running then
                        set visible to was_visible
                    else
                        quit
                    end if

                    return true
                on error errMsg
                    if was_running then
                        set visible to was_visible
                    else
                        quit
                    end if
                    return errMsg
                end try
            end tell
            """

            # First launch Excel if needed
            subprocess.run(
                ["osascript", "-e", launch_script],
                capture_output=True,
                text=True,
                check=True,
            )

            # Then perform the save operation
            result = subprocess.run(
                ["osascript", "-e", apple_script],
                capture_output=True,
                text=True,
                check=True,
            )
            if "error" in result.stderr.lower():
                raise RuntimeError(f"Excel automation failed: {result.stderr}")
            result = True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute Excel automation: {e.stderr}")
            return False
    return result
