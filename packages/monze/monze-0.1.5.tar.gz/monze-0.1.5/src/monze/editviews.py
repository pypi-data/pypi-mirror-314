import os
from pprint import pprint as ppp
import json
from flask import redirect, request, Blueprint, render_template

from general import Casting, Timetools, JINJAstuff, BaseClass, FtpAnta
from singletons import UserSettings, Sysls, Views
from emails import EmailBaseClass

from studenten import Student
from singletons import Students


# VIEWS WORDEN ALLEEN LOSGELATEN OP GROEPEN, NIET OP STUDENTEN!!!
def jinja_object(ding):
	sysls_o = Sysls()
	return JINJAstuff(ding, sysls_o.get_model())

# =============== endpoints =====================
ep_editviews = Blueprint(
	'ep_editviews', __name__,
	url_prefix="/editviews",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'edit views'

# handles one student
class View(BaseClass):
	@classmethod
	def get_model(cls) -> dict:
		views_o = Views()
		basic = views_o.empty_view()
		d = dict()
		for b in basic:
			d[b] = {'default': basic[b]}
		d['name'] = ''
		return d

@ep_editviews.get('/<int:viewid>/<path:copie>')
@ep_editviews.get('/<int:viewid>')
@ep_editviews.get('/')
def view(viewid=0, copie=None):
	copie = not copie is None

	views_o = Views()
	if viewid == 0:
		viewid = views_o.get_defaultkey()
	allviews = views_o.get()
	mijnviews = views_o.mijn_views()
	singleview = views_o.get_single_by_key(viewid)

	if singleview is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	# fieldnames are standard db field names
	fieldnames = list(Student.get_empty().keys())
	# eruit are fieldnames that cannot be used in a view, or that are always included
	eruit = ['id', 'firstname', 'lastname', 'assessment', 's_gender', 'grade_ts', 'kom_code', 'notes', 'circulars', 'customs']

	fields = dict()
	for s in fieldnames:
		if s in eruit:
			continue
		fields[s] = Student.get_nicename(s)
	# fields now contains all the standard available fields for a view

	# single[fields] contains the fields in this single view
	for s in singleview['fields']:
		if s in fieldnames:
			fields[s] = Student.get_nicename(s)
		else:
			# these are the circulars fields
			fields[s] = s

	sysls_o = Sysls()

	# these are the available groups
	groepen = sysls_o.get_sysl('s_group')

	# available email buttons:
	emailbuttons = EmailBaseClass().alle_emails()

	singleview = jinja_object(singleview)
	defaultview = None
	for key in allviews:
		if key == views_o.get_defaultkey():
			defaultview = jinja_object(allviews[key])
		else:
			allviews[key] = jinja_object(allviews[key])

	del(allviews[views_o.get_defaultkey()])

	return render_template(
		'editviews.html',
		menuitem=menuitem,
		props=UserSettings(),
		all=allviews,
		single=singleview,
		default=defaultview,
		mijnviews=mijnviews,
		kopie=copie,
		fields=fields,
		fixedfields=fieldnames,
		groepen=groepen,
		emailbuttons=emailbuttons,
	)

# for editing the view itself (topright in html)
@ep_editviews.post('/<int:viewid>')
def views_post(viewid):
	try:
		color = Casting.str_(request.form['color'], '#ffffff')
		status = Casting.int_(request.form['status'], 1)
		name = Casting.str_(request.form['changename'], '#ffffff')
	except Exception as e:
		print(e)
		return redirect(f'/editviews/{viewid}')

	views_o = Views()
	single = views_o.get_single_by_key(viewid)
	single['color'] = color
	single['status'] = status
	single['name'] = name
	views_o.make_view(single)

	return redirect(f"/editviews/{viewid}")

# for editing stuff in a view
@ep_editviews.post('/edit/<int:viewid>')
def view_edit_post(viewid):
	views_o = Views()
	single = views_o.get_single_by_key(viewid)

	if single is None:
		return redirect('/editviews/default')

	if not ('fieldname' in request.form and 'fieldnamelist' in request.form):
		return redirect(f"/editviews/{viewid}")

	try:
		veldnamen = request.form['fieldnamelist'].split(',')
	except:
		return redirect(f"/editviews/{viewid}")
	veldnaam = Casting.str_(request.form['fieldname'], '')

	if veldnaam != '':
		if 'add-field' in request.form:
			veldnamen.append(veldnaam)

		elif 'delete-field' in request.form:
			veldnamen.remove(veldnaam)

		elif 'new-cycle-field' in request.form:
			if not veldnaam in veldnamen:
				veldnamen.append(f"c_{veldnaam}")

		elif 'new-text-field' in request.form:
			if not veldnaam in veldnamen:
				veldnamen.append(f"t_{veldnaam}")

	single['fields'] = veldnamen
	views_o.make_view(single)
	return redirect(f"/editviews/{viewid}")

# for deleting view
@ep_editviews.post('/delete/<int:viewid>')
def delete_post(viewid):
	views_o = Views()
	views_o.delete(viewid)
	return redirect(f'/editviews/{views_o.get_defaultkey()}')

# step 2 in copying a view
@ep_editviews.post('/kopie/<int:copyid>')
def kopie_post(copyid):
	jus = UserSettings()
	views_o = Views()
	try:
		newname = Casting.name_safe(request.form['newname'], True)
		print(copyid, newname)
		if newname == '':
			return redirect(f'/editviews/{views_o.get_defaultkey()}')
		if newname in views_o.get():
			return redirect(f'/editviews/{views_o.get_defaultkey()}')
	except:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	# make new views with newname
	newview = views_o.get_single_by_key(copyid)
	ppp(newview)
	newid = Timetools.now_secs()
	newview['name'] = newname
	newview['alias'] = jus.alias()
	newview['created_ts'] = newid
	newview['groups'] = list()
	newview['color'] = '#ffffff'
	views_o.make_view(newview)
	return redirect(f"/editviews/{newid}")

@ep_editviews.post('/group/<int:viewid>')
def group_post(viewid):
	views_o = Views()
	view = views_o.get_single_by_key(viewid)
	if view is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	if not 'groups' in view:
		view['groups'] = list()

	groep_id = 0
	for item in request.form:
		if item in ['add-group', 'delete-group']:
			continue
		groep_id = Casting.int_(item, default=0)
	if groep_id == 0:
		return redirect(f"/editviews/{viewid}")

	if 'add-group' in request.form:
		view['groups'].append(groep_id)
	elif 'delete-group' in request.form:
		view['groups'].remove(groep_id)

	views_o.make_view(view)
	return redirect(f"/editviews/{viewid}")

@ep_editviews.post('/sort-views')
def sort_views():
	if not 'viewids' in request.form:
		return redirect(f"/editviews")

	try:
		ids: list = Casting.str_(request.form['viewids'], '').split(',')
		for i in range(len(ids)):
			ids[i] = Casting.int_(ids[i], 0)
	except:
		return redirect(f"/editviews")

	views_o = Views()
	views_o.reorder_views(ids)
	return redirect(f"/editviews")

@ep_editviews.post('/emailbutton/<int:viewid>')
def add_emailbutton(viewid):
	views_o = Views()
	view = views_o.get_single_by_key(viewid)
	if view is None:
		return redirect(f'/editviews/{views_o.get_defaultkey()}')

	if 'add-emb' in request.form:
		if not 'emailbuttons' in view:
			view['emailbuttons'] = list()
		view['emailbuttons'].append(request.form['add-emb'])

	elif 'delete-emb' in request.form:
		if not 'emailbuttons' in view:
			view['emailbuttons'] = list()
		try:
			view['emailbuttons'].remove(request.form['delete-emb'])
		except:
			pass

	views_o.make_view(view)
	return redirect(f"/editviews/{viewid}")

@ep_editviews.post('/summative/<int:viewid>')
def summative_post(viewid):
	# makes a list summative for groups.
	# only admin can edit
	# alias = "summative"
	views_o = Views()
	single = views_o.get_single_by_key(viewid)
	if single is None:
		return redirect(f'/editviews')
	single["alias"] = "summative"
	views_o.make_view(single)
	return redirect(f'/editviews/{viewid}')

@ep_editviews.post('/unsummative/<int:viewid>')
def unsummative_post(viewid):
	views_o = Views()
	single = views_o.get_single_by_key(viewid)
	if single is None:
		return redirect(f'/editviews')
	jus = UserSettings()
	single["alias"] = jus.alias()
	views_o.make_view(single)
	return redirect(f'/editviews/{viewid}')

@ep_editviews.post('/uploadsummative/<int:viewid>')
def uploadsummative_post(viewid):
	# haal lijst met summatieve gegevens
	# alle studenten in groepen gekoppeld aan view
	# s_status is niet van belang
	views_o = Views()
	# get alle views die summatief zijn en actief
	sumviews = views_o.summative_views()

	students_o = Students()
	students_o.init()
	allstudents = students_o.all_as_lod()
	# zet om in dict per student in deze view

	sysl_o = Sysls()

	dezestudents = dict()
	for s in allstudents:
		# 's_course': 1, 's_ec': 15  's_group': 1026
		try:
			course = sysl_o.get_sysl_item('s_course', s['s_course'])['name']
		except:
			course = ""

		try:
			ass = s['assessment']
		except:
			ass = 0

		d = dict(
			password=s['password'],
			name=f"{s['firstname']} {s['lastname']}",
			course=course, # naam cpnits 15 of zo
			fields=list(),
			fieldvals=list(), # sync to fields
			ass=ass,
			tabel = "",
		)
		# een groep kan maar in één summative zitten
		# een student dus ook
		for key, view in sumviews.items():
			if s['s_group'] in view['groups']:
				# IMPORTANT dit moet met lijsten want dict sorteert zichzelf
				# is ook handiger bij HTMl maken
				d['fields'] = list()
				d['fieldvals'] = list()
				for field in view['fields']:
					if not field.startswith('c_'):
						continue
					d['fields'].append(field.replace('c_', ''))
					try:
						val = Casting.int_(s['circulars'][key][field], default=0)
						d['fieldvals'].append(val)
					except:
						# if not yet valued
						d['fieldvals'].append(0)
		# nu html tabel maken
		dezestudents[s['password']] = maak_html_tabelletje(d)

	# alle data
	# zet om in veilige json
	eruit = json.dumps(dezestudents)

	# stuur naar ANTA ftp server
	anta = FtpAnta(
		'cpnits.com',
		'cpnitswebsite@cpnits.com',
		'CpnitsWebsite',
		'public_html/summative'
	)
	anta.put_grades(eruit)
	return redirect(f'/editviews/{viewid}')

def maak_html_tabelletje(d: dict) -> str:
	kleuren = ['zilver', 'groen', 'oranje', 'rood', 'blauw', 'grijs', 'wit']
	tabel = f'<table><thead><tr><td colspan="2">{d["name"]}</td>'
	# itereer kopjes
	for inh in d['fields']:
		tabel = f'{tabel}<td class="paars">{inh}</td>'

	# tweede rij
	tabel = tabel + f'<td class="paars">oral&nbsp;assessment</td></tr></thead><tbody><tr><td>{d["course"]}</td><td class="paars">score</td>'

	resit = list()
	failed = False
	# itereer toets
	for i in range(len(d['fieldvals'])):
		# logica...
		inh = d['fieldvals'][i]
		if inh == 0: # nog niets
			resit.append(0)
		elif inh == 1:  # gehaald
			resit.append(5) #
		elif inh == 2:
			if not failed:
				resit.append(4) # blauw
			else:
				resit.append(5)
		elif inh == 3: # def gezakt
			inh = 2 # bovenste rij oranje zetten
			resit.append(3) # resit rij op rood
			failed = True
			# IN DIT GEVAL kunnen alle andere vakken in resit donkergrijs worden en het eindresultaat op rood
			# ook oral is dan niet meer nodig
		else:
			resit.append(0)

		kleur = kleuren[inh]
		tabel = f'{tabel}<td class="first {kleur}"></td>'

	if d['ass'] > 0:
		if failed:
			kleur = kleuren[5] # gezakt dus niet meer nodig.
		else:
			kleur = kleuren[4]
	else:
		kleur = kleuren[0]
	tabel = tabel + f'<td rowspan="2" class="assessment {kleur}"></td></tr><tr><td>&nbsp;</td><td class="paars">resit</td>'

	# itereer resit
	noresit = True
	for inh in resit:
		kleur = kleuren[inh]
		tabel = f'{tabel}<td class="resit {kleur}"></td>'

	tabel = tabel + f'</tr></tbody></table>'
	return tabel