# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2023 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

import os
import socket
import subprocess
from time import sleep
from Core.Support import Font
from Core.Support import Language
import pyqrcode
import shutil

filename = Language.Translation.Get_Language()
filename


class Transfer:

    @staticmethod
    def File(report, name, extension):
        if os.path.exists(report):
            new = "Transfer/{}{}".format(name, extension)
            temp = "Transfer/file.txt"
            qr_file = "QRCodes/QR.eps"
            process = None
            req = False
            try:
                shutil.copyfile(report, new)
                f = open(temp, "w")
                f.write(name + extension)
                f.close()

                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 1))
                host = s.getsockname()[0]
                s.close()

                if os.name != "nt":
                    if os.getuid() == 0:
                        process = subprocess.Popen(
                            ["php", "-S", "{}:5000".format(host), "-t", "Transfer"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        req = True
                    else:
                        req = False
                else:
                    process = subprocess.Popen(
                        ["php", "-S", "{}:5000".format(host), "-t", "Transfer"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                    )
                    req = True

                if req:
                    link = "http://{}:5000".format(host)
                    print(Font.Color.GREEN + "\n[+]" + Font.Color.WHITE + Language.Translation.Translate_Language(
                            filename, "Transfer", "Generation", "None"))
                    sleep(3)
                    url = pyqrcode.create(link, version=4)
                    url.eps(qr_file, scale=8)
                    print(Font.Color.BLUE + "\n[I]" + Font.Color.WHITE + Language.Translation.Translate_Language(
                            filename, "Transfer", "Location", "None"))
                    print(Font.Color.BLUE + "\n[I]" + Font.Color.WHITE +
                        Language.Translation.Translate_Language(filename, "Database", "Link", "None").replace("DATABASE", "FILE-TRANSFER") + "{}".format(Font.Color.GREEN + link + Font.Color.WHITE))
                    inp = input(Font.Color.WHITE + Language.Translation.Translate_Language(
                        filename, "Database", "Quit", "None"))
                    print(Font.Color.BLUE + "\n[I]" + Font.Color.WHITE +
                        Language.Translation.Translate_Language(filename, "Database", "Stop", "None").replace("DATABASE", "FILE-TRANSFER"))
                    sleep(2)
                else:
                    print(Font.Color.RED + "\n[!]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Database", "NoRoot", "None").replace("DATABASE", "FILE-TRANSFER"))
            finally:
                if process is not None and process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()
                if os.path.exists(new):
                    os.remove(new)
                if os.path.exists(temp):
                    os.remove(temp)
                if os.path.exists(qr_file):
                    os.remove(qr_file)
        else:
            print(Font.Color.RED + "\n[!]" + Font.Color.WHITE + "FILE DOES NOT EXIST")
