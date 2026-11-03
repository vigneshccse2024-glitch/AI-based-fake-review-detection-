from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.models import Review
from app.services.predictor import metrics
admin_bp=Blueprint('admin', __name__, url_prefix='/admin')
def admin_required(f):
    @wraps(f)
    @login_required
    def wrapped(*a,**kw):
        if not current_user.is_admin: abort(403)
        return f(*a,**kw)
    return wrapped
@admin_bp.route('/')
@admin_required
def dashboard():
    reviews=Review.query.order_by(Review.created_at.desc()).all(); total=len(reviews); fake=sum(r.prediction=='Potentially Fake' for r in reviews)
    return render_template('admin.html', reviews=reviews[:10], total=total, fake=fake, genuine=total-fake, metrics=metrics())
