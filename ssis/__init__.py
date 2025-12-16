from flask import Flask, render_template
from os import getenv

def create_app(test_db=None) -> object:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    
    if test_db:
        # Update database connection in models
        import ssis.models
        ssis.models.db = test_db
        ssis.models.cursor = test_db.cursor()
    else:
        import ssis.models
        ssis.models.init_connection()

    # Initialize Redis
    from flask_redis import FlaskRedis
    import os
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://ssis_redis:6379/0')
    redis_client = FlaskRedis(app)
    app.extensions['redis'] = redis_client

    # import blueprints
    from .views.admin import admin
    from .views.students import student
    from .views.courses import course
    from .views.colleges import college

    # register blueprints
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(student, url_prefix='/students')
    app.register_blueprint(course, url_prefix='/courses')
    app.register_blueprint(college, url_prefix='/colleges')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
