=======
eit-sms
=======

eit-sms is a Django app that aims at scaffolding the common functionality of
sending SMS from a parent Django application. It allows you to define configs
and flow by which you would like to send SMSs, whether synchronous or asynchronous.

Quick start
-----------

1. Add "eit_sms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "eit_sms",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("sms/", include("eit_sms.urls")),

3. Run ``python manage.py migrate`` to create the models.

