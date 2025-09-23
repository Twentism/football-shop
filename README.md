pws deployed link : https://melanton-gabriel-footballshop.pbp.cs.ui.ac.id/

README for Assignment 2
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
Django is a great first framework because it gives us the full web stack out of the ORM box, templates, admin, and security, all without drowning in setup. Its use of Python makes it beginner-friendly and keeps the code readable. The framework’s objective structure (models, views, templates) teaches good design habits early. Plus, it’s safe, scalable, and has great docs, so we will spend more time building and less time finding the right tool.

README for Assignment 3
1. Data delivery makes the frontend and backend able to communicate, so the app can show and save information properly. Without it, the system would just stand alone and the user wouldn’t get updated or stored data. It’s basically the bridge that connects what the user sees with the actual database behind it.

2. JSON is better for web apps because it’s lighter, easier to read, and works directly with JavaScript, while XML has too many extra tags. JSON is also faster to process, which makes it more popular for modern platforms. In real use, JSON just feels simpler and cleaner compared to XML.

3. is_valid() checks if the form input follows the rules, and only if it’s valid I can safely use or save the data. This avoids errors and makes sure the data stored in the database is clean and correct. It’s like a checkpoint before the data is allowed to enter the system.

4. csrf_token protects forms from CSRF attacks. Without it, attackers could trick logged-in users into sending harmful requests, and this can lead to actions being done without the user even knowing. Adding the token is just a small step, but it’s a big layer of security.

5. I checked cookies, used render(request, ...), added {% csrf_token %} in every form, made sure CsrfViewMiddleware is active, fixed CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS, set DEBUG = False, redeployed, and tested again. I also fixed my models, views, and migrations so the product data shows up correctly, because at first I thought the page worked but it didn’t actually save the product. In short, I didn’t just follow the tutorial blindly but tried to troubleshoot step by step until everything finally worked.

6. One feedback maybe in terms of make it clear to the students (because sometimes the error messages are getting out of hand and students became overwhelmed.
)

Photos from Postman:
![xml ss](https://github.com/user-attachments/assets/2933a715-94bf-42f4-8725-dc2c6fcf271f)
![json ss](https://github.com/user-attachments/assets/3fa253e9-c6d9-467e-8c36-9e564c6b178a)


