def get_version():
    try:
        with open("./VERSION", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "unknown"
