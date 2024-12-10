from django_axor_auth.utils.emailing.base_template import base_template


def email_verification_template(first_name, url, email_subject='Verify your Email!'):
    return base_template(
        subject=email_subject,
        headline="Verify your Email!",
        message=[
            'Hi ' + first_name + ',',
            'Please use the below button to verify your email.',
        ],
        button_text='Verify Email',
        button_link=url,
    )
