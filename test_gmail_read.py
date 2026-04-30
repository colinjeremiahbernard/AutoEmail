from gmail_service import get_gmail_service


def _header_value(headers, name, default="(none)"):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", default)
    return default


def main():
    service = get_gmail_service()

    # Fetch recent inbox messages and then read full metadata for each.
    response = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=5)
        .execute()
    )
    messages = response.get("messages", [])

    if not messages:
        print("No inbox messages found.")
        return

    print("Latest 5 inbox messages:\n")
    for i, message in enumerate(messages, start=1):
        full = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="metadata")
            .execute()
        )
        headers = full.get("payload", {}).get("headers", [])
        subject = _header_value(headers, "Subject")
        sender = _header_value(headers, "From")
        date = _header_value(headers, "Date")
        print(f"{i}. Subject: {subject}")
        print(f"   From: {sender}")
        print(f"   Date: {date}")
        print()


if __name__ == "__main__":
    main()
