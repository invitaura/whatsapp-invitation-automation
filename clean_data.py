import pandas as pd

# 1. Load your raw Google CSV file (Change 'contacts.csv' to your actual file name)
raw_df = pd.read_csv("contacts.csv")

clean_data = []

# 2. Extract only First Name and Phone
for _, row in raw_df.iterrows():
    # Grab ONLY the First Name
    first_name = str(row["First Name"]).strip() if pd.notna(row["First Name"]) else ""
    
    # Grab the phone number
    phone = str(row["Phone 1 - Value"]) if pd.notna(row["Phone 1 - Value"]) else ""

    # Clean data only if both name and phone exist
    if first_name and phone:
        # Extract digits only to remove spaces and formatting
        clean_phone = "".join(filter(str.isdigit, phone))

        # Format with Indian Country Code (+91)
        if len(clean_phone) == 10:
            clean_phone = "+91" + clean_phone
        elif len(clean_phone) == 12 and clean_phone.startswith("91"):
            clean_phone = "+" + clean_phone
        elif not clean_phone.startswith("+"):
            # Fallback wrapper just in case
            clean_phone = "+" + clean_phone

        # Set a default group so your invitation script executes perfectly
        group = "Other"

        clean_data.append({
            "Phone": clean_phone,
            "Name": first_name,
            "Group": group
        })

# 3. Create the final Excel sheet for your blast script
output_df = pd.DataFrame(clean_data)
# output_df.to_excel("wedding_guests.xlsx", index=False)
output_df.to_csv("wedding_guests.csv", index=False)

print("📊 Cleaned Sheet Preview:")
print(output_df.head(7))
print(f"\n🎉 Successfully processed {len(output_df)} contacts into 'wedding_guests.xlsx'!")
