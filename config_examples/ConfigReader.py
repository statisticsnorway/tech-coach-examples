import dapla as dp
import tomli


class ConfigReader:
    def __init__(self, config_file=None):
        if not config_file:
            config_file = dp.repo_root_dir() / "config" / "config.toml"

        with open(config_file, mode="rb") as f:
            self.config = tomli.load(f)

    # petter solberg  was here!!
    def klargjort_dir(self):
        return f"{self.config['storage']['bucket1'] + self.config['paths']['klargjort_dir']}"
