from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class UploadDocumentForm(FlaskForm):
    document = FileField('Upload Document', 
                        validators=[
                            FileRequired(),
                            FileAllowed(['pdf', 'doc', 'docx'], 'PDF and Word documents only!')
                        ])
    submit = SubmitField('Upload and Summarize')

class ConvertPdfToWordForm(FlaskForm):
    pdf_file = FileField('Upload PDF', 
                       validators=[
                           FileRequired(),
                           FileAllowed(['pdf'], 'PDF files only!')
                       ])
    submit = SubmitField('Convert to Word') 
