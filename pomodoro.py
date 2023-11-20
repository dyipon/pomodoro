import rumps
from datetime import datetime
import Quartz

class TimeApp(rumps.App):
    POMODORO_DURATION = 45 * 60  # in seconds
    TIME_BEFORE_PAUSE = 60  # in seconds
    TIME_BEFORE_RESET = 5 * 60  # in seconds

    def __init__(self):
        super(TimeApp, self).__init__("TimeApp")
        self.elapsed_time = 0
        self.last_alert_time = 0
        self.alert_shown = False
        self.update_time(None)  # Initial value setup
        reset_button = rumps.MenuItem(title="Reset", callback=self.reset_timer)
        self.menu = [reset_button]

    @rumps.timer(1)
    def update_time(self, _):
        most = datetime.now()
        prefix_logo = "🍅"
        time_since_last_event = Quartz.CGEventSourceSecondsSinceLastEventType(Quartz.kCGEventSourceStateHIDSystemState, Quartz.kCGAnyInputEventType)
        paused_icon = "⏸️" if time_since_last_event >= self.TIME_BEFORE_PAUSE else ""
        
        # Increase elapsed time if there is activity
        if time_since_last_event < self.TIME_BEFORE_PAUSE:
            self.elapsed_time += 1

        # Reset the timer if inactivity is more than 5 minutes
        if time_since_last_event > self.TIME_BEFORE_RESET and self.elapsed_time > 10:
            print(most.strftime('%H:%M') + '> reset timer because inactivity')
            self.elapsed_time = 0

        # Calculate remaining time
        remaining_seconds = self.POMODORO_DURATION - self.elapsed_time
        minutes, seconds = divmod(abs(remaining_seconds), 60)

        # Show alert if time is over
        if remaining_seconds <= 0:
            prefix_logo = "🚶"
            if remaining_seconds % 60 == 0:
                print(most.strftime('%H:%M') + '> standup reminder')
                rumps.notification("Reminder", "", "Stand up and walk around!")

        # Set title
        prefix = prefix_logo + paused_icon
        inactivity_str = f" ({int(time_since_last_event) // 60}:{int(time_since_last_event) % 60:02})" if paused_icon else ""
        self.title = f"{prefix} {minutes:02}:{seconds:02}{inactivity_str}"

    def reset_timer(self, _):
        """Function to reset the timer."""
        most = datetime.now()
        print(most.strftime('%H:%M') + '> timer reset')
        self.elapsed_time = 0
        self.alert_shown = False

if __name__ == "__main__":
    TimeApp().run()
