Examples
========


.. _example-alone-simple:

Simple Applications with Flask-DigestAuth Alone
-----------------------------------------------

In your ``my_app.py``:

::

    from flask import Flask, request, redirect
    from flask_digest_auth import DigestAuth

    app: flask = Flask(__name__)
    ... (Configure the Flask application) ...

    auth: DigestAuth = DigestAuth()
    auth.init_app(app)

    @auth.register_get_password
    def get_password_hash(username: str) -> t.Optional[str]:
        ... (Load the password hash) ...

    @auth.register_get_user
    def get_user(username: str) -> t.Optional[t.Any]:
        ... (Load the user) ...

    @app.get("/admin")
    @auth.login_required
    def admin():
        return f"Hello, {g.user.username}!"

    @app.post("/logout")
    @auth.login_required
    def logout():
        auth.logout()
        return redirect(request.form.get("next"))


.. _example-alone-large:

Larger Applications with ``create_app()`` with Flask-DigestAuth Alone
---------------------------------------------------------------------

In your ``my_app/__init__.py``:

::

    from flask import Flask
    from flask_digest_auth import DigestAuth

    auth: DigestAuth = DigestAuth()

    def create_app(test_config = None) -> Flask:
        app: flask = Flask(__name__)
        ... (Configure the Flask application) ...

        auth.init_app(app)

        @auth.register_get_password
        def get_password_hash(username: str) -> t.Optional[str]:
            ... (Load the password hash) ...

        @auth.register_get_user
        def get_user(username: str) -> t.Optional[t.Any]:
            ... (Load the user) ...

        return app

In your ``my_app/views.py``:

::

    from my_app import auth
    from flask import Flask, Blueprint, request, redirect

    bp = Blueprint("admin", __name__, url_prefix="/admin")

    @bp.get("/admin")
    @auth.login_required
    def admin():
        return f"Hello, {g.user.username}!"

    @app.post("/logout")
    @auth.login_required
    def logout():
        auth.logout()
        return redirect(request.form.get("next"))

    def init_app(app: Flask) -> None:
        app.register_blueprint(bp)


.. _example-flask-login-simple:

Simple Applications with Flask-Login Integration
------------------------------------------------

In your ``my_app.py``:

::

    import flask_login
    from flask import Flask, request, redirect
    from flask_digest_auth import DigestAuth

    app: flask = Flask(__name__)
    ... (Configure the Flask application) ...

    login_manager: flask_login.LoginManager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> t.Optional[User]:
        ... (Load the user with the username) ...

    auth: DigestAuth = DigestAuth()
    auth.init_app(app)

    @auth.register_get_password
    def get_password_hash(username: str) -> t.Optional[str]:
        ... (Load the password hash) ...

    @app.get("/admin")
    @flask_login.login_required
    def admin():
        return f"Hello, {flask_login.current_user.get_id()}!"

    @app.post("/logout")
    @flask_login.login_required
    def logout():
        auth.logout()
        # Do not call flask_login.logout_user()
        return redirect(request.form.get("next"))


.. _example-flask-login-large:

Larger Applications with ``create_app()`` with Flask-Login Integration
----------------------------------------------------------------------

In your ``my_app/__init__.py``:

::

    from flask import Flask
    from flask_digest_auth import DigestAuth
    from flask_login import LoginManager

    auth: DigestAuth = DigestAuth()

    def create_app(test_config = None) -> Flask:
        app: flask = Flask(__name__)
        ... (Configure the Flask application) ...

        login_manager: LoginManager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id: str) -> t.Optional[User]:
            ... (Load the user with the username) ...

        auth.init_app(app)

        @auth.register_get_password
        def get_password_hash(username: str) -> t.Optional[str]:
            ... (Load the password hash) ...

        return app

In your ``my_app/views.py``:

::

    import flask_login
    from flask import Flask, Blueprint, request, redirect
    from my_app import auth

    bp = Blueprint("admin", __name__, url_prefix="/admin")

    @bp.get("/admin")
    @flask_login.login_required
    def admin():
        return f"Hello, {flask_login.current_user.get_id()}!"

    @app.post("/logout")
    @flask_login.login_required
    def logout():
        auth.logout()
        # Do not call flask_login.logout_user()
        return redirect(request.form.get("next"))

    def init_app(app: Flask) -> None:
        app.register_blueprint(bp)

The views only depend on Flask-Login, but not the actual
authentication mechanism.  You can change the actual authentication
mechanism without changing the views.
