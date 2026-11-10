import os
import signal
from textual.app import App, ComposeResult
from textual.widgets import   Header, Button, Input
from textual.containers import HorizontalGroup 
from video_list import Video_list_Search, result_int, watch_later
from textual.containers import Vertical
import subprocess 
class YT_pod(App):
    # pause =  false - means the video is going
    pause = False
    CSS = """
        Screen{
        background:black;
        }
        #unpause{
        width:20%;
        }
        #pause{
        width:40%;
        }
        #stop{
        width:60%;
        }
        #input{
        width:60%;
        border:ascii red;
        background:black;
        }
        #WL{
        width:20%;
        }
        #search{
        width:20%;
        }
        .result{
        color:white;
        width:80%;
        }
        .result:hover{
            border:solid red;
            background:black;
        }
        """
    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalGroup(

        Input(placeholder="Search...", id="input"),
        Button("Search", id="search", variant="success", flat=True),
        Button("WL", id="WL", variant="warning", flat=True),
                )
        with Vertical():
            for i in range(0, result_int):
                yield Button("", id=f"output{i}",classes="result", flat=True)
            
        yield HorizontalGroup(
            Button("KILL", id="stop", variant="error", flat=True),
            Button("||", id="pause", variant="warning", flat=True),
            )
    def on_mount(self):
        self.player = None
        self.theme = "nord"
        for i in range(0, result_int):
            self.query_one(f"#output{i}",Button).display = False

    def Watch_Later(self):

        outputs = []

        for i in range(result_int):
            outputs.append(self.query_one(f"#output{i}", Button))


        self.urls = watch_later()
        
        for i in range(result_int):
            try:
                outputs[i].label = self.urls[i]["title"] 
                outputs[i].display = True
            except:
                continue
    def SEARCH(self):
        input_widget = self.query_one("#input", Input)

        outputs = []

        for i in range(result_int):
            outputs.append(self.query_one(f"#output{i}", Button))

        text = input_widget.value

        self.urls = Video_list_Search(text)

        for i in range(result_int):
            try:
                outputs[i].label = self.urls[i]["title"] 
                outputs[i].display = True
            except:
                continue

    def on_key(self,event):
        if event.key == "enter":
            self.SEARCH()
    
    def on_button_pressed(self, event: Button.Pressed)-> None:

        if event.button.id == "stop":
            pids = subprocess.check_output(["pgrep", "mpv"], text=True).split()
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
        if event.button.id == "search":
            self.SEARCH()
        if event.button.id == "WL":
            self.Watch_Later()
        if event.button.has_class("result")  :
            for i in range(result_int):
                if event.button.id == f"output{i}":
                    if self.player and self.player.poll() is None:
                        self.player.kill()
                        self.player.wait()
                    try:
                        self.player = subprocess.Popen([
                            "mpv",
                            "--no-video",
                            "--msg-level=all=no",
                            self.urls[i]["url"]
                        ])
                    except:
                        exit()

        if event.button.id == "pause":
            pids = subprocess.check_output(["pgrep", "mpv"], text=True).split()
            for pid in pids:
                    if not self.pause :
                        os.kill(int(pid), signal.SIGSTOP)
                    elif self.pause:
                        os.kill(int(pid), signal.SIGCONT)

                    self.pause = not self.pause
if __name__ == "__main__":
    app = YT_pod()
    app.run()

