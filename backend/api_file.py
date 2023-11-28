from flask import jsonify, make_response
from functools import wraps
from backend import api, jwt, cache
from backend.models import *
from flask_restful import Resource,reqparse,marshal, fields, marshal_with, abort
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime

# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy

# User serialization fields
after_login_fields = {
    'id': fields.Integer,
    'access_token': fields.String,
}
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'is_admin': fields.Boolean
}
theatre_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'place': fields.String,
    'capacity': fields.Integer
}
show_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'rating': fields.Float,
    'tags': fields.String,
    'ticket_price': fields.Float,
    'start_time_hours': fields.Integer,
    'start_time_minutes': fields.Integer,
    'end_time_hours': fields.Integer,
    'end_time_minutes': fields.Integer,
    'theatre_id': fields.Integer,  # Include the theatre ID in the show_fields
}

user_bookings={
    'booking_id': fields.Integer,
    'show_name': fields.String,
    'theatre_name': fields.String,
    'number_of_tickets': fields.Integer,
    'booking_time': fields.DateTime,
    # Add other attributes from the Booking table if needed
}

register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help="Username cannot be blank.")
register_parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")
register_parser.add_argument('email', type=str, required=True, help="Email cannot be blank.")


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')


theatre_post_parser = reqparse.RequestParser()
theatre_post_parser.add_argument('name', type=str, required=True, help='Name is required.')
theatre_post_parser.add_argument('place', type=str, required=True, help='Place is required.')
theatre_post_parser.add_argument('capacity', type=int, required=True, help='Capacity is required.')

theatre_update_parser = reqparse.RequestParser()
theatre_update_parser.add_argument('name', type=str)
theatre_update_parser.add_argument('place', type=str)
theatre_update_parser.add_argument('capacity', type=int)


shows_post_parser = reqparse.RequestParser()
shows_post_parser.add_argument('name', type=str, required=True, help='Name is required.')
shows_post_parser.add_argument('rating', type=int, required=True, help='Rating is required.')
shows_post_parser.add_argument('tags', type=str, required=True, help='Tags are required.')
shows_post_parser.add_argument('ticket_price', type=int, required=True, help='Ticket price is required.')
shows_post_parser.add_argument('start_time_hours', type=int, required=True, help='Start time hours are required.')
shows_post_parser.add_argument('start_time_minutes', type=int, required=True, help='Start time minutes are required.')
shows_post_parser.add_argument('end_time_hours', type=int, required=True, help='End time hours are required.')
shows_post_parser.add_argument('end_time_minutes', type=int, required=True, help='End time minutes are required.')

# Request parser for updating a show
shows_put_parser = reqparse.RequestParser()
shows_put_parser.add_argument('name', type=str, required=True, help='Name is required.')
shows_put_parser.add_argument('rating', type=int, required=True, help='Rating is required.')
shows_put_parser.add_argument('tags', type=str, required=True, help='Tags are required.')
shows_put_parser.add_argument('ticket_price', type=int, required=True, help='Ticket price is required.')
shows_put_parser.add_argument('start_time_hours', type=int, required=True, help='Start time hours are required.')
shows_put_parser.add_argument('start_time_minutes', type=int, required=True, help='Start time minutes are required.')
shows_put_parser.add_argument('end_time_hours', type=int, required=True, help='End time hours are required.')
shows_put_parser.add_argument('end_time_minutes', type=int, required=True, help='End time minutes are required.')


booking_parser = reqparse.RequestParser()
booking_parser.add_argument('number_of_tickets', type=int, required=True, help='Number of tickets is required.')

