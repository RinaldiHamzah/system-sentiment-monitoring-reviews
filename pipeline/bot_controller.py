import multiprocessing
import logging
from flask import Blueprint, jsonify
from pipeline import bot_id
from pipeline import scheduler  # pastikan file ini sesuai yang sudah kamu perbaiki sebelumnya

# Inisialisasi blueprint Flask
bot_bp = Blueprint("bot_controller", __name__)

# Setup logger
logger = logging.getLogger("controller_bot")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")

# GLOBAL STATE
bot_process: multiprocessing.Process | None = None
scheduler_process: multiprocessing.Process | None = None

# BOT CONTROL FUNCTIONS
@bot_bp.post("/bot/start")
def start_bot():
    """Menjalankan bot Telegram di background process."""
    global bot_process

    if bot_process and bot_process.is_alive():
        return jsonify({"ok": False, "msg": "Bot runing."})

    # Pastikan stop event belum aktif
    bot_id.STOP_EVENT.clear()

    # Jalankan bot di proses terpisah
    bot_process = multiprocessing.Process(target=bot_id.run_bot, daemon=True)
    bot_process.start()

    logger.info(f"(PID={bot_process.pid})")
    return jsonify({"ok": True, "msg": f"(PID={bot_process.pid})"})


@bot_bp.post("/bot/stop")
def stop_bot():
    """Menghentikan bot Telegram."""
    global bot_process

    if not bot_process or not bot_process.is_alive():
        return jsonify({"ok": False, "msg": "Bot tidak sedang berjalan."})

    logger.info("STOP_EVENT")
    bot_id.STOP_EVENT.set()

    bot_process.terminate()
    bot_process.join(timeout=3)
    bot_process = None

    logger.info("Telegram dihentikan.")
    return jsonify({"ok": True, "msg": "Bot dihentikan."})

# SCHEDULER CONTROL FUNCTIONS
@bot_bp.post("/scheduler/start")
def start_scheduler():
    """Menjalankan scheduler di background process."""
    global scheduler_process

    if scheduler_process and scheduler_process.is_alive():
        return jsonify({"ok": False, "msg": "Scheduler berjalan."})

    scheduler.STOP_EVENT.clear()
    scheduler_process = multiprocessing.Process(
        target=scheduler.scheduler_loop, daemon=True
    )
    scheduler_process.start()

    logger.info(f"⏱(PID={scheduler_process.pid})")
    return jsonify({"ok": True, "msg": f"(PID={scheduler_process.pid})"})


@bot_bp.post("/scheduler/stop")
def stop_scheduler():
    """Menghentikan scheduler."""
    global scheduler_process

    if not scheduler_process or not scheduler_process.is_alive():
        return jsonify({"ok": False, "msg": "Scheduler unruning."})

    logger.info("STOP_EVENT ")
    scheduler.STOP_EVENT.set()

    scheduler_process.terminate()
    scheduler_process.join(timeout=3)
    scheduler_process = None

    logger.info("Scheduler stopped")
    return jsonify({"ok": True, "msg": "Scheduler stopped."})

# STATUS ENDPOINT
@bot_bp.get("/bot/status")
def bot_status():
    """Cek status bot Telegram."""
    running = bot_process.is_alive() if bot_process else False
    return jsonify({"bot_running": running})


@bot_bp.get("/scheduler/status")
def scheduler_status():
    """Cek status scheduler."""
    running = scheduler_process.is_alive() if scheduler_process else False
    return jsonify({"scheduler_running": running})


