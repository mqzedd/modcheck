import hashlib
import requests
from os import listdir
from os.path import isfile, join
from json import loads
import re
from directory import *

# Python program to find the SHA-1 message digest of a file


def hash_file(filename):
    """ "This function returns the SHA-1 hash
    of the file passed into it"""
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename, "rb") as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b"":
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()


endpoint = "https://api.modrinth.com/v2/version_file/"


def modcheck(dir):
    main_dir = dir + "/mods"
    onlyfiles = [f for f in listdir(main_dir) if isfile(join(main_dir, f))]
    mod_check = []
    mod_renamed = []

    for i in onlyfiles:
        reg_file_name = re.sub(r" \(.*?\)", "", i)
        if "CustomT" in reg_file_name:
            print("yess")
            print(i)
            print(reg_file_name)
        mod_hash = hash_file(main_dir + "/" + i)

        r = requests.get(endpoint + str(mod_hash), params={"algorithm": "sha1"})
        if r.status_code != 404:
            data = loads(r.text)
            modrinth_file_name = data["files"][0]["filename"]

            if modrinth_file_name != reg_file_name:
                print(modrinth_file_name)
                print(reg_file_name)
                print(mod_hash)
                mod_renamed.append(i)
        else:
            mod_check.append(i)

    print(str(len(mod_check)) + " mods were found that did not appear on modrinth\n")
    for i in mod_check:
        print(i)

    print(
        str(len(mod_renamed))
        + " mods were found that did not match with modrinth names"
    )
    for i in mod_renamed:
        print(i)


minecraft_directory = get_minecraft_working_directory()
if minecraft_directory:
    if type(minecraft_directory) != list:
        print("Minecraft working directory:", minecraft_directory)
        modcheck(minecraft_directory)
    else:
        print("Multiple instances found.")
        for i in minecraft_directory:
            print(i)
            modcheck(i)
else:
    print("Minecraft instance not found.")
input("Press Enter to continue...")

"""
Find Minecraft Instances
Find the working directories
Check mods against modrinth
"""
