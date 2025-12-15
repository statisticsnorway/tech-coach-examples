from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=["settings.toml"],
    envvar_prefix="DYNACONF",
    environments=True,
    env="default",  # Change this to gsbuckets for use with google storage buckets
)

settings_simple = Dynaconf(
    settings_files=["settings_simple.toml"],
    envvar_prefix="DYNACONF_SIMPLE",
    environments=False,
)
