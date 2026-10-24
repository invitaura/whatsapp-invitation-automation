import os
import platform
import time
import urllib.parse
import pyperclip
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# PHASE 1: CLEAN AND CONVERT RAW GOOGLE CONTACTS CSV
# ==============================================================================
# print("⏳ Phase 1: Cleaning raw Google Contacts...")

# if not os.path.exists("muki_contacts.csv"):
#     print("❌ Error: 'muki_contacts.csv' not found in this folder!")
#     print("Please place your downloaded Google Contacts CSV here and rename it to 'muki_contacts.csv'.")
#     exit()

# raw_df = pd.read_csv("muki_contacts.csv")
# clean_data = []

# for _, row in raw_df.iterrows():
#     first_name = str(row["First Name"]).strip() if pd.notna(row["First Name"]) else ""
#     phone = str(row["Phone 1 - Value"]) if pd.notna(row["Phone 1 - Value"]) else ""

#     if first_name and phone:
#         clean_phone = "".join(filter(str.isdigit, phone))

#         if len(clean_phone) == 10:
#             clean_phone = "+91" + clean_phone
#         elif len(clean_phone) == 12 and clean_phone.startswith("91"):
#             clean_phone = "+" + clean_phone
#         elif not clean_phone.startswith("+"):
#             clean_phone = "+" + clean_phone

#         clean_data.append({
#             "Phone": clean_phone,
#             "Name": first_name,
#             "Group": "Other"
#         })

# output_df = pd.DataFrame(clean_data)
# output_df.to_csv("muki_wedding_guests.csv", index=False)
# print("📊 Cleaned Guest List Preview:")
# print(output_df.head(5))
# print(f"🎉 Successfully processed {len(output_df)} valid contacts into 'muki_wedding_guests.csv'!\n")


# ==============================================================================
# PHASE 2: AUTOMATE WHATSAPP INVITATIONS VIA SELENIUM
# ==============================================================================
print("⏳ Phase 2: Launching Automation Engine...")

options = webdriver.ChromeOptions()

# FIX: Use a dedicated nested directory to completely avoid active browser file locks
script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "selenium_wp_session", "profile")
options.add_argument(f"--user-data-dir={profile_path}")

# Wedding invitation image to attach with each message
image_path = os.path.join(script_dir, "wedding_invite.jpg")
if not os.path.exists(image_path):
    print(f"❌ Error: Wedding invitation image not found at '{image_path}'")
    print("Please place your invitation image as 'wedding_invite.jpg' in the script folder.")
    exit()

# FIX: Operational stability arguments to clear DevTools port initialization crashes
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# Initialize chrome web driver binaries
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options
)

# Navigate straight to standard WhatsApp Web interface 
driver.get("https://web.whatsapp.com")

print("\n🔒 ACTION REQUIRED IN YOUR TERMINAL SCREEN:")
print("1. Look at the newly opened automated Chrome browser window.")
print("2. If you are logged out, scan the QR code using your phone's WhatsApp Link Devices feature.")
print("3. Wait until your chat list dashboard interface completely loads on screen.")
input("\n👉 Once your chats are fully loaded on screen, press ENTER here to start sending...")

print("\n🚀 Authentication passed! Initializing transmission cycle...")

df = pd.read_csv("muki_wedding_guests_copy.csv", dtype={"Phone": str})

for index, row in df.iterrows():
    phone = str(row["Phone"]).strip().replace("+", "")  
    name = str(row["Name"]).strip()

    if not phone or phone == "nan" or not name or name == "nan":
        continue

    # Clean structured invitation copy block
    message = (
        f"Hey {name},\n\n"
        "With immense joy and love, we — *Mukesh & Akhila* — would like to personally invite you "
        "to our wedding celebration! 💍✨\n\n"
        "It would truly mean the world to us to have you by our side on our special day. 🥰\n\n"
        "Check out our wedding page for more details:\n"
        f"🌐 https://mukesh-weds-akhila.netlify.app?guest={urllib.parse.quote(name)}\n\n"
        "📅 *Date:* 26-06-2026\n"
        "📍 *Venue:* Sri Krishna Mahal, Neikarapatti\n"
        "🗺️ *Location:* https://maps.app.goo.gl/AeTL48Sd41S2KEtP9\n\n"
        "We can't wait to celebrate this beautiful journey with you! 💐\n\n"
        "With love,\n"
        "Mukesh & Akhila ❤️"
    )

    # Open chat (no pre-filled text — caption will go with the image)
    whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}"

    print(f"[{index + 1}/{len(df)}] Opening chat link for {name}...")
    driver.get(whatsapp_url)

    try:
        # Wait until chat interface fully loads
        WebDriverWait(driver, 35).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]//p'))
        )
        time.sleep(3)

        # STEP 1: Upload the image via "Photos & videos"
        # Click the attachment (plus-rounded) button
        attach_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,
                '//span[@data-icon="plus-rounded"] | //span[@data-icon="plus"] | //span[@data-icon="clip"] | //span[@data-icon="attach-menu-plus"]'))
        )
        driver.execute_script("arguments[0].click();", attach_btn)
        time.sleep(3)

        # Intercept ALL file input clicks to capture the correct one
        driver.execute_script("""
            window._capturedFileInput = null;
            document.querySelectorAll('input[type="file"]').forEach(function(input) {
                input.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    window._capturedFileInput = input;
                }, { once: true, capture: true });
            });
        """)

        # Click "Photos & videos" to set WhatsApp's internal photo mode
        photos_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                '//button[@aria-label="Photos & videos"] | //button[contains(@aria-label,"Photos")]'))
        )
        driver.execute_script("arguments[0].click();", photos_btn)
        time.sleep(2)

        # Get the captured file input
        file_input = driver.execute_script("return window._capturedFileInput;")
        if not file_input:
            file_input = driver.execute_script("""
                var inputs = document.querySelectorAll('input[type="file"]');
                for (var i = 0; i < inputs.length; i++) {
                    var accept = inputs[i].accept || '';
                    if (accept.indexOf('image') !== -1 && accept.indexOf('video') !== -1) {
                        return inputs[i];
                    }
                }
                return inputs.length > 1 ? inputs[1] : inputs[0];
            """)

        file_input.send_keys(image_path)
        time.sleep(6)

        # STEP 2: Type the caption text in the image preview caption box
        caption_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                'div[data-testid="media-caption-input-container"]'))
        )
        driver.execute_script("arguments[0].focus();", caption_box)
        driver.execute_script("arguments[0].click();", caption_box)
        time.sleep(1)

        # Paste message via clipboard (preserves emojis and special characters)
        pyperclip.copy(message)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(3)

        # STEP 3: Click send — sends image with caption as one message
        send_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH,
                '//span[@data-icon="wds-ic-send-filled"] | //div[@aria-label="Send 1 selected"] | //span[@data-icon="send"]'))
        )
        driver.execute_script("arguments[0].click();", send_btn)
        time.sleep(3)
        print(f"✅ Invitation with image + caption sent to {name}.")

    except Exception as e:
        print(f"❌ Failed to send to {name}. Error: {str(e)}")

    # Safe tracking anti-spam timeout gap
    print("⏳ Sleeping 15 seconds to ensure system delivery safety...")
    time.sleep(15)

driver.quit()
print("\n🎉 All wedding invitations have been completely processed! Congratulations Akhila & Mukesh!")
