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
