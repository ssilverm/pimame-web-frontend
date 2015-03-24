from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request
import yaml
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_BINDS'] = {
    'config':        'sqlite:///config.db',
    'games':      'sqlite:///games_master.db'
}


app.config['SECRET_KEY'] = 'jdhq7864r8uihblk'
# Flask and Flask-SQLAlchemy initialization here

# class User(db.Model):
#     __bind_key__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)


db = SQLAlchemy(app)
db.create_scoped_session()


class KickstarterBackers(db.Model):
    __tablename__ = 'kickstarter_backers'
    __bind_key__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    def __unicode__(self):
        return self.name

class MenuItems(db.Model):
    __tablename__ = 'menu_items'
    __bind_key__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Text)
    icon_id = db.Column(db.Text)
    type = db.Column(db.Text)
    visible = db.Column(db.Integer)
    command = db.Column(db.Text)
    rom_path = db.Column(db.Text)
    include_full_path = db.Column(db.Integer)
    include_extension = db.Column(db.Integer)
    override_menu = db.Column(db.Integer)
    icon_file = db.Column(db.Text)
    icon_selected = db.Column(db.Text)
    position = db.Column(db.Text)
    scraper_id = db.Column(db.Text)

    def __unicode__(self):
        return self.label

class Options(db.Model):
    __tablename__ = 'options'
    __bind_key__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    max_fps = db.Column(db.Integer)
    show_ip = db.Column(db.Integer)
    show_update = db.Column(db.Integer)
    sort_items_alphanum = db.Column(db.Integer)
    sort_items_with_roms_first = db.Column(db.Integer)
    hide_emulators_with_no_roms = db.Column(db.Integer)
    hide_system_tools = db.Column(db.Integer)
    show_cursor = db.Column(db.Integer)
    allow_quit_to_console = db.Column(db.Integer)
    use_scene_transitions = db.Column(db.Integer)
    default_music_volume = db.Column(db.Float)
    theme_pack = db.Column(db.Text)
    resolution = db.Column(db.Text)    
    fullscreen = db.Column(db.Integer) 
    show_rom_clones = db.Column(db.Integer) 
    show_unmatched_roms = db.Column(db.Integer) 
    sort_roms_by = db.Column(db.Text) 
    rom_sort_order = db.Column(db.Text) 
    filter_roms_by = db.Column(db.Text) 
    #change_log = db.Column(db.Text) 
    first_run = db.Column(db.Integer)

    def __unicode__(self):
        return self.id 

class LocalRoms(db.Model):
    __tablename__ = 'local_roms'
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(db.Integer)
    title = db.Column(db.Text)
    search_terms = db.Column(db.Text)
    parent = db.Column(db.Text)
    cloneof = db.Column(db.Text)
    release_date = db.Column(db.Text)
    overview = db.Column(db.Text)
    esrb = db.Column(db.Text)
    genres = db.Column(db.Text)
    players = db.Column(db.Text)
    coop = db.Column(db.Text)
    publisher = db.Column(db.Text)
    developer = db.Column(db.Text)    
    rating = db.Column(db.Float) 
    command = db.Column(db.Text) 
    rom_file = db.Column(db.Text) 
    rom_path = db.Column(db.Text) 
    image_file = db.Column(db.Text)
    flags = db.Column(db.Text) 
    number_of_runs = db.Column(db.Integer) 

    def __unicode__(self):
        return self.title

class CustomModelView(ModelView):
    edit_template = 'edit_admin.html'
    create_template = 'create_admin.html'
    list_template = 'list_admin.html'

class LocalRomsAdmin(CustomModelView):
    column_searchable_list = ('title')
    column_filters = ('title')


admin = Admin(app, 'PiPLAY DB Interface', base_template='layout.html', template_mode='bootstrap3')
#admin = Admin(app, base_template='base_admin.html')
admin.add_view(CustomModelView(MenuItems, db.session))
admin.add_view(CustomModelView(Options, db.session))
#admin.add_view(CustomModelView(KickstarterBackers, db.session))
admin.add_view(CustomModelView(LocalRoms, db.session))

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'smc', 
		      'n64', 'gen', 'v64', 'bin', 'smd', 'SMC', 'GEN', 
		      'BIN', 'SMD', 'gba', 'GBA', 'gb', 'GB', 'ZIP']

#document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
#print yaml.dump(yaml.load(document))

@app.route("/")
def hello():
    name = "Hello World!"
    #document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
    #data = yaml.load(document)

    return render_template('index.html', name=name)

@app.route("/rom")
def rom():
    name = "Hello World!"
    #document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
    #data = yaml.load(document)
    #print data
    data = MenuItems.query.all()
    return render_template('list.html', name=name, data=data)

@app.route("/system/<system_label>")
def list_files(system_label):
    name = "Hello World!"
    #document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
    #data = yaml.load(document)
    system_data = 0

    # for d in data['menu_items']:
    # 	print d['label']
    # 	print system_label
    # 	if d['label'] == system_label:
    # 		system_data = d

    # roms = system_data['roms']
    # data = MenuItems.query.all()

    system_data = MenuItems.query.filter_by(label=system_label).first()
    roms = system_data.rom_path
    print roms

    try:
        from os import listdir
        from os.path import isfile, join
        files = [ f for f in listdir(roms) if isfile(join(roms,f)) ]
    except:
        files = None
    return render_template('files.html', files=files, system_label=system_label, system_path = "/upload/" + system_label)

@app.route("/upload/<system_label>", methods=['POST','GET'] )
def upload_files(system_label):
    #return "hi"
    name = "Hello World!"
    #document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
    #data = yaml.load(document)
    system_data = 0

    # for d in data['menu_items']:
    #     print d['label']
    #     print system_label
    #     if d['label'] == system_label:
    #         system_data = d

    # roms = system_data['roms']

    system_data = MenuItems.query.filter_by(label=system_label).first()
    roms = system_data.rom_path

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            #filename = os.path.join(roms, "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            filename = os.path.join(roms, "%s" % (file.filename) )
            file.save(filename)
            return jsonify({"success":True})

    return render_template("upload.html", system_path = "/upload/" + system_label)

@app.route("/tools", methods=['POST','GET'] )
def tools():
    return render_template("tools.html")


@app.route("/tools/<power>", methods=['POST','GET'] )
def power(power):
    if power == "reboot":
        command = "sudo reboot"
        msg = "Rebooting your system now."
    elif power == "shutdown":
        command = "sudo poweroff"
        msg = "Powering off your system now."
    else:
        msg = "Not a valid command."
        return render_template("tools.html", msg = msg)


    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    return render_template("tools.html", msg = msg)



@app.route("/ks")
def kickstarter():
    name = "Kickstarter!"
    #document = open('/home/pi/pimame/pimame-menu/ks.yaml')
    #data = yaml.load(document)

    data = KickstarterBackers.query.all()
    #print data
    return render_template('ks_list.html', name=name, data=data)




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    if 'DEBUG' in os.environ:
        app.debug = True
    app.debug = True
    app.run(host="0.0.0.0", port=80)
