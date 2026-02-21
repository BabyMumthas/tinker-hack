from app.models.database import get_connection

conn = get_connection()
c = conn.cursor()
c.execute("SELECT id, missing_full_name, image_path, length(embedding) as emb_len FROM cases")
rows = c.fetchall()
conn.close()

if not rows:
    print("NO CASES in database.")
else:
    for r in rows:
        print(f"  id={r['id']} name={r['missing_full_name']} img={r['image_path']} emb_len={r['emb_len']}")
