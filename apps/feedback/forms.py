# apps/feedback/forms.py
from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(choices=Feedback.RATING_CHOICES),
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Share your thoughts...",
                    "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                }
            ),
        }
