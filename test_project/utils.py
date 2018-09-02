import jwt, time, requests, os, string, random, urllib.parse
from django.template.loader import render_to_string




CONSTANTS = {
    'MAILGUN': {
        'API_KEY': os.environ.get('MAILGUN_API_KEY'),
        'DOMAIN': 'theadvertisements.org'
    },
    'RECAPTCHA': {
        'SITE_KEY': os.environ.get('RECAPTCHA_SITE_KEY'),
        'SECRET_KEY': os.environ.get('RECAPTCHA_SECRET_KET')
    },
    'JWT_SECRET': os.environ.get('JWT_SECRET'),
    'EMAIL': 'noreply@theadvertisements.org',
    'URL': {
        'PROTOCOL': 'http',
        'HOSTNAME': 'localhost'
    }
}





def send_email(data):
    return requests.post(
        "https://api.mailgun.net/v3/{}/messages".format(CONSTANTS.get('MAILGUN').get('DOMAIN')),
        auth=("api", CONSTANTS.get('MAILGUN').get('API_KEY')),
        data=data
    )


def password_generator(size=8, chars=string.ascii_letters + string.digits):
    """
    Returns a string of random characters, useful in generating temporary
    passwords for automated password resets.

    size: default=8; override to provide smaller/larger passwords
    chars: default=A-Za-z0-9; override to provide more/less diversity

    Credit: Ignacio Vasquez-Abrams
    Source: http://stackoverflow.com/a/2257449
    """
    return ''.join(random.choice(chars) for i in range(size))

def get_confirm_email_html(team='Team The Advertisements', activation_link='', logo=''):
    return render_to_string('emails/confirm_email.html', {
        'activation_link': activation_link,
        'logo': logo,
        'team': team
    })

def get_reset_password_html(team='Team The Advertisements', activation_link='', logo=''):
    return render_to_string('emails/reset_password.html', {
        'activation_link': activation_link,
        'logo': logo,
        'team': team
    })


def send_confirm_email(payload, email):
    email_token = jwt.encode({'payload': payload, 'exp': time.time() + 10 * 60}, CONSTANTS.get('JWT_SECRET'), algorithm='HS256')

    activation_link = "{}://{}:8000/activate-email/{}".format(
        CONSTANTS.get('URL').get('PROTOCOL'),
        CONSTANTS.get('URL').get('HOSTNAME'),
        urllib.parse.quote_plus(email_token)
    )

    send_email({
        'from': CONSTANTS.get('EMAIL'),
        'to': email,
        'subject': 'Confirm your email',
        'html': get_confirm_email_html(activation_link=activation_link)
    })



def send_reset_password_email(payload, email):
    email_token = jwt.encode({'payload': payload, 'exp': time.time() + 10 * 60}, CONSTANTS.get('JWT_SECRET', 'hello'), algorithm='HS256')

    try:

        activation_link = "{}://{}:8000/reset-password/{}".format(
            CONSTANTS.get('URL').get('PROTOCOL'),
            CONSTANTS.get('URL').get('HOSTNAME'),
            "hello"
        )

        send_email({
            'from': CONSTANTS.get('EMAIL'),
            'to': email,
            'subject': 'Reset password',
            'html': get_reset_password_html(activation_link=activation_link)
        })
    except TypeError:
        pass