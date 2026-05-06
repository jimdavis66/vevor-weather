import os
import sys


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


def main() -> None:
    port = _env_int("PORT", 5000)
    workers = _env_int("WEB_CONCURRENCY", 2)
    threads = _env_int("GUNICORN_THREADS", 4)
    timeout = _env_int("GUNICORN_TIMEOUT", 30)

    argv = [
        "gunicorn",
        "--bind",
        f"0.0.0.0:{port}",
        "--workers",
        str(workers),
        "--threads",
        str(threads),
        "--timeout",
        str(timeout),
        "app.__main__:app",
    ]

    os.execvp(argv[0], argv)


if __name__ == "__main__":
    main()
