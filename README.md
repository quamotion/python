# Automating iOS and Android Devices with the Quamotion Webdriver and Python

This repository contains a couple of guides on how to use the [Quamotion WebDriver](http://quamotion.mobi) to
automate iOS and Android devices with Python.

The Quamotion WebDriver provides, for iOS and Android:
- Full UI-level device automation. This includes automating operating system
  applications such as the Camera, applications from the App store, and browsers.
- High performance screen capturing.
- Installing, listing and uninstalling applications from application packages
  (`.apk` or `.ipa` files,...)
- Starting, enumerating and stopping all processes running on the device
- Mocking GPS coordinates
- Resigning of iOS applications using an Apple developer profile
- All this using a Windows, Linux or macOS machine and a USB cable

## Getting started

To automate iOS and Android device with Python, you'll need Python 3.x and the selenium Python package.

Install it using:

```
pip install selenium
```

We'll assume you've already downloaded and configured the Quamotion WebDriver.

## Installing an application from the App Store

In this example, we'll install an application from the App Store on your iOS device.

To achieve this, create an device automation session. Make sure to replace `72157b76f677f22c98864d62307fdff9d56fa62a`
with the UDID of your iOS device!

```python
from selenium import webdriver
driver = webdriver.Remote(
	command_executor='http://localhost:17894/wd/hub',
	desired_capabilities =
	{
		'waitForReady': True,
		'applicationType': 'Device',
		'deviceId': '72157b76f677f22c98864d62307fdff9d56fa62a'
	})
```

Once this step has completed (it may take a minute or two if this is the first time you're automating on this device),
you will be able to remotely control your iOS device.

Let's configure how we are going to automate the device. One concepts in device automation is that of 'implicit waits'; that is,
how long the WebDriver will attempt to locate an element, if you've asked it to find one.

By default, the implicit timeout is 0. That means the WebDriver will not wait for an element to appear, and just let you know
it could not find it. It may make sense to change this. For example, when you're walking through the UI of an application,
it make 100 or 200 milliseconds before the next button on which you want to click appears.

Let's set the implicit wait to 6000 milliseconds, or one minute:

```python
driver.implicitly_wait(60000)
```

Before we start automating the device, let's make sure we're in a known state and navigate to the start screen:

```python
driver.command_executor._commands["homescreen"] = ('POST', '/session/$sessionId/wda/homescreen')
driver.execute('homescreen', {})
```

Next, let's launch Safari:

```python
driver.find_element_by_link_text('Safari').click()
```

Depending on how Safari has been launched, you may either see the '' button at the top of the page, or the URL of the current location.
Depending on the scenario, run the following command:

```python
driver.find_element_by_xpath("//XCUIElementTypeButton[@value='Search or enter website name']").click()
```

or

```python
driver.find_element_by_name('URL').click()
```

The URL field will now be editable. So let's remove whatever text is being displayed there, and enter the URL
of the application we want to search for in the App Store:

```python
urlTextField = driver.find_element_by_class_name('XCUIElementTypeTextField')
urlTextField.clear();
urlTextField.send_keys('itms-apps://itunes.apple.com/us/app/apple-store/id304878510')
urlTextField.send_keys('\n')
```

This will show us a pop up, asking us whether we want to go to the App Store or not. Let's accept that alert:

```python
driver.switch_to_alert().accept()
```

You may get additional alerts, which you'll have to accept one by one.

Finally, it's time to purchase, install and launch the application. If you have previously purchased or installed
the application, some of the buttons may not be visible to you.

```python
driver.find_element_by_xpath("//XCUIElementTypeButton[@label='GET']").click()
driver.find_element_by_xpath("//XCUIElementTypeButton[@label='INSTALL']").click()
driver.find_element_by_xpath("//XCUIElementTypeButton[@label='OPEN']").click()
```

When Skype launches, you may get some additional alerts. You can accept them one by one, just like before:

```python
driver.switch_to_alert().accept()
```
