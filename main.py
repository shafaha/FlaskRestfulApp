from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:test.db:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Request parser, it parse the request
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type = str, help = "Name of the video")
video_put_args.add_argument("views", type = int, help = "Views of the video")
video_put_args.add_argument("likes", type = int, help = "Likes on the video")

# to return aanything from the Api it must be Json serializable

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True )
    views = db.Column(db.Integer, default = 0)
    likes = db.Column(db.Integer, default = 0)

    def __init__(self, name, views, likes):
        self.name = name
        self.views = views
        self.likes = likes

    def __repr__(self):
        return "The song " + self.song + " view " + str(self.views) + " likes " + str(self.likes)


# making thing serializable

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views':fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)
        return result
    @marshal_with(resource_fields)
    def put(self, video_id):
        # with the help of the request 
        args = video_put_args.parse_args()
        video = VideoModel( args['name'], args['views'], args['likes'])
        db.session.add(video)
        db.session.commit()

        #return video,201

    def delete(self, video_id):
        pass
        

api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug = True)
