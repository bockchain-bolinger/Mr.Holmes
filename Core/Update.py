# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2021-2023 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

import os
import shutil
import subprocess
from configparser import ConfigParser
from Core.Support import Font
from Core.Support import Language
from time import sleep

Conf_file = "Configuration/Configuration.ini"
Parser = ConfigParser()
Parser.read(Conf_file)
filename = Language.Translation.Get_Language()
filename


class Downloader:

    @staticmethod
    def Check_Creds():
        Attempts = 5
        Password = Parser["Settings"]["Password"]
        while Attempts > 0:
            Pass = str(input(
                Font.Color.BLUE + "\n[+]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Update", "Insert", "None").format(Attempts) + "\n\n" + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))
            while Pass == "":
                Pass = str(input(
                   Font.Color.BLUE + "\n[+]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Update", "Insert", "None").format(Attempts) + "\n\n" + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))
            if Pass == Password:
                Downloader.Update()
                return
            else:
                Attempts = Attempts - 1
                print(Font.Color.RED + "\n[!]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Update", "Wrong", "None").format(Attempts))
        inp = input(Font.Color.RED + "\n[!]" + Font.Color.WHITE +
            Language.Translation.Translate_Language(filename, "Update", "Failed", "None").format(Attempts))

    @staticmethod
    def Update():
        path = Parser["Settings"]["Path"]
        previous_cwd = os.getcwd()

        if not os.path.isdir(path):
            print(Font.Color.RED + "\n[!]" + Font.Color.WHITE + "UPDATE FAILED: invalid update path")
            return
        moved_current = False

        try:
            os.chdir(path)
            if os.path.exists("Mr.Holmes_Old"):
                shutil.rmtree("Mr.Holmes_Old",)
            if os.path.exists("Mr.Holmes"):
                shutil.move("Mr.Holmes", "Mr.Holmes_Old")
                moved_current = True

            clone = subprocess.run(["git", "clone", "https://github.com/Lucksi/Mr.Holmes"], check=False, capture_output=True, text=True)
            if clone.returncode != 0:
                print(Font.Color.RED + "\n[!]" + Font.Color.WHITE + "UPDATE FAILED: git clone error")
                if clone.stderr:
                    print(Font.Color.RED + "[!]" + Font.Color.WHITE + clone.stderr.strip())
                if moved_current and os.path.exists("Mr.Holmes_Old") and not os.path.exists("Mr.Holmes"):
                    shutil.move("Mr.Holmes_Old", "Mr.Holmes")
                return

            choice = int(input(Font.Color.BLUE + "\n[+]" + Font.Color.WHITE +
                         Language.Translation.Translate_Language(filename, "Update", "Choice", "None")))
            if choice == 1:
                shutil.rmtree("Mr.Holmes_Old", ignore_errors=True)
                print(Font.Color.WHITE + Language.Translation.Translate_Language(filename,
                      "Update", "Delete", "None"))
            else:
                print(Font.Color.WHITE + Language.Translation.Translate_Language(filename,
                      "Update", "Keep", "None"))
            sleep(3)
            print("\n")
            inp = input(Font.Color.WHITE + Language.Translation.Translate_Language(
                filename, "Update", "Success", "None"))
        finally:
            os.chdir(previous_cwd)
