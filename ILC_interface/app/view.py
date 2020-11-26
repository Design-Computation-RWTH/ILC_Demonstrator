from app import app
from flask import render_template, request, send_file, redirect, Blueprint, url_for
from io import BytesIO
from Generator.generate import csv_laden, generate_mvd_from_array
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, ZIP_STORED
import time
import requests
import base64
import pandas as pd
import sys

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("tool.html")

@app.route('/login', methods=["GET"])
def login_post():
    return render_template('login.html')

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/erstellen", methods=["GET"])
def upload_csv():
    return render_template("erstellen.html")

def decode_request(request_file):
    print("test")
    return request_file.read().decode()

def decode_request_excel(request_file):
    file_data = pd.read_excel(request_file, dtype = str)
    file_data = file_data.replace('nan', '')
    x = file_data.values
    return x

@app.route("/erstellen", methods=["POST"])
def receive_csv():
    #template_str = decode_request("xml_template")
    #view_str = decode_request("xml_view")
    try:
        datei = request.files["file-input"]

        print(datei.filename, file=sys.stderr)

        extension = datei.filename.split(".")[-1].lower()

        print("extension: {}".format(extension), file=sys.stderr)

        if(extension == "csv"):
            csv_str = decode_request(datei)
            datei_inhalt = csv_laden(csv_str.split('\n'))
        elif (extension[0:3] == "xls"):
            numpy_array = decode_request_excel(datei)
            numpy_array = numpy_array[1:,0:] # data offset
            datei_inhalt = generate_mvd_from_array(numpy_array)
            print(datei_inhalt)
        else:
            raise ValueError("File type {} is not a valid extension.".format(extension))

        memory_file = BytesIO()
        with ZipFile(memory_file, 'w') as zf:
            for elem in datei_inhalt:
                data = ZipInfo(elem[0], time.localtime(time.time())[:6])
                data.compress_type = ZIP_DEFLATED
                zf.writestr(data, elem[1])

        memory_file.seek(0)
        return send_file(memory_file, as_attachment=True, attachment_filename="datei.zip", mimetype="application/zip")

    except Exception as e:
        return render_template("erstellen.html", error_text="Error while uploading your file: {}".format(str(e)))

@app.route("/pruefen-mvd", methods=["GET"])
def upload_mvd():
    return render_template("pruefen-mvd.html")

@app.route("/pruefen-mvd", methods=["POST"])
def ifc_pruefen():
    try:
        #csv_str = decode_request("csv")
        #datei_inhalt = csv_laden(csv_str.split('\n'))

        files = {"ifcFile": ("ifc_file_path.ifc", request.files["ifc"]),"mvdXMLfile": ("mvdxml_file_path.mvdxml", request.files["mvdxml"])}
        #open("debug.mvdxml", "wb").write(mvdxml_file[1].encode())
        headers={}
        resp = requests.post("http://lbd.arch.rwth-aachen.de/mvdXMLChecker/api/check", files=files, headers=headers )
        files["ifcFile"][1].seek(0)
        files["mvdXMLfile"][1].seek(0)
        resp2 = requests.post("http://lbd.arch.rwth-aachen.de/mvdXMLChecker/api/check_plain", files=files, headers=headers )
        jasondatei=resp2.json()
        print(jasondatei)
        print("status code " + str(resp.status_code))
        print("status code " + str(resp2.status_code))

        return render_template("pruefen-mvd.html", download=True, issues=jasondatei["issues"], fine=jasondatei["element_check_results"], bcfzip64=base64.b64encode(resp.content).decode())

    except Exception as e:
        return render_template("pruefen-mvd.html", error_text="Error while uploading your file: {}".format(str(e)))


@app.route("/download", methods=["POST"])
def download():
    bcfzips64 = request.form["bcfdata"].split(",")

    binaries = [base64.b64decode(x) for x in bcfzips64]

    memory_file = BytesIO()

    with ZipFile(memory_file, 'w') as zf:
        for i, binary in enumerate(binaries):
            data = ZipInfo("bcf_file_{}.bcfzip".format(i), time.localtime(time.time())[:6])
            data.compress_type = ZIP_STORED
            zf.writestr(data, binary)

    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, attachment_filename="bcf_check.zip", mimetype="application/zip")

@app.route("/pruefen", methods=["POST"])
def pruefen():

    try:
        #csv_str = decode_request("csv")
        #datei_inhalt = csv_laden(csv_str.split('\n'))

        datei = request.files["tabelle"]
        extension = datei.filename.split(".")[-1].lower()

        print("extension: {}".format(extension))

        if(extension == "csv"):
            csv_str = decode_request(datei)
            datei_inhalt = csv_laden(csv_str.split('\n'))
        elif (extension[0:3] == "xls"):
            numpy_array = decode_request_excel(datei)
            numpy_array = numpy_array[1:,0:] # data offset
            datei_inhalt = generate_mvd_from_array(numpy_array)
        else:
            raise ValueError("File type {} is not a valid extension.".format(extension))

        issues = []

        bcfzipStrings = []

        for i, mvdxml_file in enumerate(datei_inhalt):
            files = {"ifcFile": ("ifc_file_path.ifc", request.files["ifc"]),"mvdXMLfile": (mvdxml_file[0], mvdxml_file[1].encode())}
            open("debug_{}.mvdxml".format(i), "wb").write(mvdxml_file[1].encode())
            headers={}
            resp = requests.post("http://lbd.arch.rwth-aachen.de/mvdXMLChecker/api/check", files=files, headers=headers )
            files["ifcFile"][1].seek(0)
            resp2 = requests.post("http://lbd.arch.rwth-aachen.de/mvdXMLChecker/api/check_plain", files=files, headers=headers )
            jsondatei=resp2.json()

            if resp.ok:
                bcfzipStrings.append(base64.b64encode(resp.content).decode())
            if resp2.ok:
                issues.extend(jsondatei["issues"])

            print(jsondatei)
            print("status code " + str(resp.status_code))
            print("status code plain" + str(resp2.status_code))

        return render_template("pruefen.html", download=True, issues=issues, bcfzip64=",".join(bcfzipStrings))

    except Exception as e:
        return render_template("pruefen.html", error_text="Error while uploading your file: {}".format(str(e)))


@app.route('/pruefen', methods=["GET"])
def about():
    return render_template("pruefen.html")

@app.route('/aiatemplate', methods=["GET"])
def index():
    return render_template("aiatemplate.html")
