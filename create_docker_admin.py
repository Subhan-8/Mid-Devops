from werkzeug.security import generate_password_hash
import mysql.connector
import os

# Docker internal DB credentials
DB_HOST = os.getenv('DB_HOST', 'ssis_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASSWORD', '123SubhanS')
DB_NAME = os.getenv('DB_NAME', 'ssisdb')

def add_admin():
    print("\n--- Creating Admin User for Docker ---")
    username = input("Enter new Admin Username: ")
    password = input("Enter new Admin Password: ")
    
    # Use Werkzeug to generate hash (same method as app)
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
    
    try:
        print(f"Connecting to {DB_HOST}...")
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Check if user exists
        check_query = "SELECT * FROM admin WHERE username = %s"
        cursor.execute(check_query, (username,))
        if cursor.fetchone():
            print(f"WARNING: User '{username}' already exists! Updating password...")
            query = "UPDATE admin SET password = %s WHERE username = %s"
            cursor.execute(query, (hashed_pw, username))
        else:
            query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_pw))
            
        conn.commit()
        print(f"SUCCESS: Admin '{username}' has been successfully saved to Docker DB!")
        
    except mysql.connector.Error as e:
        print(f"DATABASE ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    add_admin()
