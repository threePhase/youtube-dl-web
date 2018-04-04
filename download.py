import pprint
from flask import Flask, request
app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)

@app.route('/', methods=['GET'])
def help():
    man = ('<pre><code>'
           '{}: youtube-dl as a service\n'
           'POST outputDir [provider] [username] [password] url'
           '</code></pre>'
          ).format(__name__)
    return man

@app.route('/', methods=['POST'])
def download():
    return pp.pformat(request.form)
