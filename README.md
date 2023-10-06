# WONDERLAND DRINKS

This is an application for creating and sharing recipes for drinks. To do so you need to create an account. Users
without account can only see listing of drinks on main page, drink detail and use search bar.

After register and when login you can like or unlike a drink that is public. You have access to your dashboard where you
can see your drinks and drinks that you liked. You can edit and delete a drink if it's yours. You can also add new drink
and marked it as public, if you want to share it with others.
If you want to, you can change your password via special form.

This project is based on Python 3.11 and uses [Django framework](https://www.djangoproject.com/)
and [Bootstrap](https://getbootstrap.com/) for styling.

# Getting started

1. Clone this repository.
2. Create virtual environment:
    - `virtualenv venv`
    - `venv\Scripts\activate`
3. Install requirements:
    - `pip install -r requirements.txt`
4. Setup .env file:
    - create `.env` file in `drinks` folder based on `env.example`
5. Setup database - you can use demo database from repo or create new one:
    - if you use demo database from repo you can use already created accounts:
        - superuser: `admin` password: `admin`
        - user 1: `alicja` password: `alicja123456`
        - user 2: `bartek` password: `bartek123456`
    - if you want to create your own db:
        - delete `db.sqlite3` file
        - delete contents of `media/images` and `media/thumbnails` folders
        - go to `drinks` directory
        - `python manage.py makemigrations`
        - `python manage.py migrate`
        - `python manage.py createsuperuser`
            - pass superuser login and password in terminal
6. Run server:
   - `python manage.py runserver`
   - go to `http://127.0.0.1:8000/`
7. To access admin panel go to `http://127.0.0.1:8000/admin/`.

# How to use the project

1. On main page:
    - you can see list of drinks
    - you can click on drink name to see drink detail
    - you can use search bar to find drinks
2. To search for a drink type the phrase in search bar and click `Wyszukaj`.
    - you will see list of drinks that has the searched phrase in their name or description
    - you can click on drink name to see drink detail
3. To have access to more features register your account.
4. After login to newly created account you can:
    - access your dashboard using `Panel klienta` button
    - logout using `Wyloguj` button
    - change your password using `Zmień hasło` button
5. On your dashboard you can:
    - see drinks that you created or liked
    - add new drink recipe
    - edit or delete your drinks
6. When creating the drink by default the drink is private. Only the owner can see it.
   If you want to share it with others, mark it as public. The drink will be displayed on the main page.

# Tests
1. To run tests:
   - go to `drinks` directory
   - `python manage.py test`
2. To view code coverage:
   - `coverage run manage.py test -v 2`
   - `coverage html`
   - open `htmlcov/index.html` in browser


# TODO
- [ ] handle image formats other than `jpg`
- [ ] add product management view
- [ ] set default image for drinks
- [ ] handle upper and lowercase unicode characters in search bar same way
- [ ] improve product select in drink form
- [ ] add drink card folding
- [ ] add tests for search bar
- [ ] fix static urls in tests
- [ ] add like counter recalculation option






