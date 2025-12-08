"""ANSI color codes for terminal output"""

import sys

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @classmethod
    def success(cls, msg):
        """Print success message"""
        print(f"{cls.GREEN}✅ {msg}{cls.END}")

    @classmethod
    def error(cls, msg):
        """Print error message and exit"""
        print(f"{cls.RED}❌ {msg}{cls.END}")
        sys.exit(1)

    @classmethod
    def info(cls, msg):
        """Print info message"""
        print(f"{cls.BLUE}ℹ️  {msg}{cls.END}")

    @classmethod
    def warning(cls, msg):
        """Print warning message"""
        print(f"{cls.YELLOW}⚠️  {msg}{cls.END}")