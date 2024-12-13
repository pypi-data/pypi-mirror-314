from CommandLine import CommandLine
from Config import Config

cfg = Config('atlaversity.toml')
command_line = CommandLine(cfg)
command_line.run()
