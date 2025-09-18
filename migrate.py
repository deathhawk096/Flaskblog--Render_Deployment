from app import create_app, db
from app.models import User, Post
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


app=create_app()
app.app_context().push()


# Open a plain SQLAlchemy engine/session against the old sqlite DB
sqlite_engine = create_engine("sqlite:///instance/site.db")
sqlite_Session = sessionmaker(bind=sqlite_engine)
sqlite_session = sqlite_Session()


def row_to_dict(row, keys):
    """Convert a SQLAlchemy result row to a plain dict using provided keys."""
    return {k: row[k] for k in keys}


# --- Migrate users ---
user_result = sqlite_session.execute(text('SELECT id, username, email, password, image_file FROM "user"'))
user_rows = user_result.fetchall()
if user_rows:
    keys = user_result.keys()
else:
    keys = ["id", "username", "email", "password", "image_file"]

for r in user_rows:
    d = row_to_dict(r, keys)
    # Use db.session.get to avoid Query.get() deprecation and unexpected autoflush issues
    existing = db.session.get(User, d['id'])
    if existing is None:
        # Ensure we copy the password column (it's non-nullable in Postgres)
        new_user = User(id=d['id'], username=d['username'], email=d['email'], password=d['password'], image_file=d.get('image_file'))
        db.session.add(new_user)


# --- Migrate posts ---
post_result = sqlite_session.execute(text('SELECT id, title, date_posted, content, user_id FROM post'))
post_rows = post_result.fetchall()
if post_rows:
    pkeys = post_result.keys()
else:
    pkeys = ["id", "title", "date_posted", "content", "user_id"]

for r in post_rows:
    d = row_to_dict(r, pkeys)
    existing_post = db.session.get(Post, d['id'])
    if existing_post is None:
        new_post = Post(id=d['id'], title=d['title'], date_posted=d['date_posted'], content=d['content'], user_id=d['user_id'])
        db.session.add(new_post)


# Commit to the target (Postgres) DB
db.session.commit()

print("successfully done")