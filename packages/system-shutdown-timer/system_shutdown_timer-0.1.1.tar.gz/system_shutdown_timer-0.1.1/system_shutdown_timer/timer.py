import os
import time
import platform


class SystemShutdownTimer:
    """A library to set timers for closing all applications and shutting down the system."""

    @staticmethod
    def close_all_apps():
        """Force close all applications."""
        system = platform.system()
        if system == "Windows":
            os.system("taskkill /F /IM *")
        elif system in ("Linux", "Darwin"):  # Linux or macOS
            os.system("killall -9 $(ps -e | awk '{print $1}')")
        else:
            print("Unsupported operating system")

    @staticmethod
    def shutdown_laptop():
        """Shut down the laptop."""
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /s /t 0")
        elif system == "Linux":
            os.system("shutdown now")
        elif system == "Darwin":  # macOS
            os.system("shutdown -h now")
        else:
            print("Unsupported operating system")

    @staticmethod
    def set_timer(minutes):
        """Set a timer to close all apps and shut down the laptop after the given minutes."""
        seconds = minutes * 60
        print(f"Timer set for {minutes} minutes ({seconds} seconds).")
        time.sleep(seconds)
        print("Closing all apps...")
        SystemShutdownTimer.close_all_apps()
        print("Shutting down the laptop...")
        SystemShutdownTimer.shutdown_laptop()

    @staticmethod
    def timer_options():
        """Provides predefined timer options."""
        print("\nChoose a timer option:")
        print("1. 5 minutes")
        print("2. 15 minutes")
        print("3. 20 minutes")
        print("4. 25 minutes")
        choice = input("Enter your choice (1-4): ").strip()

        options = {
            "1": 5,
            "2": 15,
            "3": 20,
            "4": 25
        }

        if choice in options:
            SystemShutdownTimer.set_timer(options[choice])
        else:
            print("Invalid choice. Please select a valid option.")


def main():
    """Entry point for CLI usage."""
    print("Welcome to the System Shutdown Timer CLI!")
    SystemShutdownTimer.timer_options()
