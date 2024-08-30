---
share: true
featured: true
title: A comprehensive guide to  multi-timezone support in Django
slug: a_comprehensive_guide_to__multi-timezone_support_in_django
tags:
  - python
  - django
  - timezone
description: >
 Discover how to seamlessly manage timezones in Django and empower your applications with user-centric solutions.
 This article is your essential guide to precise and efficient multi-timezone support.
publish_date: 2023-10-11
upload_path: posts
---

> **TL;DR**: To support multiple timezones in your Django project, you need a way to request your users' specific timezones and create a middleware that uses `django.timezone.activate(user_tz)` to enable a specific timezone for a user globally on your site. This ensures that every use of `django.timezone.now()` uses the activated timezone. If you prefer reading code directly, see [middleware.py](https://github.com/Tobi-De/leerming/blob/main/leerming/profiles/middleware.py) and [models.py](https://github.com/Tobi-De/leerming/blob/main/leerming/profiles/models.py).

Throughout this article, I'll guide you on setting up multi-timezone support in a Django project. This post is aimed at beginners (assuming basic Django knowledge) and intermediates. If what I'm writing seems blatantly obvious to you, you're likely not in one of these categories, so please bear with us.

### Introduction

Time is universally a challenging subject to deal with, especially in software engineering. Handling time zones correctly is hard. Luckily for us, when working with Django, a significant portion of the work has already been done.

For the longest time (literally until yesterday), I thought that the piece of code below was enough to have timezones fully managed and working in Django:

```python
# settings.py
TIME_ZONE = "UTC"  # Sometimes, I'd switch this to my primary audience's timezone.
USE_TZ = True
```

It turns out I was wrong, or at least I was missing the full picture. There's a bit more work left if you want to consider every user's timezone. Let's explore what's left to do.

> **Note** The official [Django documentation on timezones](https://docs.djangoproject.com/en/4.2/topics/i18n/timezones/) is very well written, so I highly suggest you read it. However, this article will provide you with the essentials, at least that's what I hope.

### The Basics

First, let's start with the basics. In Python, there are two types of datetime objects: naive and aware. We'll keep it simple. Naive datetime objects hold no timezone information, while aware datetimes hold timezone information.

When you have the `USE_TZ` setting set to `True` in your project settings (as shown in the snippet above), Django will ensure that all the DateTime objects you create are timezone-aware. This is, of course, assuming that you use Django's timezone module to create your dates.

```python
from django.utils import timezone

now = timezone.now()
```

This works if you're not concerned about user-specific timezones, and you're not doing anything fancy with datetime. But what if you are?

### The Challenge

Let me paint a picture: I'm building an app where I need to send daily notifications to users at specific times. My project's timezone is set to `UTC` – the recommended practice by most of the Django community. Here's the twist: I live in a UTC+1 timezone, and I realized my notifications were coming in an hour late. My cousin, who lives in Europe at a different timezone, also uses my app. Changing the default timezone wasn't an option. My cousin and I, along with potentially many other users, needed to navigate the app seamlessly without time feeling off. Scheduling and time management are at the core of my app, and I couldn't afford to mess that up.
So, I decided to dive deep into understanding how Django deals with time zones – something I'd never made a priority before.

After reading and re-reading the Django documentation, things started to click. First, let's grasp the fundamentals and then dive into setting up our timezone magic.

There are two important concepts that Django uses: the "default time zone" and the "current time zone."

- The **default time zone** is the timezone you set in your Django settings via `TIME_ZONE`.
- The **current time zone** is the timezone used for rendering. It's the one in which your users will browse your site.

The `current time zone` defaults to the `default time zone` unless you **activate** the user's specific timezone using `django.utils.timezone.activate`.

Does it start to make sense?
Django, by default, doesn't know a user's timezone. It's not typically available in request data, so it sticks with the default timezone. You need to ask your users for their time zone – a simple form does the trick – and then manually activate it. The easiest and probably the best way to do this is through a middleware.

### Setting Up Multi-Timezone Support

Now, let's dive into a simple example. We'll create a user `Profile` model to collect and store each user's timezone. For simplicity's sake, I'll leave out the non-essential parts of the code.

Here's a model for our users' profiles:

```python
import zoneinfo

TIMEZONES_CHOICES = [(tz, tz) for tz in zoneinfo.available_timezones()]

class Profile(TimeStampedModel):
    user = models.OneToOneField(
        "users.User", related_name="profile", on_delete=models.CASCADE
    )
    timezone = models.CharField(
        verbose_name=_("Fuseau horaire"),
        max_length=50,
        default="UTC",
        choices=TIMEZONES_CHOICES,
    )
```

With the model above, we have a simple `CharField` to hold the user's timezone and a choices field to render a select using a Django form. You can customize the list of available timezones obtained from the `zoneinfo module`. For a simpler user experience, you might choose to filter it by continent or display the city as the label.

> Tip: If you're displaying a long list of timezones, consider using a select element with a search feature(e.g, [tom-select](https://github.com/orchidjs/tom-select)) for a better user experience.

You'll need to create a form and a view to set the timezone value – standard Django stuff.

Now, let's create the middleware to activate the user's timezone:

```python
import zoneinfo

from django.utils import timezone

from .models import Profile


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                timezone.deactivate()
            else:
                timezone.activate(zoneinfo.ZoneInfo(profile.timezone))
        else:
            timezone.deactivate()
        return self.get_response(request)
```

This middleware activates the user's timezone if they're authenticated and have a profile. In other cases, we call `deactivate`, which sets the timezone to the default. While this last step is not strictly required, that's how the Django docs suggest doing it, so let's stick with that. To complete the setup, don't forget to register your middleware in your settings within the `MIDDLEWARE` list.

```python
MIDDLEWARE = [
     ...
    "your_app.middleware.TimezoneMiddleware",
]
```

With this setup, we've made sure that every call to `timezone.now` will takes the user's specific timezone into account. When datetime objects are saved to the database, they are automatically converted to UTC. For example, in my case (UTC+1), if I input "6:00 pm" on the UI to record a time, it will be saved in the database as `5:00 pm` (though it will still be rendered as "6:00 pm" to me on the frontend).

### Quick Tips and bits:

If you need to create a timezone-aware datetime object manually, for example by combining a date and time, here's how you do it:

```python
import datetime as dt

naive_datetime = dt.datetime.combine(my_date, my_time)
aware_datetime = timezone.make_aware(naive_datetime, zoneinfo.ZoneInfo(user_timezone))
```

The code below will generate a new migration every time you run `python manage.py makemigrations`:

```python
TIMEZONES_CHOICES = [(tz, tz) for tz in zoneinfo.available_timezones()]

class Profile(models.Model):
  timezone = models.CharField(
          verbose_name=_("Fuseau horaire"),
          max_length=50,
          default="UTC",
          choices=TIMEZONES_CHOICES,
      )
```

The culprit line is `choices=TIMEZONES_CHOICES`. A simple fix is to update the migrations file to use the  `TIMEZONES_CHOICES` constant directly:

```python
class Migration(migrations.Migration):
    ...

    operations = [
        ...
        migrations.AddField(
            model_name="profile",
            name="timezone",
            field=models.CharField(
                choices=TIMEZONES_CHOICES,
                default="UTC",
                max_length=50,
            ),
        ),
    ]
```


### Conclusion

There you have it! Your Django app is now fully equipped to support multiple timezones.
I hope this article adds a touch of timezone magic to your Django projects.
Thanks for the read.
