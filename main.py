# main.py
from filemanager.helpers.s3_helpers import upload_file, list_versions, download_file


# from analyzer import analyze_csv


def main():
    print("\nWelcome to the Versioned File Manager + Analyzer")
    print("1. Upload File to S3")
    print("2. List File Versions")
    print("3. Download Specific Version")
    print("4. Analyze CSV File")
    print("5. Exit")

    while True:
        user_id = input("Enter your UserID for this session: ")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            upload_file(user_id)
        elif choice == "2":
            list_versions(user_id)
        elif choice == "3":
            download_file(user_id)
        # elif choice == "4":
        #     analyze_csv()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
