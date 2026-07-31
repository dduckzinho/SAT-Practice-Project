
class Timer:
    def __init__(self, root, timerLabel, totalSeconds, mode="exit", command=None):
        self.root=root
        self.label=timerLabel
        self.total_seconds=totalSeconds
        self.time_left=totalSeconds
        self.overtime_seconds=0
        
        self.mode=mode
        self.command=command
        
        self.is_running=False
        self.is_paused=False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self._update()

    def togglePause(self, button):
        if not self.is_running and not self.is_paused:
            return

        if self.is_paused:
            self.is_paused=False
            button.config(text="Pause")
            self._update()
        else:
            self.is_paused=True
            button.config(text="Resume")

    def stop(self):
        self.is_running=False

    def _update(self):
        if not self.is_running or self.is_paused:
            return

        if self.time_left>0:
            minutes, seconds=divmod(self.time_left, 60)
            self.label.config(text=f"{minutes:02d}:{seconds:02d}", fg="black")
            self.time_left-=1
            self.root.after(1000, self._update)

        else:
            if self.mode=="exit":
                self.is_running=False
                self.label.config(text="00:00 - Time's Up!", fg="red")
                if self.command:
                    self.command()

            elif self.mode=="overtime":
                minutes, seconds = divmod(self.overtime_seconds, 60)
                self.label.config(text=f"+{minutes:02d}:{seconds:02d} (OT)", fg="red")
                self.overtime_seconds+=1
                self.root.after(1000, self._update)