from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        user = User(name='Project Admin', email='admin@example.com', is_admin=True)
        user.set_password('Admin@12345')
        db.session.add(user); db.session.commit()
        print('Admin created: admin@example.com / Admin@12345')
    else:
        print('Admin already exists.')
