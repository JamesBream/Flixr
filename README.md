# Flixr

**Flixr** is a simple example of a Flask-powered web app designed to read data from a web API and interact with a local relational database.

Specifically, **Flixr** presents movie data from **TMDB.com**'s public API in a simplistic but presentable fashion inspired by **Google's Material Design language**. The simple front end allows user registration and bookmarking of popular movies.

## Getting Started
Flixr is built for Python 3.5+ and can be configured by running the following
```
pip install -r requirements.txt
```

This will install all dependencies required by Flixr though it is recommended to use a python virtual environment as Flixr has not been tested with the latest releases of many of its dependencies.

The final step is to configure your `config.py` file. This can be done by duplicating and renaming the `config_.py` template included. The basic requirements are a MySQL database with the associated user and password. Also, an API key is required to access TMDB.com's API which can be obtained for free with a registered account on their website.