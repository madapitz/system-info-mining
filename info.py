import socket
import subprocess
import platform
import re
import uuid
import psutil
import os
import netifaces
import cpuinfo
if platform.system() == 'Linux':
	import apt

def getHostName():
	hostname = socket.gethostname()
	return hostname

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def getSerialNumber(os):
	if os == 'Linux':
		#se requieren permisos de administrador
		return subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-serial-number' ]).decode("utf-8").strip('\n')
	elif os == 'Windows':
		#si retorna 0 es culpa del fabricante de la maquina
		sn = subprocess.check_output(['wmic', 'bios', 'get', 'serialnumber' ]).decode("utf-8").strip('\r\r\n')
		return re.findall(r'[^SerialNumber\r\n ].*\w\S',sn)[0]

def getManufacturer(os):
	if os == 'Linux':
		return "Canonical Ltd"
	elif os == 'Windows':
		# manu = subprocess.check_output(['wmic', 'computersystem', 'get', 'manufacturer']).decode("utf-8").strip('\n')
		return "Microsoft"

def getOS():
	return platform.system()

def getOSVersion(os):
	if os == "Linux":
		return platform.dist()[1]
	elif os == 'Windows':
		return platform.version()

def getModel(os):
	if os == 'Linux':
		return subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-version' ]).decode("utf-8").strip('\n')
	elif os == 'Windows':
		model = subprocess.check_output(['wmic', 'computersystem', 'get', 'model']).decode("utf-8").strip('\n')
		return re.findall(r'[^Model\r\n ].*\w\S',model)[0]

#solo para windows
def getSP():
	return platform.win32_ver()[2]

def getMAC():
	return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getRAMInfo():
	#hacer version para windows
	if platform.system() == 'Linux':
		ramname = subprocess.check_output(['sudo', 'dmidecode', '-t', '17']).decode("utf-8").strip('\n')
		info = {
			'nombre': re.findall('DDR', ramname)[0] + ramname[810],
			'total':psutil.virtual_memory().total / 1048576,
			'unidad': 'MB',
			'tipo': 'RAM',
			'disponible': psutil.virtual_memory().available / 1048576
		}

		return info
	elif platform.system() == 'Windows':
		ram = subprocess.check_output(['wmic','memorychip','get','MemoryType']).decode("utf-8").strip(' \r\n')

		info = {
			'nombre': re.findall(r'[^MemoryType\r\n ].*\S',ram)[0],
			'total':psutil.virtual_memory().total / 1048576,
			'unidad': 'MB',
			'tipo': 'RAM',
			'disponible': psutil.virtual_memory().available / 1048576
		}

		return info

def getHardDiskInfo():
	#os.getenv("SystemDrive") para windows
	if platform.system() == 'Linux':
		tipo = subprocess.check_output(['cat', '/sys/block/sda/queue/rotational']).decode("utf-8").strip('\n')
		if tipo == '1':
			tipoD = 'HDD'
		else:
			tipoD = 'SDD'
	elif platform.system() == 'Windows':
		tipo = subprocess.check_output(['wmic', 'diskdrive', 'get', 'caption']).decode("utf-8").strip('\n')
		gold = re.findall(r'[SDD|HDD]',tipo)[0]
		if gold == []:
			tipoD = 'unknown'
		else:
			tipoD = gold

	for i in psutil.disk_partitions():
		if i.mountpoint == '/':
			nombre = i.device
			break
		else:
			nombre = '/'

	info = {
		'nombre': psutil.disk_partitions()[0].device,
		'total': psutil.disk_usage('/').total / 1048576,
		'unidad': 'MB',
		'tipo': 'HDD',
		'disponible': psutil.disk_usage('/').free / 1048576
	}

	return info

def getNetworkInterfaces():
	infoArray = []
	interfaces = netifaces.interfaces()
	for i in interfaces:
		info = {}
		try:
			info = {
				'nombre': i,
				'ip': netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
			}
			
		except Exception as e:
			info = {
				'nombre': i,
				'ip': netifaces.ifaddresses(i)[netifaces.AF_LINK][0]['addr']
			}
		finally:
			if netifaces.gateways()['default'][netifaces.AF_INET][1] == info['nombre']:
				info['gateway'] = netifaces.gateways()['default'][netifaces.AF_INET][0]
			else:
				info['gateway'] = 'none'
			
			infoArray.append(info)

	return infoArray

