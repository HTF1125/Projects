"""ROBERT"""
import os
import sys
import click
import logging

logger = logging.getLogger("app")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "../..")))


def init_dotenv(file_path=".env") -> bool:
    """A alternative to load_dotenv package"""
    try:
        from dotenv import load_dotenv

        return load_dotenv(file_path)
    except ImportError:
        import os

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    # Ignore comments and empty lines
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
            return True
        return False

if init_dotenv(".env"):
    logger.info("Load `.env` Successful.")


import app



@click.command()
@click.argument("task", default="db")
@click.option('--reload', is_flag=True, default=False, help='Enable or disable reloading')
def cli(task: str, reload: bool = True) -> None:
    if task == "db":
        app.db.update_meta()
    elif task == "web":
        logger.info("Launching Web...")
        app.web.main.app.run(debug=True, use_reloader=reload)
    elif task == "report":
        logger.info("[CLI]")
        from app.tasks.MarketDaily import get_report
        report = get_report()
        print(report)


if __name__ == "__main__":
    cli()
