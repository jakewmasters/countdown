import tkinter as tk
import datetime
import re
import threading


class Countdown(tk.Tk):
    def __init__(self):
        super().__init__()

        # logic variables
        in_datetime = None

        # window meta
        self.title("Countdown Timer")
        self.geometry("400x400")
        self.resizable(False, False)

        # styling
        self.standard_font = (None, 16)

        # content
        self.main_frame = tk.Frame(self, width=400, height=400, bg="MediumPurple4")

        self.prompt_label = tk.Label(self.main_frame, text="Enter a date in the following format:\nMM/DD/YYYY @ HH:MM", bg="MediumPurple4", fg="black", font=self.standard_font)
        self.timestamp_entry = tk.Entry(self.main_frame, bg="white", fg="black", font=self.standard_font)
        self.enter_button = tk.Button(self.main_frame, text="Enter", bg="lightgrey", fg="black", command=self.enter, font=self.standard_font)
        self.countdown_label = tk.Label(self.main_frame, text="", bg="MediumPurple4", fg="black", font=self.standard_font)
        self.stop_button = tk.Button(self.main_frame, text="Stop", bg="lightgrey", fg="black", command=self.stop, font=self.standard_font, state="disabled")
        
        # packing
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        self.prompt_label.pack(fill=tk.X, pady=15)
        self.timestamp_entry.pack(fill=tk.X, padx=50, pady=(0,20))
        self.enter_button.pack(fill=tk.X, padx=100, pady=(0,25))
        self.countdown_label.pack(fill=tk.X, pady=(0,30))
        self.stop_button.pack(fill=tk.X, side=tk.BOTTOM, padx=100)

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)


    def enter(self):
        # verify that something was actually entered
        if not self.timestamp_entry.get():
            self.countdown_label['text'] = "Input needed."
            return None
        
        # verify that input matches to correct format using regex
        in_str = self.timestamp_entry.get()
        if re.match("^\d{2}/\d{2}/\d{4} @ \d{2}:\d{2}$", in_str) == None:
            self.countdown_label['text'] = "Incorrect format."
            return None
        # testing timestamp: 08/18/2019 @ 09:00

        # create datetime object from input
        try:
            read_datetime = datetime.datetime.strptime(in_str, "%m/%d/%Y @ %H:%M")
        except ValueError:
            self.countdown_label['text'] = "Houston..."
            return None
        
        # verify that entered timestamp is in the future
        self.in_datetime = read_datetime
        
        # replace entry_frame with countdown_frame
        # self.countdown_label['text'] = "Successfully created object."
        self.timestamp_entry.configure(state="disabled")
        self.enter_button.configure(state="disabled")

        # call start()
        self.start()

    def setup_worker(self):
        worker = RenderThread(self, self.in_datetime)
        self.worker = worker
    
    def start(self):
        if not hasattr(self, "worker"):
            self.setup_worker()
        
        self.timestamp_entry.configure(state="disabled")
        self.enter_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.worker.start()
    
    def stop(self):
        self.worker.end = True
        self.timestamp_entry.configure(state="normal")
        self.enter_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        del self.worker
        self.countdown_label['text'] = "Countdown finished."
        return

    def update_countdown(self, time_str):
        self.countdown_label['text'] = time_str
        self.update_idletasks()

    def safe_destroy(self):
        if hasattr(self, "worker"):
            self.worker.force_quit = True
            self.after(100, self.safe_destroy)
        else:
            self.destroy()
    

class RenderThread(threading.Thread):
    def __init__(self, master, in_datetime):
        super().__init__()
        self.master = master
        self.in_datetime = in_datetime

        self.end = False # set this variable whenever thread should stop
        self.force_quit = False
    
    def run(self):
        while True:
            if not self.end and not self.force_quit:
                self.main_loop()
            if datetime.datetime.now() >= self.in_datetime:
                if not self.force_quit:
                    self.master.stop()
                    break
            elif self.end:
                break
            elif self.force_quit:
                del self.master.worker
                return
            else:
                continue
        return
    
    def main_loop(self):
        now = datetime.datetime.now()
        if now < self.in_datetime:
            delta = (self.in_datetime - now)
            hours = delta.seconds // 3600
            minutes = (delta.seconds - (hours * 3600)) // 60
            seconds = delta.seconds - (hours * 3600) - (minutes * 60)
            time_str = str(delta.days) + " days\n" +  str(hours) + " hours\n" + str(minutes) + " minutes\n" + str(seconds) + " seconds"
            if not self.force_quit:
                self.master.update_countdown(time_str)

if __name__ == "__main__":
    countdown = Countdown()
    countdown.mainloop()