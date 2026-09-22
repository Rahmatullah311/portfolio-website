# apps/feedback/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse
from .models import Feedback
from .forms import FeedbackForm


def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            content_type_id = request.POST.get("content_type_id")
            object_id = request.POST.get("object_id")

            content_type = get_object_or_404(ContentType, id=content_type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)

            feedback = form.save(commit=False)
            feedback.content_type = content_type
            feedback.object_id = object_id
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()

            messages.success(request, "Thank you for your feedback!")

            # Redirect back to the content detail page
            if hasattr(content_object, "get_absolute_url"):
                return redirect(content_object.get_absolute_url())
            else:
                return redirect("/")
        else:
            messages.error(request, "Please correct the errors below.")

    # If not POST or form invalid, redirect to home
    return redirect("/")
