#IMPORTS NEEDED FOR THE PROGRAM
from selenium import webdriver
from time import sleep
import webbrowser

#VARIABLE USED ON THE PROGRAM
url         = "https://psmobile.hccs.edu"
url2        = "http://www.ratemyprofessors.com"
college     = "HOUSTON COMMUNITY COLLEGE"
subject     = "History"
catalog_nbr = "1301"
class_name  = subject[:4].upper() + catalog_nbr
section     = ""
session     = ""
time        = ""
instructor  = ""
campus      = ""
status      = ""
link        = ""
grade       = ""
results     = dict()
instructors = dict()

#OPEN A BROWSER AND ACCESS HCC WEBSITE TO LOOK FOR CLASSES
browser = webdriver.Firefox()
browser.get(url)
browser.find_element_by_link_text("Class Search").click()

elements = browser.find_elements_by_tag_name("button")

for element in elements:
	if "Select a Career" in element.text:
		element.click()
		browser.find_element_by_link_text("Semester Credit Hour").click()
	if "Select a Subject" in element.text:
		element.click()
		browser.find_element_by_link_text(subject).click()

browser.find_element_by_id("search-catalog-nbr").send_keys(catalog_nbr)
browser.find_element_by_id("buttonSearch").click()

print "GATHERING INFORMATION..."

#ACCESSING THE LINKS RESULTED FROM THE SEARCH CRITERIA AND STORE THEM
sleep(10)
element = browser.find_element_by_id("search-results")
elements = element.find_elements_by_tag_name("a")
for element in elements:
	link = element.get_attribute("href")
	section, session, time, instructor, campus, status = [item.split(':',1)[1] for item in element.text.split('\n')]
	if results.get(class_name,0):
		results[class_name].append({'section':section,'session': session,'time': time, 'instructor': instructor,'campus': campus,'status': status,'link': link})
	else:
		results[class_name]=[{'section':section,'session': session,'time': time, 'instructor': instructor,'campus': campus,'status': status,'link': link}]
	if not instructors.get(instructor, 0): instructors[instructor] = {}

#REMOVE THE STAFF FROM INSTRUCTORS DICTIONARY
if instructors.has_key(' Staff'): instructors.pop(" Staff")
		
#SEARCH FOR THE INSTRUCTOR ON RATEMYPROFESSOR
print "CHECKING PROFESSOR RATING"
browser.get(url2)
for instructor in instructors:
	sleep(5)
	element = browser.find_element_by_id("searchr")
	element.send_keys(instructor)
	element.submit()
	element = browser.find_element_by_id("searchResultsBox")
	elements = element.find_elements_by_tag_name("a")
	for element in elements:
		if instructor.split()[0] and  instructor.split()[1] and college in element.text:
			instr_id = element.get_attribute("href").split('=')[1]
			print instructor,instr_id
			instructors[instructor] = {'id':instr_id, 'grade':0}
			element.text
			print "\n"

#ACCESS THE RATEMYPROFESSOR TO GET THE RATE FOR EACH FOUNDED INSTRUCTOR
for instructor in instructors:
	instr_id = instructors[instructor].get('id', 0)
	if instr_id:
		sleep(5)
		link = url2 + "/ShowRatings.jsp?tid=" + instr_id
		browser.get(link)
		grade = browser.find_element_by_class_name("grade").text
		print instructor, grade
		instructors[instructor]['grade'] = grade
		print "\n"

#CLOSE THE BROWSER
browser.close()

#BUILDING THE HTML FILE WITH A LIST OF CLASSES AVAILABLE, INSTRUCTOR, RATE AND SOURCE LINK
with open('ratemyhccprofessors.html', 'a') as fh:
	fh.write(r"<HTML><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"\
	"<link rel='stylesheet' type='text/css' href='style.css'><title>RATE MY HCC PROFESSORS</title>"\
	"</head><BODY><TABLE>")
	fh.write(r"<TR><TH>section</TH><TH>session</TH><TH>time</TH><TH>instructor</TH><TH>instructor"\
	" rate</TH><TH>rate link</TH><TH>campus<TH>status</TH><TH>classlink</TH></TH></TR>")
	for result in results[class_name]:
		instructor = result['instructor']
		if instructors.has_key(instructor):
			if instructors[instructor].get('id', 0) and instructors[instructor].get('grade', 0):
				instr_id = instructors[instructor].get('id')
				grade = instructors[instructor].get('grade')
				link = url2 + "/ShowRatings.jsp?tid=" + instr_id
				fh.write(r"<TR><TD>" + result['section'] + r"</TD> " + r"<TD>" + result['session']+ 
				r"</TD>"+ r"<TD>" + result['time'] + r"</TD>"+ r"<TD>" + result['instructor']+ 
				r"</TD>"+ r"<TD>" + grade + r"</TD>"+ r"<TD><a href='" + link + 
				r"'>more info</a></TD>" + r"<TD>" + result['campus'] + r"</TD>"+ r"<TD>" + 
				result['status'] + r"</TD>" + r"<TD>"  + r"<a href='" + result['link'] + 
				r"'>more info</a></TD></TR>")
			else:
				fh.write(r"<TR><TD>" + result['section'] + r"</TD> " + r"<TD>" + result['session'] + 
				r"</TD>"+ r"<TD>" + result['time'] + r"</TD>"+ r"<TD>" + result['instructor']+ 
				r"</TD>"+ r"<TD>" + "NF" + r"</TD>"+ r"<TD>" + "NF" + r"</TD>"+ r"<TD>" + 
				result['campus'] + r"</TD>"+ r"<TD>" + result['status'] + r"</TD>"+ r"<TD>" + 
				r"<a href='" + result['link'] + r"'>more info</a></TD></TR>")
		else:
			fh.write(r"<TR><TD>" + result['section'] + r"</TD> " + r"<TD>" + result['session']+ 
			r"</TD>"+ r"<TD>" + result['time'] + r"</TD>"+ r"<TD>" + result['instructor'] + 
			r"</TD>"+ r"<TD>" + "N/A" + r"</TD>"+ r"<TD>" + "N/A" + r"</TD>"+ r"<TD>" + 
			result['campus'] + r"</TD>"+ r"<TD>" + result['status'] + r"</TD>"+ r"<TD>" + 
			r"<a href='" + result['link'] + r"'>more info</a></TD></TR>")
	fh.write("</TABLE></BODY></HTML>")

#OPEN THE FINAL REPORT
webbrowser.open(r'ratemyhccprofessors.html')
