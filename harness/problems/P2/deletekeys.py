import os

# Define a list of filenames to be deleted
files_to_delete = ["keys.txt", "encrypt.py"]

print("Starting file deletion process...")

# Loop through each file in the list
for filename in files_to_delete:
    # Check if the file exists in the current directory
    if os.path.exists(filename):
        try:
            # If it exists, delete the file
            os.remove(filename)
            print(f"Success: '{filename}' has been deleted.")
        except OSError as e:
            # Handle potential errors (e.g., permission issues or it's a directory)
            print(f"Error: Could not delete '{filename}'. Reason: {e}")
    else:
        # If the file does not exist, print a message
        print(f"Info: '{filename}' not found. No action taken.")

print("\nProcess finished.")