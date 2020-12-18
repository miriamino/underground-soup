from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import pandas as pd
import numpy as np

from .models import Question, Choice, Answer, User, Matching
from .matching import update_matches


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'dating/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:100]

class QuestionSelfView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'dating/detail_self.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class QuestionOtherView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'dating/detail_other.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ProfileViewSelf(LoginRequiredMixin, generic.ListView):
    model = Answer
    template_name = "dating/profile_self.html"

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)

class MatchesView(LoginRequiredMixin, generic.ListView):
    model = Matching
    template_name = "dating/potential_matches.html"
    context_object_name = "matches"

    def get_queryset(self):
        return Matching.objects.filter(user=self.request.user)

@login_required
def profile_other(request, username):
    user_id = User.objects.get(username=username)
    answer_list = get_list_or_404(Answer.objects.filter(user=user_id.pk))
    score = get_object_or_404(Matching.objects.filter(user=request.user.pk, other_user=user_id.pk))
    username = username
    print(score.forward_score)
    return render(request, 'dating/profile_other.html', { 'answer_list': answer_list, 'score' : score, 'username': username})

@login_required
def vote_self(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    if request.POST.get('private') == 'private':
        public = False
    else:
        public = True
    answer, created = Answer.objects.update_or_create(
        user=request.user,
        question=question,
        defaults={ 
            'public_self' : public, 
            'answer_self' : selected_choice },
    )
    redirect_url = reverse('dating:detail_other', args=[question.id])
    return HttpResponseRedirect(redirect_url)

@login_required
def vote_other(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    importance = request.POST.get('importance')
    choicelist = request.POST.getlist('choice')
    if request.POST.get('private') == 'private':
        public = False
    else:
        public = True
    answer, created = Answer.objects.update_or_create(
                user=request.user,
                question=question,
                defaults= { 
                    'public_other' : public,
                    'importance' : importance,
                    }
            )
    answer.answer_other.clear()
    for c in choicelist:
        answer.answer_other.add(question.choice_set.get(pk=c))
    redirect_url = reverse('dating:index')
    return HttpResponseRedirect(redirect_url)


