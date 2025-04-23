from django.shortcuts import render, redirect
from django.db import connections
from django.utils import timezone
# Create your views here.

def index(request):
    query = "SELECT id, task, description, completed  FROM Todo;"
    with connections['default'].cursor() as cursor:
        cursor.execute(query)
        todos_list = cursor.fetchall()


    # Convert raw SQL result to list of dicts
    todos = [
        {'id': row[0], 'task': row[1], 'description': row[2], 'completed': row[3]}
        for row in todos_list
    ]
    upcoming = [todo for todo in todos if not todo['completed']]
    completed = [todo for todo in todos if todo['completed']]

    return render(request, 'myApp/index.html', {
        'upcoming': upcoming,
        'completed': completed
    })

    #return render(request,'myApp/index.html')



def todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'
        created_at = timezone.now()

        query = """
            INSERT INTO Todo (task, description, completed, created_at)
            VALUES (%s, %s, %s, %s);
        """
        # Use raw SQL to insert the task into the ToDo table


        with connections['default'].cursor() as cursor:
            cursor.execute(query, [task, description, completed, created_at])

        return redirect('index')  # After creation, go to home

    return render(request, 'myApp/todo.html')

def update_tasks(request):
    if request.method == "POST":
        completed_ids = request.POST.getlist('completed_tasks')
        #completed_ids = [int(i) for i in completed_ids]

        with connections['default'].cursor() as cursor:
            query = "UPDATE Todo SET completed = TRUE WHERE id = %s;"
            for todo_id in completed_ids:
                cursor.execute(query, [todo_id])

    return redirect('index')

def delete_task(request, id):
    query = "DELETE FROM Todo WHERE id = %s;"
    with connections['default'].cursor() as cursor:
        cursor.execute(query, [id])
    return redirect('index')


def edit_task(request, id):
    if request.method == "POST":
        new_task = request.POST.get('task')
        new_description = request.POST.get('description')
        query = "UPDATE Todo SET task = %s, description = %s WHERE id = %s;"
        with connections['default'].cursor() as cursor:
            cursor.execute(query, [new_task,new_description, id])
        return redirect('index')
    else:
        query = "SELECT id, task, description, completed FROM Todo WHERE id = %s;"
        with connections['default'].cursor() as cursor:

            cursor.execute(query, [id])
            task = cursor.fetchone()

        task_dict = {
            'id': task[0],
            'task': task[1],
            'description': task[2],
            'completed': task[3],
            'created_at' : timezone.now()
        }

        return render(request, 'myApp/edit_task.html', {'task': task_dict})
        #return render(request, 'myApp/edit_task.html', {'task': task})






