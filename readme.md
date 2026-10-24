# How to use the automation

## 1. Import the contacts from the Google Contacts

* Import the contacts as `Google CSV`
* Save the file in the root foder with the name `contacts.csv`
* It will contain the columns with the label `First Name,Middle Name,Last Name,Phonetic First Name,Phonetic Middle Name,Phonetic Last Name,Name Prefix,Name Suffix,Nickname,File As,Organization Name,Organization Title,Organization Department,Birthday,Notes,Photo,Labels,Phone 1 - Label,Phone 1 - Value,Phone 2 - Label,Phone 2 - Value
`


## 2. Clean the Data

* As the `contacts.csv` has lot of unwanted data, we should clean the data.
* Run the following command in the root path (Command Prompt)
```bash
python clean_data.py
```
* This will create a file `wedding_guests.csv` in the root folder


## 3. Get the Guests numbers
* Run the following command in the root path (Command Prompt)
```bash
python getNumber.py
```
* This will create a file `phone_numbers.txt` with the list of phone numbers


## 4. Validate the whatsapp numbers
* We need to validate that the numbers with the whatsapp
* Create a file named `numbers.txt` under the folder `validate_wp`
* Copy and paste the values from `phone_numbers.txt` to `numbers.txt`
* Run the following commands in the folder path: `validate_wp`
```bash
npm install
```
```bash
node bulk_check.js
```
* This will create the file `valid_numbers.txt` - The list of numbers in whatsapp

## 5. Manually delete the data
* Delete the contacts that are non-whatsapp number in the `wedding_guests.csv` with the help of the log from the previous step

## 6. Automate the whatsapp

* Edit the file `whatsapp_auto.py` :
  * If you need to include the image, save the image with the name `wedding_invite.jpg` in the root folder, If not delete the blocks for the image.
  * Change the message contain `message` 
* Now, run the command in the command prompt in the root folder location:
  ```bash
  python whatsapp_auto.py
  ```
