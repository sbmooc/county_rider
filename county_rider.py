from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
import yaml

app = Flask(__name__)

def collect_config(path: str):

    with open(path, 'r') as hdl:
       config = yaml.safe_load(hdl)

    return config

config = collect_config('config.yaml')
client_id = config['client_id']
client_secret = config['client_secret']
authorization_base_url = 'https://www.strava.com/oauth/authorize'
token_url = 'https://www.strava.com/oauth/token'
root_url = 'https://www.strava.com/api/v3'


@app.route("/county_map", methods=['GET'])
def collect_activities():

    strava = OAuth2Session(client_id, token=session['oauth_token'])

    return jsonify(strava.get(f'{root_url}/athlete').json())


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    strava = OAuth2Session(client_id, redirect_uri='http://localhost:5000/callback')
    authorization_url, state = strava.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    code = request.args.get('code')

    strava = OAuth2Session(client_id=client_id,
                           state=session['oauth_state'])

    token = strava.fetch_token(token_url,
                               code=code,
                               client_secret=client_secret,
                               )

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.

    session['oauth_token'] = token
    #
    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    strava = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(strava.get('https://www.strava.com/api/v3/athlete').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host='localhost', debug=True)


