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
            phone = request.POST.get('phone', None)
            Subject = request.POST.get('subject', None)
            Message = request.POST.get('message', None)

            if FullName and Email_ID and phone and Subject and Message:

                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                if not(re.search(regex,Email_ID)):
                    dicts = {'message': "Please enter valid email address!"}
                    return render(request,'index.html',{'dict':dicts['message']})
                    # form_error = True
                    # messages.error(request, "Please enter valid email address!")
                
                else:
                    if not(form_error):
                        visitor = visitorquery(name = FullName,email = Email_ID,phone = phone, subject = Subject, message = Message)
                        visitor.save()

                        email_text = '<p>Name : {}</p>'.format(FullName)
                        email_text += '<p>Email : {}</p>'.format(Email_ID)
                        email_text += '<p>Phone : <a href="tel:{}">{}</a></p>'.format(phone,phone)
                        email_text += '<p>Subject : {}</p>'.format(Subject)
                        email_text += '<p>Message : {}</p>'.format(Message)
                        
                        email_textc ='<p>Thank You {}</p>'.format(FullName)
                        email_textc += '<p>I will contact you shortly. when you feel free you can contact me on given number <a href="tel:9586549727">9586549727</a><br/><br/>Thanks & Regards,<br/>Harsh Vekariya</p>'

                        recipientsc = [visitor.email]
                        recipients = ["vekariyaharsh01@gmail.com"]
                        msg = MIMEText(email_text, 'html')
                        msgc = MIMEText(email_textc, 'html')
                        msg["Subject"] = "Harsh Portfolio"
                        msgc["Subject"] = "Harsh Vekariya"
                        msg["From"] = visitor.email

                        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        smtp_server.login("vekariyaharsh01@gmail.com", "vpzzirbsyaffawhr")
                        smtp_server.sendmail("vekariyaharsh01@gmail.com", recipients, msg.as_string())
                        smtp_server.sendmail(visitor.email, recipientsc, msgc.as_string())
                        smtp_server.quit()
                        return redirect('Portfolio_app:home_view')
            else:
                dicts = {'message': "All fields are  required.."}
                return render(request,'index.html',{'dict':dicts['message']})

 