from derive_key import get_key_from_password, load_or_create_salt
from database import create_database, save_password, get_passwords

def main():
  salt = load_or_create_salt()
  master_pw = input("Enter your master password: ")
  key = get_key_from_password(master_pw, salt)

  # Create database for this user
  create_database(master_pw)

  while True:
    choice = input("1. Save Password\n2. View Passwords\n3. Exit\nChoose: ")
    if choice == '1':
      site = input("Website: ")
      user = input("Username: ")
      pw = input("Password: ")
      save_password(site, user, pw, key, master_pw)
      print("Password saved successfully!")
    elif choice == '2':
      get_passwords(key, master_pw)
    else:
      break

if __name__ == "__main__":
  main()
