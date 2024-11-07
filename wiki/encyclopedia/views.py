from django.shortcuts import render, redirect

import random
import markdown2


from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
            })

    

def pages(request, page):
    y = util.get_entry(page)
    x = markdown2.markdown(y)

    if y == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/true_page.html", {
            "x":x, "page": page
        } )
    
def new_page(request):

    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        x = util.get_entry(title)
        if x is not None:
            return render(request, "encyclopedia/repeated_page.html")
        else:
            util.save_entry(title, content)
            url = reverse('pages', args=[title])
            return redirect(url)

        
def edit(request, page):
    if request.method == "GET":
        x = util.get_entry(page)
        return render(request, "encyclopedia/edit.html" ,{
            "x":x, "page":page
        })
    else:
        edited_content = request.POST["edited_content"]
        util.save_entry(page,edited_content)
        url = reverse('pages', args=[page])
        return redirect(url)
        



def random_page(request):
    list = util.list_entries()
    list_random = random.choice(list)
    url = reverse('pages', args=[list_random])
    return redirect(url)

def search(request):
    search_term = request.POST["q"]
    result = util.get_entry(search_term)
    if result != None:
        url = reverse('pages', args=[search_term])
        return redirect(url)
    lista = util.list_entries()
    search_result = []
    for palavra in lista:
        if search_term.lower() in palavra.lower():
            search_result.append(palavra)
    return render(request, "encyclopedia/search_result.html" ,{
        "search_result": search_result
    })



    





    

#list_entries
#save_entry
#get_entry
