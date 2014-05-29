=====
Email Tracker
=====

EmailTracker allows you to keep track of all messages send from your django site.


Quick start
-----------

1. Add "email_tracker" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'email_tracker',
    )

2. Add email_tracker.south_migrations to your SOUTH_MIGRATION_MODULES setting:
	
	SOUTH_MIGRATION_MODULES = {
	    'email_tracker': 'email_tracker.south_migrations',
	}

3. Run `python manage.py migrate` to create the email_tracker models.

4. Start the development server and visit http://127.0.0.1:8000/admin/email_tracker/
   to observe created mails and categories (you'll need the Admin app enabled).

