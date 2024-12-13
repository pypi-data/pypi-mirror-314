from prompt_toolkit import print_formatted_text as print
from prompt_toolkit import  HTML

class Logging():
    message_list = []

    @staticmethod
    def blue(msg):
        print(HTML(f'<ansiblue>{msg}</ansiblue>'))

    @staticmethod
    def green(msg, end = '\n'):
        print(HTML(f'<ansigreen>{msg}</ansigreen>'), end=end)

    @staticmethod
    def magenta(msg, end = '\n'):
        print(HTML(f'<ansimagenta>{msg}</ansimagenta>'), end=end)

    @staticmethod
    def cyan(msg, end = '\n'):
        print(HTML(f'<ansicyan>{msg}</ansicyan>'), end=end)

    @staticmethod
    def red(msg, end = '\n'):
        print(HTML(f'<ansired>{msg}</ansired>'), end=end)

    @staticmethod
    def yellow(msg, end = '\n'):
        print(HTML(f'<ansiyellow>{msg}</ansiyellow>'), end=end)

    @staticmethod
    def gray(msg, end = '\n'):
        print(HTML(f'<ansigray>{msg}</ansigray>'), end=end)

    @staticmethod
    def ok(msg):
        Logging.green(msg)

    @staticmethod
    def warning(msg):
        Logging.message_list.append(f'WARNING: {msg}')
        Logging.yellow(msg)

    @staticmethod
    def error(msg):
        Logging.message_list.append(f'ERROR: {msg}')
        Logging.red(msg)
        # raise ValueError(msg)

    @staticmethod
    def clear_message_list():
        Logging.message_list = []

    @staticmethod
    def get_message_list():
        return Logging.message_list
