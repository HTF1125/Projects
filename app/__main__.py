"""ROBERT"""
import os
import sys


if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv

        load_dotenv(".env")
    except ImportError:
        pass


# add current package to the path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(__file__), "../..")))

import click
import app

import logging
logger = logging.getLogger(__name__)

@click.command()
@click.argument("task", default="db")
def cli(task: str) -> None:
    if task == "db":
        logger.info("Updating Database...")
        # robo.db.admin.update_px()
        app.database.admin.update_px()
    elif task == "web":
        logger.info("Launching Web...")
        app.web.main.app.run(debug=True)
    elif task == "report":
        from app.tasks.MarketDaily import get_report
        report = get_report()
        print(report)

    msg = "*" * 20 + "[TASK COMPLETE]" + "*" * 20
    logger.info(msg)


if __name__ == "__main__":
    cli()
