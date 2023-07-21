from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_mail(title, html_address, context, to_email):
    html_content = render_to_string(html_address,
                                    context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(title,
                                 text_content,
                                 to=[to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
