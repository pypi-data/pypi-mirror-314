import jinja2
from flask import Blueprint
blueprint = Blueprint('filters', __name__)

from general import Casting, Timetools, Mainroad
from singletons import Sysls

# ============= JINJA FILTERS =============
# using the decorator
@blueprint.app_template_filter('gradecss')
def gradecss(grade):
	grade = Casting.int_(grade, default=0)
	if grade >= 55:
		return 'grade-passed'
	elif grade >= 10:
		return 'grade-failed'
	return 'grade-not'

@blueprint.app_template_filter('filtername')
def filtername(name):
	fnames = {
		'registratie': 'register',
		'studenten': 'students',
		'beoordelen': 'grading',
		'alumni': 'alumni',
		'niet': 'not',
		'noshow': 'noshow',
		'alle': 'all'
	}
	if name in fnames.keys():
		return fnames[name]
	return name

@blueprint.app_template_filter('gender')
def gender(name):
	if name.lower() in ['m']:
		return '&#9794;'
	elif name.lower() in ['v', 'f']:
		return '&#9792;'
	else:
		return '&#9893;'

@blueprint.app_template_filter('initials')
def initials(name):
	name = name.split(' ')
	eruit = ''
	for n in name:
		eruit = f"{eruit}{n.upper()}"
	return eruit

@blueprint.app_template_filter('circ')
def circular_color(val):
	val = Casting.int_(val, 0)
	try:
		sysls = Sysls()
		cees = sysls.get_sysl('s_circular')
		return cees[val]['color']
	except:
		return '#eeeeee'

@blueprint.app_template_filter('circlass')
def circular_colorclass(val):
	classes = ['c-nul', 'c-een', 'c-twee', 'c-drie']
	val = Casting.int_(val, 0)
	try:
		return classes[val]
	except:
		return 'c-nul'

@blueprint.app_template_filter('nonone')
def nonone(s):
	if s is None:
		return ''
	elif s in ['None', 'none']:
		return ''
	else:
		return s

from urllib.parse import quote
@blueprint.app_template_filter('urlsafe')
def urlsafe(s):
	try:
		return quote(str(s))
	except:
		return s

@blueprint.app_template_filter('nbsp')
def nbsp(s):
	try:
		return s.replace(' ', '&nbsp;')
	except:
		return s

@blueprint.app_template_filter('vier')
def vier(i):
	try:
		return f'{i:04d}'
	except:
		return i

@blueprint.app_template_filter('date')
def asdate(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, withtime=False)
	except:
		return i

@blueprint.app_template_filter('datetime')
def asdatetime(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, withtime=True)
	except:
		return i

@blueprint.app_template_filter('datetimelocal')
def asdatetime(i):
	try:
		if i < 1:
			return ''
		return Timetools.ts_2_td(i, rev=True, local=True)
	except:
		return i
