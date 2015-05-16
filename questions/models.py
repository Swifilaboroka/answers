from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from polymorphic import PolymorphicModel

from core.utils import PathAndRename


class Category(MPTTModel):

    """Category Model"""

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    title = models.CharField(_("Category Title"), max_length=300, blank=False, help_text=_(
        "The category title as you want it displayed"))
    description = models.TextField(
        _("Description"), blank=True, help_text=_("A more detailed description of the category"))
    parent = TreeForeignKey("Category", blank=True, null=True, default=None,
                            verbose_name=_("Parent Category"), on_delete=models.PROTECT)
    active = models.BooleanField(_("Active"), default=True)
    # Sortable property
    order = models.PositiveIntegerField()

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        ordering = ['order']


class Quiz(models.Model):

    """A quiz is a collection os questions"""

    # ordering choices
    DATE_ORDER = '1'
    ALPHABETICAL_ORDER = '2'
    RANDOM_ORDER = '3'

    QUESTION_ORDERING_CHOICES = (
        (DATE_ORDER, _('Date')),
        (ALPHABETICAL_ORDER, _('Alphabetical')),
        (RANDOM_ORDER, _('Random')),
    )

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    title = models.CharField(_("Title"), max_length=300, blank=False)
    slug = AutoSlugField(populate_from='title', editable=True, unique=True, null=False, max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=_("Category"))
    description = models.TextField(
        _("Description"), blank=True, help_text=_("A more detailed description of the quiz"))
    question_ordering = models.CharField(
        _("Question Ordering"), max_length=1, choices=QUESTION_ORDERING_CHOICES, blank=False, default=ALPHABETICAL_ORDER, help_text=_("How should the questions in this quix be ordered?"))
    max_questions = models.PositiveIntegerField(
        blank=True, null=True, default=None, verbose_name=_("Max Questions"),
        help_text=_("Number of questions to be answered on each attempt."))
    answers_after_question = models.BooleanField(
        blank=False, default=False,
        help_text=_("Show answers after each question?"),
        verbose_name=_("Answers after question"))
    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=_("Show answers at the end of the whole quiz?"),
        verbose_name=_("Answers at end"))
    single_attempt = models.BooleanField(
        blank=False, default=False,
        help_text=_("If yes, only one attempt by"
                    " a user will be permitted."
                    " Non users cannot sit this exam."),
        verbose_name=_("Single Attempt"))
    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])
    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))
    fail_text = models.TextField(
        verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))
    draft = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Draft"),
        help_text=_("If yes, the quiz is not displayed"
                    " in the quiz list and can only be"
                    " taken by users who can edit"
                    " quizzes."))

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __unicode__(self):
        return self.title


class Question(PolymorphicModel):

    """
    Base class for all types of questions
    """

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    quiz = models.ManyToManyField(Quiz, verbose_name=_("Quiz"), blank=True)
    title = models.CharField(
        _("Question"), max_length=300, blank=False, help_text=_("The question as you want it displayed"))
    description = models.TextField(
        _("Description"), blank=True, help_text=_("A more detailed description of the question"))
    image = models.ImageField(_("Image"), upload_to=PathAndRename(
        "questions/"), blank=True, null=True, default=None)
    required = models.BooleanField(
        _("Required"), default=True, help_text=_("Is this question required?"))
    explanation = models.TextField(_("Explanation"), blank=True, help_text=_(
        "Explanation to be shown after the question has been answered"))
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=_("Category"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __unicode__(self):
        return self.title


class TextQuestion(Question):

    """A type of question that expects short text answers"""

    class Meta:
        verbose_name = _("Text Question")
        verbose_name_plural = _("Text Questions")

    def __unicode__(self):
        return self.title


class EssayQuestion(Question):

    """A type of question that expects essay type answers"""

    class Meta:
        verbose_name = _("Essay Question")
        verbose_name_plural = _("Essay Questions")

    def __unicode__(self):
        return self.title


class MultipleChoiceQuestion(Question):

    """
        A type of question where the user is presented with a list of options to pick from
        The choices themselves are MultipleChoiceAnswer objects
    """

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")

    def __unicode__(self):
        return self.title


class MultipleChoiceAnswer(models.Model):

    """The answer choices to a multipel choice question"""

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    question = models.ForeignKey(MultipleChoiceQuestion, verbose_name=_("Question"))
    title = models.CharField(_("Answer"), max_length=300, blank=False, help_text=_(
        "INput the answer as you want it displayed"))
    correct_answer = models.BooleanField(
        _("Correct Answer"), default=False, help_text=_("Is this a correct answer?"))

    class Meta:
        verbose_name = "Multiple Choice Answer"
        verbose_name_plural = "Multiple Choice Answers"

    def __unicode__(self):
        return self.title


class RatingQuestion(Question):

    """A question used to rate things from Very Poor/Very Bad to Very Good"""

    # choices
    # VERY_POOR = '1'
    # POOR = '2'
    # AVERAGE = '3'
    # GOOD = '4'
    # VERY_GOOD = '5'

    # RATING_CHOICES = (
    #     (VERY_POOR, _('Very Poor')),
    #     (POOR, _('Poor')),
    #     (AVERAGE, _('Average')),
    #     (GOOD, _("Good")),
    #     (VERY_GOOD, _("Very Good")),
    # )

    # choices = models.CharField(
    #     _("Rating Choices"), max_length=1, choices=RATING_CHOICES, blank=False)

    class Meta:
        verbose_name = _("Rating Question")
        verbose_name_plural = _("Rating Questions")

    def __unicode__(self):
        return self.title


class BooleanQuestion(Question):

    """A type of question where the user is expected to select from two options: True/False, Yes/No, etc"""

    true_label = models.CharField(_("True Label"), max_length=50, default=_(
        "True"), help_text=_("What will represent the True/Yes option"))
    false_label = models.CharField(_("False Label"), max_length=50, default=_(
        "False"), help_text=_("What will represent the False/No option"))
    correct_answer = models.NullBooleanField(_("Correct Answer"), blank=True, null=True, default=None, help_text=_(
        "Which is the correct answer to this question?"))

    class Meta:
        verbose_name = "Boolean Question"
        verbose_name_plural = "Boolean Questions"

    def __unicode__(self):
        return self.title