def getGPUinfo():
	#hacer version de windows
	if platform.system() == 'Linux':
		cap = subprocess.check_output(["lspci", "-vnn"]).decode("utf-8").strip('\n')
		resl = subprocess.check_output(["sudo","lshw", "-C","display"]).decode("utf-8").strip('\n')
		info = {
			'capacidad':re.findall(r"[0-9]..",re.findall(r"\bsize.*M\b",cap)[1])[0],
			'unidad': 'MB',
			'resolucion': re.split('\s',re.findall(r"\bwidth:.*s\b",resl)[0])[1] + ' ' + re.split('\s',re.findall(r"\bwidth:.*s\b",resl)[0])[2]
		}

		return info
	elif platform.system() == 'Windows':
		precap = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "adapterram"]).decode("utf-8").strip('\n')
		cap = re.findall(r'[^AdapterRam\r\n ].*\w\S',precap)[0]
		preresl = subprocess.check_output(["wmic", "path", "win32_VideoController", "get", "currentverticalresolution"]).decode("utf-8").strip('\n')
		resl = re.findall(r'[^CurrentVerticalResolution\r\n ].*\w\S',preresl)[0]
		info = {
			'capacidad':str(int(cap)/1048576),
			'unidad': 'MB',
			'resolucion': resl
		}

		return info

def getPrinters(so):
	if so == 'Linux':
		printers = subprocess.check_output(["lpstat", "-t"]).decode("utf-8").strip('\n')
		ports = re.findall(r'usb|smb', printers)

		prList = []
		for x in ports:
			prList.append({
				'puerto': x,
				'driver': 'none'
				})

		return prList
	elif so == 'Windows':
		prList = []
		preport = subprocess.check_output(["wmic", "printer","get", "portname"]).decode("utf-8").strip('\n')
		ports = re.findall(r'[^PortNameXPSPortHRFAXnul\r\n ].*\w\S',preport)
		print(ports)
		pred = subprocess.check_output(["wmic", "printer","get", "drivername"]).decode("utf-8").strip('\n')
		drivers = re.findall(r'[^DriverName\r\n ].*\w\S',pred)
		print(drivers)
		for x in drivers:
			prList.append({
				'puerto': 'none',
				'driver': x
				})
		
		if len(drivers) > 3:
			for y in range(3,len(drivers)):
				if y - 3 < len(ports):
					prList[y]['puerto'] = ports[y - 3]


		return prList

def getProcessorInfo():
	proc = cpuinfo.get_cpu_info()

	info = {
		'nombre': proc['brand'],
		'fabricante': proc['vendor_id'],
		'cache': proc['l2_cache_size'],
		'vreloj': proc['hz_actual'],
		'nucleos': str(proc['count'])
	}

	return info

def getAllInstalledApps(so):
	#2191
	# nombre, categoria, clave, fecha inst, fabricante
	if so == "Linux":
		AppName = []

		cache = apt.Cache()

		for mypkg in cache:
		    if cache[mypkg.name].is_installed:
		        AppName.append(mypkg.name)
		
		return AppName
	elif so == "Windows":
		app = []
		name = []
		clave = []
		fecha = []
		vendor = []
		try:
			nm = subprocess.check_output(["wmic", "product","get", "name"]).decode("utf-8").strip('\n')
			name = re.findall(r'[^Name\r\n ].*\w\S',nm)
			cv = subprocess.check_output(["wmic", "product","get", "IdentifyingNumber"]).decode("utf-8").strip('\n')
			clave = re.findall(r'[^IdentifyingNumber\r\n ].*\w\S',cv)
			fi = subprocess.check_output(["wmic", "product","get", "installdate"]).decode("utf-8").strip('\n')
			fecha = re.findall(r'[^InstallDate\r\n ].*\w\S',fi)
			vd = subprocess.check_output(["wmic", "product","get", "vendor"]).decode("utf-8").strip('\n')
			vendor = re.findall(r'[^Vendor\r\n ].*\w\S',vd)
		except Exception as e:
			# nm = subprocess.check_output(["wmic", "product","get", "name"]).decode("utf-16").strip('\n')
			# name = re.findall(r'[^Name\r\n ].*\w\S',nm)
			# cv = subprocess.check_output(["wmic", "product","get", "IdentifyingNumber"]).decode("utf-16").strip('\n')
			# clave = re.findall(r'[^IdentifyingNumber\r\n ].*\w\S',cv)
			# fi = subprocess.check_output(["wmic", "product","get", "installdate"]).decode("utf-16").strip('\n')
			# fecha = re.findall(r'[^InstallDate\r\n ].*\w\S',fi)
			# vd = subprocess.check_output(["wmic", "product","get", "vendor"]).decode("utf-16").strip('\n')
			# vendor = re.findall(r'[^Vendor\r\n ].*\w\S',vd)
			pass

		if len(name) != 0:
			for x in range(0,len(name)-1):
				app.append({
					'nombre':name[x],
					'clave':clave[x],
					'fecha': fecha[x],
					'fabricante': vendor[x]
					})

		return app

