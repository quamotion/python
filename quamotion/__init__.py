import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

def ensure_quamotion_running():
	# Get the status page, to make sure the Quamotion WebDriver is up and running. This can come in handy
	# if you have just (re)started the Quamotion service.
	try:
		r = requests.get('http://localhost:17894/wd/hub/status', timeout=5)
	except Exception as e:
		raise Exception('Failed to connect to the Quamotion WebDriver. Please make sure the WebDriver service is running!')

def add_quamotion_extensions(driver):
	driver.command_executor._commands["homescreen"] = ('POST', '/session/$sessionId/wda/homescreen')
	driver.command_executor._commands["get_installed_apps"] = ('GET', '/quamotion/device/$deviceId/app?strict&all')
	driver.command_executor._commands["get_running_processes"] = ('GET', '/quamotion/device/$deviceId/process?strict')
	driver.command_executor._commands["launch_app"] = ('POST', '/quamotion/device/$deviceId/app/$appId/launch?strict')
	driver.command_executor._commands["uninstall_app"] = ('DELETE', '/quamotion/device/$deviceId/app/$appId?strict')
	driver.command_executor._commands["kill_app"] = ('POST', '/quamotion/device/$deviceId/app/$appId/kill?strict')
	driver.command_executor._commands["set_location"] = ('POST', '/session/$sessionId/location')
	driver.command_executor._commands["get_appId"] = ('GET', '/session/$sessionId/quamotion/appId')
	driver.command_executor._commands["scroll_to"] = ('POST', '/session/$sessionId/element/$elementId/quamotion/scrollTo')
	driver.command_executor._commands["scroll_to_visible"] = ('POST', '/session/$sessionId/element/$elementId/quamotion/scrollToVisible')

def device(deviceId, reuse_existing_session = True, take_screenshots = False):
	ensure_quamotion_running()

	driver = webdriver.Remote(
		command_executor='http://localhost:17894/wd/hub',
		desired_capabilities =
		{
			'waitForReady': True,
			'applicationType': 'Device',
			'deviceId': deviceId,
			'takesScreenshot': take_screenshots,
			'reuseExistingSession': reuse_existing_session
		})
	
	driver.deviceId = deviceId

	add_quamotion_extensions(driver)
	return driver

def web(deviceId, reuse_existing_session = True):
	ensure_quamotion_running()

	driver = webdriver.Remote(
		command_executor='http://localhost:17894/wd/hub',
		desired_capabilities =
		{
			'waitForReady': True,
			'applicationType': 'Web',
			'deviceId': deviceId,
			'takesScreenshot': False,
			'reuseExistingSession': reuse_existing_session
		})
	
	driver.deviceId = deviceId
	driver.w3c = True

	add_quamotion_extensions(driver)
	return driver
	
def home_screen(self):
	return self.execute('homescreen', {} )

def get_installed_apps(self):
	return self.execute('get_installed_apps', { 'deviceId': self.deviceId } )

def get_running_processes(self):
	return self.execute('get_running_processes', { 'deviceId': self.deviceId } )

def launch_app(self, app_id, arguments = [ ]):
	return self.command_executor._request('POST', self.command_executor._url + '/quamotion/device/' + self.deviceId + '/app/' + app_id + '/launch?strict', json.dumps(arguments))

def uninstall_app(self, app_id):
	return self.execute('uninstall_app', { 'deviceId': self.deviceId, 'appId': app_id } )

def kill_app(self, app_id):
	return self.execute('kill_app', { 'deviceId': self.deviceId, 'appId': app_id } )

def set_location(self, latitude, longitude):
	return self.execute('set_location', { 'latitude': latitude, 'longitude': longitude } )

def get_appId(self):
	return self.execute('get_appId', {} )['value']

def scroll_to(self, container_id, xpath):
	return self.execute('scroll_to', { 'elementId': container_id, 'value': xpath, 'using': By.XPATH  } )

def scroll_to_visible(self, element_id):
	return self.execute('scroll_to_visible', {'elementId': element_id} )

webdriver.Remote.home_screen = home_screen
webdriver.Remote.get_installed_apps = get_installed_apps
webdriver.Remote.get_running_processes = get_running_processes
webdriver.Remote.launch_app = launch_app
webdriver.Remote.uninstall_app = uninstall_app
webdriver.Remote.kill_app = kill_app
webdriver.Remote.set_location = set_location
webdriver.Remote.get_appId = get_appId
webdriver.Remote.scroll_to = scroll_to
webdriver.Remote.scroll_to_visible = scroll_to_visible
