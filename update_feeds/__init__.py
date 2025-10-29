import logging
from datetime import datetime
import azure.functions as func
from feed_updater import run_update


def main(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('Timer trigger function ran past due time!')

    logging.info('Python timer trigger function ran at %s', datetime.utcnow())

    try:
        run_update()
        logging.info("RSS feed update complete.")
    except Exception:
        logging.exception("RSS feed update failed.")