def exportSystemInfo():
	f = open('info.txt','w')
	f.write('Datos del equipo:\n')
	f.write('nombre: ' + getHostName() + '\n')
	f.write('ip: ' + get_ip() + '\n')
	f.write('modelo: ' + getModel(platform.system()) + '\n')
	f.write('numero serial: ' + getSerialNumber(platform.system()) + '\n')
	f.write('sistema operativo: ' + getOS() + '\n')
	f.write('version: ' + getOSVersion(platform.system()) + '\n')
	if getOS() == 'Windows':
		f.write('sp: ' + getSP() + '\n')
	f.write('fabricante so: ' + getManufacturer(platform.system()) + '\n')
	f.write('mac: ' + getMAC() + '\n')

def exportMemoryInfo():
	ram = getRAMInfo()
	hd = getHardDiskInfo()
	f = open('info.txt','a')
	f.write('\nMemoria:\n')
	f.write('nombre: ' + ram["nombre"] + '\n')
	f.write('total: ' + str(ram["total"]) + '\n')
	f.write('unidad: ' + ram["unidad"] + '\n')
	f.write('tipo: ' + ram["tipo"] + '\n')
	f.write('disponible: ' + str(ram["disponible"]) + '\n')
	f.write('-------\n')
	f.write('nombre: ' + hd["nombre"] + '\n')
	f.write('total: ' + str(hd["total"]) + '\n')
	f.write('unidad: ' + hd["unidad"] + '\n')
	f.write('tipo: ' + hd["tipo"] + '\n')
	f.write('disponible: ' + str(hd["disponible"]) + '\n')

def exportNetworkI():
	ni = getNetworkInterfaces()
	f = open('info.txt','a')
	f.write('\nAdaptadores de red:\n')
	for x in ni:
		f.write('nombre: ' + x['nombre'] + '\n')
		f.write('ip: ' + x['ip'] + '\n')
		f.write('gateway: ' + x['gateway'] + '\n')
		f.write('-------\n')

def exportGPUInfo():
	gpu = getGPUinfo()
	f = open('info.txt','a')
	f.write('\nTarjeta de video:\n')
	f.write('capacidad: ' + gpu['capacidad'] + '\n')
	f.write('unidad: ' + gpu['unidad'] + '\n')
	f.write('resolucion: ' + gpu['resolucion'] + '\n')

def exportPrintersInfo():
	pr = getPrinters(platform.system)
	print(pr)
	f = open('info.txt','a')
	f.write('\nImpresoras:\n')
	if pr != None:
		for x in pr:
			f.write('puerto: ' + x['puerto'] + '\n')
			f.write('driver: ' + x['driver'] + '\n')
			f.write('-------\n')

def exportProcessorInfo():
	proc = getProcessorInfo()
	f = open('info.txt','a')
	f.write('\nProcesador:\n')
	f.write('nombre: ' + proc['nombre'] + '\n')
	f.write('fabricante: ' + proc['fabricante'] + '\n')
	f.write('cache: ' + proc['cache'] + '\n')
	f.write('velocidad de reloj: ' + proc['vreloj'] + '\n')
	f.write('nucleos: ' + proc['nucleos'] + '\n')
	f.write('-------\n')

def exportInstalledApps():
	apps = getAllInstalledApps(platform.system())
	f = open('info.txt','a')
	f.write('\nSoftware:\n')
	if platform.system() == 'Linux':
		for x in apps:
			f.write('nombre: ' + x + '\n')
			f.write('-------\n')
	elif platform.system() == 'Windows':
		for x in apps:
			f.write('nombre: ' + x['nombre'] + '\n')
			f.write('clave: ' + x['clave'] + '\n')
			f.write('fecha instalacion: ' + x['fecha'] + '\n')
			f.write('fabricante: ' + x['fabricante'] + '\n')
			f.write('-------\n')

def exportAllInfo():
	exportSystemInfo()
	exportMemoryInfo()
	exportNetworkI()
	exportGPUInfo()
	exportPrintersInfo()
	exportProcessorInfo()
	exportInstalledApps()

if __name__ == '__main__':
	#grep " install" /var/log/dpkg.log*
	#wmic computersystem get model
	exportAllInfo()