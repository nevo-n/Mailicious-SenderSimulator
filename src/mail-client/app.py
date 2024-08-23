import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import mimetypes
from email import encoders
from email.mime.base import MIMEBase

app = Flask(__name__)
CORS(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    sender = request.form['sender']
    receiver = request.form['receiver']
    subject = request.form['subject']
    content = request.form['content']
    file = request.files.get('attachment')

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    # Attach the file, if provided
    if file:
        # Read the file content and attach it
        mime_type, encoding = mimetypes.guess_type(file.filename)
        part = MIMEBase(mime_type.split('/')[0],mime_type.split('/')[1])
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file.filename}')
        msg.attach(part)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('localhost', 25) as server:
            # server.starttls()  # Uncomment if server supports TLS
             server.sendmail(sender, receiver, msg.as_string())
        return jsonify({'success': True, 'message': 'Email sent!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

