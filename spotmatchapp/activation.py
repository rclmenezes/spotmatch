# Adapted from http://codingnstuff.com/2010/01/create-your-user-management-frontend-in-django/

from django.core.mail import send_mail
from hashlib import md5
from django.template import loader, Context
import time
 
def send_activation(user):
    time.sleep(5) # makes email wait
    code = md5(user.username).hexdigest()
    url = "http://spotmatch.rmenez.es/activate/?user=%s&code=%s" % (user.username,  code)
    template = loader.get_template('activation.html')
    context = Context({
        'username': user.username, 
        'url': url, 
    })
 
    send_mail('Activate account at super site', template.render(context), 'no-reply@example.com', [user.email])