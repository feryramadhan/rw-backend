from app.helper.helper import get_pg_connection

def test_pg_connection():
    try:
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        print("Connection to PostgreSQL successful!")
        return True
    except Exception as e:
        print(f"Connection to PostgreSQL failed: {e}")
        return False

if __name__ == "__main__":
    test_pg_connection()

# Run this command
# python -m  app.db.test_connection