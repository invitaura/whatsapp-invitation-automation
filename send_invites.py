import time
import pandas as pd
import pyautogui
import pywhatkit as kit

# 1. Load your cleaned CSV file (ensuring phone numbers stay as text strings)
csv_file = "wedding_guests.csv"
df = pd.read_csv(csv_file, dtype={'Phone': str})

print(f"Loaded {len(df)} guests from CSV. Starting the invitation process...\n")

# 2. Loop through each guest in the dataset
for index, row in df.iterrows():
    # Safely extract and clean data strings
    phone = str(row["Phone"]).strip()
    name = str(row["Name"]).strip()

    # Skip empty rows if any exist in the CSV
    if not phone or phone == "nan" or not name or name == "nan":
        print(f"⚠️ Skipping row {index + 1}: Missing name or phone number.")
        continue

    # 3. Personalized message template
    message = (
        f"Hey {name}! ✨ Big news—I am getting married! 💍\n\n"
        "I would be absolutely thrilled to have you share in our joy "
        "and celebrate this special day with us. Save the date!\n\n"
        "Here is our digital invitation link with all the venue and timing details: "
        "[INSERT_YOUR_DIGITAL_INVITE_LINK_HERE]\n\n"
        "Hope to see you there! Please let me know if you can make it. ❤️"
    )

    print(f"[{index + 1}/{len(df)}] Sending invitation to {name} ({phone})...")

    try:
        # 4. Automate WhatsApp Web to send the message
        kit.sendwhatmsg_instantly(
            phone_no=phone, 
            message=message, 
            wait_time=30, 
            tab_close=True
        )

        kit.sendwhatmsg_instantly(
        phone_no=phone, message=message, wait_time=25, tab_close=False
        )
        time.sleep(2)  # Wait 2 seconds for text to populate
        pyautogui.press("" \
        "" \
        "enter")  # Force press the Enter key to send!

        # 5. Anti-Spam Safety Delay (25 seconds)
        print(f"✅ Message sent to {name}. Waiting 25 seconds for safety...")
        time.sleep(25)

    except Exception as e:
        print(f"❌ Failed to send to {name}. Error: {e}")

print("\n🎉 All wedding invitations from your CSV have been processed!")
