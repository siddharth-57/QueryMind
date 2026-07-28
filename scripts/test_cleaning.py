from src.preprocessing.cleaning import EmailCleaningService


service = EmailCleaningService()


emails = [
    (
        "Windows Line Endings",
        "Hello\r\nWorld\r\nAgain",
    ),
    (
        "Trailing Spaces",
        "Hello    \nWorld     ",
    ),
    (
        "Extra Blank Lines",
        "Hello\n\n\n\nWorld",
    ),
    (
        "Leading and Trailing Blank Lines",
        "\n\nHello Team\n\n",
    ),
    (
        "Empty Email",
        "",
    ),
]


for title, email in emails:
    print("=" * 60)
    print(title)
    print("-" * 60)

    print("BEFORE:")
    print(repr(email))

    cleaned = service.clean(email)

    print("\nAFTER:")
    print(repr(cleaned))
    print()