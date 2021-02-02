from app import db

class Champion(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    build_item = db.Column(db.String(2048))
    support_socket = db.Column(db.String(2048))
    counter = db.Column(db.String(2048))
    be_countered = db.Column(db.String(2048))
    skill_up = db.Column(db.String(2048))
    how_to_play = db.Column(db.String(2048))
    combo = db.Column(db.String(2048))
    combine_with = db.Column(db.String(2048))
    how_to_use_skill = db.Column(db.String(2048))
    introduce = db.Column(db.String(2048))
    
    def __repr__(self):
        return '<Champion {}>'.format(self.id)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer)
    message_question = db.Column(db.String(2048))
    message_answer = db.Column(db.String(2048))
    intent = db.Column(db.String(2048))
    action = db.Column(db.String(2048))
    entities = db.Column(db.String(2048))

    def __repr__(self):
        return '<Conversation {}> - message_question: {}'.format(self.conversation_id, self.message_question)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))