from app import create_app,db
from app.models import User
from flask_cors import CORS, cross_origin

app = create_app()

