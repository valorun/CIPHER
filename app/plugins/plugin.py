from flask import Blueprint, render_template
from app.model import config

class Plugin():
    def __init__(self, name, import_name, label, icon):
        self.plugins = {}
        self.name = name
        self.label = label
        self.icon = icon
        self.blueprint = Blueprint(name, import_name, static_folder='static', static_url_path='/'+name+'/static', template_folder='templates')

    def register(self, app, plugins):
        self.plugins=plugins
        app.register_blueprint(self.blueprint)

    def render_page(self, template_name_or_list, **context):
        return render_template(template_name_or_list, plugins=self.plugins, label=self.label, icon=self.icon, robot_name=config.getRobotName(), **context)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.blueprint.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def __repr__(self):
        return '<Plugin %r>' % self.name