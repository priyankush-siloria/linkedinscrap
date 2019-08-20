
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException, TimeoutException
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
from sqlite3 import Error
import os
from pyvirtualdisplay import Display
import smtplib
import time
import imaplib
import email
import json
from .models import *
import traceback
# from datetime import datetime, date, timedelta


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
driver_path = os.path.join(base_dir, 'chromedriver')
database = os.path.join(base_dir, 'db.sqlite3')

# create_sqlite3 connection
def create_connection(db_file): 
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

# Code for read mail
def getCode():
	try:
		mail = imaplib.IMAP4_SSL('imap.gmail.com')
		mail.login('sandeepaviox@gmail.com', 'aviox@2019')
		# mail.login('kishanaviox@gmail.com', 'aviox@2019')
		mail.list()
		mail.select("inbox") 
		result, data = mail.uid('search', None, "UNSEEN")
		latest_email_uid = data[0].split()[-1]
		result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
		raw_email = data[0][1]	
		email_message = email.message_from_bytes(raw_email)
		code = ""
		if "here's your PIN" in email_message['Subject']:
				payloads = str(email_message.get_payload()[0])
				list_for_code=payloads.split('\n')
				code=list_for_code[14].split(':')[1]
				print("innnnnnnnnnnnnnnnnnnnnnnnnnnnnn CODE ......")
		return code

	except Exception as e:

		file = open("read_code_error.txt","w")
		file.write(str(e))
		file.write(traceback.format_exc()) 
		file.close()
		raise e

		
# driver = webdriver.Chrome( desired_capabilities=capabilities, executable_path="/home/aviox/Documents/Python/MArio/3-5-19/script/drivers/chromedriver_linux64/chromedriver", options=options)
# driver = webdriver.Chrome( executable_path="/home/aviox/Documents/Python/MArio/3-5-19/script/drivers/chromedriver_linux64/chromedriver")
def send_keys(element, keys):
		# input und checkboxen clearen
	if element.get_attribute("type") == "checkbox":
		if element.get_attribute("checked"):
			element.send_keys(Keys.SPACE)
	else:    
		# inputfelder clearen
		element.clear()
	element.send_keys(keys)



def check_verification(driver):
	while True:
		try:

			driver.find_element_by_id("email-pin-challenge")

			code=getCode()
			print(code)
			driver.find_element_by_id("input__email_verification_pin").send_keys(code)
			driver.find_element_by_id("email-pin-submit-button").click()
			print('Enter Code')
			time.sleep(20)						
		except NoSuchElementException:
			# print("Done verification")
			break
def sucess_login(driver):
	try:
		driver.find_element_by_id("username")	
		return False
	except NoSuchElementException:
		# print("Done verification")
		return True
	
