# pipeline/scheduler.py
import schedule
import time
import logging
import multiprocessing
from pipeline.pipeline import run_pipeline

logger = logging.getLogger("scheduler")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")

# Event untuk menghentikan scheduler
STOP_EVENT = multiprocessing.Event()

def scheduler_loop(interval_minutes: int = 2):
    """Loop utama scheduler dengan kemampuan berhenti menggunakan STOP_EVENT."""
    schedule.every(interval_minutes).minutes.do(run_pipeline)
    logger.info(f"⏱ Scheduler aktif setiap {interval_minutes} menit.")

    while not STOP_EVENT.is_set():
        schedule.run_pending()
        time.sleep(1)

    logger.info("Scheduler dihentikan dengan aman.")

def start_scheduler(interval_minutes: int = 2):
    """Start scheduler di proses terpisah."""
    STOP_EVENT.clear()
    scheduler_process = multiprocessing.Process(target=scheduler_loop, args=(interval_minutes,))
    scheduler_process.start()
    logger.info(f"Scheduler dijalankan (PID={scheduler_process.pid})")
    return scheduler_process

def stop_scheduler():
    """Stop scheduler yang sedang berjalan."""
    STOP_EVENT.set()
    logger.info("STOP_EVENT dikirim ke scheduler.")
