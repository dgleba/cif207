# orginally from flask-admin auth example.

# http://v206b2:920/admin/#


import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers

from sqlalchemy.ext.automap import automap_base
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import column_property


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create Flask application

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define models

# existing table in dgnote130 mysql database....
#http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html

# reflect models from the database...


connection = db.engine.connect()

db.metadata.reflect(db.engine, only=['cilisting1', 'leader'])

Base = automap_base(metadata=db.metadata)
#  ?  Base = declarative_base()
Base.prepare()


Cilisting1 = Base.classes.cilisting1
#States = Base.classes.states

# class Books(db.Model):
    # __tablename__ = 'books'
    # def __str__(self):
        # return self.title

		
# ref:
# https://gist.github.com/nickretallack/7552307
# http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database
# http://docs.sqlalchemy.org/en/latest/core/reflection.html#reflecting-all-tables-at-once
# http://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				
		
roles_users = db.Table(
    'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

		
		
# Setup Flask-Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Flask views

# flask admin cuts off my url  --- this noworky.. #  http://stackoverflow.com/questions/26585050/flask-admin-pages-inaccessible-in-production
@app.route('/')
@app.route('/ciy207/')

def index():
    return render_template('index.html')


# Create admin

admin = flask_admin.Admin(
    app,
    'cif207',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add model views



admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))

#admin.add_view(MyModelView(Books, db.session))
admin.add_view(MyModelView(Cilisting1, db.session))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    #db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    #uncomment to build.... 
    #if not os.path.exists(database_path):
     #  build_sample_db()

    # Start app
    app.run(host='0.0.0.0', debug=True)
