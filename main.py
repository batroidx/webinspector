import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests


class App(ttk.App):
    def __init__(self):
        super().__init__(title="WebInspector 0.1.0", theme="bootstrap-light")
        self.geometry("1000x700")
        self.init_interface()

    def get_section_label(self, label, obj):
        return ttk.Label(obj, text=label, font=("", 8))

    def get_content(self, url):
        self.status_tab_pane_progress.start(10)
        self.get_button.configure(state=DISABLED)
        self.log("log", f"Trying to get {url}")

        threading.Thread(
            target=self._fetch_url,
            args=(url,),
            daemon=True
        ).start()

    def _fetch_url(self, url):
        try:
            rslt = requests.get(url, timeout=15)
            rslt.raise_for_status()
            self.after(0, self._on_success, rslt.text)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    def _on_success(self, text):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self._stop_loading()

    def _on_error(self, message):
        self.log("err", message)
        self._stop_loading()

    def _stop_loading(self):
        self.status_tab_pane_progress.stop()
        self.get_button.configure(state=NORMAL)

    def log(self, logtype, text):
        match logtype:
            case "log":
                self.status_tab_pane_content.insert("end", f"[log] {text}\n")
            case "err":
                self.status_tab_pane_content.insert("end", f"[err] {text}\n")
        self.status_tab_pane_content.see("end")

    def init_interface(self):
        hor_paned = ttk.Panedwindow(self, orient=HORIZONTAL)
        hor_paned.pack(fill=BOTH, expand=YES)

        left_pane = ttk.Frame(hor_paned, padding=10)
        ttk.Label(left_pane, text="Website").pack(anchor=W, pady=(0, 5))
        self.get_section_label("Url", left_pane).pack(anchor=W)
        site_entry = ttk.Entry(left_pane, font=("Consolas", 10))
        site_entry.pack(anchor=W, fill=X)
        self.get_section_label("WSI Request", left_pane).pack(anchor=W)
        object_entry = ttk.Text(left_pane, font=("Consolas", 10))
        object_entry.pack(fill=BOTH)

        self.get_button = ttk.Button(
            left_pane, text="Get",
            command=lambda: self.get_content(url=site_entry.get())
        )
        self.get_button.pack(side=BOTTOM, fill=X)
        hor_paned.add(left_pane, weight=2)

        ver_paned = ttk.Panedwindow(self, orient=VERTICAL)

        content_pane = ttk.Frame(ver_paned, padding=10)
        ttk.Label(content_pane, text="Content").pack(anchor=W, pady=(0, 5))
        self.textbox = ttk.Text(content_pane)
        self.textbox.pack(fill=BOTH, expand=YES)
        ver_paned.add(content_pane, weight=3)

        tab_pane = ttk.Notebook(ver_paned)
        ver_paned.add(tab_pane, weight=2)

        status_tab_pane = ttk.Frame(tab_pane)
        self.status_tab_pane_progress = ttk.Progressbar(
            status_tab_pane,
            mode="indeterminate",
            bootstyle="info striped",
        )
        self.status_tab_pane_progress.pack(side=BOTTOM, fill=X)

        self.status_tab_pane_content = ttk.Text(status_tab_pane)
        self.status_tab_pane_content.pack(fill=BOTH, expand=YES)
        tab_pane.add(status_tab_pane, text="Status")

        hor_paned.add(ver_paned, weight=3)


if __name__ == '__main__':
    app = App()
    app.mainloop()