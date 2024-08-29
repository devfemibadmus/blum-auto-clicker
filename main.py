import pyautogui, pygetwindow as gw, time, keyboard, random
from pynput.mouse import Button, Controller

class AutoClicker:
    def __init__(self):
        self.mouse = Controller()
        self.paused = False
        self.current_skip = 0
        self.skip_count = 0
        self.window_name = "TelegramDesktop"
        time.sleep(0.5)

    def click(self, x, y):
        """Simulates a mouse click at the given coordinates with slight randomness."""
        self.mouse.position = (x, y + random.randint(1, 3))
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def toggle_pause(self):
        """Toggles the pause state when 'q' is pressed."""
        self.paused = not self.paused
        if self.paused:
            print('[✅] | Paused.')
        else:
            print('[✅] | Resumed.')
        time.sleep(0.2)

    def start(self):
        """Starts the auto-clicking process."""
        self.skip_count = int(input("[✅] | Enter number of skips before clicking: "))

        while True:
            if keyboard.is_pressed('q'):
                self.toggle_pause()

            if self.paused:
                continue

            # Get the window based on the provided name
            window = self.get_target_window()
            if not window:
                print(f"[❌] | Window - {self.window_name} not found! Waiting for it to reopen...")
                self.wait_for_window()
                continue

            # Activate and process window if found
            self.process_window(window)

    def get_target_window(self):
        """Attempts to get the target window by its name."""
        windows = gw.getWindowsWithTitle(self.window_name)
        return windows[0] if windows else None

    def wait_for_window(self):
        """Waits until the target window reappears."""
        while not self.get_target_window():
            time.sleep(1)
        print(f"[✅] | Window found - {self.window_name}\n[✅] | Press 'q' to pause.")

    def process_window(self, window):
        """Handles the target window by taking a screenshot and performing auto-clicking."""
        # Ensure the window is activated
        try:
            window.activate()
        except:
            window.minimize()
            window.restore()

        # Get window dimensions and take a screenshot
        window_rect = (window.left, window.top, window.width, window.height)
        screenshot = pyautogui.screenshot(region=window_rect)

        # Scan through pixels in the screenshot
        self.scan_and_click_pixels(screenshot, window_rect)

    def scan_and_click_pixels(self, screenshot, window_rect):
        """Scans the screenshot for target pixels and clicks them if found."""
        width, height = screenshot.size

        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = screenshot.getpixel((x, y))
                
                # Define the color range for detection
                if (0 <= b <= 124) and (102 <= r <= 219) and (200 <= g <= 254):
                    if self.current_skip < self.skip_count:
                        self.current_skip += 1
                        continue  # Skip this click

                    # Reset the skip counter and perform the click
                    self.current_skip = 0
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    self.click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    break  # Stop after one click for this loop iteration

if __name__ == "__main__":
    auto_clicker = AutoClicker()
    auto_clicker.start()

print('[✅] | Stopped.')
