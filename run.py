from backend import app, db
from backend.models import User
from backend.celery1 import make_celery

celery = make_celery(app)
celery.set_default()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin_username = "admin"
        admin_password = "admin123" 
        admin_email= "admin@gmail.com"
        # Check if the admin user already exists
        admin_user = User.query.filter_by(username=admin_username).first()
        if not(admin_user):
        # Create the admin user and add it to the database
            admin_user = User(username=admin_username, password=admin_password, email=admin_email, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)

