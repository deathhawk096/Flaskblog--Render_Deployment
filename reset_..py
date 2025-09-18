from app import create_app, db
from sqlalchemy import text

app = create_app()
app.app_context().push()

# Reset sequence for user table
db.session.execute(
    text('SELECT setval(pg_get_serial_sequence(\'"user"\', \'id\'), COALESCE((SELECT MAX(id)+1 FROM "user"), 1), false)')
)

# Reset sequence for post table
db.session.execute(
    text('SELECT setval(pg_get_serial_sequence(\'post\', \'id\'), COALESCE((SELECT MAX(id)+1 FROM post), 1), false)')
)

db.session.commit()
print("✅ Sequences reset successfully!")