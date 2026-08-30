from datetime import datetime

def flog(e: str) -> str:
    return f"{datetime.now().strftime('%H:%M:%S')} - {e}"