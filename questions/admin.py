from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin  # , PolymorphicChildModelAdmin

from questions.models import Quiz, Question, MultipleChoiceQuestion, MultipleChoiceAnswer
from questions.models import RatingQuestion, TextQuestion, EssayQuestion, BooleanQuestion


class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    pass


class MultipleChoiceAnswerAdmin(admin.ModelAdmin):
    pass


class RatingQuestionAdmin(admin.ModelAdmin):
    pass


class TextQuestionAdmin(admin.ModelAdmin):
    pass


class EssayQuestionAdmin(admin.ModelAdmin):
    pass


class BooleanQuestionAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    child_models = (
        (MultipleChoiceQuestion, MultipleChoiceQuestionAdmin),
        (RatingQuestion, RatingQuestionAdmin),
        (TextQuestion, TextQuestionAdmin),
        (EssayQuestion, EssayQuestionAdmin),
        (BooleanQuestion, BooleanQuestionAdmin),
    )

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceAnswer, MultipleChoiceAnswerAdmin)
admin.site.register(RatingQuestion, RatingQuestionAdmin)
admin.site.register(TextQuestion, TextQuestionAdmin)
admin.site.register(EssayQuestion, EssayQuestionAdmin)
admin.site.register(BooleanQuestion, BooleanQuestionAdmin)
