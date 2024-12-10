import os
import sys
import time
import libtmux

class tmuxhandler(object):
    def __init__(self, session_name:str, time_to_wait:int=0, display:bool=False):
        self.session_name = session_name
        self.session = None
        for session in libtmux.Server().list_sessions():
            if session.name == self.session_name:
                self.session = session
                break

        if self.session is None:
            self.session = libtmux.Server().new_session(session_name=self.session_name)

        self.time_to_wait = time_to_wait
        self.display = display
        self._pane = None
        self._history = []

    @property
    def pane(self):
        if self._pane is None:
            pane = self.session.list_windows()[0].list_panes()[0]
        else:
            pane = self._pane

    def send(self, content:str, enter:bool=False):
        content = content.strip()

        self._history += [content]
        self.pane.send_keys(content, enter=enter)

        if self.time_to_wait != 0:
            if display:print("[", end='', flush=True)
            for _ in range(self.time_to_wait):
                if display:print(".", end='', flush=True)
                time.sleep(1)
            if display:print("]", flush=True)

    def recieve(self) -> str:
        return self(self.pane.cmd("capture-pane", "-p").stdout)

    def clear(self):
        self.pane.clear()

    def __enter__(self):
        return self

    def __exit__(self, a=None, b=None, c=None):
        libtmux.Server().kill_session(target_session=self.session_name)
        self.session = None
