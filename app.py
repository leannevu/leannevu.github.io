import os
from pathlib import Path

from flask import Flask, abort, redirect, send_from_directory, url_for

from projects.routes.analysis_productivity_routes import analysis_bp
from projects.routes.model_behavior_routes import model_behavior_bp
from projects.routes.my_dashboard_routes import newdashboard_bp
from projects.routes.optimization_routes import optimization_bp
from projects.routes.scrum_routes import scrum_bp


ROOT_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = ROOT_DIR / "projects"

app = Flask(
    __name__,
    static_folder=str(PROJECTS_DIR / "static"),
    static_url_path="/projects/static",
    template_folder=str(PROJECTS_DIR / "templates"),
)
app.secret_key = os.environ.get("STUDY_DASHBOARD_SECRET_KEY", "dev-only-change-me")

app.register_blueprint(optimization_bp, url_prefix="/projects/optimization")
app.register_blueprint(analysis_bp, url_prefix="/projects/analysis-productivity")
app.register_blueprint(scrum_bp, url_prefix="/projects/scrum")
app.register_blueprint(newdashboard_bp, url_prefix="/projects/study-vault")
app.register_blueprint(model_behavior_bp, url_prefix="/projects/model-behavior")


@app.get("/")
@app.get("/index.html")
def portfolio():
    return send_from_directory(ROOT_DIR, "index.html")


@app.get("/projects")
@app.get("/projects/")
def projects_index():
    return redirect(url_for("portfolio") + "#projects", code=302)


@app.get("/projects/study-dashboard")
def study_dashboard_alias():
    return redirect(url_for("newdashboard.index"), code=301)


@app.get("/blog")
@app.get("/blog/")
def blog_index():
    return send_from_directory(ROOT_DIR / "blog", "index.html")


LEGACY_PROJECT_PATHS = {
    "optimization": "optimization.optimization",
    "analysis-productivity": "analysis_productivity.analysis_productivity",
    "scrum": "scrum.scrum",
    "study-dashboard": "newdashboard.index",
    "my_dashboard": "newdashboard.index",
    "newdashboard": "newdashboard.index",
    "model-behavior": "model_behavior.model_behavior",
}


@app.get("/<project_name>")
def legacy_project_redirect(project_name):
    endpoint = LEGACY_PROJECT_PATHS.get(project_name)
    if endpoint:
        return redirect(url_for(endpoint), code=301)
    return _serve_public_file(project_name)


@app.get("/assets/<path:filename>")
def portfolio_assets(filename):
    return send_from_directory(ROOT_DIR / "assets", filename)


@app.get("/blog/<path:filename>")
def portfolio_blog(filename):
    return send_from_directory(ROOT_DIR / "blog", filename)


def _serve_public_file(filename):
    path = ROOT_DIR / filename
    allowed_suffixes = {".html", ".css", ".js"}
    if path.is_file() and path.suffix.lower() in allowed_suffixes:
        return send_from_directory(ROOT_DIR, filename)
    abort(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
