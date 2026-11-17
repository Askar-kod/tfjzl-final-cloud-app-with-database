from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        selected_ids = []
        for key, value in request.POST.lists():
            if key.startswith('choice_'):
                for val in value:
                    selected_ids.append(int(val))
        
        # Создаем сабмит и привязываем выбранные варианты ответов
        submission = Submission.objects.create(enrollment_id=1) # или корректный enrollment
        submission.choices.set(selected_ids)
        submission.save()
        
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    score = 0
    total_score = 0
    
    for question in course.question_set.all():
        total_score += question.grade
        selected_choices = submission.choices.filter(question=question)
        selected_ids = [c.id for c in selected_choices]
        if question.is_get_score(selected_ids):
            score += question.grade
            
    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'total_score': total_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
