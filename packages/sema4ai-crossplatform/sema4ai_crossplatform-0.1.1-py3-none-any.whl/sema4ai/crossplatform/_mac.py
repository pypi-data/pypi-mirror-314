from pathlib import Path
import platform
import subprocess

IS_MAC = platform.system() == "Darwin"


def _trigger_excel_on_mac(filepath: str) -> bool:
    """Trigger Excel to open and save a file using AppleScript.

    Args:
        filepath: Path to the Excel file to save

    Returns:
        True if the operation was successful, False otherwise
    """
    result = False
    if IS_MAC:
        print("Triggering Excel save on MacOS Excel app")
        # Convert to absolute path
        abs_path = str(Path(filepath).resolve())

        # First, check if Excel is installed and launch if needed
        launch_script = """
            tell application "System Events"
                if not (exists application "Microsoft Excel") then
                    return false
                end if
                set isExcelRunning to (exists (processes where name is "Microsoft Excel"))
                if not isExcelRunning then
                    tell application "Microsoft Excel"
                        launch
                        set visible to false
                    end tell
                    -- Wait for process to appear
                    set startTime to current date
                    repeat until exists (processes where name is "Microsoft Excel")
                        delay 0.5
                        if (current date) - startTime > 10 then
                            error "Excel process did not start within 10 seconds"
                        end if
                    end repeat
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
                check=True,
            )
            if "false" in launch_result.stdout.lower():
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
            raise RuntimeError(f"Failed to execute Excel automation: {e.stderr}")
    return result
