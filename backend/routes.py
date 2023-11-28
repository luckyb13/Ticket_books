from flask import render_template, send_file
from backend import app, db, mail
from backend.models import *
from flask_mail import Message
from celery import shared_task     
from dateutil.relativedelta import relativedelta
import csv

# -------SENDING MAILS --------

@shared_task
def send_email():
    users= User.query.all()
    for user in users:
        if user.id !=1 and not(user.bookings):
            user_mail= user.email
            msg = Message('Reminder to book your favorite movie shows', sender='admin@example.com', recipients=[user_mail])
            msg.body = f"It looks like you haven't booked anything yet. This is a gentle reminder to book and enjoy your favorite movie at your favorites place"
            mail.send(msg)
    return 'Test emails sent successfully!'

@shared_task
def send_reports_email():
    users= User.query.all()
    for user in users:
        info=[]
        username=user.username
        if user.id ==1:
            continue
        current_date = datetime.utcnow()

# Calculate the date for the previous month
        previous_month_date = current_date - relativedelta(months=1)

        month = previous_month_date.month
        year = previous_month_date.year
        # month = current_date.month
        # current_year = current_date.year

        # print(previous_month, previous_year)
        bookings = Booking.query.filter(
        Booking.user_id == user.id,
        db.func.extract('month', Booking.booking_time) == month,
        db.func.extract('year', Booking.booking_time) == year).all()
        count= len(bookings)
        total_tickets=0
        for booking in bookings:
            d={}
            show = booking.show
            theatre= show.theatre
            total_tickets += booking.number_of_tickets
            d={
                'name': show.name, 
                'rating': show.rating, 
                'theatre': theatre.name, 
                'tickets': booking.number_of_tickets,
            }
            info.append(d)
            # print(info)
            # print(show.name, show.rating, theatre.name, booking.number_of_tickets )
        t=render_template('report_template.html', info=info, total_tickets=total_tickets, count=count, username=username, month=month, year= year)        
        user_mail= user.email
        msg = Message('Html report of your previous month bookings', sender='admin@example.com', recipients=[user_mail], html=t)
        # msg.body = t
        mail.send(msg)
        
        # print(t)
    return 'HTML reports Generated successfully!'

# -----CSV EXPORT JOB-----
@shared_task
def export_csv(id):
    theatre= Theatre.query.get(id)
    shows= theatre.shows
    total_bookings=0
    total_rating=0
    for show in shows:
        total_bookings += len(show.bookings)
        total_rating += show.rating
    if not(shows):
        theatre_info={
        "id":theatre.id,
        "name": theatre.name,
        "No. of shows":0,
        "Available seats": theatre.capacity,
        "No. of bookings": total_bookings,
        "average show rating": "-", 
    }
    else:    
        avg_rating= total_rating/len(shows)
        theatre_info={
            "id":theatre.id,
            "name": theatre.name,
            "No. of shows":len(shows),
            "Available seats": theatre.capacity,
            "No. of bookings": total_bookings,
            "average show rating": avg_rating, 
        }
    print(theatre.id)        
    csv_file_path = f"theatre_info_{theatre.id}.csv"
    print(csv_file_path)
    
    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)    
        # Write the attribute names as the first column
        writer.writerow(["Attribute", "Value"])
        # Write the attribute-value pairs to the CSV file
        for attribute, value in theatre_info.items():
            writer.writerow([attribute, value])

    # print(f"CSV file '{csv_file_path}' generated successfully.")
    # msg = Message('Theatre Info Csv Report', sender='admin@example.com', recipients=['admin@example.com'])
    # msg.body = 'Please find the attached theatre information report.'
    # with app.open_resource(f"../{csv_file_path}") as fp:
    #     msg.attach("theatre_info.csv", "text/csv", fp.read())
    # mail.send(msg)
    
    return 'theatre info csv report exported and mailed successfully!'




# -----------------------ROUTES------------------
# @app.route("/")
# def home():

@app.route('/download_csv/<int:id>', methods=['GET'])
def download_csv(id):
    csv_file_path = f"../theatre_info_{id}.csv"
    return send_file(csv_file_path, as_attachment=True)

@app.route('/admin/export_csv/<int:id>')
def trigger_celery_task(id):
    result = export_csv.delay(id)
    while not result.ready():
        pass
    return {"message": "Theatre info file is generated. Click on download csv button to start downloading."}, 201
    