from django.shortcuts import redirect, render
from Portfolio_app.models import *
from django.views.generic import TemplateView
from django.contrib import messages
from django.template.loader import render_to_string
import os, re
from email.mime.text import MIMEText
import smtplib



# Create your views here.


class home_view(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if request.method == 'POST':
            form_error = False
            FullName = request.POST.get('name', None)
            Email_ID = request.POST.get('email', None)
            Subject = request.POST.get('subject', None)
            Message = request.POST.get('message', None)


            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            

            if FullName in ['', None] or Subject in ['', None] or Message in ['', None]:
                messages.error(request, "All fields are  required..")
                form_error = True
                

            else:

                if not(re.search(regex,Email_ID)):
                    form_error = True
                    messages.error(request, "Please enter valid email address!")
                
                else:
                    if not(form_error):
                        visitor = visitorquery(name = FullName,email = Email_ID, subject = Subject, message = Message)
                        visitor.save()
                        print(visitor,'----------------')

                        email_text = f"""
                        name : {FullName}
                        email : {Email_ID}
                        Subject : {Subject}
                        Message : {Message}"""

                        email_textc = f"""
                        Thank you {FullName}
                        I will contact you shortly
                        Regards,
                        Harsh Vekariya"""

                        recipientsc = [visitor.email]
                        recipients = ["vekariyaharsh01@gmail.com"]
                        msg = MIMEText(email_text)
                        msgc = MIMEText(email_textc)
                        msg["Subject"] = "Harsh Portfolio"
                        msgc["Subject"] = "Harsh Vekariya"
                        msg["From"] = visitor.email

                        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        smtp_server.login("vekariyaharsh01@gmail.com", "vpzzirbsyaffawhr")
                        smtp_server.sendmail("vekariyaharsh01@gmail.com", recipients, msg.as_string())
                        smtp_server.sendmail(visitor.email, recipientsc, msgc.as_string())
                        smtp_server.quit()
                        return redirect('Portfolio_app:home_view')

 