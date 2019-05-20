from app import db

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50), unique=True)
    email    = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs    = db.relationship("Blog", backref="owner")
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Blog(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(50))
    body     = db.Column(db.String(500))
    owner_id    = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
    
    def __repr__(self):
        return '<Blogs %r>' % self.title