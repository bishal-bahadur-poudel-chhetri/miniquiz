from django.shortcuts import render
from miniquiz.models import *

from accounts.models import *
from django.db.models import Sum
from miniquiz.form  import * 

# Create your views here.
def admin(request):

    context={
        'totalCategory':Category.objects.filter(category__isnull=False).count(),
        'totalReport':Category.objects.filter(report__gte=20).count(),
        'totalAccount':Account.objects.all().count(),
        'Account':Account.objects.all().values().order_by('-date_joined')[0:4],
        'checkbox':Category.objects.filter(is_verified=False),
        'reportedCategory':Category.objects.filter(report__gte=20,is_verified=True),
    }



    return render(request,'admins/admin.html',context)



def leaders(request):
    userlist=leaderboards.objects.select_related('authorsID').values('authorsID__username','authorsID__email','authorsID__profile_image').annotate(Sum('score'))[0:10]

    context={
        'userlist':userlist,
    }
    print(leaderboards.objects.select_related('authorsID').values('authorsID__username','authorsID__profile_image','authorsID__email').annotate(Sum('score')))
    return render(request,'admins/leaders.html',context)


def users(request):
    context={
        'Account':Account.objects.all().values().order_by('-date_joined'),
    }
    
    return render(request,'admins/users.html',context)

def question(request):
    image=ImageForm()
    if request.user.is_admin:
        user=request.user
        if request.method=='POST':
            form = ImageForm(request.POST,request.FILES)
            print(request.POST)
            author_id=Account.objects.filter(username=user).values('id')
            categoryImage="/categoryImage/"+request.POST['categoryImage']
            print(categoryImage)
            print(author_id)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                dweet = form.save(commit=False)
                dweet.authors_id = author_id
                dweet.categoryImage=categoryImage
                dweet.save()
        
    context={
        'categories':Category.objects.filter(authors=request.user),
        'questionDetail':Questions.objects.select_related('question','category').values('category__categoryName','question','question_answer'),
        'form':image
        
    }



    #  [{'category__categoryName': 'bisal', 'question': 'what is your name ?', 'question_answer': 166}, {'category__categoryName': 'bisal', 'question': 'what is your name ?', 'question_answer': 167}, {'category__categoryName': 'bisal', 'question': 'what is your name ?', 'question_answer': 168}, {'category__categoryName': 'bisal', 'question': 'what is your name ?', 'question_answer': 169}]>


    a=Questions.objects.select_related('question','category').values('category__categoryName','question','question_answer').distinct()
    print(a.values())
    print(a.values('category__categoryName','question'))





    
    return render(request,'admins/categories.html',context)

