import hashlib
import os
import json

HASH_FILE = "file_hashes.json"

def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"❌ Error reading file '{file_path}': {e}")
        return None

def save_hashes(hashes):
    """Save file hashes to a JSON file."""
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

def load_hashes():
    """Load existing hashes from a JSON file."""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def main():
    while True:
        print("\n File Integrity Checker")
        print("1. Generate & Store File Hashes")
        print("2. Check File Integrity")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            files = input("Enter file paths to monitor (comma-separated): ").split(",")
            hashes = load_hashes()
            found_files = 0  # Track valid files

            for file in files:
                file = file.strip()
                if os.path.exists(file):
                    hashes[file] = calculate_hash(file)
                    print(f"✅ Stored hash for '{file}'")
                    found_files += 1
                else:
                    print(f"❌ Error: File '{file}' not found.")

            if found_files > 0:
                save_hashes(hashes)
                print("✅ Hashes saved successfully.")
            else:
                print("⚠️ No valid files found. Hashes were NOT saved.")

        elif choice == "2":
            hashes = load_hashes()
            if not hashes:
                print("⚠️ No hashes found. Please generate hashes first.")
                continue

            for file, old_hash in hashes.items():
                if os.path.exists(file):
                    new_hash = calculate_hash(file)
                    if new_hash == old_hash:
                        print(f"✅ File '{file}' is unchanged.")
                    else:
                        print(f"⚠️ WARNING: File '{file}' has been modified!")
                else:
                    print(f"❌ ALERT: File '{file}' is missing!")

        elif choice == "3":
            print("🔒 Exiting the File Integrity Checker. Stay Secure!")
            break
        else:
            print("❌ Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()
