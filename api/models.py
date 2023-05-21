from django.db import models

class Problem(models.Model):
    code = models.CharField(max_length=10, unique=True)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    input_file = models.FileField(upload_to='input_files/')
    output_file = models.FileField(upload_to='output_files/')

class Submission(models.Model):
    user = models.CharField(max_length=100)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    code = models.TextField()
    compilation_error = models.TextField(blank=True, null=True)
    execution_error = models.TextField(blank=True, null=True)
    output_file = models.FileField(blank=True, null=True)
    result = models.CharField(max_length=2, blank=True, null=True)
