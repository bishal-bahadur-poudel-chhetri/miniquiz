from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from accounts.views import *
from django.contrib.auth.models import User
from .form import ImageForm
import json
from django.db.models import Sum


def home(request):
    form=ImageForm()
    if request.user.is_authenticated:
        user=request.user
        if request.method=='POST':
            form = ImageForm(request.POST)
            print(request.POST)
            author_id=Account.objects.filter(username=user).values('id')
            categoryImage="/categoryImage/"+request.POST['categoryImage']
            print(categoryImage)
            print(author_id)
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.authors_id = author_id
                dweet.categoryImage=categoryImage
                dweet.save()
                redirect("/getquestion")
        
        context={
        'n':Category.objects.count(),
        'categories':Category.objects.filter(authors=user).order_by('update_at')[0:5],
        'categoryImage':Category.objects.all(),
        
        'form':form,
        'quizCategory':Category.objects.exclude(authors=user)[0:4],
        'CategoryOwner':Account.objects.get(username=user),
        'form':form
        
        }
    else:
        print("hello")
        context={
            'quizCategory':Category.objects.all()[0:4],
        }
    


    

    return render(request,'miniquiz/home.html',context)

def quiz(request,uuid_check):
    categoryImg=Category.objects.filter(uid=uuid_check).values('categoryImage').first()
    categoryUrl="http://127.0.0.1:8000/media/" + categoryImg['categoryImage']
    context={
    'category':Questions.objects.filter(category_id=uuid_check),
    'id':uuid_check,
    'categoryImage':categoryUrl,
    'categoryName':Category.objects.filter(uid=uuid_check).values('authors_id')
    }
    return render(request,'miniquiz/test.html',context)


def getquiz(request,uuid_check):
    try:
        question_obj=Questions.objects.filter(category_id=uuid_check)     
        print(question_obj)
        data=[]
        for question_objs in question_obj:
            categories=str(question_objs.category.categoryName)
            uid=str(question_objs.category.uid)

            data.append({
                "question":question_objs.question,
                "answer":question_objs.get_answer(),
                'questionid':question_objs.questionid,
                "uid":uid
            })
            payload={'status':True,'category':categories,'data':data,'categoryid':uid}
        print(uid) 
        return JsonResponse(payload)
          
    except Exception as e:
        print(e)
        return HttpResponse("something went wrong")



def get_answer(self):
    answer_object=list(Answer.objects.filter(question=self))
    data=[]
        
    for answer_objects in answer_object:
        data.append({
            'answer':answer_objects.answer,
            'is_correct':answer_objects.is_correct
            
        })
    return data


def home_view(request,hi,uuid_check):
    try:

        print(Questions.objects.get(questionid=hi).delete())
        

    except:
        print("a")
    return render(request,'miniquiz/test.html')

def add(request,uuid_check):

    if request.method == 'POST':
        post_data=json.loads(request.body.decode("UTF-8"))


        name=post_data['title']
        option1=post_data['opt1']
        option2=post_data['opt2']
        option3=post_data['opt3']
        option4=post_data['opt4']
        quest=Questions(question=name,category_id=uuid_check)
        quest.save()
        questionid=Questions.objects.filter(question=name).values('questionid')
        Answer1=Answer(answer=option1,question_id=questionid)
        Answer2=Answer(answer=option2,question_id=questionid)
        Answer3=Answer(answer=option3,question_id=questionid)
        Answer4=Answer(answer=option4,question_id=questionid)
        Answer1.save()
        Answer2.save()
        Answer3.save()
        Answer4.save()


    return render(request,'miniquiz/quiz.html')


