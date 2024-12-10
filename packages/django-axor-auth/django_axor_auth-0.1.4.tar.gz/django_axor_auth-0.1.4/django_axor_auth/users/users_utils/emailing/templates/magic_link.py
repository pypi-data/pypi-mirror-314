from django_axor_auth.utils.emailing.base_template import base_template


def magic_link_template(first_name, url, email_subject):
    return base_template(
        subject=email_subject,
        headline="Your Sign In Link is Here",
        message=[
            'Hi ' + first_name + ',',
            'Use the link below to continue signing in.',
        ],
        button_text='Sign In',
        button_link=url,
    )
