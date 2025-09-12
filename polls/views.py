from django.contrib import messages
from django.db.models import QuerySet, F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from polls.models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    def get_queryset(self) -> QuerySet:  # در صفحه با question_list در دسترس هست
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
class DetailView(generic.DetailView):
    model = Question  # در صفحه با question در دسترس هست
    template_name = 'polls/detail.html'
# def detail(request, pk):
#     question: Question = get_object_or_404(Question, pk=pk)
#     choices: QuerySet[Choice] = question.choice_set.all()
#     context = {
#         'question': question,
#         'choices': choices,  # اینجوری اتوکامپلیت کار می کنه
#     }
#     return render(request, 'polls/detail.html', context)

def vote(request, pk):
    question: Question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if not choice_id:
            messages.error(request, "You didn't select a choice")
            return redirect('polls:detail', pk=question.pk)
        else:
            try:
                selected_choice = question.choice_set.get(pk=choice_id)
            except Choice.DoesNotExist:
                messages.error(request, "Invalid choice")
                return redirect('polls:detail', pk=question.pk)

            selected_choice.votes = F('votes') + 1
            selected_choice.save()
            messages.success(request, "Your vote was recorded!")
            return redirect('polls:results', pk=question.pk)
    else:
        return render(request, 'polls/detail.html', {
            'question': question,
            'choices': question.choice_set.all()
        })

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# def results(request, pk):
#     question: Question = get_object_or_404(Question, pk=pk)
#     choices: QuerySet[Choice] = question.choice_set.all()
#     context = {
#         'question': question,
#         'choices': choices,
#     }
#     return render(request, 'polls/results.html', context)
