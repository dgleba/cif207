# orginally from flask-admin auth example.



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Title:  .
-----------------------2016-01-24[Jan-Sun]21-44PM

# ref - reflect database:



# http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html
# https://gist.github.com/nickretallack/7552307
# http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database
# http://docs.sqlalchemy.org/en/latest/core/reflection.html#reflecting-all-tables-at-once
# http://www.blog.pythonlibrary.org/2010/09/10/sqlalchemy-connecting-to-pre-existing-databases/



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Title:  .
-----------------------2016-01-24[Jan-Sun]21-43PM

"""
ref:
https://flask-admin.readthedocs.org/en/latest/introduction/#customizing-built-in-views

sqlalchemy reflected column names:
http://stackoverflow.com/questions/19215759/sqlalchemy-reflecting-tables-and-columns-with-spaces
http://stackoverflow.com/questions/7679893/how-to-override-a-column-name-in-sqlalchemy-using-reflection-and-descriptive-syn
http://docs.sqlalchemy.org/en/latest/core/metadata.html
"""    



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define models

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# existing table in dgnote130 mysql database....

#http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html


connection = db.engine.connect()
#db.metadata.reflect(bind=db.engine)

db.metadata.reflect(db.engine, only=['books', 'states'])

Base = automap_base(metadata=db.metadata)
Base.prepare()

Books = Base.classes.books


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Sqlalchemy Reflect
# https://gist.github.com/nickretallack/7552307
#http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database

#db = SQLAlchemy(app)
# connection = db.engine.connect()
# db.metadata.reflect(bind=db.engine)

#Models
# class Books(db.Model):
	# __table__ = db.metadata.tables['books']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#   http://stackoverflow.com/questions/25828721/foreign-key-relationship-in-flask-admin-when-using-sqlalchemy-automap

# def obj_books(obj):
    # return obj.title

# def obj_states(obj):
    # return obj.state


# mapped classes are now created with names by default
# matching that of the table name.

#Base.classes.books.__str__ = obj_books
#Base.classes.states.__str__ = obj_states


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# manually define books table  -- works, but I want to automap.

# class books(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(30))
    # description = db.Column(db.Text, nullable=False)
    # def __unicode__(self):
        # return self.title

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
		

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Title:  .
-----------------------2016-01-23[Jan-Sat]19-53PM

# Create dummy secrey key so we can use sessions
#SECRET_KEY = '123456790'
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dg417:dg@localhost/dgnote130'

# Flask-Security config
app.config['SECURITY_PASSWORD_SALT'] = "ATGUOHAELKiubahiughaerGOJAEGj"


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
