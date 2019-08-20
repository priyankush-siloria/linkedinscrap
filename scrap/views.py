
from django.views.generic import TemplateView, View
from .models import *
from .forms import DayFrequencyForm, RateFrequencyForm
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
import json
from .forms import *
from django.contrib import messages
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
from sqlite3 import Error
from django.template.loader import render_to_string
from .LinkedInScript import mainScript
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
import time
class Index(TemplateView):
	template_name = 'index.html'
	def get(self,request):
		automations = Automations.objects.all()
		return render(request,self.template_name, locals())


class StartThread(View):
	scrap_id=''
	def get(self,request):
		linkedin_user=request.GET.get("linkedin_user")
		scrap_id = request.GET.get("id")
		automations = Automations.objects.all()
		now=timezone.now()
		try:
			running_script = ScriptInterval.objects.filter(running=True)
			if running_script:
				response_data = {
					"status":False,
					"message":"Scraping on automation "+running_script[0].automation.name+" is already running. Wait until this finished."

				}
				return HttpResponse(json.dumps(response_data), content_type="application/json") 
			get_interval,uja=ScriptInterval.objects.get_or_create(automation_id=int(scrap_id))
	
			fmt = '%Y-%m-%d %H:%M:%S'
			d1 = datetime.strptime(str(get_interval.interval).split('.')[0], fmt)
			d2 = datetime.strptime(str(now).split('.')[0], fmt)
			minutes_diff = (d2 - d1).total_seconds() / 60.0
			testing = True
			if minutes_diff >= 60:
				new_thread = threading.Thread(name='mythread', target=self.startScrap, args=(int(scrap_id),))
				new_thread.daemon = True
				new_thread.start()
				get_interval.interval=now
				get_interval.running=True
				get_interval.save()
				response_data = {
						"status":True,
						"message":"Scrapping is started."

					} 
			else:
				print("Will be after"+str(120-minutes_diff))
				after=round(60-minutes_diff, 2)
				subject = "Script Alert"
				sccuess_status=" New execution request is placed for scraping script. But script it executed recentaly. So wait for "+str(int(after))+" minutes to make new execution request. "
				recipients = ['mario@sdg360.com','rajindermohan001@gmail.com',"director@avioxtechnologies.com"]
				# send_status = mailSend(subject, recipients, html_message=sccuess_status)
				response_data = {
						"status":False,
						"message":sccuess_status

					} 
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		except Exception as e:
			raise e
			return render(request,'index.html')

	def startScrap(self,automationid=0):
		try:
			if automationid !=0:
				status=mainScript(automationid)

				if status['status'] == False:
					print("Not Authenticate")
					error_status=status['msg']	
					recipients = ['mario@sdg360.com','rajindermohan001@gmail.com',"director@avioxtechnologies.com"]
					subject = "Script Status"
					# send_status = mailSend(subject, recipients, html_message=error_status)
					
				if status['status'] == True:
					sccuess_status="Linked in scraping script is completed successfully for instant run."	
					recipients = ['mario@sdg360.com','rajindermohan001@gmail.com',"director@avioxtechnologies.com"]
					# send_status = mailSend(subject, recipients, html_message=sccuess_status)
				ScriptInterval.objects.filter(automation__id=automationid).update(running=False)
		except Exception as e:
			ScriptInterval.objects.filter(automation__id=automationid).update(running=False)
			raise e

def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		return True
	except Exception as e:
		print(str(e))
		return False

 
class StopThread(View):
	def get(self,request):
		try:
			automations = Automations.objects.all()
			scrap_id = request.GET.get("id")
			for th in threading.enumerate():
				thread_name = th.getName()
				if thread_name is "mythread":
					# th.stop()
					th.daemon = False
				print("Stoped..")
		except Exception as e:
			print(e)
		return render(request,'index.html')


