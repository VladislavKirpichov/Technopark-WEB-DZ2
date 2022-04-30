from urllib import request
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic import ListView

from .models import Question, Answer, Profile, Tag


# Create your views here.

PAGINATION_SIZE = 10


def paginator(objects_list, request, per_page=20):
    pages = Paginator(objects_list, PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)

    return pages, page

def make_content(objects_list, request, per_page=20):
    pages, page = paginator(objects_list, request, per_page)

    content = {
        "paginator": pages,
        "page_content": page,
        "tags": Tag.objects.all().values()[:20]
    }

    return content


def index(request):
    return render(request, "index.html", make_content(Question.objects.all().values(), request))


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    qstn = Question.objects.get_question_by_id(i).values()
    if len(qstn) == 0:
        return HttpResponseNotFound("<h1>404 Page Not Found:(</h1>")

    answers, answer = paginator(Question.objects.get_question_answers(i).values(),
                                request, PAGINATION_SIZE)
    content = {
        "question": qstn[0],
        "paginator": answers,
        "answers": answer,
    }

    return render(request, "question_page.html", content)


def tag(request, tag: str):
    pages = paginator(Question.objects.get_questions_by_tag(tag).values(), PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page = pages.get_page(page_number)
    return render(request, "index.html", {"paginator": pages, "page_content": page})


def hot(request):
    return render(request, "index.html", {"page_content": list(Question.objects.get_popular())})


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "registration.html")

