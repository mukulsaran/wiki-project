
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from . import util
from django import forms
import secrets
import markdown2


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-3 '}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-9','rows': 7 }))
    edit = forms.BooleanField(initial=False,widget=forms.HiddenInput(),required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    markdowner = markdown2.Markdown()
    titles = util.list_entries()
    if title not in titles:
         return render(request,"encyclopedia/error.html",{
             "title":title
         })
    else:
        return render(request,"encyclopedia/page.html",{
            "contents": markdowner.convert(util.get_entry(title)),
            "title": title,
        }) 


def search(request):
    value = request.GET["q"]
    for entries in util.list_entries():
        if(value.upper() == entries.upper()):
            value = entries
            return HttpResponseRedirect(reverse("page", kwargs={'title': value })) 
    
    subStringEntries = [] 
    for entry in util.list_entries():
        if value.upper() in entry.upper():
            subStringEntries.append(entry)
    
    return render(request, "encyclopedia/index.html",{
        "entries": subStringEntries,
        "search": True,
        "value": value
    }) 


def createNewPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            edit = form.cleaned_data["edit"]
            if util.get_entry(title) is None or edit is True:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("page", args=(title,)))
            else:
                return render(request,"encyclopedia/newPage.html",{
                    "form": form,
                    "existing":True,
                    "title":title
                })
        return render(request,"encyclopedia/newPage.html",{
            "form":form,
            "existing": False
        })
    return render(request,"encyclopedia/newPage.html",{
        "form": NewPageForm(),
        "existing": False,
    })


def edit(request,title):
    content = util.get_entry(title)
    if content is None:
        return render(request,"encyclopedia/error.html",{
            "title":title
        })
    else:
        form = NewPageForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = content
        form.fields["edit"].initial = True
        return render(request,"encyclopedia/newPage.html",{
            "form": form,
            "edit": form.fields["edit"].initial,
            "title":form.fields["title"].initial,
        })
    
def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("page",args=(randomEntry,)))