class AddAutomation(TemplateView):
	template_name='add_automation.html'
	def get(self,request):
		try:
			day_form = DayFrequencyForm
			rate_form = RateFrequencyForm
			locations = Geography.objects.all()
			srlevel = SeniorityLevel.objects.all()
			period = YearAtCompany.objects.all()
			functionatcom = FunctionAtComapny.objects.all()
			year_of_experience=YearofExperience.objects.all()
			user = LinkedIn.objects.all()

		except Exception as e:
			raise e
	
		return render(request,self.template_name, locals())

	def post(self,request):
		print("rijgiojg0re")
		try:
			name = request.POST.get("name")
			geography = request.POST.get("geography")
			srlevel = request.POST.get("srlevel")
			period = request.POST.get("period")
			functions = request.POST.get("functions")
			experience=request.POST.get("experience")
			day = request.POST.get("day")
			rate = request.POST.get("rate")
			user=request.POST.get('users')
			print("ahcsdjhsdafdfmndskjfnd"+str(user))
			automation = Automations(
				user_id=user,
				name=name,
				day=day,
				rate=rate
				)
			if geography=="0":
				automation.geography_status=False
			else:	
				automation.geography_id=geography
				automation.geography_status=True

			if srlevel=="0":
				automation.srlevel_status=False
			else:	
				automation.srlevel_id=srlevel
				automation.srlevel__status=True

			if functions=="0":
				automation.functionsatcompanyl_status=False
			else:	
				automation.functionsatcompany_id=functions
				automation.functionsatcompanyl_status=True

			if experience=="0":
				automation.yearsofexperience_status=False
			else:	
				automation.yearsofexperience_id=experience
				automation.yearsofexperience_status=True

			if period=="0":
				automation.period_status=False
			else:	
				automation.period_id=period
				automation.period_status=True
			automation.status=True
			automation.save()
			value=''
			if rate == 'W':
				value=7
			if rate == 'M':
				value=30
			save_cron=Cron(automation_id=automation.id,execution_rate=value)
			save_cron.save()
			messages.success(request, 'Automation added successfully')
		except Exception as e:
			raise e
		return HttpResponseRedirect(reverse('add'))

class ShowAutomations(TemplateView):
	template_name='index-three.html'
	def get(self,request):
		return render(request,self.template_name, locals())


class AllData(TemplateView):
	template_name='all.html'
	def get(self,request):
		scraped_data = AutomationData.objects.filter(status="P")
		return render(request,self.template_name, locals())

class ChangeAllStatus(View):

	def post(self,request):

		response = {}
		status =  request.POST.get('status')

		try:
			AutomationData.objects.all().update(status = status)	
			response["status"] = True
			response["msg"] = "Status is changed successfully."

		except Exception as e:
			response["status"] = True
			response["msg"] = "Some error occur. Please try again." + str(e)

		return HttpResponse(json.dumps(response), content_type="application/json")

class Actions(View):

	def post(self,request):
		response = {}
		ids =  request.POST.get('ids')
		id_list = ids.split(',')
		action =  request.POST.get('action')

		scraped_data = AutomationData.objects.filter(pk__in=id_list)

		if action == 'delete':
			scraped_data.delete()

		elif action == 'accept':
			scraped_data.update(status="A")

		elif action == 'reject':
			scraped_data.update(status="R")

		return HttpResponseRedirect('/alldata')


class Reject(TemplateView):
	template_name='reject.html'
	def get(self,request):
		scraped_data = AutomationData.objects.filter(status="R")
		return render(request,self.template_name, locals())

class Linked(TemplateView):
	template_name='linked.html'
	def get(self,request):
		return render(request,self.template_name, locals())

	def post(self, request):
		email=request.POST.get("email")
		pwd=request.POST.get ("password")

		try:
			check_email=LinkedIn.objects.get(email=email)

			messages.error(request,'This email already exists.')
			return render(request, self.template_name,locals())
			# return HttpResponseRedirect("linked")

		except LinkedIn.DoesNotExist as e:
			LinkedIn.objects.create(email=email,password=pwd)
			return HttpResponseRedirect("/linked/")

class Changestatus(View):
	def post(self,request):
		response = {}
		try:
			data_id = request.POST.get('id')
			status = request.POST.get('status')
			auto = AutomationData.objects.get(id=data_id)
			auto.status=status
			auto.save()

			response["status"] = True
			response["msg"] = "Status is changed successfully."
		except Exception as e:
			response["status"] = True
			response["msg"] = "Some error occur. Please try again."
		return HttpResponse(json.dumps(response), content_type="application/json")
			



class Database(TemplateView):
	template_name='database.html'
	def get(self,request):
		scraped_data = AutomationData.objects.filter(status="A")
		return render(request,self.template_name, locals())

class User(TemplateView):
	template_name='users.html'
	def get(self,request):
		user = LinkedIn.objects.all()
		print(user)
		return render(request,self.template_name, locals())

