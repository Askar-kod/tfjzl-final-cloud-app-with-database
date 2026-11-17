from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Submission, Choice, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        enrollment = Enrollment.objects.create(user=request.user, course=course)
        
    if request.method == 'POST':
        selected_ids = []
        for key, value in request.POST.lists():
            if key.startswith('choice_'):
                for val in value:
                    selected_ids.append(int(val))
        
        submission = Submission.objects.create(enrollment=enrollment)
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
        'total_score': total_score,
        'selected_ids': [c.id for c in submission.choices.all()],
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
