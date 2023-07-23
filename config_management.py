import os
import logging
import desired_state
import backup_and_rollback
import interactive_mode
import config_management_tools

# Set up logging
logging.basicConfig(filename='config_management.log', level=logging.INFO)

def disclaimer():
    print("DISCLAIMER: Use at your own risk. This script is provided as-is without warranty of any kind.")

def menu():
    # ... (previous menu function)

def load_desired_state_from_file(filepath):
    try:
        desired_state.load_from_file(filepath)
        print("Desired state loaded successfully.")
    except Exception as e:
        print(f"Error loading desired state: {e}")

def validate_desired_state():
    if desired_state.is_valid():
        print("Desired state is valid.")
    else:
        print("Desired state is not valid.")

def main():
    disclaimer()
    desired_state.initialize()  # Initialize desired state from default values or empty state
    backup_and_rollback.initialize()  # Initialize backup state

    while True:
        menu()
        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            current_state = desired_state.get_current_state()
            print("Current state:")
            print(current_state)

        elif choice == '2':
            print("Desired state:")
            print(desired_state.get_desired_state())

        elif choice == '3':
            desired_state.save_to_file()
            print("Desired state saved to the configuration file.")

        elif choice == '4':
            filepath = input("Enter the path to the configuration file: ")
            load_desired_state_from_file(filepath)

        elif choice == '5':
            validate_desired_state()

        elif choice == '6':
            changes_needed = desired_state.compare_states()
            if changes_needed:
                interactive_mode.review_changes(changes_needed)
            else:
                print("No changes needed.")

        elif choice == '7':
            interactive_mode.modify_desired_state()

        elif choice == '8':
            if interactive_mode.confirm_apply_changes():
                changes_needed = desired_state.compare_states()
                if changes_needed:
                    if backup_and_rollback.create_backup():
                        if desired_state.apply_changes():
                            print("Changes applied successfully.")
                        else:
                            print("Failed to apply changes. Please check the logs for details.")
                            backup_and_rollback.rollback()
                    else:
                        print("Failed to create a backup. Changes not applied.")
                else:
                    print("No changes needed.")

        elif choice == '9':
            exit()

        else:
            print("Invalid choice. Please select a valid option (1-9).")

if __name__ == "__main__":
    main()
