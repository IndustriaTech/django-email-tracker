=============
Email Tracker
=============

EmailTracker allows you to keep track of all messages send from your django site.

Installation
------------

In order to install the email tracker::

	pip install https://github.com/IndustriaTech/django-email-tracker/archive/master.zip


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

4. Sync your database with :code:`python manage.py migrate` to create the email_tracker models.

5. Start the development server and visit http://127.0.0.1:8000/admin/email_tracker/
   to observe created mails and categories (you'll need the Admin app enabled).


Integration with other mail backends
------------------------------------

If you want to use some custom email backend than you can configre :code:`EMAIL_TRACKER_BACKEND` setting to point to your custom backend.
::

    EMAIL_BACKEND = 'email_tracker.backends.EmailTrackerBackend'
    EMAIL_TRACKER_BACKEND = 'my_project.backends.CustomEmailBackend'


Django-Anymail integration
--------------------------

If you are using :code:`django-anymail` there is no need need to configure :code:`EMAIL_BACKEND` to point to :code:`EmailTrackerBackend`
:code:`django-email-tracker` will automatically track mails sent trough :code:`django-anymail`.

If you want to disable this automatic integration you can set in settings::

    EMAIL_TRACKER_USE_ANYMAIL = False
