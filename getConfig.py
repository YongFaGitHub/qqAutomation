import os, sys
import configparser

#读取配置文件
def ReadConfig(confname,key,code): 
	data=''
	cfg = configparser.RawConfigParser()
	
	if not os.path.exists(confname):
		input(confname + '没有找到，请检查路径是否正确')
		sys.exit(-1)
	with open(confname, mode='rb') as f:
		content = f.read()
	if content.startswith(b'\xef\xbb\xbf'):     # 去掉 utf8 bom 头
		content = content[3:]
	cfg.read_string(content.decode('utf8'))
	if not cfg.sections():
		input('读取配置文件失败')
		sys.exit(-1)
		 
	SrcRoot = cfg.get(key, code).strip()
	return SrcRoot

#读取文本文件
def getText(filename):
    data=[]
    with open(filename,encoding='UTF-8') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            pass
            listData = []
            for i in lines.split():
                listData.append(i)
            pass
            data.append(listData)
			
    return data
def setText(filename,user,area,status):
	#将文件读取到内存中
	with open(filename,"r",encoding="utf-8") as f:
		lines = f.readlines() 
	#写的方式打开文件
	with open(filename,"w",encoding="utf-8") as f_w:
		for line in lines:
			if user in line:
			#替换
				line = line.replace(area,area+" ----"+status)
				print(line)
			f_w.write(line)
def setText2(filename,user,password,area,status):
	#将文件读取到内存中
	with open(filename,"r",encoding="utf-8") as f:
		lines = f.readlines() 
	#写的方式打开文件
	with open(filename,"w",encoding="utf-8") as f_w:
		line = (user," ",password," ",area+" ----"+status)
		print(line)
		f_w.write(str(line))
