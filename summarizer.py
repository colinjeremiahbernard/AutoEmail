from groq import Groq
from groq import AuthenticationError
from config import get_groq_api_key

client = Groq(api_key=get_groq_api_key())

def summarize_email(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Summarize this email briefly."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except AuthenticationError as exc:
        raise RuntimeError(
            "Groq authentication failed (invalid/revoked GROQ_API_KEY). "
            "Generate a new key in Groq Console and update your GROQ_API_KEY environment variable."
        ) from exc