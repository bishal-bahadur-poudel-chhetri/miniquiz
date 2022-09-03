from django.db import models
from django.contrib.auth import get_user_model
import uuid,random
from django.utils import timezone




# from django.contrib.auth import get_user_model
username =get_user_model()

# Create your models here.e
#Base class(Common model used in all table)
class BaseModel(models.Model):
    update_at=models.DateField(auto_now=True)
    created_at=models.DateField(auto_now=True)
    class Meta:
        abstract=True



def get_profile_image_filepath(self, filename):
	return 'categoryImage/' + str(self.pk) + "/" + str(self.pk)+'.png'

def get_default_profile_image():
	return "default/category.jpg"

#Quiz Cateagories
class Category(BaseModel):
    #unique Identity Number
    uid=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    #Image file default(category.png)
    categoryImage=models.ImageField(upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    #Category Name
    categoryName=models.CharField(max_length=100)
    #Category Description
    description = models.TextField()
    #Category Author(Foreign Key from account app Account models)
    authors = models.ForeignKey(username,on_delete=models.CASCADE,related_name="author")
    #Report Count
    report=models.IntegerField(default=0)
    #boolean of user Verification 
    is_verified	= models.BooleanField(default=False)

    def __str__(self):
        return self.categoryName

  
 





#Questions(Has no base models)
class Questions(models.Model):
    #AutoIncrement Question ID
    questionid = models.AutoField(primary_key=True)
    #Category ID(foreing Key from miniquiz app Category model)
    category=models.ForeignKey(Category,related_name="category",on_delete=models.CASCADE)
    #updated Date
    update_at=models.DateField(auto_now=True)
    #Created Date
    created_at=models.DateField(auto_now=True)
    #Questions
    question=models.CharField(max_length=100)
    def __str__(self)->str:
        return self.question

    #used in fetch data which contain Question and its answer with its is 
    def get_answer(self):
        answer_object=list(Answer.objects.filter(question=self))
        data=[]
        
        for answer_objects in answer_object:
            data.append({
                'answer':answer_objects.answer,
                'is_correct':answer_objects.is_correct
            })
        return data

class Answer(BaseModel):
    answer_id = models.AutoField(primary_key=True)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=100)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class follower(BaseModel):
    follower=models.CharField(max_length=1000)
    user=models.CharField(max_length=1000)
    

    def __str__(self):
        return self.user


    
class leaderboards(BaseModel):
    score=models.IntegerField(default=0)
    categoryIdentity=models.ForeignKey(Category,default="4f0b25fab8804cdb8adb1a8511147060",on_delete=models.SET_DEFAULT,null=True,blank=True)
    authorsID = models.ForeignKey(username,on_delete=models.CASCADE,related_name="authorIdentity")


    def __str__(self):
        return self.authorsID.username

    def delete(self, using=None):
        if self.categoryIdentity_id:
            self.categoryIdentity_id.delete()
        super(categoryIdentity_id, self).delete(using)




    








    



    