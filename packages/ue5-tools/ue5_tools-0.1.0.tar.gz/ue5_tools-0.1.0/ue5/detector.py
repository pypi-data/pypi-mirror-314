import os


def get_platform_from_config(platform: str):
    if platform == "Windows":
        return "Win64"

    raise ValueError("Invalid os for build, please manually specify a platform")


def find_ue_base_dir(platform: str):
    if platform == "Windows":
        return os.path.join("C:\\", "Program Files", "Epic Games")

    raise ValueError("Invalid os for build, please manually specify a UE install location")


def find_ue_install(base_dir: str, version: str):
    return os.path.join(str(base_dir), f"UE_{version}")


def find_scripts_location(ue_install_dir: str):
    return os.path.join(str(ue_install_dir), "Engine", "Build", "BatchFiles")