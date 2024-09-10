import os
import psutil


def get_minecraft_working_directory():
    process_name = "javaw.exe"
    instances = []
    for proc in psutil.process_iter(["name", "cwd"]):
        if proc.info["name"] == process_name:
            instances.append(proc.info["cwd"])
    if len(instances) == 1:
        return instances[0]
    else:
        print(f"Found {len(instances)} instances of {process_name}.")
        return instances
    return None


if __name__ == "__main__":
    minecraft_directory = get_minecraft_working_directory()
    if minecraft_directory:
        print("Minecraft working directory:", minecraft_directory)
    else:
        print("Minecraft instance not found.")
