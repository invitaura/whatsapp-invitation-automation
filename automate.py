import time
import pandas as pd
import pyautogui
import pywhatkit as kit

# ==============================================================================
# PHASE 1: CLEAN AND CONVERT RAW GOOGLE CONTACTS CSV
# ==============================================================================
print("⏳ Phase 1: Cleaning raw Google Contacts...")

# Load your raw Google CSV file
raw_df = pd.read_csv("contacts.csv")
clean_data = []

# Extract only First Name and Phone
for _, row in raw_df.iterrows():
    first_name = str(row["First Name"]).strip() if pd.notna(row["First Name"]) else ""
    phone = str(row["Phone 1 - Value"]) if pd.notna(row["Phone 1 - Value"]) else ""

    if first_name and phone:
        # Extract digits only to remove spaces, brackets, and dashes
        clean_phone = "".join(filter(str.isdigit, phone))

        # Format with Indian Country Code (+91)
        if len(clean_phone) == 10:
            clean_phone = "+91" + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith("91"):
            clean_phone = "+" + clean_phone
        elif not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone

        group = "Other"

        clean_data.append({
            "Phone": clean_phone,
            "Name": first_name,
            "Group": group
        })

# Create and save the intermediate cleaned CSV
output_df = pd.DataFrame(clean_data)
output_df.to_csv("wedding_guests.csv", index=False)

print("📊 Cleaned Sheet Preview:")
print(output_df.head(7))
print(f"🎉 Successfully processed {len(output_df)} contacts into 'wedding_guests.csv'!\n")


# ==============================================================================
# PHASE 2: AUTOMATE WHATSAPP INVITATIONS FROM THE CLEANED DATA
# ==============================================================================
print("⏳ Phase 2: Starting WhatsApp invitation automation...")

# Load the newly created CSV file (ensuring phone numbers stay as text strings)
df = pd.read_csv("wedding_guests.csv", dtype={'Phone': str})
print(f"Loaded {len(df)} guests from CSV. Starting the process...\n")

# Loop through each guest in the dataset
for index, row in df.iterrows():
    phone = str(row["Phone"]).strip()
    name = str(row["Name"]).strip()

    # Skip empty rows if any exist
    if not phone or phone == "nan" or not name or name == "nan":
        print(f"⚠️ Skipping row {index + 1}: Missing name or phone number.")
        continue

    # Personalized wedding message template
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
        # 1. Open WhatsApp Web and load chat (Wait 30 seconds to make sure it loads fully)
        kit.sendwhatmsg_instantly(
            phone_no=phone, 
            message=message, 
            wait_time=30, 
            tab_close=False
        )
        
        # 2. Short buffer to guarantee the message text populates the text box
        time.sleep(3)  
        
        # 3. Hardware fallback: Force-press the Enter key to guarantee it sends
        pyautogui.press("enter")  
        print(f"✅ Message sent to {name}.")

        # 4. Anti-Spam Safety Delay: Pause for 25 seconds before moving to the next person
        print("⏳ Waiting 25 seconds for safety...")
        time.sleep(25)

    except Exception as e:
        print(f"❌ Failed to send to {name}. Error: {e}")

print("\n🎉 All wedding invitations from your CSV have been processed completely!")
