from runserver import db
import datetime


class UserRequests(db.Model):
    __tablename__ = 'user_requests'
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(80))
    tk_id = db.Column(db.String(80))
    datetime = db.Column(db.DateTime(), default=datetime.datetime.now)
    message = db.Column(db.String(1024))

    def save(self):
        db.session.add(self)
        db.session.commit()