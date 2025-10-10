# Simple File Handling Script in Python
# This script allows users to read, write, append, and read & write to a text file.

# The file we are going to use
FILENAME = "nomes.txt"

# Loop that keeps the program running until the user exits
while True:
    print("\n=== FILE HANDLING MENU ===")
    print("1) Read file ('r')")
    print("2) Write new file ('w')")
    print("3) Append to file ('a')")
    print("4) Read & Write ('r+')")
    print("5) Exit")

    # Ask the user to choose an option
    choice = input("Choose an option: ").strip()

    # --------------------------------------------------------------
    # Option 1: Read file
    # --------------------------------------------------------------
    if choice == "1":
        try:
            # Open the file in read mode ('r')
            with open(FILENAME, "r") as file:
                content = file.read().strip()
                # If there is content, print it
                if content:
                    print("\n--- File Content ---")
                    print(content)
                    print("---------------------")
                # If the file is empty, show a message
                else:
                    print("\nThe file is empty.")
        # Handle the case when the file does not exist
        except FileNotFoundError:
            print("\nFile not found. Create or write one first.")

    # --------------------------------------------------------------
    # Option 2: Write new file (overwrite)
    # --------------------------------------------------------------
    elif choice == "2":
        print("\nWARNING: This will overwrite the file completely!")
        confirm = input("Type 'YES' to continue: ").strip().upper()

        if confirm == "YES":
            # Ask the user for new content
            data = input("Enter new content: ").strip()
            # Open the file in write mode ('w')
            with open(FILENAME, "w") as file:
                file.write(data + "\n")
            print(f"\nFile '{FILENAME}' overwritten successfully.")
        else:
            print("\nOperation canceled.")

    # --------------------------------------------------------------
    # Option 3: Append new content to the file
    # --------------------------------------------------------------
    elif choice == "3":
        # Ask the user for new data to add
        data = input("Enter text to append: ").strip()

        if data:
            # Open the file in append mode ('a')
            with open(FILENAME, "a") as file:
                file.write(data + "\n")
            print("\nContent appended successfully.")
        else:
            print("\nNothing entered. File unchanged.")

    # --------------------------------------------------------------
    # Option 4: Read & Write in the same session
    # --------------------------------------------------------------
    elif choice == "4":
        try:
            # Open the file in read and write mode ('r+')
            with open(FILENAME, "r+") as file:
                # Read and display current file content
                content = file.read()
                print("\n--- Current File Content ---")
                print(content if content.strip() else "(File empty)")
                print("------------------------------")

                # Ask the user for new data to add
                new_data = input("\nEnter new content to append: ").strip()

                if new_data:
                    file.write("\n" + new_data)
                    print("\nContent added using r+ mode.")
                else:
                    print("\nNo content entered.")
        # Handle missing file error
        except FileNotFoundError:
            print("\nFile not found. Create it first using option 2.")

    # --------------------------------------------------------------
    # Option 5: Exit the program
    # --------------------------------------------------------------
    elif choice == "5":
        print("\nExiting program... Goodbye!")
        break

    # --------------------------------------------------------------
    # Invalid option entered
    # --------------------------------------------------------------
    else:
        print("\nInvalid option. Please choose 1–5.")
