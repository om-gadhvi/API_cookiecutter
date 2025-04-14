from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def students(request):
    student=[
            {'student_id' : 1,
            'name' : 'Om Gadhvi',
            'age' : 20},
            
            {'student_id' : 2,
            'name' : 'Sanchay',
            'age' : 22} 
        
    ]
    
    
    return HttpResponse(student)