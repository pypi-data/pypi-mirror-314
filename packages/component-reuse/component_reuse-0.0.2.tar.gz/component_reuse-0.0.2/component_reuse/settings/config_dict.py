from pydantic import ConfigDict

config_dict = ConfigDict(extra="forbid", str_strip_whitespace=True)
