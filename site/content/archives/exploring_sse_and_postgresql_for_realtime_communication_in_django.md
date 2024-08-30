---
share: true
featured: true
title: Exploring SSE and PostgreSQL for Real-time Communication in Django
slug: exploring_sse_and_postgresql_for_realtime_communication_in_django
tags:
  - python
  - django
  - sse
  - postgresql
  - starlette
description: Discover how we improved our Django project's realtime notification system by leveraging Server-Sent Events (SSE) and PostgreSQL LISTEN/NOTIFY.
publish_date: 2023-09-16
upload_path: /
---

>**TL;DR**: In this article, I explore how we built a relay system to serve real-time notifications to our Django project using Server-Sent Events (SSE) and PostgreSQL LISTEN/NOTIFY. Check out the final project on GitHub [here](https://github.com/Tobi-De/sse_relay_server). 🚀

![sse relay transmission diagram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b6esukxv1aw2io3jbr7p.png)

Recently, at my workplace, I was tasked with creating a real-time notification system for one of our Django projects. I opted for [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) (SSE). Luckily for me, around that time Django 4.2 introduced async iterators support for StreamingHttpResponse, which seemed ideal. However, as I delved deeper into the project, I decided instead to build a relay service using [Starlette](https://github.com/Tobi-De/sse_server_postgres_listen_notify) which transmits messages received through the PostgreSQL LISTEN/NOTIFY protocol to client browsers connected via SSE.

It all began with an excellent post on [Writing a chat application in Django 4.2 using async StreamingHttpResponse, Server-Sent Events, and PostgreSQL LISTEN/NOTIFY](https://valberg.dk/django-sse-postgresql-listen-notify.html). I read the post and successfully applied the concepts. This wasn't my first encounter with the PostgreSQL LISTEN/NOTIFY protocol; I knew that tools like Procrastinate (a Python task queue) also used it. This protocol was appealing because it eliminated the need to introduce additional infrastructure like Redis into our setup since we were already using PostgreSQL as our database. In the end, what I did added an extra service to our setup, but I think it was worth it, even just for the idea it sparked.

Initially, the setup worked seamlessly. Notifications were correctly transmitted and received. We switched from using Gunicorn to Daphne to run the project, and everything seemed fine. However, after a while, a colleague noticed that our server was constantly receiving requests on our SSE async view. It turned out that the connection was consistently disrupted, causing the browser to repeatedly attempt reconnection. This ultimately led to our PostgreSQL database sporadically crashing with an error message stating "too many clients."

At this point, we did something that, now that I think of it, makes absolutely no sense. We split our Django server into two instances: one running in WSGI mode with Gunicorn, and the other under Daphne in ASGI mode. It did not resolve the issue, maybe we did that thinking it would mitigate the issue. Who knows. However, it did provide me with an idea – replacing the Django app running under Daphne with something better suited for asynchronous operations.

I ended up creating a relay using [Starlette](https://www.starlette.io), which transmitted messages received through the PostgreSQL [LISTEN](https://www.postgresql.org/docs/current/sql-listen.html)/[NOTIFY](https://www.postgresql.org/docs/15/sql-notify.html) protocol to client browsers connected via SSE (The diagram above). This solution proved to be more stable and reliable than the Django approach. Furthermore, it allowed me to simplify the original Django project by completely removing the ASGI setup and code from the project. I was not very fond of the idea of mixing and matching sync and asynchronous code anyway, so this was a win for me. For a straightforward communication method via SSE in Django, this approach worked pretty well.

I've noticed several repositories on GitHub exploring similar ideas. I'm curious about its long-term viability 🤔, but for now, it works pretty well with our setup. After all, we only need the async stuff for real-time notifications. It was not worth turning our entire project into ASGI just for that. Plus, we can easily use the relay for some other precise and simple stuff in the project like updating charts, etc.

Thanks for reading! I've turned the relay project into a package and a Docker image; you can check it out at [https://github.com/Tobi-De/sse_relay_server](https://github.com/Tobi-De/sse_relay_server).
