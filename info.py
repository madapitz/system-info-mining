import socket
import subprocess
import platform
import re
import uuid
import psutil
import os
import netifaces
import gpuinfo
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
		return subprocess.check_output(['wmic', 'bios', 'get', 'serialnumber' ])

def getManufacturer(os):
	if os == 'Linux':
		return subprocess.check_output(['sudo', 'dmidecode', '-s', 'system-manufacturer' ]).decode("utf-8").strip('\n')
	elif os == 'Windows':
		return 'por investigar'

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

#solo para windows
def getSP():
	return platform.win32_ver().csd

def getMAC():
	return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getRAMInfo():
	#hacer version para windows
	ramname = subprocess.check_output(['sudo', 'dmidecode', '-t', '17']).decode("utf-8").strip('\n')
	info = {
		'nombre': re.findall('DDR', ramname)[0] + ramname[810],
		'total':psutil.virtual_memory().total / 1048576,
		'unidad': 'MB',
		'tipo': 'RAM',
		'disponible': psutil.virtual_memory().available / 1048576
	}

	return info

def getHardDiskInfo():
	#os.getenv("SystemDrive") para windows
	tipo = subprocess.check_output(['cat', '/sys/block/sda/queue/rotational']).decode("utf-8").strip('\n')
	if tipo == '1':
		tipoD = 'HDD'
	else:
		tipoD = 'SDD'

	for i in psutil.disk_partitions():
		if i.mountpoint == '/':
			nombre = i.device
			break

	info = {
		'nombre': nombre,
		'total': psutil.disk_usage('/').total / 1048576,
		'unidad': 'MB',
		'tipo': tipoD,
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
	cap = subprocess.check_output(["lspci", "-vnn"]).decode("utf-8").strip('\n')
	resl = subprocess.check_output(["sudo","lshw", "-C","display"]).decode("utf-8").strip('\n')
	info = {
		'capacidad':re.findall(r"[0-9]..",re.findall(r"\bsize.*M\b",cap)[1])[0],
		'unidad': 'MB',
		'resolucion': re.split('\s',re.findall(r"\bwidth:.*s\b",resl)[0])[1] + ' ' + re.split('\s',re.findall(r"\bwidth:.*s\b",resl)[0])[2]
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

def getAllInstalledApps(so):
	#2191
	if so == "Linux":
		AppName = []

		cache = apt.Cache()

		for mypkg in cache:
		    if cache[mypkg.name].is_installed:
		        AppName.append(mypkg.name)
		
		return AppName

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
	f = open('info.txt','a')
	f.write('\nImpresoras:\n')
	if pr != None:
		for x in pr:
			f.write('puerto: ' + x['puerto'] + '\n')
			f.write('driver: ' + x['driver'] + '\n')
			f.write('-------\n')

def exportInstalledApps():
	apps = getAllInstalledApps(platform.system())
	f = open('info.txt','a')
	f.write('\nSoftware:\n')
	for x in apps:
		f.write('nombre: ' + x + '\n')
		f.write('-------\n')

def exportAllInfo():
	exportSystemInfo()
	exportMemoryInfo()
	exportNetworkI()
	exportGPUInfo()
	exportPrintersInfo()
	exportInstalledApps()

if __name__ == '__main__':
	#grep " install" /var/log/dpkg.log*
	exportAllInfo()
	