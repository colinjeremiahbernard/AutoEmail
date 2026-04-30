import sys
from gmail_service import get_gmail_service, get_unread_emails, get_email_content
from phishing_detector import is_phishing
from summarizer import summarize_email
from reply_generator import generate_reply

def main():
    if hasattr(sys.stdout, 'buffer'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    service = get_gmail_service()
    messages = get_unread_emails(service)

    for msg in messages:
        msg_id = msg['id']
        email_text = get_email_content(service, msg_id)

        print("\n--- NEW EMAIL ---\n")
        print(email_text)

        if is_phishing(email_text):
            print("⚠️ Phishing detected! Skipping...\n")
            continue

        try:
            summary = summarize_email(email_text)
            reply = generate_reply(email_text)
        except RuntimeError as exc:
            print(f"\nConfiguration error: {exc}\n")
            return

        print("\n📌 SUMMARY:")
        print(summary)

        print("\n✉️ REPLY DRAFT:")
        print(reply)

if __name__ == "__main__":
    main()