import os
import subprocess

from conan import ConanFile

from ue5.detector import get_platform_from_config, find_ue_install, find_ue_base_dir, find_scripts_location


class UE5:

    def __init__(self, conanfile: ConanFile, uplugin_name: str):
        if conanfile.options.platform == None:
            self.platform = get_platform_from_config(conanfile.settings.os)
        else:
            self.platform = str(conanfile.options.platform)

        if conanfile.options.ue_base_dir == None:
            self.ue_base_dir = find_ue_base_dir(conanfile.settings.os)
        else:
            self.ue_base_dir = str(conanfile.options.ue_base_dir)

        self.ue_version = str(conanfile.options.ue_version)

        ue_install_path = find_ue_install(self.ue_base_dir, self.ue_version)
        scripts_folder = find_scripts_location(ue_install_path)

        if conanfile.settings.os == "Windows":
            self.script_path = os.path.join(scripts_folder, "RunUAT.bat")
        else:
            self.script_path = os.path.join(scripts_folder, "RunUAT.sh")

        self.plugin_path = os.path.join(conanfile.source_folder, uplugin_name)

    def build(self, build_folder: str):
        base_cmd = [self.script_path, "BuildPlugin", f'-plugin={self.plugin_path}', f'-package={build_folder}',
                    f"-TargetPlatforms={self.platform}", f"-HostPlatforms={self.platform}"]
        subprocess.run(base_cmd)

