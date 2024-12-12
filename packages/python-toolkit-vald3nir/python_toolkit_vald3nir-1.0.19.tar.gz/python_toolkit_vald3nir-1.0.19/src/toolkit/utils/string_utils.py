import uuid


def create_uuid() -> str:
    return str(uuid.uuid4())


def format_email_to_key(email: str) -> str:
    return email.replace("@", "_").replace(".", "_")
