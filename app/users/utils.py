import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_login import current_user
#import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email
import cloudinary.uploader


def get_public_id_from_url(url):
    # Remove query params if any
    url = url.split('?')[0]
    # Split by /upload/ and take the second part
    try:
        path_after_upload = url.split('/upload/')[1]
        # Remove file extension
        public_id = os.path.splitext(path_after_upload)[0]
        return public_id
    except IndexError:
        return None




def save_pic(form_pic):
    default_url='https://res.cloudinary.com/dpqj7lbrj/image/upload/v1758270767/default_zb1f4a.jpg'
    result= cloudinary.uploader.upload(form_pic,
                                       folder='profile_pics',
                                       transformation=[{'width':125,'height':125,'crop':'fill'}])
    

    if current_user.image_file and current_user.image_file != default_url:
        public_id=get_public_id_from_url(current_user.image_file)
        if public_id:
            try:
                cloudinary.uploader.destroy(public_id=public_id)
            except Exception as e:
                raise e

    return result['secure_url']





def send_email(user):
    
    token = user.get_reset_token()
    reset_url = url_for('users.reset_password', token=token, _external=True)

    message = Mail(
        from_email= Email(os.environ.get('VERIFIED_SENDER_EMAIL'),'Flask Reset Password'),
        to_emails=user.email,
        subject='Password Reset Request',
        html_content=f'''<p>To reset your password, visit the following link:</p>
        <p><a href= "{reset_url}">{reset_url}</a></p>
        <p>If you did not make this request, simply ignore this email.</p>''')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        sg.send(message)
    except Exception as e:
        raise e 
    






#def send_email(user):
#    """Send email using SendGrid API instead of SMTP"""
#    try:
#        token = user.get_reset_token()
#        
#        # SendGrid API endpoint
#        url = "https://api.sendgrid.com/v3/mail/send"
#        
#        # Get environment variables
#        api_key = os.environ.get('SENDGRID_API_KEY')
#        from_email = os.environ.get('VERIFIED_SENDER_EMAIL')
#        
#        if not api_key:
#            raise ValueError("SendGrid API key not found in environment variables")
#        
#        # Email data
#        data = {
#            "personalizations": [
#                {
#                    "to": [{"email": user.email}],
#                    "subject": "Password Reset Request"
#                }
#            ],
#            "from": {"email": from_email},
#            "content": [
#                {
#                    "type": "text/plain",
#                    "value": f"""To reset your password, visit the following link:
#{url_for('users.reset_password', token=token, _external=True)}
#
#If you did not make this request then simply ignore this email and no changes will take place!
#"""
#                }
#            ]
#        }
#        
#        # Headers
#        headers = {
#            "Authorization": f"Bearer {api_key}",
#            "Content-Type": "application/json"
#        }
#        
#        # Send the request
#        response = requests.post(url, json=data, headers=headers, timeout=30)
#        
#        if response.status_code == 202:
#            print(f"Email sent successfully to {user.email}")
#            return True
#        else:
#            print(f"Failed to send email. Status: {response.status_code}, Response: {response.text}")
#            raise Exception(f"SendGrid API returned status {response.status_code}")
#            
#    except Exception as e:
#        print(f"Failed to send email: {str(e)}")
#        current_app.logger.error(f"Email sending failed: {str(e)}")
#        raise e
