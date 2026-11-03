import csv, io
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from app import db
from app.models import Review
from app.services.predictor import predict

main_bp=Blueprint('main', __name__)
@main_bp.route('/')
def index(): return render_template('index.html')
@main_bp.route('/about')
def about(): return render_template('about.html')
@main_bp.route('/contact')
def contact(): return render_template('contact.html')
@main_bp.route('/detect', methods=['GET','POST'])
@login_required
def detect():
    result=None
    if request.method=='POST':
        text=request.form.get('review_text','').strip()
        if len(text)<5: flash('Please enter at least 5 characters.', 'danger')
        else:
            try:
                label, confidence, explanation = predict(text)
                review=Review(user_id=current_user.id,text=text,prediction=label,confidence=confidence,explanation='; '.join(explanation)); db.session.add(review); db.session.commit()
                result={'label':label,'confidence':round(confidence*100,2),'explanation':explanation,'text':text}
            except FileNotFoundError as e: flash(str(e),'warning')
    return render_template('detect.html', result=result)
@main_bp.route('/history')
@login_required
def history(): return render_template('history.html', reviews=Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all())
@main_bp.route('/history.csv')
@login_required
def history_csv():
    out=io.StringIO(); w=csv.writer(out); w.writerow(['Review ID','Review Text','Prediction','Confidence','Created At'])
    for r in Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()): w.writerow([r.id,r.text,r.prediction,f'{r.confidence:.4f}',r.created_at.isoformat()])
    return Response(out.getvalue(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=review_history.csv'})
