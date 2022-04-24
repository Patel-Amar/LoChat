from flask import Flask, request, g, render_template
from blueprints.register import register as register_blueprint
from blueprints.auth import auth as auth_blueprint
from blueprints.home import home as home_blueprint
from blueprints.communities import communities as communities_blueprint
from blueprints.about import about as about_blueprint
from blueprints.account_settings import account_settings as account_settings_blueprint

app = Flask( __name__ )
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Blueprints
app.register_blueprint( register_blueprint )
app.register_blueprint( auth_blueprint )
app.register_blueprint( home_blueprint )
app.register_blueprint( communities_blueprint )
app.register_blueprint( about_blueprint )
app.register_blueprint( account_settings_blueprint )
