from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from .utils import time_ago


@login_required
def home(request):
    """Home page showing only APPROVED questions with strand=ALL."""
    questions = Question.objects.filter(status='APPROVED', strand='ALL')
    context = {
        'questions': questions,
        'page_title': 'Home',
    }
    return render(request, 'questions/home.html', context)


@login_required
def strands(request):
    """Strand selection page."""
    return render(request, 'questions/strands.html', {'page_title': 'Strands'})


@login_required
def strand_detail(request, strand):
    """Display questions for a specific strand."""
    if strand not in ['HUMSS', 'ABM', 'TVL', 'GAS']:
        messages.error(request, 'Invalid strand selected.')
        return redirect('questions:strands')
    
    questions = Question.objects.filter(status='APPROVED', strand=strand)
    context = {
        'questions': questions,
        'strand': strand,
        'page_title': f'{strand} Questions',
    }
    return render(request, 'questions/strand_detail.html', context)


@login_required
def question_detail(request, pk):
    """Question detail page with answers."""
    question = get_object_or_404(Question, pk=pk)
    
    # Only show approved questions to non-authors, or pending/rejected to author
    if question.status != 'APPROVED' and question.author != request.user:
        messages.error(request, 'This question is not available.')
        return redirect('questions:home')
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            messages.success(request, 'Your answer has been posted!')
            return redirect('questions:detail', pk=pk)
    else:
        form = AnswerForm()
    
    answers = question.answers.all()
    context = {
        'question': question,
        'answers': answers,
        'form': form,
        'page_title': question.title,
    }
    return render(request, 'questions/question_detail.html', context)


@login_required
def my_questions(request):
    """User's question history."""
    questions = Question.objects.filter(author=request.user)
    context = {
        'questions': questions,
        'page_title': 'My Questions',
    }
    return render(request, 'questions/my_questions.html', context)


@login_required
def ask_question(request):
    """Create a new question."""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Your question has been submitted and is pending approval.')
            return redirect('questions:my_questions')
    else:
        form = QuestionForm()
    
    return render(request, 'questions/ask_question.html', {'form': form, 'page_title': 'Ask a Question'})


@login_required
def edit_question(request, pk):
    """Edit a question (only by author)."""
    question = get_object_or_404(Question, pk=pk)
    
    if question.author != request.user:
        messages.error(request, 'You do not have permission to edit this question.')
        return redirect('questions:detail', pk=pk)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            # Reset status to PENDING after edit
            question = form.save(commit=False)
            question.status = 'PENDING'
            question.save()
            messages.success(request, 'Question updated and is pending approval again.')
            return redirect('questions:detail', pk=pk)
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'questions/edit_question.html', {'form': form, 'question': question, 'page_title': 'Edit Question'})


@login_required
def delete_question(request, pk):
    """Delete a question (only by author)."""
    question = get_object_or_404(Question, pk=pk)
    
    if question.author != request.user:
        messages.error(request, 'You do not have permission to delete this question.')
        return redirect('questions:detail', pk=pk)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('questions:my_questions')
    
    return render(request, 'questions/delete_question.html', {'question': question, 'page_title': 'Delete Question'})


@login_required
def reported_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # ✅ THIS IS THE KEY LINE YOU WERE MISSING
    question.is_reported = True
    question.save(update_fields=['is_reported'])

    messages.success(request, "Question has been reported.")
    return redirect('questions:detail', pk=pk)

