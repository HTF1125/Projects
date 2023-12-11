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
<<<<<<< HEAD
@click.option('--reload', is_flag=True, default=False, help='Enable or disable reloading')
def cli(task: str, reload: bool = True) -> None:
=======
@click.argument("reload", default=False)
def cli(task: str, reload: bool = False) -> None:
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
    if task == "db":
        app.db.update_data()
    elif task == "web":
        logger.info("Launching Web...")
<<<<<<< HEAD
        app.web.main.app.run(debug=True, use_reloader=reload)
=======
        app.web.main.app.run(debug=True, use_reloader=True)
>>>>>>> 3a8d11a3ae1c822184425cb0a9faf53060b96302
    elif task == "report":
        logger.info("[CLI]")
        from app.tasks.MarketDaily import get_report
        report = get_report()
        print(report)


if __name__ == "__main__":
    cli()
