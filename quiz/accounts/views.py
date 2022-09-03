from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from .models import *
from accounts.forms import RegistrationForm,Accountauthentication
from api.views import *

def loginSigninController(request):
	type=2
	if request.POST:
		if request.POST['type'] == 'login':
			Login_user=logins(request)
			if Login_user is not None:
				login(request,Login_user)
				checkif_admin=Account.objects.filter(username=Login_user).values('is_admin').first()
				type=2
				if checkif_admin["is_admin"] ==False:
					return redirect('/getquestion/')
				else:
					return redirect('/admins')

			else:
				type=1
		elif request.POST['type'] == 'Signup':
			conform=register_view(request)
			if conform == 200:
				return redirect("otp")
	



	context={
		'loginerror':type
	}


		


				



		

	return render(request,'account/login.html',context)




def register_view(request,*args,**kwargs):
	user=request.user
	context={}
	form =RegistrationForm(request.POST)
	print(request.POST)
	if form.is_valid():
		email=form.cleaned_data.get('email').lower()
		username=form.cleaned_data.get('username').lower()
		raw_password=form.cleaned_data.get('password1')
		request.session['email']=email
		# user=authenticate(email=email,password=raw_password)
		
		if email:
			user = Account.objects.filter(email__iexact = email)
			if user.exists():
				print("User Exist")
			else:
				old = tempProfile.objects.filter(email__iexact = email)
				if old.exists():
					if old.exists():
						for i in old:
							i.username=username
							i.password=raw_password
							i.save()

					a=RegisterAPI(request)
					print(a)
					otp=a.data['data'][0]
					return a.data['status']

				else:
					a=tempProfile(email=email,username=username,password=raw_password)
					a.save()
					new = tempProfile.objects.filter(email__iexact = email)
					# if counts > 100:
					# 	print("hello")
					# new.count = counts +1
					# print('Count Increase', counts)
					a=RegisterAPI(request)
					otp=a.data['data'][0]
					return a.data['status']
					# if a.data['status']==200:
					# 	return redirect("otp")
					# else: 
					# 	print("hello world 2")
	else:
		context['registration_form']=form




def otpverification(request):
	email=request.session['email']
	context={'email':email}
	if request.POST:
		
		req=request.POST
		userotp=req['one']+req['two']+req['three']+req['four']
		email=request.session['email']
		emailUser=tempProfile.objects.filter(email=email).values('email').first()
		Userotp=tempProfile.objects.filter(otp=userotp).values()
		
		try:
			
			if userotp==Userotp[0]['otp']:
				old = tempProfile.objects.filter(email__iexact = email)
				new_update=Account.objects.all()

				temp_data=old.first()
				temp_data.validated=True
				temp_data.save()
				email=temp_data.email
				password=temp_data.password
				print(password)
				a=Account(email=email,username=temp_data.username)
				a.set_password(password)
				a.save()

				user=authenticate(email=email,password=password)
				login(request,user)
				response=redirect('/getquestion/')
				return response
		
		except:
			error="Invalid OTP"
			context={
				'email':email,
				"error":error
			}
			return render(request,'account/otpinput.html',context)




	# print(request.POST['otp'])
	return render(request,'account/otpinput.html',context)

	




def home(request):
	user=request.user
	if user.is_authenticated:
		return HttpResponse(f'you are alreday authenticate as {user.email}.')
	else:
		return redirect("register")
def logout_view(request):
	logout(request)
	return redirect("/getquestion")

def logins(request):
	if request.POST:
		form=Accountauthentication(request.POST)
		if form.is_valid:
			email=request.POST['email']
			password=request.POST['password']
			print(email,password)
			user=authenticate(request,email=email,password=password)
			
			return user

		# else:
		# 	return False


	return render(request,'account/login.html')



def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect
