import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Document, TempEmail
from app.forms import UploadDocumentForm, ConvertPdfToWordForm
from app.utils import extract_text_from_pdf, extract_text_from_docx, summarize_text, convert_pdf_to_docx
from app.utils import generate_temp_email, clean_expired_emails

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = UploadDocumentForm()
    
    if form.validate_on_submit():
        file = form.document.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(file_path)
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            text = extract_text_from_docx(file_path)
        else:
            flash('Unsupported file format', 'danger')
            return redirect(url_for('main.index'))
        
        # Summarize the text
        summary = summarize_text(text, current_app.config['OPENAI_API_KEY'])
        
        # Save to database
        document = Document(filename=filename, file_path=file_path, summary=summary)
        db.session.add(document)
        db.session.commit()
        
        return redirect(url_for('main.summary', doc_id=document.id))
    
    return render_template('index.html', form=form, title='Sumzap - Document Summarizer')

@main.route('/summary/<int:doc_id>')
def summary(doc_id):
    document = Document.query.get_or_404(doc_id)
    return render_template('summary.html', document=document, title='Document Summary')

@main.route('/convert', methods=['GET', 'POST'])
def convert():
    form = ConvertPdfToWordForm()
    
    if form.validate_on_submit():
        file = form.pdf_file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        file.save(file_path)
        
        # Convert PDF to DOCX
        docx_path = convert_pdf_to_docx(file_path)
        
        # Provide download link
        return send_file(docx_path, as_attachment=True)
    
    return render_template('convert.html', form=form, title='PDF to Word Converter')

@main.route('/temp-email', methods=['GET', 'POST'])
def temp_email():
    # Clean expired emails
    clean_expired_emails()
    
    if request.method == 'POST':
        email, password = generate_temp_email()
        return render_template('temp_email.html', email=email, password=password, title='Temporary Email')
    
    return render_template('temp_email.html', title='Temporary Email')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500 
