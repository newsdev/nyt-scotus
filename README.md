!()[https://cloud.githubusercontent.com/assets/109988/9570384/0af77540-4f58-11e5-834d-e46eaaf0bf97.png]

## Getting Started
* Get the code, set up your environment and install requirements.
```
mkvirtualenv nyt-scotus
git clone git@github.com:newsdev/nyt-scotus.git && cd nyt-scotus
pip install -r requirements.txt
add2virtualenv .
export DJANGO_SETTINGS_MODULE=config.dev.settings
```

* Before you can load data, you need to have a Postgres database called `nyt_scotus_dev` and a user `nyt_scotus_dev` that can do basically everyting on that database.
```
createdb nyt_scotus_dev
createuser nyt_scotus_dev
psql nyt_scotus_dev
alter user nyt_scotus_dev with superuser;
```

* Now you can load data.
```
django-admin load_base_data
```