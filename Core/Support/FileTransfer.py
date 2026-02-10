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
            shutil.copyfile(report, new)
            temp = "Transfer/file.txt"
            f = open(temp, "w")
            f.write(name + extension)
            f.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 1))
            host = s.getsockname()[0]
            s.close()
            if os.name != "nt":
                if os.getuid() == 0:
                    subprocess.Popen(
                        ["php", "-S", "{}:5000".format(host), "-t", "Transfer"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    Req = True
                    link = "http://{}:5000".format(host)
                else:
                    Req = False
            else:
                subprocess.Popen(
                    ["php", "-S", "{}:5000".format(host), "-t", "Transfer"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                )
                Req = True
                link = "http://{}:5000".format(host)

            if Req:
                print(Font.Color.GREEN + "\n[+]" + Font.Color.WHITE + Language.Translation.Translate_Language(
                        filename, "Transfer", "Generation", "None"))
                sleep(3)
                url = pyqrcode.create(link, version=4)
                url.eps('QRCodes/QR.png', scale=8)
                print(Font.Color.BLUE + "\n[I]" + Font.Color.WHITE + Language.Translation.Translate_Language(
                        filename, "Transfer", "Location", "None"))
                print(Font.Color.BLUE + "\n[I]" + Font.Color.WHITE +
                    Language.Translation.Translate_Language(filename, "Database", "Link", "None").replace("DATABASE", "FILE-TRANSFER") + "{}".format(Font.Color.GREEN + link + Font.Color.WHITE))
                inp = input(Font.Color.WHITE + Language.Translation.Translate_Language(
                    filename, "Database", "Quit", "None"))
                os.remove(new)
                os.remove(temp)
                os.remove("QRCodes/QR.png")
                if os.name != "nt":
                    subprocess.run(["killall", "php"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                else:
                    subprocess.run(["taskkill", "/F", "/IM", "php.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                print(Font.Color.BLUE + "\n[I]" +
                    Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Database", "Stop", "None").replace("DATABASE", "FILE-TRANSFER"))
                sleep(2)
            else:
                print(Font.Color.RED + "\n[!]" + Font.Color.WHITE +
                  Language.Translation.Translate_Language(filename, "Database", "NoRoot", "None").replace("DATABASE", "FILE-TRANSFER"))
        else:
            print(Font.Color.RED + "\n[!]" + Font.Color.WHITE + "FILE DOES NOT EXIST")
