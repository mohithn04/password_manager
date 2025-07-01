import sqlite3
import hashlib
from derive_key import encrypt_password, decrypt_password

def get_user_db_name(master_password):
  """Generate a unique database name based on the master password"""
  # Create a hash of the master password to use as database identifier
  password_hash = hashlib.sha256(master_password.encode()).hexdigest()[:16]
  return f'vault_{password_hash}.db'

def create_database(master_password):
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Create table
  c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL
              )
            ''')

  # Save (commit) the changes
  conn.commit()

  # Close the connection
  conn.close()


def save_password(website, username, password, key, master_password):
  # Encrypt the password using the derived key
  encrypted_password = encrypt_password(key, password)
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Insert a row of data
  c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
    (website, username, encrypted_password))

  # Save (commit) the changes
  conn.commit()

  # Close the connection
  conn.close()


def get_passwords(key, master_password):
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Query the database with ID
  c.execute("SELECT id, website, username, password FROM passwords")

  # Decrypt the passwords
  rows = c.fetchall()
  passwords = []
  if rows:
    for row in rows:
      entry_id, website, username, encrypted_pw = row # unpack the row
      decrypted_pw = decrypt_password(key, encrypted_pw)
      passwords.append({
        'id': entry_id,
        'website': website,
        'username': username,
        'password': decrypted_pw
      })

  # Close the connection
  conn.close()
  return passwords


def update_password(entry_id, website, username, password, key, master_password):
  """Update an existing password entry"""
  # Encrypt the password using the derived key
  encrypted_password = encrypt_password(key, password)
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Update the entry
  c.execute("UPDATE passwords SET website=?, username=?, password=? WHERE id=?",
    (website, username, encrypted_password, entry_id))

  # Save (commit) the changes
  conn.commit()

  # Close the connection
  conn.close()


def delete_password(entry_id, master_password):
  """Delete a password entry"""
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Delete the entry
  c.execute("DELETE FROM passwords WHERE id=?", (entry_id,))

  # Save (commit) the changes
  conn.commit()

  # Close the connection
  conn.close()


def get_password_by_id(entry_id, key, master_password):
  """Get a specific password entry by ID"""
  db_name = get_user_db_name(master_password)
  conn = sqlite3.connect(db_name)
  c = conn.cursor()

  # Query the database for specific ID
  c.execute("SELECT id, website, username, password FROM passwords WHERE id=?", (entry_id,))
  row = c.fetchone()

  if row:
    entry_id, website, username, encrypted_pw = row
    decrypted_pw = decrypt_password(key, encrypted_pw)
    result = {
      'id': entry_id,
      'website': website,
      'username': username,
      'password': decrypted_pw
    }
  else:
    result = None

  # Close the connection
  conn.close()
  return result
