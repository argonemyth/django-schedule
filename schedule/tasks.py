from time import sleep
import smtplib
from pynliner import Pynliner

from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from celery import task

class NoContent(Exception):
    """
    Will raise when there is there is no text or html content.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def render_email(context, text_template, html_template=None):
    """
    Render a email given by the template name
    """
    try:
        t = loader.get_template(text_template)
        text_content = t.render(context)
    except TemplateDoesNotExist:
        text_content = None

    if html_template:
        try:
            html_content = Pynliner().from_string(
                render_to_string(html_template, context)).run()
        except TemplateDoesNotExist:
            html_content = None
    else:
        html_content = None

    if not text_content and not html_content:
        #print "None of the following two templates are found: %s and %s" % (text_template, html_template)
        raise NoContent("None of the following two templates are found: %s and %s" % (text_template, html_template))

    return text_content, html_content


@task()
def send_emails(event):
    """
    The task sends update email to all the users who reserved for the event.
    html_template, text_template = email.newsletter.get_templates()
    """
    print "Going to sent event update emails."
    sender = 'hello@mpython.org' 
    subject = 'Updates for %s' % event.title
    text_template = "emails/event_update.txt"
    html_template = "emails/event_update.html"

    for user in event.get_reservations():
        # Construct the email
        email_context = Context({'event': event,
                                 'site': Site.objects.get_current(),
                                 'recipient': user.profile.get_full_name_or_username })
        text_content, html_content = render_email(email_context,
                                                  text_template,
                                                  html_template)
        if html_content:
            msg = EmailMultiAlternatives(subject, text_content, 
                                         sender, [user.email])
            msg.attach_alternative(html_content, "text/html")
        else:
            msg = EmailMessage(email.subject, text_content, sender,
                              [user.email])

        try:
            msg.send()
            #blast_logger.info(to_email.infoValue + " - Email Sent")
            print "Update Email Sent to %s" % user.email
            sleep(20)
        except Exception as e:
            #blast_logger.error("%s - Unknown Failer %s" % (to_email.infoValue, e))
            print "Update Email sending failure - %s" % (user.email,)


    print 'Update emails all sent.'
    
    return True
