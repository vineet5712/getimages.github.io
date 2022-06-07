from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from python_test.models import Student
# Create your views here.
def studentinfo(request):
    stud = Student.objects.all()
    print("Myoutput",stud)
    return render(request,'enroll/studetails.html',{'stu': stud})
