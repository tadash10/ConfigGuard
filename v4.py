import os
import logging
import argparse
import json
import desired_state
import backup_and_rollback
import interactive_mode
import config_management_tools
import secure_input_handling
import automated_testing
import user_messages
import interactive_configuration_setup

# Set up logging
logging.basicConfig(filename='config_management.log', level=logging.INFO)

def disclaimer():
    user_messages.display_message("DISCLAIMER: Use at your own risk. This script is provided as-is without warranty of any kind.")

def configure_logging():
    # Set up logging
    logging.basicConfig(filename='config_management.log', level=logging.INFO)

def load_desired_state_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            desired_state.load(data)
            print("Desired state loaded successfully.")
    except Exception as e:
        print(f"Error loading desired state: {e}")

def validate_desired_state():
    if desired_state.is_valid():
        print("Desired state is valid.")
    else:
        print("Desired state is not valid.")

def show_changes_needed(changes_needed):
    for category, items in changes_needed.items():
        for name, values in items.items():
            print(f"Changes needed for '{name}' in '{category}' category:")
            for key, value in values.items():
                print(f"    {key}: {value}")

def get_user_confirmation():
    while True:
        user_input = input("Apply changes? (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    disclaimer()
    configure_logging()

    # Interactive Configuration Setup
    interactive_configuration_setup.setup_logging_preferences()
    config_management_tools.setup()
    # ... (Add setup functions for other configuration tools if applicable)

    parser = argparse.ArgumentParser(description='Configuration Management Tool')
    parser.add_argument('--config-file', metavar='config_file', type=str, default='desired_state.json',
                        help='Path to the configuration file containing the desired state (default: desired_state.json)')
    args = parser.parse_args()

    desired_state.load_from_file(args.config_file)

    while True:
        interactive_mode.menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            current_state = desired_state.get_current_state()
            print("Current state:")
            print(current_state)

        elif choice == '2':
            print("Desired state:")
            print(desired_state.get_desired_state())

        elif choice == '3':
            current_state = desired_state.get_current_state()
            changes_needed = desired_state.compare_states(current_state)
            if changes_needed:
                show_changes_needed(changes_needed)
            else:
                print("No changes needed.")

        elif choice == '4':
            current_state = desired_state.get_current_state()
            changes_needed = desired_state.compare_states(current_state)
            if changes_needed:
                show_changes_needed(changes_needed)
                if get_user_confirmation():
                    if backup_and_rollback.create_backup():
                        if desired_state.apply_changes(changes_needed):
                            print("Changes applied successfully.")
                        else:
                            print("Failed to apply changes. Please check the logs for details.")
                            backup_and_rollback.rollback()
                    else:
                        print("Failed to create a backup. Changes not applied.")
            else:
                print("No changes needed.")

        elif choice == '5':
            exit()

        else:
            print("Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    main()
