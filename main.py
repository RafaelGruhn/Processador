"""Main from core."""
import logging
from models import Memory, ULA

LOGGER = logging.getLogger(__name__)

def main():
    ula = ULA()
    ula.execute()

if __name__ == '__main__':
    main()