def update(request,uuid_check,questionsid):
        if request.method == 'POST':
            post_data=json.loads(request.body.decode("UTF-8"))


            name=post_data['title']
            option1=post_data['opt1']
            option2=post_data['opt2']
            option3=post_data['opt3']
            option4=post_data['opt4']
            questio=Questions(question=name,category_id=uuid_check,questionid=questionsid)
            questio.save()
            quest=Questions.objects.get(questionid=questionsid,question=name)
            questionids=Answer.objects.filter(question=quest).values('answer_id')
            Answer1=Answer(answer=option1,answer_id=questionids[0]['answer_id'],question_id=questionsid)
            Answer2=Answer(answer=option2,answer_id=questionids[1]['answer_id'],question_id=questionsid)
            Answer3=Answer(answer=option3,answer_id=questionids[2]['answer_id'],question_id=questionsid)
            Answer4=Answer(answer=option4,answer_id=questionids[3]['answer_id'],question_id=questionsid)
            Answer1.save()
            Answer2.save()
            Answer3.save()
            Answer4.save()
        return render(request,'miniquiz/quiz.html')

def detail(request):
    request.GET.get('quizid')
   

    if request.user.is_authenticated:
        currentuser=request.user.username 
        uuid_check=request.GET.get('quizid')
        uid_check_url="/getquestion/get?quizid="+uuid_check
        username=str(request.user).upper()
        
        authorid=Category.objects.filter(uid=uuid_check).values('authors').first()
        a=Account.objects.filter(id=authorid['authors']).values('username').first()
        username=a['username']
        profileImage=Account.objects.filter(username=username).values('profile_image').first()
        profile_image="http://127.0.0.1:8000/media/"+profileImage['profile_image']
        print(username)


        # username=Account.objects.filter(id=authorid).values()
        # print(username)
        if request.method=='POST':
            values=request.POST['value']
            user=request.POST['user']
            followerss=request.POST['follower']
            if values == 'follow':
                followers_count=follower(follower=followerss,user=user)
                followers_count.save()
            if values == 'unfollow':
                a=follower.objects.filter(user=user).values('id').first()
                id=a['id']
                followers_count=follower(follower=followerss,user=user,id=id)
                followers_count.delete()

            




        user_followers=len(follower.objects.filter(user=username))
        user_following=len(follower.objects.filter(follower=username))
        user_follower_list=follower.objects.filter(user=username)
        print(user_follower_list)
        user_follower_list1=[]
        for i in user_follower_list:
            user_follower_list0=i.follower
            user_follower_list1.append(user_follower_list0)
        if currentuser in user_follower_list1:
            follow_button_value="unfollow"
            print("hi")

        else:
            print(currentuser)
            follow_button_value="follow"


        


        





    context={
        'categoryCount':Category.objects.filter(authors=authorid['authors']).count(),
        'name':username,
        'image':profile_image,
        'follower':user_followers,
        'following':user_following,
        'follow_button_value':follow_button_value,
        'next_btn':uid_check_url,
        
        
        
    }
   
   
    return render(request,'miniquiz/userDetail.html',context)

def miniquiz(request):
    uuid_check=request.GET.get('quizid')
    a=Category.objects.all().values()
    context={
        'id': uuid_check,
    }

    return render(request,'miniquiz/miniquiz.html',context)





def categorydelete(request):
    context={}
    try:
        if request.method == 'GET':
            user_id=request.GET.get('uid')
            print(user_id)
            deletecategory=Category.objects.filter(uid=user_id)
            deletecategory.delete()
    except:
        print("error")
    return render(request,'miniquiz/home.html',context)


def categoryadd(request):
    context={}
    try:
        if request.method == 'GET':
            user_id=request.GET.get('uid')
            print(user_id)
            deletecategory=Category.objects.filter(uid=user_id).update(is_verified=True)

            
    except:
        print("error")
    return render(request,'miniquiz/categories.html',context)



def leaderboard(request):
    dashboard=leaderboards.objects.select_related('authorsID').values('authorsID__username','authorsID__email','authorsID__profile_image','score').annotate(total_price=Sum('score'))[0:3]
    userlist=leaderboards.objects.select_related('authorsID').values('authorsID__username','authorsID__email','authorsID__profile_image','score').annotate(total_price=Sum('score'))[0:10]

  
    context={
        'leaderboard':dashboard,
        'userlist':userlist,
    }
    print(context)
    return render(request,'miniquiz/leaderboard.html',context)

def categories(request):
    context={
        'categories':Category.objects.order_by('update_at'),
    }
    return render(request,'miniquiz/categories.html',context)

    




