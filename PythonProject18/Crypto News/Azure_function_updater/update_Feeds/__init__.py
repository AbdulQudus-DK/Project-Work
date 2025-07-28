import logging
from datetime import datetime
import azure.functions as func
from feed_updater import run_update

app = func.FunctionApp()

@app.schedule(
    schedule="0 */5 * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=False
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('Timer trigger function ran past due time!')
    logging.info('Python timer trigger executed at %s', datetime.utcnow())

    try:
        run_update()
        logging.info("RSS feed update complete.")
    except Exception:
        logging.exception("RSS feed update failed.")
