from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from answers.models import Answer


class ReviewMixin(object):
    """
    Control who can take a peer review
    """

    def dispatch(self, *args, **kwargs):
        review = self.get_object()
        # dont allow a non reviewer to review
        if review.reviewers.all() and (self.request.user.userprofile not in review.reviewers.all()):
            messages.add_message(
                self.request, messages.WARNING, _('Sorry, you do not have access to that section'))
            return redirect('dashboard')
        # not more than one reviews
        if review.quiz.single_attempt and Answer.objects.filter(userprofile=self.request.user.userprofile).filter(review=review).exists():
            messages.add_message(
                self.request, messages.WARNING, _("You can only review once"))
            return redirect('dashboard')
        return super(ReviewMixin, self).dispatch(*args, **kwargs)
