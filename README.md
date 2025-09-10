pws deployed link : https://melanton-gabriel-footballshop.pbp.cs.ui.ac.id/

Answers:
1. Step-by-step implementation
I started by creating a new Django project and app, then added the app to INSTALLED_APPS so Django knows it exists. Next, I built the Product model with the six required fields, threw in extras like stock and brand, and registered it in the admin for quick testing. I connected urls.py to a view in views.py that fetches products via the model and passes them to an HTML template. Finally, I ran makemigrations and migrate to turn my model into a real database table and tested everything locally before pushing it out.

2. diagram
<img width="1572" height="1045" alt="Blank board" src="https://github.com/user-attachments/assets/c18a704e-1b69-466b-a613-58616df4e39a" />


3. Role of settings.py
Think of settings.py as the project’s control center / room, it decides what apps to load, where the database lives, where to find templates, and how to serve static files. It also controls middleware, security (like ALLOWED_HOSTS and CSRF protection), and logging. Without it, Django wouldn’t know how to stitch together the moving parts of the project. In short, it’s the “brain” of the app, and changing it can make or break our deployment.

4. Database migration in Django
Migrations are Django’s way of turning Python code into database tables without writing SQL by hand. I run makemigrations to capture model changes as migration files, and migrate to actually apply them to the database. Django records which migrations have been applied so it never repeats them. It’s basically a time machine for our database schema, letting us evolve it safely as our app grows.

5. Why Django as a starting framework
Django is a great first framework because it gives us the full web stack out of the box—ORM, templates, admin, security—all without drowning in setup. Its use of Python makes it beginner-friendly and keeps the code readable. The framework’s opinionated structure (models, views, templates) teaches good design habits early. Plus, it’s safe, scalable, and has great docs, so we will spend more time building and less time reinventing the wheel.
