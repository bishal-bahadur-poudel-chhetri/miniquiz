
from django.contrib import admin
from django.urls import path,include,re_path
from . import views


urlpatterns = [


    path('<uuid:uuid_check>', views.getquiz,name="context"),
    path('', views.home,name="context"),
    path('quiz/<uuid:uuid_check>', views.quiz,name="context"),
    path('<uuid:uuid_check>/delete/<int:hi>', views.home_view,name="context"),

    path('<uuid:uuid_check>/add',views.add,name="context"),
    path('<uuid:uuid_check>/<int:questionsid>/update',views.update,name="context"),
    path('play',views.detail,name="context"),
    path('get',views.miniquiz,name="context"),

    path('categorydelete',views.categorydelete),
    path('submitscore',views.submitscore),
    path('thanks',views.thanks),




    path('categoryadd',views.categoryadd,name="context"),

    path('categories',views.categories,name="context"),
    path('leaderboard',views.leaderboard,name="context"),




    














    
    # path('form/', views.home_view),

]
