import subprocess
import sys
import threading
import asyncio
import time

from cli.entities.setting import Settings
from cli.utils.shell import Shell
from cli.utils.singleton import singleton
from cli.utils.ui import UI


def show_loading_spinner(is_loading, message="Loading, please wait ..."):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    while is_loading.is_set():
        for char in spinner:
            sys.stdout.write(f'\r{char} {message}')
            time.sleep(0.1)
            sys.stdout.flush()
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()

@singleton
class Aws:
    session = ""

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    # private
    def __git_check_session_command(self):
        cmd = "git ls-remote"
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

    # ----------------------

    # public
    async def check_session(self):
        self.session = "<r>྾</r>"
        await self.__checksesionloading(self)

    # ----------------------

    # private
    async def __checksesionloading(self):
        is_loading = threading.Event()
        is_loading.set()

        spinner_thread = threading.Thread(target=show_loading_spinner, args=(is_loading, "Wait ..."))
        spinner_thread.start()

        try:
            await self.loop.run_in_executor(None, self.__git_check_session_command)
            self.session = "<g>✔</g>"
        except:
            self.session = "<r>྾</r>"
        finally:
            is_loading.clear()
            spinner_thread.join()

    # ----------------------

    # private
    async def __signin(self):
        UI().clear()
        UI().pheader("AWS Sign In")

        Settings().load()
        aws_profile = Settings().config['aws_profile']

        if aws_profile == '' or aws_profile is None or aws_profile == 'username':
            UI().pline()
            UI().ptext(f'│ <r>Please configure your aws profile</r>')
            UI().ptext(f'│ Setting Path: <y>{Settings().file_path}</y>')
            UI().pline()
            UI().pcontinue()
            return

        else:
            UI().pline()

            await self.__checksesionloading()

            if self.session == "<g>✔</g>":
                UI().ptext(f'│ <g>You are already logged in</g>')
                UI().ptext(f'│ Profile: <y>{aws_profile}</y>')
                UI().pline()
                UI().pcontinue()
                return

            code = Shell().run(['aws', 'sso', 'login', '--profile', aws_profile])
            if code == 0:
                self.session = "<g>✔</g>"
                UI().psuccess()
            else:
                self.session = "<r>྾</r>"
                UI().perror()

    # public
    def sign_in(self):
        try:
            self.loop.run_until_complete(self.__signin())
        except KeyboardInterrupt:
            return
