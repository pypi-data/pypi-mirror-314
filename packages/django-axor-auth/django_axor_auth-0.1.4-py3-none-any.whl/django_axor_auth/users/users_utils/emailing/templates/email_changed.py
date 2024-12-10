from django_axor_auth.utils.emailing.base_template import base_template


def email_changed_template(first_name, url, email_subject='Email Changed Successfully!'):
    return base_template(
        subject=email_subject,
        headline="Your email was changed!",
        message=[
            'Hi ' + first_name + ',',
            'The change was successfully. Next step, use the button below to finish the verification process.',
            'If you did not make this change, please contact our support immediately.',
        ],
        button_text='Verify Email',
        button_link=url,
    )
