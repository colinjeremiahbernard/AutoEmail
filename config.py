import os


def get_groq_api_key():
    # Try reading from a local .env file manually (no extra modules required)
    env_key = None
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GROQ_API_KEY="):
                    env_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    key = env_key or (os.getenv("GROQ_API_KEY") or "").strip().strip('"').strip("'")
    
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Set it in your environment before running."
        )
    if key in {"YOUR_NEW_KEY", "PASTE_NEW_KEY_HERE"}:
        raise RuntimeError(
            "GROQ_API_KEY is still a placeholder value. Replace it with a real Groq key."
        )
    if not key.startswith("gsk_"):
        raise RuntimeError(
            "GROQ_API_KEY format is invalid (expected it to start with 'gsk_')."
        )
    return key
