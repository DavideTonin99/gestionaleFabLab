# DEPLOY THE APP ON HEROKU

---

1. Install whitenoise, gunicorn, psycopg2, dj-database-url and python-decouple:
    
        pip install whitenoise
        pip install gunicorn
        pip install psycopg2
        pip install dj-database-url
        pip install python-decouple
        
1. Add requirements.txt file
        
        pip freeze > requirements.txt
        
2. Add runtime.txt file, for example:

        python-3.6.0
        
3. Add Procfile:

        web: gunicorn gestionaleFabLab.wsgi --log-file -
        
4. Modify wsgi.py (lines to add with - before):
    
        import os

        from django.core.wsgi import get_wsgi_application
        - from whitenoise.django import DjangoWhiteNoise
        
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestionaleFabLab.settings")
        
        application = get_wsgi_application()
        - application = DjangoWhiteNoise(application)
        
5. Modify settings.py:

        from decouple import config
        import dj_database_url
        
        # Database settings
        SECRET_KEY = config('SECRET_KEY')
        DEBUG = config('DEBUG', default=False, cast=bool)
        DATABASES = {
            'default':
                dj_database_url.config(
                    default=config('DATABASE_URL')
                )
            }
        
        # For static files loading
        STATIC_URL = '/static/'
        STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'gestionaleapp/static'),
        )
        
        Modify also on heroku the variables:
        - Go to settings of the applications, click reveal vars
          and config SECRET_KEY, DATABASE_URL, USER, PASSWORD. 
          You can see this varaibles in the database informations/settings.
       

On heroku you can set automatic deploy from a github project, 
so everytime you pull, heroku upload changes almost in real time.

*Davide Tonin, Forigo Ettore, Novelli Matteo, Conti Enrico*