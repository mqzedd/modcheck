import hashlib
import requests
from os import listdir
from os.path import isfile, join
from json import loads
import re
from time import sleep
from time import time
from tqdm.contrib.concurrent import thread_map
from directory import *


def hash_file(filename):
    """ "This function returns the SHA-1 hash
    of the file passed into it"""
    h = hashlib.sha1()
    with open(filename, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


endpoint = "https://api.modrinth.com/v2/version_file/"


def send_request(mod_hash):
    r = requests.get(endpoint + str(mod_hash), params={"algorithm": "sha1"})
    return r


def modcheck(dir):
    """Check the mods in the given directory against Modrinth's db on SHA-1 hashes"""

    main_dir = dir + "/mods"
    onlyfiles = [f for f in listdir(main_dir) if isfile(join(main_dir, f))]
    file_hashes = [hash_file(main_dir + "/" + i) for i in onlyfiles]
    api_results = []
    """ for i in tqdm(file_hashes):
        api_results.append(send_request(i))
     """
    api_results = thread_map(
        send_request, file_hashes, max_workers=100, desc="Checking Hashes"
    )  # uses threading to send the requests in parallel, appending the results to the api_results map
    unverified_mods = []
    mod_name_discrepancies = []
    for index, i in enumerate(onlyfiles):

        reg_file_name = re.sub(r" \(.*?\)", "", i)
        r = api_results[index]
        if r.status_code != 404:
            data = loads(r.text)
            modrinth_file_name = data["files"][0]["filename"]
            if modrinth_file_name != reg_file_name:
                mod_name_discrepancies.append(modrinth_file_name)
        else:
            unverified_mods.append(i)
    print(
        str(len(unverified_mods)) + " mods were found that did not appear on modrinth"
    )
    for i in unverified_mods:
        print(i)
    print(
        str(len(mod_name_discrepancies))
        + " mods were found that did not match with modrinth names"
    )
    for i in mod_name_discrepancies:
        print(i)


start = time()
minecraft_directory = get_minecraft_working_directory()
# minecraft_directory = "C:/Users/210284/Desktop/MC/MultiMC/instances/Simply Optimized-1.21-1.0(1)/.minecraft"
if minecraft_directory:
    if type(minecraft_directory) != list:
        print("Minecraft working directory:", minecraft_directory)
        modcheck(minecraft_directory)
    else:
        print("Multiple instances found.")
        for i in minecraft_directory:
            print("Minecraft working directory:", i + "\n")
            sleep(0.5)
            modcheck(i)
else:
    print("Minecraft instance not found.")
end = time()
print(f"Execution time: {end - start:.2f} seconds")
input("Press Enter to continue...")


"""
Find Minecraft Instances
Find the working directories
Check mods against modrinth
"""
