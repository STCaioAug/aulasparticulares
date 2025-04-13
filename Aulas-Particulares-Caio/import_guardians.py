import os
from datetime import datetime
import psycopg2

# Database connection using environment variables
db_url = os.environ.get('DATABASE_URL')

# List of guardians (name, phone, WhatsApp link)
guardians = [
    ("Daniella Risola", "+55 19 98224-4747", "https://wa.me/5519982244747"),
    ("Marcela", "+55 19 98911-3534", "https://wa.me/5519989113534"),
    ("Maysa", "+55 19 99891-6701", "https://wa.me/5519998916701"),
    ("Karin", "+55 11 97626-9474", "https://wa.me/5511976269474"),
    ("Giovanela", "+55 19 98186-7873", "https://wa.me/5519981867873"),
    ("Mariana", "+55 19 99130-8899", "https://wa.me/5519991308899"),
    ("Silvia", "+55 19 99602-8813", "https://wa.me/5519996028813"),
    ("Gisele", "+55 19 99928-4241", "https://wa.me/5519999284241"),
    ("Márcia", "+55 19 99603-7665", "https://wa.me/5519996037665"),
    ("Jacqueline Polisel", "+55 19 97402-9787", "https://wa.me/5519974029787"),
    ("Leandro", "+55 11 97679-6336", "https://wa.me/5511976796336")
]

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    # Insert guardians into the guardian table
    for name, phone, whatsapp in guardians:
        # Check if guardian already exists
        cursor.execute("SELECT id FROM guardian WHERE name = %s", (name,))
        result = cursor.fetchone()
        
        if result:
            # Update existing guardian
            guardian_id = result[0]
            cursor.execute(
                "UPDATE guardian SET phone = %s, whatsapp = %s, updated_at = %s WHERE id = %s",
                (phone, whatsapp, datetime.utcnow(), guardian_id)
            )
            print(f"Updated guardian: {name}")
        else:
            # Insert new guardian
            cursor.execute(
                "INSERT INTO guardian (name, phone, whatsapp, created_at, updated_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (name, phone, whatsapp, datetime.utcnow(), datetime.utcnow())
            )
            guardian_id = cursor.fetchone()[0]
            print(f"Added new guardian: {name} with ID: {guardian_id}")
    
    # Commit changes
    conn.commit()
    print("Guardian data import completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()