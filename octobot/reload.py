from re import L
import subprocess

import requests


class CodeReloader:
    # https://maxhalford.github.io/blog/flask-sse-no-deps/
    def format_sse(self, data: str, event: str|None = None) -> str:
        msg = ''.join([
            f'data: {line}\n'
            for line in data.splitlines()
        ]) + '\n    '
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg

    def message(self, msg: str) -> str:
        return self.format_sse(msg, 'message')

    def reload(self):
        apk_url = 'https://github.com/ManchesterMachineMakers/RobotController/releases/download/latest/TeamCode-release-.apk'
        apk_path = 'TeamCode.apk'

        yield self.message('Starting...')
        yield self.message('Initializing ADB...')

        yield self.message(
            subprocess.run(['adb', 'devices'], text=True).stdout
        )

        yield self.message('Downloading APK...')

        r = requests.get(apk_url, stream=True)
        with open(apk_path, 'wb') as fd:
            i = 0
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
                yield self.format_sse(str(i := i + 1), 'progress')
        
        yield self.message('Downloaded!')

        yield self.message('Uninstalling previous version...')
        yield self.message(
            subprocess.run(['adb', 'uninstall', 'com.qualcomm.ftcrobotcontroller'], text=True).stdout
        )

        yield self.message('Installing new version...')
        yield self.message(
            subprocess.run(['adb', 'install', apk_path], text=True).stdout
        )

        yield self.message('Launching...')
        yield self.message(
            subprocess.run(['adb', 'shell', 'monkey', '-p', 'com.qualcomm.ftcrobotcontroller', '1'], text=True).stdout
        )
