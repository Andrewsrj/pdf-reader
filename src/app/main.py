from __future__ import annotations

import sys

from app.bootstrap import create_application


def main() -> int:
    application, window = create_application(sys.argv)
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
