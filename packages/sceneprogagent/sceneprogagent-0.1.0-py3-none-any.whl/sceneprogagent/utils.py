def print_colored(text: str, color: str = "default", silent: bool = False):
        if silent:
            return
        """
        Prints text in various colors.
        
        Args:
            text (str): The text to print.
            color (str): The color of the text. Options are:
                        "black", "red", "green", "yellow", "blue", "magenta",
                        "cyan", "white", or "default".
        """
        colors = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "default": "\033[39m"
        }
        
        reset = "\033[0m"
        color_code = colors.get(color.lower(), colors["default"])
        
        print(f"{color_code}{text}{reset}")