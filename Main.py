from submaking import Flashcard

def main():
    flashcard_app = Flashcard()

    while True:
        print("\nFlashcard Manager")
        print("1. Select File")
        print("2. Add Flashcard")
        print("3. Remove Flashcard")
        print("4. Update Flashcard")
        print("5. Display All Flashcards")
        print("6. Display Flashcard by Index")
        print("7. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            set_name = input("Enter the name of the flashcard set (without extension): ")
            flashcard_app.set_current_set(set_name)
            flashcard_app.flashcards = flashcard_app.load_flashcards()
            print(f"Switched to flashcard set: {set_name}")

        elif choice == '2':
            title = input("Enter the term: ")
            description = input("Enter the description: ")
            print(flashcard_app.add_flashcard(title, description))

        elif choice == '3':
            index = int(input("Enter the index of the flashcard to remove: "))
            print(flashcard_app.delete_flashcard(index))

        elif choice == '4':
            index = int(input("Enter the index of the flashcard to update: "))
            title = input("Enter the new term: ")
            description = input("Enter the new description: ")
            print(flashcard_app.update_flashcard(index, title, description))

        elif choice == '5':
            print("\nAll Flashcards:")
            print(flashcard_app.display_flashcards())

        elif choice == '6':
            index = int(input("Enter the index of the flashcard to display: "))
            print(flashcard_app.display_flashcard_from_index(index))

        elif choice == '7':
            print("Exiting Flashcard Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
