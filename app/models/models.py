import uuid
import enum
from datetime import datetime
from app import db


def gen_uuid():
    return str(uuid.uuid4())


class Status(enum.Enum):
    running = 1
    paused = 2
    completed = 3
    stopped = 4


class TimerData(db.Model):
    name = db.Column(db.String(128))
    time = db.Column(db.Integer)
    isGlobal = db.Column(db.Boolean, default=True)
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('user_data.id'), default='admin', nullable=True)


class Record(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    timer_id = db.Column(db.String(36), db.ForeignKey('timer_data.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum(Status))
    user_id = db.Column(db.String(36), db.ForeignKey('user_data.id'))

    timers = db.relationship('TimerData', backref='record', lazy=True)

    def json_format(self):
        return {
            'id': self.id,
            'timer_id': self.timer_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'completed': self.completed,
            'status': self.status.name if self.status else None,  # Convert enum to string
            'user_id': self.user_id
        }


class UserData(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(128), nullable=False)
    link = db.Column(db.String(128), nullable=True)

    timers = db.relationship('TimerData', backref='user', lazy=True)
    records = db.relationship('Record', backref='user', lazy=True)