# from sqlalchemy.event import listen
# from backend import app, db
# from backend.models import User
# print("hello")
# # @app.route("/")
# # def land():
# #     return "hello"

# # @app.route("/about")
# # def about():
# #     return render_template('about.html')


# # Callback function to create admin user after tables are created
# def create_admin_user(*args, **kwargs):
#     admin_username = "admin"
#     admin_password = "admin123"  # In a real application, you should hash the password

#     # Check if the admin user already exists
#     admin_user = User.query.filter_by(username=admin_username).first()
#     if admin_user:
#         return

#     # Create the admin user and add it to the database
#     admin_user = User(username=admin_username, password=admin_password, is_admin=True)
#     db.session.add(admin_user)
#     db.session.commit()

# # Connect the callback function to the 'after_create_all' event
# db.event.listen(db.Model, 'after_create_all', create_admin_user)
