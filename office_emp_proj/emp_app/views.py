from django.shortcuts import render,HttpResponse
from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q
# Create your views here.
def index(request):
  return render(request,'index.html')

def all_emp(request):
  emps = Employee.objects.all()
  context = {
        'emps' : emps
  }
  print(context)
  return render(request,'all_emp.html',context)
def add_emp(request):
    if request.method == 'POST':
        # Correctly access POST data using [] brackets
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])

        # Create and save the new employee
        new_emp = Employee(
            firstname=firstname, 
            lastname=lastname, 
            salary=salary, 
            phone=phone, 
            dept_id=dept, 
            role_id=role, 
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse('Employee added successfully')

    elif request.method == 'GET':
        return render(request, 'add_emp.html')

    else:
        return HttpResponse('An Exception Occurred! Employee has not been added.')


def remove_emp(request,emp_id = 0):
  if emp_id:
     try:
        emp_to_be_removed= Employee.objects.get(id = emp_id)
        emp_to_be_removed.delete()
        return HttpResponse("Employee Removed Successfully ")
     except:
        return HttpResponse("Please enter a valid emp id ")
  emps = Employee.objects.all()
  context = {
        'emps' : emps
  }
  print(context)
  return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        emps = Employee.objects.all()

        # Apply filters based on user input
        if name:
            emps = emps.filter(Q(firstname__icontains=name) | Q(lastname__icontains=name))
        if dept:
            emps = emps.filter(dept__name=dept) 
        if role:
            emps = emps.filter(role__name=role) 
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
       return HttpResponse('An error Occured!!')
