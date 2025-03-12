import json
from flask import Flask, request, redirect, make_response, render_template, url_for

app = Flask(__name__)

# Load TARGET_HOSTS from a JSON file
with open("config/target_hosts.json", "r") as file:
    TARGET_HOSTS = json.load(file)

@app.route('/', methods=["GET", "POST"], defaults={'path': ''})
@app.route('/<path:path>', methods=["GET", "POST"])
def handle_request(path):
    query_string = request.query_string.decode("utf-8")
    query_suffix = f"?{query_string}" if query_string else ""
    
    if request.method == "POST" and "inst" in request.form:
        inst = request.form["inst"]
        target = TARGET_HOSTS.get(inst, {})
        target_host = target.get("host")
        
        if not target_host:
            return "Invalid institution selected. Please try again.", 400
        
        url = f"{target_host}/{path}{query_suffix}"
        response = make_response(redirect(url))  # Redirect to target host
        
        if "remember" in request.form and request.form["remember"] == "savecookie":
            response.set_cookie("reshareInst", inst, max_age=3600)
        
        return response
    
    if 'reshareInst' not in request.cookies:
        return render_template('wayf.html', target_hosts=TARGET_HOSTS)

    inst = request.cookies.get("reshareInst")
    target = TARGET_HOSTS.get(inst, {})
    target_host = target.get("host")
    
    if not target_host:
        return "Invalid institution stored in cookies. Please select again.", 400
    
    # Ensure root URL also redirects to the target host
    if not path:
        return redirect(f"{target_host}{query_suffix}", code=302)
    
    url = f"{target_host}/{path}{query_suffix}"
    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
