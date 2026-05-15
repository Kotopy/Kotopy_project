import sqlite3
import os

path_mapping = {
    "books/الصحه_النفسيه.jpg": "books/al_sihha_al_nafsiyya.jpg",
    "books/المخ_ذكر_أم_أنثى.jpg": "books/al_mukh.jpg",
    "books/سيكولوجيا_الانسان_المقهور.jpg": "books/psychology_al_insan.jpg",
    "books/فن_الكلام.jpg": "books/fan_al_kalam.jpg",
    "books/فهم_الامراض_النفسية.jpg": "books/fahm_al_amrad.jpg",
    "books/محاط_مرضي_نفسيين.jpg": "books/muhat_bi_al_marda.jpg",
    "books/مستعمل.jpg": "books/musta3mal.jpg",
    "books/مفتقد_الحياة.jpg": "books/muftaqid_al_hayat.jpg"
}

def update_database(db_path):
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        updated_count = 0
        for old_path, new_path in path_mapping.items():
 
            cursor.execute("UPDATE books_book SET image = ? WHERE image = ?", (new_path, old_path))
            if cursor.rowcount > 0:
                print(f"Updated: {old_path} -> {new_path}")
                updated_count += cursor.rowcount
        
        conn.commit()
        conn.close()
        print(f"Successfully updated {updated_count} records in {db_path}")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
  
    update_database("db.sqlite3")
