#!/bin/bash

dropdb nyt_scotus_dev
createdb nyt_scotus_dev
django-admin migrate
django-admin syncdb
