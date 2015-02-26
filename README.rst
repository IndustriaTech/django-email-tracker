=====
Email Tracker
=====

EmailTracker allows you to keep track of all messages send from your django site.

Installation
-----------

In order to install the email tracker::

	pip install git+git://github.com/MagicSolutions/django-email-tracker.git
	

Quick start
-----------

1. Add :code:`email_tracker` to your :code:`INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
        ...
        'email_tracker',
    )

2. Set your :code:`EMAIL_BACKEND` setting::

    EMAIL_BACKEND = 'email_tracker.backends.EmailTrackerBackend'

3. If you use South you need to add :code:`email_tracker.south_migrations` to your :code:`SOUTH_MIGRATION_MODULES` setting::
	
	SOUTH_MIGRATION_MODULES = {
	    'email_tracker': 'email_tracker.south_migrations',
	}

4. Sync your database with :code:`python manage.py syncdb` or of you use South :code:`python manage.py migrate` to create the email_tracker models.

5. Start the development server and visit http://127.0.0.1:8000/admin/email_tracker/
   to observe created mails and categories (you'll need the Admin app enabled).

