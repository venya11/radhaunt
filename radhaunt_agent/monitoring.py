import psutil
from datetime import datetime


def get_server_status() -> str:
    boot_time_timestamp = psutil.boot_time()
    uptime_seconds = datetime.now().timestamp() - boot_time_timestamp
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    cpu_usage = psutil.cpu_percent(interval=0.5)
    
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    ram_used_gb = round(ram.used / (1024 ** 3), 2)
    ram_total_gb = round(ram.total / (1024 ** 3), 2)

    status_message = (
        "📊 <b>SERVER STATUS:</b>\n\n"
        f"⏱ <b>Uptime:</b> {hours}h {minutes}m\n"
        f"💿 <b>CPU:</b> {cpu_usage}%\n"
        f"🧠 <b>RAM:</b> {ram_usage}% ({ram_used_gb}Gb / {ram_total_gb}Gb)"
    )

    return status_message