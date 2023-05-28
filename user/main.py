from fastapi import FastAPI, HTTPException

from .postgresdatabase import postgres_session
from .models import PostgresUser
from .mongodatabase import mongo_collection
from .schemas import User

app = FastAPI()


@app.post('/register')
def register_user(user: User):
    # Check if email already exists in PostgreSQL
    postgres_user = postgres_session.query(PostgresUser).filter_by(email=user.email).first()
    if postgres_user:
        raise HTTPException(status_code=400, detail='Email already exists.')

    # Save user details to PostgreSQL
    postgres_user = PostgresUser(first_name=user.first_name, password=user.password, email=user.email, phone=user.phone)
    postgres_session.add(postgres_user)
    postgres_session.commit()

    # Save profile picture to MongoDB
    profile_picture = {'user_id': postgres_user.id, 'profile_picture': user.profile_picture}
    mongo_collection.insert_one(profile_picture)

    return {'message': 'User registered successfully.'}

@app.get('/user/{user_id}')
def get_user(user_id: int):
    # Retrieve user details from PostgreSQL
    postgres_user = postgres_session.query(PostgresUser).filter_by(id=user_id).first()
    if not postgres_user:
        raise HTTPException(status_code=404, detail='User not found.')

    # Retrieve profile picture from MongoDB
    profile_picture = mongo_collection.find_one({'user_id': user_id})
    if not profile_picture:
        raise HTTPException(status_code=404, detail='Profile picture not found.')

    user_details = {
        'id': postgres_user.id,
        'first_name': postgres_user.first_name,
        'email': postgres_user.email,
        'phone': postgres_user.phone,
        'profile_picture': profile_picture['profile_picture']
    }
    return user_details