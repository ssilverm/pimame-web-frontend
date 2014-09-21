from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request
import yaml
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'smc', 
		      'n64', 'gen', 'v64', 'bin', 'smd', 'SMC', 'GEN', 
		      'BIN', 'SMD', 'gba', 'GBA', 'gb', 'GB', 'ZIP']

document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
#print yaml.dump(yaml.load(document))

@app.route("/")
def hello():
    name = "Hello World!"
    document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')

    data = yaml.load(document)

    return render_template('index.html', name=name, data=data)

@app.route("/rom")
def rom():
    name = "Hello World!"
    document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')

    data = yaml.load(document)
    print data
    return render_template('list.html', name=name, data=data)

@app.route("/system/<system_label>")
def list_files(system_label):
    name = "Hello World!"
    document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')

    data = yaml.load(document)
    system_data = 0

    for d in data['menu_items']:
    	print d['label']
    	print system_label
    	if d['label'] == system_label:
    		system_data = d

    roms = system_data['roms']
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
    document = open('/home/pi/pimame/pimame-web-frontend/config.yaml')
    data = yaml.load(document)
    system_data = 0

    for d in data['menu_items']:
        print d['label']
        print system_label
        if d['label'] == system_label:
            system_data = d

    roms = system_data['roms']

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
    document = open('/home/pi/pimame/pimame-menu/ks.yaml')

    data = yaml.load(document)
    print data
    return render_template('ks_list.html', name=name, data=data)




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    if 'DEBUG' in os.environ:
        app.debug = True
    app.debug = True
    app.run(host="0.0.0.0", port=80)
