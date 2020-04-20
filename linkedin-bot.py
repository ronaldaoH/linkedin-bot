from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui 
import time
import sys
import config


def login(driver, user, pwd):
	url = "https://www.linkedin.com/uas/login?_l=es"
	driver.get(url)
	print(user)
	print(pwd)
	#u, p = extraer_credenciales()
	username = driver.find_element_by_id("username")
	username.send_keys(user)
	password = driver.find_element_by_id("password")
	password.send_keys(pwd)
	driver.find_element_by_xpath("//button[contains(text(), 'Iniciar sesión')]").click()
	print("successfully logged in")

def interfaz():
	def click_button():
		print("[+] Corriendo")
		ok = messagebox.askyesno(message="¿Desea continuar?", title="Desea correr el bot?")
		if ok:
			print(entry_1.get(), entry_3.get(), entry_5.get())
			entry_1.delete(first=0,last=1000)
			entry_2.delete(first=0,last=1000)
			entry_3.delete(first=0,last=1000)
			entry_5.delete(first=0,last=1000)

			user = str(entry_1.get())
			pwd = str(entry_2.get())
			kw = str(entry_3.get())
			mensaje = str(entry_5.get())
			#try:
			driver  = inicializar_firefox()
			login(entry_1.get(), entry_2.get(), driver)
			conectar(driver, entry_3.get(), entry_5.get())
			#except:
			#	messagebox.showinfo("AUTOLINKEDIN", "Termino!")
			#	root.destroy()
			#	print("Error inesperado:", sys.exc_info())

def extraer_credenciales():
	username = config.username	
	password = config.password
	return username, password

def inicializar_firefox():
	driver = webdriver.Firefox(executable_path=r'browsers/geckodriver.exe')
	time.sleep(5)	
	return driver



def cerrar_conversaciones(driver):
	ocs = driver.find_elements_by_xpath("//*[contains(@data-control-name , 'overlay.close_conversation_window')]")
	print("[+] CONVERSACIONES ABIERTAS : " , len(ocs))
	if ocs:
		for oc in ocs:
			print(oc.text)
			oc.click()

def conectar(driver, kw, msj):
	i  = 1
	try:
		SCROLL_PAUSE_TIME = 0.5
		url = 'https://www.linkedin.com/search/results/people/?keywords='
		driver.get(url +kw)
		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			connects = driver.find_elements_by_xpath("//button[contains(@aria-label, 'Conectar con')]")
			names = driver.find_elements_by_class_name("actor-name")
			cerrar_conversaciones(driver)
			contnames = 0
			for c in connects:
				time.sleep(2)
				cerrar_conversaciones(driver)
				print(c.click())
				ea = driver.find_element_by_xpath("//button[contains(@aria-label, 'Añadir una nota')]")
				if ea:
					ea.click()
					ta = driver.find_element_by_tag_name("textarea")
					if ta: 
						ta.click()
						nombre = c.get_attribute("aria-label").replace("Conectar con ","").split(" ")
						nombre = nombre[0]
						contnames = contnames +1
						print("NOMBRE : ", nombre)
						texto =  msj
						print(texto)
						ta.send_keys( texto )
						ei = driver.find_element_by_xpath("//button[contains(@aria-label, 'Enviar invitación')]")
						#ei2 = driver.find_element_by_xpath("//button[contains(@aria-label, 'Hecho')]")
						if ei:
							ei.click()
						#elif ei2:
						#	ei2.click()
						else:
							pyautogui.press("esc")

				print("[+] Connection request sent ", c.get_attribute("aria-label").replace("Conectar con ",""))
				time.sleep(2)
			time.sleep(2)
			pyautogui.press('space')
			time.sleep(SCROLL_PAUSE_TIME)
			new_height = driver.execute_script("return document.body.scrollHeight")
			
			if new_height == last_height:
				i= i +1
				if "page" in url:
					url = 'https://www.linkedin.com/search/results/people/?keywords='
				url = url+kw + '&page='+ str(i)
				driver.get(url)
			last_height = new_height
	except:
		print("UN ERROR LO SOLUCIONA TODO")
		print("Error inesperado:", sys.exc_info())
		driver.get(url) 
		raise 

def main():
	driver  = inicializar_firefox()
	login(driver, config.username, config.password)
	conectar(driver, config.kw, config.mensaje)

if __name__ == "__main__":
	main()