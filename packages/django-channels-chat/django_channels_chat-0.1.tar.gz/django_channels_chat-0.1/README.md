=====
Django Channel Chat
=====

Django Channel Chat is a basic example of a Chat made with Django Channels

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django-channels-chat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-channels-chat',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('chat/', include('chat.urls')),

3. Run `python manage.py migrate` to create the django-channels-chat models.

4. Start the development server and visit http://127.0.0.1:8000/chat/
   to start a chat.

5. Visit http://127.0.0.1:8000/chat/ to participate in the chat.