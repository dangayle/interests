from __future__ import unicode_literals
from __future__ import print_function
from pprint import pprint
import redis
import bottle
from bottle import BaseTemplate
from bottle import jinja2_view as view
from bottle import jinja2_template as template
from faker import Factory
from slugify import slugify
from time import time

db = redis.Redis("localhost")

test_people = {
    "person1": {
        "name": "Jim Guy",
        "interests": ['Python','programming','music','guitar','post-rock']
    },
    "person2": {
        "name": "Bob Person",
        "interests": ['Ruby','programming','music','drums','jazz']
    },
    "person3": {
        "name": "Julie Friend",
        "interests": ['knitting','music','flute','jazz']
    }
}

@bottle.route('/')
def home():
    return "Home"
    # for person in test_people:

@bottle.route('/test_insert')
def test_insert():
    pipe = db.pipeline()
    for person in test_people.values():
        print(person)
        slug = slugify(person['name'], to_lower=True)
        if db.hget("users:{}".format(slug), "slug") is None:
            data = {
                "id": db.incr('ids:user'),
                "slug": slug,
                "published": time(),
                "name": person['name'],
                "interests": person['interests'],
            }
            pipe.hmset("users:{}".format(data['slug']), data)
            for interest in person['interests']:
                pipe.sadd(interest, data['slug'])
    pipe.execute()

@bottle.route('/static/<filepath:path>')
def serve_static(filepath):
    """Serve files from static dir."""
    return bottle.static_file(filepath, root='static')

# bottle.TEMPLATE_PATH.insert(0, '../views/')
bottle.debug(True)
bottle.run(host='localhost', port=8080, reloader=True)
