from parser_regex import parse_sms_regex

def main():
    with open("data/sms_samples.txt", "r") as file:
        messages = file.readlines()

    for msg in messages:
        msg = msg.strip()
        if not msg:
            continue

        print("\nRAW:", msg)

        result = parse_sms_regex(msg)
        print("PARSED:", result)


if __name__ == "__main__":
    main()