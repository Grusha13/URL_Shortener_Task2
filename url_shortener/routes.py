from os import link

import url_shortener
from .extensions import db
from .models import Link
from flask import Blueprint, flash, render_template, request, redirect, url_for

from url_shortener.models import Link

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url)

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/addlink', methods=['POST'])
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html' , 
        new_link=link.short_url, original_url=link.original_url)

@short.route('/addlink', methods=['POST'])
def add_link():
    custom_url = request.form['custom_url']
    custom = Link(custom_url=custom_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html' , 
        new_link=link.short_url, custom_url=custom.custom_url)

@short.route('/stats')
def stats():
    links = Link.query.all()

    return render_template('stats.html' , links=links)

@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