class DeleteUser(View):
	def get(self,request,*args,**kwargs):
		res={}
		try:
			auto_id=request.GET.get("id")
			LinkedIn.objects.get(id=int(auto_id)).delete()
			res['status']=True
		except Exception as e:
			res['status']=False
			raise e
		return HttpResponse(json.dumps(res),content_type="application/json")


class EditUser(TemplateView):
	template_name="edit_user.html"
	def get(self,request,*args,**kwargs):
		
		try:
			auto_id=kwargs["id"]
			user = LinkedIn.objects.get(id=auto_id)
			update = LinkedIn.objects.filter(id=auto_id)
		except Exception as e:
			raise e
		return render(request,self.template_name, locals())

	def post(self,request,*args,**kwargs):
		
		try:
			name=request.POST.get("email")
			password=request.POST.get("password")
			auto_id=request.POST.get("auto_id")
			save_data = LinkedIn.objects.get(id=int(auto_id))
			save_data.email=name
			save_data.password=password
			save_data.save()

		except Exception as e:
			raise e
		return HttpResponseRedirect("/")

class DeleteAutomation(View):

	def get(self,request,*args,**kwargs):
		res={}
		try:
			auto_id=request.GET.get("id")
			Automations.objects.get(id=int(auto_id)).delete()
			res['status']=True
		except Exception as e:
			res['status']=False
			raise e
		return HttpResponse(json.dumps(res),content_type="application/json")



class EditAutomation(TemplateView):
	template_name="edit_auto.html"
	def get(self,request,*args,**kwargs):		
		try:
			auto_id=kwargs["id"]
			data = Automations.objects.get(id=int(auto_id))
			geography=Geography.objects.all()
			seniority_level=SeniorityLevel.objects.all()
			year_atCompany=YearAtCompany.objects.all()
			function_at_comapny=FunctionAtComapny.objects.all()
			year_of_experience=YearofExperience.objects.all()
			days = DayFrequencyForm
			rate=RateFrequencyForm
		except Exception as e:
			raise e
		return render(request,self.template_name, locals())

	def post(self,request,*args,**kwargs):	
		try:
			name=request.POST.get("name")
			geography=request.POST.get("geography")
			srlevel=request.POST.get("srlevel")
			period=request.POST.get("period")
			functions=request.POST.get("functions")
			experience=request.POST.get("experience")
			day=request.POST.get("day")
			rate=request.POST.get("rate")
			auto_id=request.POST.get("auto_id")

			save_data = Automations.objects.get(id=int(auto_id))
			save_data.name=name
			if geography=="0":
				save_data.geography_status=False
			else:	
				save_data.geography_id=geography
				save_data.geography_status=True

			if srlevel=="0":
				save_data.srlevel_status=False
			else:	
				save_data.srlevel_id=srlevel
				save_data.srlevel__status=True

			if functions=="0":
				save_data.functionsatcompanyl_status=False
			else:	
				save_data.functionsatcompany_id=functions
				save_data.functionsatcompanyl_status=True

			if experience=="0":
				save_data.yearsofexperience_status=False
			else:	
				save_data.yearsofexperience_id=experience
				save_data.yearsofexperience_status=True

			if period=="0":
				save_data.period_status=False
			else:	
				save_data.period_id=period
				save_data.period_status=True
			
			save_data.day=day
			save_data.rate=rate
			save_data.save()

		except Exception as e:
			raise e
		return HttpResponseRedirect("/")

class AddCron(View):
	def get(self,request):
		print("------------CRRRONNN")
		res={}
		try:
			print("--=-")
			automation_id=request.GET.get('automation_id')
			cron=Cron.objects.get(automation_id=automation_id)		
			cron.last_exe_date=timezone.now()
			cron.is_active = True
			cron.save()
		except Exception as e:
			raise e
		return HttpResponse(json.dumps(res),content_type="application/json")

		

class PauseSchduale(View):
	def get(self,request):
		print("--------PauseSchduale--------")
		res={}
		try:
			print("--=-")
			automation_id=request.GET.get('automation_id')
			cron=Cron.objects.get(automation_id=automation_id)		
			cron.is_active = False
			cron.save()
			res['status']=True
		except Exception as e:
			res['status']=False
			raise e
		return HttpResponse(json.dumps(res),content_type="application/json")