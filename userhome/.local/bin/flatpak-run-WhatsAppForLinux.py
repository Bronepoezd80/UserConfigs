#!/usr/bin/env python
"""
    Jakob Janzen (me)
    jakob.janzen80@gmail.com
    2022-12-19

    Source of the Author (not me):
    https://github.com/eneshecan/whatsapp-for-linux
"""
import os as _os
import os.path as _ospath
import sys as _sys
import subprocess as _subprocess

user_config_dir = ".config"
app_name = "WhatsAppForLinux"
app_config_dir = "whatsapp-for-linux"
app_settings = "settings.conf"


class Application(object):
    def __init__(self):
        from pathlib import Path as _Path
        from os.path import join as _join
        self.name = app_name
        self.user_config_dir = _join(_Path.home(), user_config_dir)
        self.config_dir = _join(self.user_config_dir, app_config_dir)
        self.settings = _join(self.config_dir, app_settings)

        self.found = self.get()
        self.running = None

        class Web:
            allow_permissions = True
            hw_accel = 1

        class General:
            close_to_tray = True
            start_in_tray = True
            start_minimalized = True
            header_bar = True
            zoom_level = 1

        self.web = Web
        self.general = General
        self.proc = None

    def _run(self, command_):
        output = _subprocess.run(command_, capture_output=True)
        return output.stdout.decode('utf-8').split('\n')

    def _search(self, command_):
        return [application
                for application in self._run(command_)
                if self.name in application]

    def _get(self, command_):
        application = self._search(command_)
        return len(application) > 0 and application[0] or None

    def write_settings(self):
        if not _ospath.isdir(self.config_dir):
            _os.mkdir(self.config_dir)
        with open(self.settings, 'w') as settings:
            set_boolean = lambda option: "true" if option else "false"
            settings.write("""[web]
allow-permissions={0}
hw-accel={1}

[general]
close-to-tray={2}
start-in-tray={3}
start-minimized={4}
header-bar={5}
zoom-level={6}
""".format(set_boolean(self.web.allow_permissions),
           self.web.hw_accel,
           set_boolean(self.general.close_to_tray),
           set_boolean(self.general.start_in_tray),
           set_boolean(self.general.start_minimalized),
           set_boolean(self.general.header_bar),
           self.general.zoom_level))
        return

    def remove_settings(self):
        if _ospath.isdir(self.config_dir):
            import shutil as _shutil
            _shutil.rmtree(self.config_dir)
            if not _ospath.isdir(self.config_dir):
                return True
        return False

    def get(self):
        return self._get(["flatpak", "list", "--columns=application"])

    def get_running(self):
        return self._get(["flatpak", "ps", "--columns=application"])

    def run(self):
        _os.unsetenv("GTK_MODULES")
        self.proc = _subprocess.Popen(["flatpak", "run", self.found])
        return

    def kill(self):
        _subprocess.run(["flatpak", "kill", self.found])
        return

    def wait(self):
        import time as _time
        while True:
            if self.proc.poll() or self.get_running():
                break
            _time.sleep(0.1)
        return


def main():
    app = Application()
    if app.found:
        app.write_settings()
        app.running = app.get_running()
        print("application: {}".format(app.found))
        print("running: {}".format(app.running))
        if app.running:
            print("killing {} ...".format(app.found))
            app.kill()
        print("starting {} ...".format(app.found))
        app.run()
        app.wait()
        app.running = app.get_running()
        print("application: {}".format(app.found))
        print("running: {}".format(app.running))
    else:
        print("application {} not found, removing configuration ...".format(app.name))
        if app.remove_settings():
            print("application configuration removed")
    return


if __name__ == "__main__":
    main()

