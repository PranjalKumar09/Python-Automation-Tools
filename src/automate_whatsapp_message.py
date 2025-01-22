import pywhatkit as pyw
import time

# Function to send a WhatsApp message immediately
def send_message_now():
    phone_number = input("Enter the recipient's phone number (with country code): ")
    message = input("Enter the message to send: ")
    try:
        pyw.sendwhatmsg_instantly(phone_number, message)
        print(f"Message sent to {phone_number} successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def schedule_message():
    phone_number = input("Enter the recipient's phone number (with country code): ")
    message = input("Enter the message to send: ")
    hour = int(input("Enter the hour (24-hour format): "))
    minute = int(input("Enter the minute: "))
    try:
        pyw.sendwhatmsg(phone_number, message, hour, minute)
        print(f"Message scheduled to {phone_number} at {hour}:{minute}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_image():
    phone_number = input("Enter the recipient's phone number (with country code): ")
    image_path = input("Enter the full path to the image: ")
    caption = input("Enter a caption (optional, press Enter to skip): ")
    try:
        pyw.sendwhats_image(phone_number, image_path, caption)
        print(f"Image sent to {phone_number} successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def display_menu():
    print("\n=== WhatsApp Automation Menu ===")
    print("1. Send a WhatsApp message now")
    print("2. Schedule a WhatsApp message")
    print("3. Send a WhatsApp image")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    return choice

def main():
    while True:
        choice = display_menu()
        if choice == "1":
            send_message_now()
        elif choice == "2":
            schedule_message()
        elif choice == "3":
            send_image()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        time.sleep(2) 

if __name__ == "__main__":
    main()
    