# Custom decorator to check if the user is an admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_user = get_jwt_identity()
            print("inside admin required function")
            if not current_user['is_admin']:
                # return jsonify()
                response = make_response(jsonify(message='You are not an admin'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response 
            return fn(*args, **kwargs)
        except Exception as e:
            print(e)
            response = make_response(jsonify(message='Invalid token or token expired'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response    
    return wrapper

def user_auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_user = get_jwt_identity()
            user_id = kwargs.get('user_id')  # Assumes the user ID is passed as a keyword argument in the route

            if not user_id or current_user['id'] != user_id:
                response = make_response(jsonify(message='Unauthorized to access this resource'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response 

            return fn(*args, **kwargs)
        except Exception as e:
            print(e)
            response = make_response(jsonify(message='Invalid token or token expired'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response    
    return wrapper



#-------- DEFINING RESOURCES-------
#-------- DEFINING RESOURCES-------
class UserRegistration(Resource):
    def post(self):
        args = register_parser.parse_args()

        # Check if the username already exists in the database
        if User.query.filter_by(username=args['username']).first():
            return {"message": "Username already exists."}, 409

        # Create a new user object and add it to the database
        new_user = User(username=args['username'], password=args['password'], is_admin=False, email=args['email'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully."}, 201

# User login resource
class UserLoginResource(Resource):
    # @marshal_with(after_login_fields)
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:    
            access_token = create_access_token(identity={'id': user.id, 'name': user.username, 'is_admin': user.is_admin})
            us_fl= {'id': user.id, 'access_token': access_token}
            user.last_login = datetime.now()
            db.session.commit()
            return marshal(us_fl, after_login_fields)
        else:
            return {"message": "invalid credentials"}, 401

# # Admin user resource
# class AdminUserResource(Resource):

#     @jwt_required()
#     def get(self, user_id):
#         current_user = get_jwt_identity()
#         user = User.query.get(user_id)
#         if not (user):
#                 return 'admin not found', 404
#         elif current_user['id'] != user_id:
#             return 'Unauthorized access', 403
#         elif not(current_user['is_admin']):
#             return 'You are not an admin', 403
#         else:
#             return marshal(user, user_fields)
class TheatreListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        # print("inside get api ")
        theatres = Theatre.query.all()
        if theatres:
            return marshal(theatres, theatre_fields)
        else:
            return {"message": "No theatres found"}
    
    @jwt_required()
    @admin_required
    def post(self):
        args = theatre_post_parser.parse_args()
        name = args['name']
        place = args['place']
        capacity = args['capacity']
        # Create a new theatre instance
        new_theatre = Theatre(name=name, place=place, capacity=capacity)
        db.session.add(new_theatre)
        db.session.commit()
        cache.delete('theatres')
        return {'message': 'Theatre created successfully'}, 201
# Add the resource to the API with the specified URL

class TheatreManipulateResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, id):
        args = theatre_update_parser.parse_args()
        # Get the theatre by ID from the database
        theatre = Theatre.query.get(id)
        if not theatre:
            return {'message': 'Theatre not found'}, 404

        # Update the theatre attributes if provided
        theatre.name = args['name']
        theatre.place = args['place']
        theatre.capacity = args['capacity']
        db.session.commit()
        cache.delete('theatres')
        return {'message': 'Theatre updated successfully'}, 200

    @jwt_required()
    @admin_required
    def delete(self, id):
        # Get the theatre by ID from the database
        theatre = Theatre.query.get(id)
        if not theatre:
            return {'message': 'Theatre not found'}

        db.session.delete(theatre)
        db.session.commit()
        cache.delete('theatres')
        return {'message': 'Theatre deleted successfully'}, 200


class ShowListResource(Resource):
    @jwt_required()
    @admin_required
    @marshal_with(show_fields)
    def get(self, theatre_id):
        # print("inside get shows")
        shows = Show.query.filter_by(theatre_id=theatre_id).all()
        return shows

    @jwt_required()
    @admin_required
    def post(self, theatre_id):
        args = shows_post_parser.parse_args()

        # Create a new show for the given theatre_id
        new_show = Show(
            name=args['name'],
            rating=args['rating'],
            tags=args['tags'],
            ticket_price=args['ticket_price'],
            start_time_hours=args['start_time_hours'],
            start_time_minutes=args['start_time_minutes'],
            end_time_hours=args['end_time_hours'],
            end_time_minutes=args['end_time_minutes'],
            theatre_id=theatre_id
        )

        db.session.add(new_show)
        db.session.commit()

        return {'message': 'Show created successfully'}, 201

class ShowManipulateResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, theatre_id, show_id):
        args = shows_put_parser.parse_args()
        # Here, you can update the show with the given show_id using your database implementation
        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404
        for key, value in args.items():
            if value is not None:
                setattr(show, key, value)
        db.session.commit()
        return {'message': 'Show updated successfully'}
    
    @jwt_required()
    @admin_required
    def delete(self, theatre_id, show_id):
        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404 
        db.session.delete(show)
        db.session.commit()
        return {'message': 'Show deleted successfully'}, 200


class UserTheatreListResource(Resource):
    @jwt_required()
    @user_auth_required
    def get(self, user_id):
        theatres = cache.get('theatres')
        if not(theatres):
            # print("not cached yet")
            theatres = Theatre.query.all()
            # timeout is in seconds, 100 for project, 30 for viva
            cache.set('theatres', theatres, timeout=200)
        if theatres:
            return marshal(theatres, theatre_fields)
        else:
            return {"message": "No theatres found"}   

class UserTheatreResource(Resource):
    @jwt_required() 
    @user_auth_required
    def get(self, user_id, theatre_id):
        # theatre = cache.get(f'theatre_{theatre_id}')
        # print(f"cache: {theatre}")  
        # if not(theatre):
        #     print("not cached yet")
        theatre = Theatre.query.get(theatre_id)
        if not theatre:
            return {'message': 'Theatre not found'}

            # timeout is in seconds, 100 for project, 30 for viva
            # cache.set('theatres', theatres, timeout=200)
        theatre_data = {
            "id": theatre.id,
            "name": theatre.name,
            "place": theatre.place,
            "capacity": theatre.capacity,
            
        }
        # return jsonify(theatre_data)
        response = make_response(jsonify(theatre_data), 200)
        response.headers['Content-Type'] = 'application/json'
        return response# return marshal(theatre, theatre_fields)
        # else:
        #     return {"message": "No theatres found"}   
 
        #  return marshal(theatres, theatre_fields)
        # else:
        #     return {"message": "No theatres found"}
    
class UserShowListResource(Resource):
    @jwt_required()
    @user_auth_required
    @marshal_with(show_fields)
    def get(self, user_id):
        # print("inside get shows")
        shows = Show.query.all()
        return shows

class UserBookTicketResource(Resource):
    @jwt_required()
    @user_auth_required
    def post(self, user_id, show_id):
        data = booking_parser.parse_args()
        number_of_tickets = int(data['number_of_tickets'])

        # Check if the show exists
        show = Show.query.get(show_id)
        if not show:
            return {'message': 'Show not found'}, 404
        theatre = show.theatre
        cap= theatre.capacity
        # print(cap)
        if cap==0:
              return {'message': 'theatre is full, there are no seats left'}, 403
        elif number_of_tickets > theatre.capacity:
            return {'message': f'theatre does not have that much seats left, you can book maximum of {cap} seats'}, 422
        else:
            remaining_capacity = cap - number_of_tickets
            theatre.capacity = remaining_capacity
            db.session.commit()
            booking = Booking(user_id=user_id, show_id=show_id, number_of_tickets=number_of_tickets)
            db.session.add(booking)
            db.session.commit()
            return {'message': 'Booking created successfully'}


class UserBookingListResource(Resource):
    @jwt_required()
    @user_auth_required
    # @marshal_with(show_fields)
    def get(self, user_id):
        try:
            bookings = Booking.query.filter_by(user_id=user_id).all()

            # Create a list to store the result with show_id and show_name
            result = []
            for booking in bookings:
                # Retrieve the corresponding Show record based on show_id
                # print(0)
                show = Show.query.get(booking.show_id)
                theatre_name= show.theatre.name
                # Create a dictionary with show_id and show_name
                show_info = {
                    'booking_id': booking.id,
                    'show_name': show.name,
                    'theatre_name': theatre_name,
                    'number_of_tickets': booking.number_of_tickets,
                    'booking_time': booking.booking_time,
                    # Add other attributes from the Booking table if needed
                }

                # Append the dictionary to the result list
                result.append(show_info)

            return marshal(result, user_bookings)
        except Exception as e:
            # print(e)
            return {'message': 'An error occurred while fetching bookings'}, 500

#-------- ADDING RESOURCES-------
#-------- ADDING RESOURCES-------
api.add_resource(UserRegistration, '/api/register')
api.add_resource(UserLoginResource, '/api/login')
api.add_resource(TheatreListResource, '/api/admin/theatres')
# api.add_resource(AdminUserResource, '/api/admin/<int:user_id>')
api.add_resource(TheatreManipulateResource, '/api/theatre/<int:id>')

api.add_resource(ShowListResource, '/api/<int:theatre_id>/shows')
api.add_resource(ShowManipulateResource, '/api/<int:theatre_id>/show/<int:show_id>')        

api.add_resource(UserTheatreListResource, '/api/user/<int:user_id>/theatres')
api.add_resource(UserShowListResource, '/api/user/<int:user_id>/shows')
api.add_resource(UserBookTicketResource, '/api/user/<int:user_id>/<int:show_id>/ticketBookings')
api.add_resource(UserBookingListResource, '/api/user/<int:user_id>/bookings')
api.add_resource(UserTheatreResource, '/api/user/<int:user_id>/theatre/<int:theatre_id>')
