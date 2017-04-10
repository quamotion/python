import requests
from selenium import webdriver

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
	
def device(deviceId, reuse_existing_session = True):
	ensure_quamotion_running()

	driver = webdriver.Remote(
		command_executor='http://localhost:17894/wd/hub',
		desired_capabilities =
		{
			'waitForReady': True,
			'applicationType': 'Device',
			'deviceId': deviceId,
			'takesScreenshot': False,
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
	return self.execute('homescreen', {})

def get_installed_apps(self):
	return self.execute('get_installed_apps', { 'deviceId': self.deviceId } )

def get_running_processes(self):
	return self.execute('get_running_processes', { 'deviceId': self.deviceId } )

def launch_app(self, app_id):
	return self.execute('launch_app', { 'deviceId': self.deviceId, 'appId': app_id } )

def uninstall_app(self, app_id):
	return self.execute('uninstall_app', { 'deviceId': self.deviceId, 'appId': app_id } )

def kill_app(self, app_id):
	return self.execute('kill_app', { 'deviceId': self.deviceId, 'appId': app_id } )

webdriver.Remote.home_screen = home_screen
webdriver.Remote.get_installed_apps = get_installed_apps
webdriver.Remote.get_running_processes = get_running_processes
webdriver.Remote.launch_app = launch_app
webdriver.Remote.uninstall_app = uninstall_app
webdriver.Remote.kill_app = kill_app

