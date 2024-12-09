from flask import Flask, redirect, request, render_template
import logging
import sys
import os
import webbrowser
# import tkinter as tk
# from tkinter import filedialog, simpledialog
import pathlib

monzepad = str(pathlib.Path(__file__).parent.resolve())
if not monzepad in sys.path:
	sys.path.insert(0, monzepad)

import jinja_filters
from general import (
	Casting,
	Timetools,
	Mainroad,
	Startup,
	Css,
)

_version = "0.1.5"
_devdev = False
# _pid = str(os.getpid())
Mainroad.version = _version

# for stopping process via prompt
Startup.optionals(sys.argv)
# for checking correct version
Startup.check_version()

# check if settings and onedrive is known
# exit if wrong or cancelled
odpath = Startup.get_odpath()

# check settings, login, or exit
Startup.check_settings(odpath)

from singletons import (
	Sysls,
	UserSettings,
)

app = Flask(__name__, template_folder='templates', static_folder='static', root_path=monzepad)
app.config['FLASK_DEBUG'] = app.config['DEBUG'] = _devdev
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'nq023489cnJGH#F!'
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'cookieboogle'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = 24 * 60 * 60
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
app.config['initialized'] = False
app.config['version'] = _version

app.url_map.strict_slashes = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.before_request
def before_request():
	return
	''' 
	# check if mainroad is complete,
	# if not goto login page
	rp = request.full_path
	if '/static/' in rp or '/favicon.ico' in rp or '/generate/' in rp:
		return

	jus = UserSettings()
	# print('Before request', request.path)
	# handling the first request, restarting where we left of
	rp = rp.rstrip('?')
	rp = rp.rstrip('/')

	if jus.is_new():
		# after startup of butterfly, go to last url
		jus.set_prop('isnew', False)
		jus.set_prop('prev_url', '')
		# get the previouw url and go there (so it is current as well)
		lasturl = jus.get_prop('last_url', default='/home')
		if lasturl in ['', '/', '/home']:
			return redirect('/home')
		else:
			jus.set_prop('prev_url', '')
			return redirect(lasturl)
	else:
		# don't store paths with args
		if len(request.args) > 0:
			pass
		elif len(request.form) > 0:
			pass
		else:
			lasturl = jus.get_prop('last_url', default='')
			if lasturl == rp:
				pass
			elif lasturl in ['', '/', '/home']:
				jus.set_prop('prev_url', '')
			else:
				jus.set_prop('prev_url', lasturl)
			# remember the current url
			jus.set_prop('last_url', rp)
	'''

@app.after_request
def add_header(res):
	res.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
	res.headers["Pragma"] = "no-cache"
	res.headers["Expires"] = "0"
	res.headers['X-Content-Type-Options'] = ''
	res.headers['Access-Control-Allow-Origin'] = '*'
	res.headers['Access-Control-Allow-Methods'] = 'get, post'
	res.cache_control.public = True
	res.cache_control.max_age = 0
	return res

@app.get('/')
def index():
	return redirect('/home')

app.register_blueprint(jinja_filters.blueprint)

from home import ep_home
app.register_blueprint(ep_home)

from studenten import ep_studenten
app.register_blueprint(ep_studenten)

from groepen import ep_groepen
app.register_blueprint(ep_groepen)

from views import ep_views
app.register_blueprint(ep_views)

from editviews import ep_editviews
app.register_blueprint(ep_editviews)

# from endpoint.hunts import ep_hunts
# app.register_blueprint(ep_hunts)

from emails import ep_email
app.register_blueprint(ep_email)

from beheer import ep_beheer
app.register_blueprint(ep_beheer)

from website import ep_website
app.register_blueprint(ep_website)

if not app.config['DEBUG']:
	@app.errorhandler(Exception)
	def handle_error(e):
		Mainroad.loglog(f"error {e}")
		Mainroad.loglog(f"\t{request.full_path}")
		return redirect('/home')

def run():
	if not app.config['initialized']:
		startup = os.path.join(monzepad, "startup.html")
		app.config['initialized'] = True
		if not app.config['DEBUG']:
			webbrowser.open_new(f"file://{startup}")
		print(f"{Css.good()}Butterfly is served on http://127.0.0.1:5000/, version {app.config['version']}{Css.reset()}")
	app.run(port=5000, debug=app.config['DEBUG'], use_reloader=False)

if __name__ == '__main__':
	run()