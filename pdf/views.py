from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io 
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm


    def get_success_url(self):
        return reverse("login")





def accept(request):

    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")

        profile = Profile(name=name,
                          email=email,
                          phone=phone,
                          summary=summary,
                          degree=degree,
                          school=school,
                          university=university,
                          previous_work=previous_work,
                          skills=skills)
        profile.save()

    return render(request,"pdf/accept.html")


@login_required(login_url="login")
def resume(request,id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template("pdf/resume.html")
    html = template.render({"user_profile" : user_profile})
    options = {
        "page-size" : "Letter",
        "encoding" : "UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options)

    response = HttpResponse(pdf,content_type="application/pdf")
    response["Content-Disposition"] = "attachment"
    filename = "resume.pdf"

    return response

@login_required(login_url="login")
def list(request):
    profiles = Profile.objects.all()
    return render(request, "pdf/list.html",{"profiles":profiles})
