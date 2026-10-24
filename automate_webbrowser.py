import platform
import time
import urllib.parse  # 1. Added Python's native URL encoder
import webbrowser
import pandas as pd
import pyautogui

# ==============================================================================
# PHASE 1: CLEAN AND CONVERT RAW GOOGLE CONTACTS CSV
# ==============================================================================
print("⏳ Phase 1: Cleaning raw Google Contacts...")

raw_df = pd.read_csv("contacts.csv")
clean_data = []

for _, row in raw_df.iterrows():
    first_name = (
        str(row["First Name"]).strip() if pd.notna(row["First Name"]) else ""
    )
    phone = str(row["Phone 1 - Value"]) if pd.notna(row["Phone 1 - Value"]) else ""

    if first_name and phone:
        clean_phone = "".join(filter(str.isdigit, phone))

        if len(clean_phone) == 10:
            clean_phone = "+91" + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith("91"):
            clean_phone = "+" + clean_phone
        elif not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone

        clean_data.append(
            {"Phone": clean_phone, "Name": first_name, "Group": "Other"}
        )

output_df = pd.DataFrame(clean_data)
output_df.to_csv("wedding_guests.csv", index=False)
print(f"🎉 Processed {len(output_df)} contacts into 'wedding_guests.csv'!\n")


# ==============================================================================
# PHASE 2: AUTOMATE WHATSAPP INVITATIONS (SINGLE TAB BEHAVIOUR)
# ==============================================================================
print("⏳ Phase 2: Launching WhatsApp Web initialisation...")

# Detect if operating system is Mac or Windows for browser tab shortcuts
IS_MAC = platform.system() == "Darwin"

# Open WhatsApp Web once so you can log in / ensure connection is active
webbrowser.open("https://web.whatsapp.com/")
print("\n❗ IMPORTANT ❗")
print("1. Ensure your browser window is active and maximized.")
print("2. Make sure you are logged into WhatsApp Web.")
print("Waiting 15 seconds for initial connection setup...")
time.sleep(15)

df = pd.read_csv("wedding_guests.csv", dtype={"Phone": str})

for index, row in df.iterrows():
    phone = str(row["Phone"]).strip()
    name = str(row["Name"]).strip()

    if not phone or phone == "nan" or not name or name == "nan":
        continue

    # Clean URL text encoding for linebreaks and special characters
    message = (
        f"Hey {name}! \n\n"
        "With great joy, we invite you to celebrate the wedding of\n"
        "Akhila ❤️ Mukesh 💍✨\n\n"
        "Your presence would mean a lot to us on this special day.\n\n"
        "📅 Date: 26-06-2026\n"
        "📍 Venue: https://maps.app.goo.gl/VtSJzTkdTcSiAS4k8?g_st=ac \n\n"
        "Please find all the details here:\n"
        f"🌐 https://mukesh-weds-akhila.netlify.app?guest={name}\n\n"
        "Looking forward to celebrating together! 😊"
    )

    # 2. FIXED: Use urllib.parse.quote to safely encode your message text
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

    print(
        f"[{index + 1}/{len(df)}] Opening chat link for {name} ({phone})..."
    )

    # Opens the exact link string in your current active web window frame
    webbrowser.open(whatsapp_url)

    # Wait for the specific friend's chat page interface layout to render fully
    time.sleep(20)

    # Force press the 'Enter' key to execute send mechanism natively
    pyautogui.press("enter")
    print(f"✅ Message sent to {name}.")

    # Short buffer to ensure processing pipeline has cleared
    time.sleep(2)

    # Close the current chat tab layout safely so next iteration starts fresh
    print("🧹 Closing tab to prevent clutter...")
    if IS_MAC:
        pyautogui.hotkey("command", "w")
    else:
        pyautogui.hotkey("ctrl", "w")

    # Anti-Spam Safety Delay before starting next person
    print("⏳ Waiting 15 seconds for safety...")
    time.sleep(15)

print(
    "\n🎉 All wedding invitations from your CSV have been processed completely!"
)
