import logging
import os


def get_settings():
    return {
        "APP_ENV": os.getenv("APP_ENV", "dev"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "API_TIMEOUT_SECONDS": int(os.getenv("API_TIMEOUT_SECONDS", "30")),
    }


def configure_logging(level_name="INFO"):
    logging.basicConfig(
        level=getattr(logging, level_name.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main():
    settings = get_settings()
    configure_logging(settings["LOG_LEVEL"])
    logging.info("service starting with settings=%s", settings)


if __name__ == "__main__":
    main()
