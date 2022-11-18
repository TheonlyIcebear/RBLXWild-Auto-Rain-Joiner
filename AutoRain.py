#!/usr/bin/env python -W ignore::DeprecationWarning

import cloudscraper, subprocess, pyautogui, selenium, threading, websocket, requests, random, logging, base64, json, time, ssl, sys, os
from discord_webhook import DiscordWebhook, DiscordEmbed
from websocket import create_connection
from win10toast import ToastNotifier
from CaptchaBypass import Solver
from termcolor import cprint
from random import randbytes
from zipfile import *
from sys import exit


class main:
	def __init__(self):
		logging.basicConfig(filename="errors.txt", level=logging.DEBUG)
		self.hwid = current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
		self.crashPoints = None
		self.multiplier = 0
		self.version = "1.0.0"
		os.system("")
		try:
			self.getConfig()
			self.JoinRains()
		except KeyboardInterrupt:
			self.print("Exiting program.")
			os._exit(0)
		except Exception as e:
			open("errors.txt", "w+").close()
			now = time.localtime()
			logging.exception(f'A error has occured at {time.strftime("%H:%M:%S %I", now)}')
			self.print("An error has occured check logs.txt for more info", "error")
			time.sleep(2)
			raise
			os._exit(0)

	def print(self, message="", option=None, end="", base=False): # print the ui's text with
		print("[ ", end="")
		if base:
			end = "\r"
		else:
			end = (" "*50)+"\n"
		if not option:
			cprint("AUTORAIN", "cyan", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "cyan", end=end)
		elif option == "error":
			cprint("ERROR", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red", end=end)
		elif option == "warning":
			cprint("WARNING", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow", end=end)
		elif option == "yellow":
			cprint("AUTORAIN", "yellow", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "yellow", end=end)
		elif option == "good":
			cprint("AUTORAIN", "green", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "green", end=end)
		elif option == "bad":
			cprint("AUTORAIN", "red", end="")
			print(" ] ", end="")
			if message:
				cprint(message, "red", end=end)


	def sendwbmsg(self,url,message,title,color,content):
		if "https://" in url:
			data = {
				"content": content,
				"username": "Smart Bet",
				"embeds": [
									{
										"description" : message,
										"title" : title,
										"color" : color
									}
								]
			}
			r = requests.post(url, json=data)

	def clear(self): # Clear the console
		os.system('cls' if os.name == 'nt' else 'clear')


	def installDriver(self, version=None):
		uiprint = self.print
		if not version:
			uiprint("Installing newest chrome driver...", "warning")
			latest_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
		else:
			uiprint(f"Installing version {version} chrome driver...", "warning")
			latest_version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}").text
		download = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip")


		
		subprocess.call('taskkill /im "chromedriver.exe" /f')
		try:
			os.chmod('chromedriver.exe', 0o777)
			os.remove("chromedriver.exe")
		except:
			pass


		with open("chromedriver.zip", "wb") as zip:
			zip.write(download.content)


		with ZipFile("chromedriver.zip", "r") as zip:
			zip.extract("chromedriver.exe")
		os.remove("chromedriver.zip")
		uiprint("Chrome driver installed.", "good")




	def getConfig(self): # Get configuration from config.json file
		uiprint = self.print
		with open("config.json", "r+") as data:
			config = json.load(data)

			try:
				self.ping = config["webhook_ping"]
				self.webhook = DiscordWebhook(url=config["webhook"], content=self.ping)
				self.webhook_enabled = config["webhook_enabled"]
				self.notifications = config["notifications_enabled"]
				self.minimum_amount = float(config["minimum_amount"])
				self.autojoin = config["auto_join"]
				self.path = config["tesseract_path"]
				self.key = config["key"]
				self.auth = config["auth"]
				self.cookie = config["cloudflare_cookie"]
			except KeyError as k:
				uiprint(f"Invalid {k} key inside JSON file. Please redownload config from Gitub", "error")
				time.sleep(1.6)
				os._exit(0)


		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("] ", end="")
		print(base64.b64decode(b'V2ViaG9vayBhbmQgTm90aWZjYXRpb24gY29kZSBieSBhbXByb2NvZGUgKGh0dHBzOi8vZ2l0aHViLmNvbS9hbXByb2NvZGUvQmxveGZsaXAtcmFpbi1ub3RpZmllcik=').decode('utf-8'))
		print("[", end="")
		cprint(base64.b64decode(b'IENSRURJVFMg').decode('utf-8'), "cyan", end="")
		print("] ", end="")
		print(base64.b64decode(b'QXV0byBKb2luZXIgYnkgSWNlIEJlYXIjMDE2Nw==').decode('utf-8'))
		time.sleep(3)
		self.clear()

		self.headers = {
			"x-auth-token": self.auth
		}

		try:
			self.ws = self.Connect(self.cookie)
		except websocket._exceptions.WebSocketBadStatusException as w:
			uiprint("Invalid cookie!", "error")
			time.sleep(3.2)
			os._exit(0)
		ws = self.ws

		j = {"authToken":self.auth,"clientTime":round(time.time()*(10**3))}
		j = str(j).replace("'", '"').replace(" ", "")

		ws.send("40")
		ws.recv()
		while True:
			ws.send(f'42["authentication",{j}]')
			recv = ws.recv().replace("42", "").replace("40", "")
			if type(json.loads(recv)) == list:
				break
		rain = json.loads(recv)[1]
		
		self.start = rain["events"]["rain"]["pot"]["createdAt"]
		self.prize = rain["events"]["rain"]["pot"]["prize"]
		time.sleep(0.5)

		
		ws.send('42["chat:subscribe",{"channel":"EN"}]')
		ws.send('42["livefeed:subscribe"]')
		
	def Connect(self, cookie):
		return create_connection("wss://rblxwild.com/socket.io/?EIO=4&transport=websocket",
								header={
										"Host": "rblxwild.com",
										"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
										"Accept": "*/*",
										"Accept-Language": "en-US,en;q=0.5",
										"Accept-Encoding": "gzip, deflate, br",
										"Sec-WebSocket-Version": "13",
										"Origin": "https://rblxwild.com",
										"Sec-WebSocket-Extensions": "permessage-deflate",
										"Sec-WebSocket-Key": str(base64.b64encode(randbytes(16)).decode('utf-8')),
										"Connection": "keep-alive, Upgrade",
										"Cookie": cookie,
										"Sec-Fetch-Dest": "websocket",
										"Sec-Fetch-Mode": "websocket",
										"Sec-Fetch-Site": "same-origin",
										"Pragma": "no-cache",
										"Cache-Control": "no-cache",
										"Upgrade": "websocket",
				}, sslopt={"cert_reqs": ssl.CERT_NONE},
				suppress_origin=True,
			)

	def JoinRains(self):
		webhook_enabled = self.webhook_enabled
		notifications = self.notifications
		autojoin = self.autojoin
		webhook = self.webhook
		headers = self.headers
		uiprint = self.print
		start = self.start
		prize = self.prize
		path = self.path
		key = self.key
		ws = self.ws

		realclass = None
		uiprint("Program started. Press Ctrl + C to exit")
		uiprint(base=True)


		while True:
			try:
				msg = json.loads(ws.recv().replace("42", ""))
			except json.decoder.JSONDecodeError as j:
				continue

			if msg == 2:
				ws.send("3")
				continue

			if not msg[0] == "events:rain:updatePotVariables":
				continue
			
			while True:
				request = requests.get("https://bfpredictor.repl.co/rain", 
											data={"key": key, 
												  "hwid": self.hwid,
												  "start": start
											}, headers=headers
										)
				
				# timeleft = 30 - ((round(time.time())-self.start)/60)

				if request.status_code == 403:
					uiprint("Invalid key! To buy a valid key create a ticket on the discord. https://discord.gg/blox", "error")
					input("Press enter to exit >> ")

					os._exit(0)
				elif request.status_code == 500:
					uiprint("Internal server error. Trying again 1.5 seconds...", "error")
					time.sleep(1.5)
				elif request.status_code == 200:
					timeleft = round(float(request.text), 2)
					break
				else:
					uiprint("Internal server error. Trying again 1.5 seconds...", "error")
					time.sleep(1.5)

			timeleft = 30 - ((round(time.time())-self.start)/60)
			if timeleft > 2:
				prize = msg[1]["newPrize"]
				sys.stdout.write("\033[K")
				cprint(f"Timleft: {round(timeleft)} minutes, Prize: {prize}"+(" "*50), "cyan", end="\r")
				continue
			else:
				cprint("", end="\r")

			duration = timeleft
			sent = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(int(time.time())))
			uiprint(f"RBLXWild Rain!", "green")
			uiprint(f"Rain amount: {prize} R$", "yellow")
			uiprint(f"Expiration: {duration} minutes", "yellow")
			uiprint(f"Host: RBLXwild", "yellow")
			uiprint(f"Timestamp: {sent}", "yellow")
			if notifications: 
				ToastNotifier().show_toast("RBLXWild Rain!", f"Rain amount: {prize} R$\nExpiration: {duration} minutes\nHost: RBLXwild\n\n", icon_path="assets/Bloxflip.ico", duration=10)

			userid = requests.get(f"https://api.roblox.com/users/get-by-username?username=RBLXwild").json()['Id']
			thumburl = (f"https://www.roblox.com/headshot-thumbnail/image?userId={userid}&height=50&width=50&format=png")
			if webhook_enabled:
				try:
					embed = DiscordEmbed(title=f"RBLXwild is hosting a chat rain!", url="https://rblxwild.com", color=0xFFC800)
					embed.add_embed_field(name="Rain Amount", value=f"{prize} R$")
					embed.add_embed_field(name="Expiration", value=f"{duration} minutes")
					embed.add_embed_field(name="Host", value=f"[RBLXwild](https://rblxwild.com)")
					embed.set_timestamp()
					embed.set_thumbnail(url=thumburl)
					webhook.add_embed(embed)
					webhook.execute()
					webhook.remove_embed(0)
				except:
					pass

			if autojoin:
				uiprint("Joining rain...")
				start = pyautogui.locateCenterOnScreen('assets/Join.png', confidence = 0.7)
				if not start:
					uiprint("Join rain button not found. Opening RBLXWild now...", "warning")
					subprocess.call("start https://rblxwild.com",shell=True)
					time.sleep(5)
				while True:
					start = pyautogui.locateCenterOnScreen('assets/Join.png', confidence = 0.7)
					if start:
						pyautogui.moveTo(*start,0.5)
						pyautogui.click()
						Solver(path, key)
						uiprint("Joined rain successfully!", "good")

					else:
						uiprint("Failed to locate button even after site opened.", "error")
						time.sleep(5)
						continue

					break

			time.sleep(timeleft)


if __name__ == "__main__":
	main()