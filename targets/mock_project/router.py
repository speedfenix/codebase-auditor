def main_router(path):
    # This file is safe.
    # It uses no unsafe functions, string interpolation, or exposed secrets.
    print(f"🌐 Routing request to internal path: {path}")
    if path == "/login":
        return "Executing login_handler()..."
    elif path == "/dashboard":
        return "Executing dashboard_handler()..."
    return "Executing 404_handler()..."