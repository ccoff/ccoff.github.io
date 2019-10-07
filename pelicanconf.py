#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date

AUTHOR = u'Chris Coffey (ccoff)'
SITENAME = u'0xCC0FF'
SITESUBTITLE = 'A companion blog to my GitHub account'
SITEURL = ''
#GITHUB_URL = 'https://github.com/ccoff'

PATH = 'content'

TIMEZONE = 'Europe/London'
CURRENT_YEAR = date.today().year

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
#FEED_ALL_RSS = 'feeds/all.rss.xml'

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('GitHub', 'https://github.com/ccoff'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
# https://github.com/duilio/pelican-octopress-theme
THEME = 'themes/pelican-octopress-theme'
STATIC_PATHS = ['images']
# Post date will be from file timestamp. To set a specific date, use 'Date:' in
# the metadata:
DEFAULT_DATE = 'fs'
LOAD_CONTENT_CACHE = False
PAGE_URL = 'pages/{slug}'
ARTICLE_URL = '{slug}'
CATEGORY_URL = 'category/{slug}'
TAG_URL = 'tag/{slug}'
AUTHOR_URL = 'author/{slug}'
MENUITEMS = [('About', '/pages/about')]
# Octopress theme doesn't seem to honor this one:
#DISPLAY_PAGES_ON_MENU = True
#DISPLAY_CATEGORIES_ON_MENU = True

