from functools import partial

from flask import Flask, current_app
import requests
from lxml import etree
import flask.cli
import logging

# do not show werkzeug logs
log = logging.getLogger('werkzeug')
log.disabled = True
flask.cli.show_server_banner = lambda *args: None

app = Flask(__name__)

@app.route('/')
def welcome():
    return "PyPI Proxy to filter requests to pypi site. Try /simple", 200, {"Content-Type": "text/html"}

@app.route('/simple')
def simple():
    url = current_app.config["PYPI_SERVER_URL"]
    atags, html_root = read_url_links(url)
    pypi_packages = set()
    for x in atags:
        package_name = x.attrib["href"].strip('/').split('/')[-1]
        pypi_packages.add(package_name)
        x.attrib["href"] = f"/simple/{package_name}"
    current_app.pypi_packages = pypi_packages
    return etree.tostring(html_root, encoding=str), 200, {"Content-Type": "text/html"}


def read_url_links(url):
    content_html = requests.get(url).text
    # replace malformed <br> tags, without this they would get stripped out
    content_html = content_html.replace('</br>', '<br>')
    parser = etree.HTMLParser()
    html_root = etree.fromstring(content_html, parser)
    atags = html_root.findall(".//a")
    return atags, html_root


@app.route('/simple/<package>/')
def package(package):
    if not hasattr(current_app, "pypi_packages"):
        simple()
    if package not in current_app.pypi_packages:
        return "Package not found", 404, {"Content-Type": "text/plain"}

    url = f"{current_app.config['PYPI_SERVER_URL']}/{package}"
    atags, html_root = read_url_links(url)
    for x in atags:
        x.attrib["href"] = f"/simple/{package}/{x.attrib['href'].split('/')[-1]}"
    return etree.tostring(html_root, encoding=str), 200, {"Content-Type": "text/html"}

@app.route('/simple/<package>/<path:subpath>')
def package_version(package, subpath):
    if not hasattr(current_app, "pypi_packages"):
        simple()
    if package not in current_app.pypi_packages:
        return "Package not found", 404, {"Content-Type": "text/plain"}

    # on github pages, packages are on the same level as 'simple'
    # and PYPI_SERVER_URL ends with 'simple', that's why /../ is needed
    url = f"{current_app.config['PYPI_SERVER_URL']}/../{subpath}"
    resp = requests.get(url)
    return resp.content, resp.status_code, {"Content-Type": resp.headers.get("Content-Type")}

def run(pypi_server_url):
    app.config["PYPI_SERVER_URL"] = pypi_server_url
    app.run(host="127.0.0.1", port=4549, debug=False)

_pypi_proxy_thread = None

def start_pypi_proxy(pypi_server_url):
    global _pypi_proxy_thread
    if not _pypi_proxy_thread:
        import threading
        _pypi_proxy_thread = threading.Thread(target=partial(run, pypi_server_url), daemon=True)
        _pypi_proxy_thread.start()


if __name__ == '__main__':
    run("https://oarepo.github.io/pypi/packages/simple")