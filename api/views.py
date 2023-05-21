from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics,status
from .models import Submission
from .serializers import SubmissionCreateSerializer
import subprocess

@api_view(['GET'])
def getData(request):
    Problem = {
                'Problem':{
                    'code':'A',
                    'problem':'sum x+y',
                    'time_limit':'1s',
                },
                'Problem':{
                    'code':'B',
                    'problem':'Fibonacci',
                    'time_limit':'1s',
                },
              }
    return Response(Problem)


def compare_outputs(user_output_file, problem_output_file):
    with open(user_output_file, 'r') as user_file, open(problem_output_file, 'r') as problem_file:
        user_output = user_file.read().strip()
        problem_output = problem_file.read().strip()
        if user_output == problem_output:
            return "AC"
        else:
            return "WA"

class SubmissionCreate(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Compilation du fichier C/C++
        submission = serializer.instance
        source_code = submission.code
        language = submission.language
        compiled_file = 'tp'

        if language in ['c', 'cpp']:
            if language == 'c':
                with open('code.c', 'w') as file:
                    file.write(source_code)
                compiler_cmd = ['gcc', '-o', compiled_file,'code.c']
            else:  # cpp
                with open('code.cpp', 'w') as file:
                    file.write(source_code)
                compiler_cmd = ['g++', '-o', compiled_file, 'code.cpp']

            compilation_process = subprocess.run(
                compiler_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if compilation_process.returncode != 0:
                # La compilation a échoué
                error_message = compilation_process.stderr.decode('utf-8')
                submission.compilation_error = error_message
                submission.save()
                return Response({'detail': 'Compilation error', 'error_message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            with open('code_1.py', 'w') as file:
                file.write(source_code)

            compiled_file='code_1.py'
        # Exécution du fichier compilé avec les entrées de problème
        problem = submission.problem
        input_file = problem.input_file.path
        output_file = 'media/output_files/output.txt'
        time_limit = problem.time_limit

        execution_cmd = [compiled_file]
        execution_process = subprocess.run(
            execution_cmd,
            stdin=open(input_file, 'r'),
            stdout=open(output_file, 'w'),
            timeout=time_limit
        )

        if execution_process.returncode != 0:
            # L'exécution a échoué (Time Limit Exceeded)
            submission.execution_error = 'TLE'
            submission.save()
            return Response({'detail': 'Execution error', 'error_message': 'TLE'}, status=status.HTTP_400_BAD_REQUEST)

        # Comparaison des fichiers de sortie
        problem_output_file = problem.output_file.path
        result = compare_outputs(output_file, problem_output_file)

        submission.output_file = output_file
        submission.result = result
        submission.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
