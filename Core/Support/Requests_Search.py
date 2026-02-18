# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2021-2023 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

 master
from requests import exceptions as RequestExceptions
from Core.Support import Font
from Core.Support import Language
from Core.Support import Headers
from Core.Support import HttpClient
 master

filename = Language.Translation.Get_Language()
filename


class Search:

    @staticmethod
    def _update_tags(subject, tag, unique, tags, most_tags):
        if subject == "PHONE-NUMBER":
            return

        for current_tag in tag:
            if current_tag in unique and current_tag not in most_tags:
                most_tags.append(current_tag)
            if current_tag in tags:
                if current_tag not in most_tags:
                    most_tags.append(current_tag)
            else:
                tags.append(current_tag)

    @staticmethod
    def _handle_found(writable, report, site1, name, main, tag, subject, unique, tags, most_tags):
        if writable is True:
            with open(report, "a", encoding="utf-8") as report_file:
                report_file.write(site1 + "\r\n")
            print(Font.Color.BLUE +
                  "[I]" + Font.Color.WHITE + "TAGS:[{}]".format(Font.Color.GREEN + ",".join(tag) + Font.Color.WHITE))
            Search._update_tags(subject, tag, unique, tags, most_tags)
        else:
            with open(report, "a", encoding="utf-8") as report_file:
                report_file.write("{}:{}\r\n".format(name, main))

    @staticmethod
    def _write_results(json_file, json_file2, successfull, successfull_name):
        names_payload = {
            "Names": [{"name": "{}".format(element)} for element in successfull_name]
        }
        sites_payload = {
            "List": [{"site": "{}".format(element)} for element in successfull]
        }
        FileIO.Json.write_atomic(json_file2, names_payload)
        FileIO.Json.write_atomic(json_file, sites_payload)

    @staticmethod
    def search(error, report, site1, site2, http_proxy, sites, data1, username, subject, successfull, name, successfullName, is_scrapable, ScraperSites, Writable, main, json_file, json_file2, Tag, Tags, MostTags):
        unique = ["Chess", "Books", "Pokemon", "Lol/League of Legends", "Minecraft", "Roblox", "Modelling", "Anime", "Shopping", "Writing", "Stories", "OSU", "ThemeForest", "Meme", "Python", "Ruby", "Npm", "Health", "Map", "File-Sharing", "Colors", "Crypto", "Speedrun", "Steam", "BitCoin", "Playstation", "Gallery", "Chess.com", "Badge"]
        headers = Headers.Get.classic()
        if name == "Twitter":
            headers = Headers.Get.Twitter()
master
        try:
            searcher = HttpClient.Client.get(
                url=site2, headers=headers, proxies=http_proxy, timeout=10, allow_redirects=True)
        except RequestExceptions.RequestException:
            print(Font.Color.RED + "[!]" + Font.Color.WHITE +
                  Language.Translation.Translate_Language(filename, "Default", "Connection_Error2", "None"))
            return

 master
        if error == "Status-Code":
            if searcher.status_code == 200:
                print(Font.Color.YELLOW + "[v]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "Found", "None").format(subject, username))
                print(Font.Color.YELLOW +
                      "[v]" + Font.Color.WHITE + "LINK: {}".format(site1))
                Search._handle_found(Writable, report, site1, name, main, Tag, subject, unique, Tags, MostTags)
                successfull.append(site1)
                successfullName.append(name)
                if is_scrapable == "True":
                    ScraperSites.append(name)
            elif searcher.status_code == 404 or searcher.status_code == 204:
                print(Font.Color.RED + "[!]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "NotFound", "None").format(subject, username))
            else:
                print(Font.Color.BLUE + "[N]" +
                      Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Default", "Connection_Error2", "None") + str(searcher.status_code))
master
        elif error == "Message":
            text = sites[data1]["text"]
            if text in searcher.text:
                print(Font.Color.RED + "[!]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "NotFound", "None").format(subject, username))
            else:
                print(Font.Color.YELLOW + "[v]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "Found", "None").format(subject, username))
                print(Font.Color.YELLOW +
                      "[v]" + Font.Color.WHITE + "LINK: {}".format(site1))
                Search._handle_found(Writable, report, site1, name, main, Tag, subject, unique, Tags, MostTags)
                successfull.append(site1)
                successfullName.append(name)
                if is_scrapable == "True":
                    ScraperSites.append(name)

        elif error == "Response-Url":
            response = sites[data1]["response"]
            if searcher.url == response:
                print(Font.Color.RED + "[!]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "NotFound", "None").format(subject, username))
            else:
                print(Font.Color.YELLOW + "[v]" + Font.Color.WHITE +
                      Language.Translation.Translate_Language(filename, "Default", "Found", "None").format(subject, username))
                print(Font.Color.YELLOW +
                      "[v]" + Font.Color.WHITE + "LINK: {}".format(site1))
                Search._handle_found(Writable, report, site1, name, main, Tag, subject, unique, Tags, MostTags)
                successfull.append(site1)
                successfullName.append(name)
                if is_scrapable == "True":
                    ScraperSites.append(name)

        Search._write_results(json_file, json_file2, successfull, successfullName)
