def confirm_action(message):
    choice = input(f"{message} (y/n): ").strip().lower()
    return choice in ['y', 'yes']

def choose_from_list(options):
    print(f"\nChoose an option:")
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    while True:
        try:
            choice = int(input("\nEnter number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
