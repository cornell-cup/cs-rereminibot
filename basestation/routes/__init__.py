from .index_routes import index_bp

def init_app(app):
    app.register_blueprint(index_bp)
