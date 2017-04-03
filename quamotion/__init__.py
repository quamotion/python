from selenium import webdriver

def device(deviceId):
	driver = webdriver.Remote(
		command_executor='http://localhost:17894/wd/hub',
		desired_capabilities =
		{
			'waitForReady': True,
			'applicationType': 'Device',
			'deviceId': deviceId
		})

        driver.command_executor._commands["homescreen"] = ('POST', '/session/$sessionId/wda/homescreen')
        driver.command_executor._commands["get_installed_apps"] = ('GET', '/quamotion/device/$deviceId/app?strict')
        driver.command_executor._commands["get_running_processes"] = ('GET', '/quamotion/device/$deviceId/process?strict')
        
        driver.deviceId = deviceId

        return driver

def home_screen(self):
        return self.execute('homescreen', {})

def get_installed_apps(self):
        return self.execute('get_installed_apps', { 'deviceId': self.deviceId } )

def get_running_processes(self):
        return self.execute('get_running_processes', { 'deviceId': self.deviceId } )

webdriver.Remote.home_screen = home_screen

webdriver.Remote.get_installed_apps = get_installed_apps

webdriver.Remote.get_running_processes = get_running_processes

