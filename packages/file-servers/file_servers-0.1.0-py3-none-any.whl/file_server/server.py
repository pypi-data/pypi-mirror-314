import os
import sys

from flask import Flask, jsonify, render_template, request, send_from_directory


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


def getfile(sub_dir=""):
    root = os.getcwd().replace("\\", "/") + "/data/"
    res = {"dirs": [], "files": [], "cur": sub_dir}
    path = os.getcwd().replace("\\", "/") + "/data/" + sub_dir
    for item in os.scandir(path):
        if item.is_dir():
            res["dirs"].append((item.path.replace(root, ""), item.name))
        else:
            res["files"].append((item.path.replace(root, ""), item.name))
    return res


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload")
def upload_file():
    return render_template("upload.html")


@app.route("/uploader", methods=["POST"])
def upload_success():
    if request.method == "POST":
        f = request.files["file_data"]
        try:
            upload_path = "data/upload/"
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            f.save(upload_path + f.filename)
            return jsonify({"code": 200, "msg": "上传成功"})
        except Exception as e:
            return "请上传文件"


# 显示下载文件的界面
@app.route("/down/<path:sub_dir>", methods=["GET"])
def download_page_sub_dir(sub_dir=""):
    root = os.getcwd().replace("\\", "/") + "/data/"
    path = os.getcwd().replace("\\", "/") + "/data/" + sub_dir
    print(sub_dir)
    print(path)
    if os.path.isdir(path):
        res = {"dirs": [], "files": [], "cur": sub_dir}
        for item in os.scandir(path):
            if item.is_dir():
                res["dirs"].append((item.path.replace(root, ""), item.name))
            else:
                res["files"].append((item.path.replace(root, ""), item.name))
        return render_template("download.html", res=res)
    else:
        return send_from_directory(os.path.split(path)[0], os.path.split(path)[-1])


@app.route("/down/", methods=["GET"])
def download_page():
    if not os.path.exists("data"):
        os.mkdir("data")
    res = getfile()
    print(res)
    return render_template("download.html", res=res)


@app.route("/download_file/<path:sub_dir>", methods=["GET"])
def download_file(sub_dir):
    if request.method == "GET":
        path = os.getcwd().replace("\\", "/") + "/data/" + sub_dir
        return send_from_directory(
            os.path.split(path)[0], os.path.split(path)[-1], as_attachment=True
        )