def mainScript(automationid):
	
	automation_obj=Automations.objects.get(id=automationid)

	display = Display(visible=0, size=(800, 600))
	display.start()
	status_dict=dict()
	print("1")
	options = webdriver.ChromeOptions()
	options.add_argument('--disable-gpu')
	options.add_argument('--disable-impl-side-painting')
	options.add_argument('--disable-gpu-sandbox')
	options.add_argument('--disable-accelerated-2d-canvas')
	options.add_argument('--disable-accelerated-jpeg-decoding')
	options.add_argument('--no-sandbox')
	options.add_argument('--test-type=ui')
	options.add_argument('--disable-dev-shm-usage')   
	print("2")
	try:
		driver = webdriver.Chrome(executable_path=driver_path, options=options)
	except Exception as e:
		raise e
	
	print("3")

	try:
		driver.execute_script('''window.open("about:blank", "_blank");''')
		print("")
		time.sleep(1)
		driver.switch_to.window(driver.window_handles[0])
		time.sleep(3)
		driver.get("https://www.linkedin.com/uas/login")
		print("4")

		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))

		username = automation_obj.user.email

		password = automation_obj.user.password
		print(username,password)
		send_keys(driver.find_element_by_id("username"), username)
		send_keys(driver.find_element_by_id("password"), password)
		print("----submit------")
		# print(driver.page_source)
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
		driver.find_element_by_xpath("//button[@type='submit']").click()
		is_login = sucess_login(driver)
		print("--------Logged in-------------")
		print("5")
		if "Adding a phone number adds security" in driver.page_source:

			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//button[contains(text(),'Skip')]"))));
			
			driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
			print("--------Adding a phone number adds security-------------")

		if not is_login:
			# return {'status':False,'msg':'Linkedin blocked access for today try after 24 hours.'}
			status_dict['status']=False
			status_dict['msg']='Linkedin blocked access for today try after 24 hours.'
		check_verification(driver)
		# print(driver.page_source)
		driver.get("https://www.linkedin.com/sales/search/people?viewAllFilters=true")

		# print(driver.page_source)
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//div[@data-test-filter-code='GE']"))));
		
		# driver.find_element_by_xpath("//div[@id='ember139']").click()

		# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='Remove viewed Leads from search']")))
		# driver.find_element_by_xpath("//button[@title='Remove viewed Leads from search']").click()
		p_url=''
		if automation_obj.geography:
			if automation_obj.geography_status:
				driver.find_element_by_xpath("//div[@data-test-filter-code='GE']").click()
				
				# driver.find_element_by_xpath("//input[@id='ember134-typeahead-region']").send_keys(geo[2])
				driver.find_element_by_xpath("//input[@placeholder='Add locations']").send_keys(automation_obj.geography.title)
				# geography_montreal = driver.find_elements_by_xpath(".//ol[@class='search-filter-typeahead__list overflow-y-auto']/li[@class='t-sans flex align-items-center']")[1].click()

				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='"+automation_obj.geography.title+"']")))
				driver.find_element_by_xpath("//button[@title='"+automation_obj.geography.title+"']").click()
				driver.find_element_by_xpath("//li-icon[@type='minus-icon']").click()

		if automation_obj.srlevel:
			if automation_obj.srlevel_status:
				driver.find_element_by_xpath("//div[@id='ember181']").click()

				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='"+automation_obj.srlevel.title+"']")))
				driver.find_element_by_xpath("//button[@title='"+automation_obj.srlevel.title+"']").click()
				driver.find_element_by_xpath("//li-icon[@type='minus-icon']").click()

		if automation_obj.period:
			if automation_obj.period_status:
				driver.find_element_by_xpath("//div[@id='ember193']").click()
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='"+automation_obj.period.title+"']")))
				driver.find_element_by_xpath("//button[@title='"+automation_obj.period.title+"']").click()
				driver.find_element_by_xpath("//li-icon[@type='minus-icon']").click()

		if automation_obj.functionsatcompany:
			if automation_obj.functionsatcompanyl_status:
				driver.find_element_by_xpath("//div[@id='ember198']").click()
				
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ("//input[@id='ember198-typeahead']"))))
				# driver.find_element_by_xpath("//input[@id='ember187-typeahead']").send_keys(function[2])
				driver.find_element_by_xpath("//input[@placeholder='Add functions']").send_keys(automation_obj.functionsatcompany.title)
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='"+automation_obj.functionsatcompany.title+"']")))
				driver.find_element_by_xpath("//button[@title='"+automation_obj.functionsatcompany.title+"']").click()
				driver.find_element_by_xpath("//li-icon[@type='minus-icon']").click()

		if automation_obj.yearsofexperience:
			if automation_obj.yearsofexperience_status:
				exp_div = driver.find_element_by_xpath("//div[@id='ember209']")
				move_to_element_div = ActionChains(driver).move_to_element(exp_div)
				move_to_element_div.click().perform()
				# driver.find_element_by_xpath("//div[@id='ember209']").click()
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@title='"+automation_obj.yearsofexperience.title+"']")))
				driver.find_element_by_xpath("//button[@title='"+automation_obj.yearsofexperience.title+"']").click()
				driver.find_element_by_xpath("//li-icon[@type='minus-icon']").click()

		driver.find_element_by_xpath("//button[@class='button-primary-medium']").click()

		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@class='pv5 ph2 search-results__result-item']")))
		
		p_url=driver.current_url

		pagination = driver.find_elements_by_xpath("//ol[@class='search-results__pagination-list']/li")
		last_page_number = pagination[-1].find_element_by_xpath(".//button").get_attribute("data-page-number")
		last_page_number = int(last_page_number)
		print('last_page_number',last_page_number)
		count = 0
		driver.get(p_url)
		print("6")
		for page_number in range(1,last_page_number):
			
			file = open("timout_exceptiondemo.txt","w")
			file.write(str("page_number....."+str(page_number))) 
			file.close() 
			try:
				print("7")
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@class='pv5 ph2 search-results__result-item']")))
			except TimeoutException:
				time.sleep(60)
				driver.switch_to.window(driver.window_handles[0])
				# print(driver.page_source)
				print("errro timeout  refresh page")
				driver.get(p_url)
				time.sleep(3) 
				file = open("reloaded_file.html","w")
				file.write(str(driver.page_source)) 
				file.close()
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				for ij in range(1,40,4):
					print("-------pages--------",ij)
					if page_number>ij:
						print("in if")
						next_page_button1 = driver.find_element_by_xpath("//button[@data-page-number='"+str(ij+1)+"']")
						Hover1 = ActionChains(driver).move_to_element(next_page_button1)
						print("click")
						Hover1.click().perform()
						# next_page_button1.click()
						time.sleep(2)
					else:
						print("-------required--------",page_number)
						next_page_button1 = driver.find_element_by_xpath("//button[@data-page-number='"+str(page_number)+"']")
						# next_page_button1.click()
						Hover1 = ActionChains(driver).move_to_element(next_page_button1)
						print("click")
						Hover1.click().perform()
						break
				time.sleep(3)
				file = open("page_source.txt","w")
				file.write(str(driver.page_source)) 
				file.close() 
				WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//li[@class='pv5 ph2 search-results__result-item']")))
			result_list = driver.find_elements_by_xpath("//li[@class='pv5 ph2 search-results__result-item']")
			print("8")
			# p_url=driver.current_url
			# update cureent url here with same var
			print("items_length-----",str(len(result_list)))
			print("page_number....."+str(page_number))
			item_count = 1
			if len(result_list)==10:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(4)
				result_list = driver.find_elements_by_xpath("//li[@class='pv5 ph2 search-results__result-item']")
			for item in result_list:
				print("items_length-----",str(len(result_list)))
				print("page_number....."+str(page_number))
				print("item_number....."+str(item_count))
				# if item_count< len(result_list) and item_count<23:
				# 	try:
				# 		driver.execute_script("arguments[0].scrollIntoView();", result_list[item_count+1])
				# 	except Exception as e:
				# 		pass
				item_count = item_count + 1
				# if item_count == len(result_list):
				# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(1)
				print("9")
				name = ""
				try:
					name = item.find_element_by_xpath(".//dt[@class='result-lockup__name']").text
				except NoSuchElementException as e:
					pass
				print("10")
				profile_url = ""
				try:
					profile_url = item.find_element_by_xpath(".//dt[@class='result-lockup__name']/a").get_attribute("href")
				except NoSuchElementException as e:
					pass
				# person_data = AutomationData.objects.filter(url=profile_url)
				# if person_data:
				# 	time.sleep(3)
				# 	continue
				print("11")
				desc = ""
				try:
					desc = item.find_element_by_xpath(".//dd[@class='result-lockup__highlight-keyword']").text
				except NoSuchElementException as e:
					pass
				print("12")
				company_name = ""
				function = ""
				sr_level = ""
				designation_split = []
				print("---------------------------")
				print(desc)
				print("---------------------------")
				desc_split_desc = desc.split("at")
				print(desc_split_desc)
				if len(desc_split_desc)>=2:
					company_name = desc_split_desc[-1]
					designation_split = (desc_split_desc[0]).split("of")
				if len(designation_split)==2:
					sr_level = designation_split[0]
					function = designation_split[1]
				else:
					function = desc_split_desc[0]
				company_name_split = company_name.split("\n")
				print(company_name_split)
				company_name = company_name_split[0]
				if not company_name:
						company_name = ("|".join(company_name_split))
				

				# driver.execute_script('''window.open("about:blank", "_blank");''')
				# print("")
				# time.sleep(1)
				# driver.switch_to.window(driver.window_handles[0])
				time.sleep(1)
				driver.switch_to.window(driver.window_handles[1])
				driver.get(profile_url)
				try:
					time.sleep(3)
					# WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//dd[@class='profile-topcard__educations flex mt3']")))
					print("13")
					education=None
					try:
						education = driver.find_element_by_xpath("//dd[@class='profile-topcard__educations flex mt3']")
					except NoSuchElementException as e:
						pass
					print("14")
					education_text = ""
					try:
						if education:
							education_text = education.find_element_by_xpath(".//span[@class='align-self-center']").text
					except NoSuchElementException as e:
						pass
					print("15")
					education_text = education_text.strip()
					grade_start = ""
					grade_end = ""
					degree = ""
					if education_text:
						grade = education_text[-11:]
						# print(grade)
						grade_split = grade.split("–")
						if(len(grade_split)>1):
							degree = education_text[:-11]
							grade_start = (grade_split[0]).strip()
							grade_end = (grade_split[1]).strip()
						else:
							degree = education_text.strip()
					if not company_name:
						desc = ""
						try:
							desc = driver.find_element_by_xpath(".//dd[@class='mt2']").text
						except NoSuchElementException as e:
							pass
						company_name = ""
						if desc:
							desc_split_desc = desc.split("at")
							company_name = desc_split_desc[-1]
					# print(driver.page_source)
					status='P'
					# cur.execute('DELETE FROM scrap_automationdata')
					person_data = AutomationData.objects.filter(url=profile_url)
					if not person_data:
						AutomationData.objects.create(
							companyname=company_name,
							name=name,
							senioritylevel=sr_level,
							function=function,
							degree=degree,
							gradyearstart=grade_start,
							gradyearend=grade_end,
							user=automation_obj.user,
							automation=automation_obj,
							status=status,
							url=profile_url
							)
						print("---------------------not exist inserted--------------------")
					else:
						AutomationData.objects.create(
							companyname=company_name,
							name=name,
							senioritylevel=sr_level,
							function=function,
							degree=degree,
							gradyearstart=grade_start,
							gradyearend=grade_end,
							user=automation_obj.user,
							automation=automation_obj,
							status=status,
							url=profile_url,
							isduplicated=True
							)
						print("-----------------------already existed---------------------")
					print(profile_url)
					# task=(company_name,name,sr_level,function,degree,grade_start,grade_end,profile_url)
					# cur.execute(sql,task)
					# conn.commit()
					# print(task)
					print("Running...")
				except NoSuchElementException as e:
					print(str(e))
					print("16")
					print("NoSuchElementException-----Education not available")
					print("17")
					status_dict['status']=False
					status_dict['msg']=str(e)
					pass
				except Exception as e:
					print(str(e))
					print("18")
					print("---------elements_error-------")
					print("19")
					status_dict['status']=False
					status_dict['msg']=str(e)
					pass
				time.sleep(1)
				# try:
				# 	driver.close()
				# except Exception as e:
				# 	pass
				
				driver.switch_to.window(driver.window_handles[0])
				# if count==4:
				# 	print("new page")
				# 	break
				count = count +1
			# if count==10:
			# 	print("new page end")
			# 	break
			print("new page opened")
			file = open("pre_page.txt","w")
			file.write(str(driver.page_source)) 
			file.close()
			next_page = page_number+1
			if next_page != last_page_number:
				print("20")
				next_page_button = driver.find_element_by_xpath("//button[@data-page-number='"+str(next_page)+"']")
				print("21")
				Hover = ActionChains(driver).move_to_element(next_page_button)
				print("22")
				Hover.click().perform()

				print("23")
				time.sleep(5)
				file = open("next_page.txt","w")
				file.write(str(driver.page_source)) 
				file.close()
		print("sucess mail will is send.")
		status_dict['status']=True
		status_dict['msg']="All data is scraped sucessfully. Please check on the website."
		time.sleep(10)
	except NoSuchElementException as e:
		print('------NoSuchElementException-------')
		status_dict['status']=False
		status_dict['msg']= 'Some elements are changed please check'
	except Exception as e:
		raise e
		print('--------Error------')
		status_dict['status']=False
		status_dict['msg']= 'Some error occure.Please try later or contact your developer.'
		driver.quit()

	finally:	
		driver.quit()
		display.stop()
	return status_dict


def get_cron():

	conn = create_connection(database)
	cur = conn.cursor()
	try:
		cur.execute("SELECT * FROM scrap_cron WHERE is_active={}".format(1))
		crons = cur.fetchall()
		print(crons)

		for job in crons:
			last_exe_date=job[2]
			interval_day=job[4]
			last_exe_date1 = datetime.strptime(last_exe_date,  '%Y-%m-%d').date()
			current_date = date.today().isoformat()  
			days_after = (last_exe_date1+timedelta(days=int(interval_day))).isoformat()
			if current_date == days_after:
				print("Schduale Script is Running.....")
				mainScript(job[3])
				cur.execute('UPDATE scrap_cron SET last_exe_date = ? WHERE id = ?', [current_date, job[0]])
				conn.commit()
				print('last_exe_date Updated.')					
			else:
				print('No Running Script for today.') 

	except Exception as e:
		raise e
	finally:
		conn.close()
if __name__ == '__main__':
	get_cron()





