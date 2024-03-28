from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text = models.TextField()

    def __str__(self):
        return self.question_text