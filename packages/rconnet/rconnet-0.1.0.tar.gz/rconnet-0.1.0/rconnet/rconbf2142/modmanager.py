from .default import Default
from .modules.modmanager.bf2cc import Bf2cc
import re

class ModManager(Default):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bf2cc = Bf2cc(self)

    def start(self):
        super().start()
        if self.rcon_invoke("bf2cc check") == "rcon: unknown command: 'bf2cc'":
            raise Exception("Modmanager is not installed on the server")

    def list_modules(self):
        modules = {}
        pattern = r"^(.*?)\s+v(\d+\.\d+)\s+\(\s+(.*?)\s+\)$"
        lines = self.rcon_invoke("mm listModules")
        for line in lines.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                modules[match.group(1)] = {
                    "version": match.group(2),
                    "status": match.group(3)
                }

        return modules

    def config(self):
        pattern = r'(?P<section>\w+)\.(?P<option>\w+)\s+(?:(?P<value_int>\d+)|\"(?P<value_str>[^\"]+)\")'
        sections = {}

        data = self.rcon_invoke("mm printRunningConfig")
        for line in data.split("\n"):
            line = line.strip()

            if line.startswith("#"):
                continue

            match = re.match(pattern, line)

            if not match:
                continue

            section = match.group('section')
            option = match.group('option')
            value = match.group('value_int') or match.group('value_str')

            if value.isdigit(): value = int(value)

            sections[section] = sections.get(section, {})

            if option.startswith("add") or option == "loadModule":
                sections[section][option] = sections[section].get(option, [])
                sections[section][option].append(value)
            else:
                sections[section][option] = sections[section].get(option, value)

        return sections

    def reload_module(self, module:str):
        return self.rcon_invoke("mm reloadModule %s" % module)

    def start_module(self, module:str):
        return self.rcon_invoke("mm startModule %s" % module)

    def shutdown_module(self, module:str):
        return self.rcon_invoke("mm shutdownModule %s" % module)

    def load_module(self, module:str):
        return self.rcon_invoke("mm loadModule %s" % module)

    def save_config(self):
        return self.rcon_invoke("mm saveConfig")

    def set_param(self, module:str, option:str, value:str):
        return self.rcon_invoke("mm setParam %s %s %s" % (module, option, value))