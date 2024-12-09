Introduction
============

django-fs-livesettings is the Django-related reusable app provides the ability to store settings in a database and configure settings via an admin interface.


Installation
============

Install ``django-fs-livesettings`` using ``pip``::

    $ pip install django-fs-livesettings

Add the ``'livesettings'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file::

    INSTALLED_APPS = (
        ...
        'livesettings',
        ...
    )

Add ``LIVESETTINGS_CONF`` to a ``settings.py`` file::

    LIVESETTINGS_CONF = (
        ('MY_SETTING_1', 'email', u'Description of this setting.'),
        ('MY_SETTING_2', 'char', u'Description of this setting.'),
    )

where, first parameter is a setting's name, second — it's type and third — description.

List of types::

    boolean
    char
    date
    datetime
    decimal
    email
    file
    image
    integer
    time
    url


Usage
=====

Just import livesttings and call that setting you want::

    from livesettings.conf import livesettings
    print(livesettings.MY_SETTING_1)


Credits
=======

`Fogstream <http://fogstream.ru>`_
