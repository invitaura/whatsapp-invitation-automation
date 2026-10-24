import csv

with open('wedding_guests.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    phones = [row['Phone'].strip() for row in reader]

with open('phone_numbers.txt', 'w') as txtfile:
    txtfile.write('\n'.join(phones))

print(f"Extracted {len(phones)} phone numbers to phone_numbers.txt")
