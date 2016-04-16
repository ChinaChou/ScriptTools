#!/usr/bin/python
#coding:utf-8
import sys,paramiko,time,logging
from os.path import basename

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
try:
    groupName = sys.argv[1]
    serviceName = sys.argv[2]
    newWar = sys.argv[3]
except Exception,e:
    logging.error('Usage: bsyDeploy.py [nop|app|mgmt|preapp] [bms|mss1|mss2|pop...] /path/to/example.war')
    sys.exit(199)

data = {
    'nop':{
        'ip':['10.10.10.141','10.10.10.143','10.10.10.145'],
        'nss':{'releaseName':'abl-nss-web'},
        'oas':{'releaseName':'abl-oas-web'},
        'pop':{'releaseName':'bsy-pop-web'}            
        },
    'app':{
        'ip':['10.10.10.101','10.10.10.103','10.10.10.105'],
        'mss1':{'releaseName':'bsy-mss-web'},
        'mss2':{'releaseName':'bsy-mss-web'},
        'sms':{'releaseName':'abl-sms-web'},
        'crm':{'releaseName':'bsy-crm-web'},
        'mds':{'releaseName':'bsy-mds-web'}
    },
    'mgmt':{
        'ip':['10.10.10.150'],
        'bms':{'releaseName':'abl-bms-web'},
        'cms':{'releaseName':'abl-cms-web'}
    },
    'preapp':{
        'ip':['10.10.10.151'],
        'bms':{'releaseName':'abl-bms-web'},
        'cms':{'releaseName':'abl-cms-web'},
        'mss':{'releaseName':'bsy-mss-web'},
        'sms':{'releaseName':'abl-sms-web'},
        'sso':{'releaseName':'abl-sso-web'},
        'pop':{'releaseName':'bsy-pop-web'},
        'crm':{'releaseName':'bsy-crm-web'},
        'mds':{'releaseName':'bsy-mds-web'}
    }
}

if groupName not in data or serviceName not in data[groupName]:
    logging.error("Argument Errror! {0} doesn't exist OR {1} not in {2}".format(groupName,serviceName,groupName))
    sys.exit(198)

username = 'test'
port = 22
pkey = paramiko.RSAKey.from_private_key_file('/home/test/.ssh/id_rsa')
releaseName = data[groupName][serviceName]['releaseName']
releaseDir = '/usr/local/{0}/webapps/{1}'.format(serviceName,releaseName)
uploadedFile = '/tmp/{0}.war'.format(releaseName)
dstFile = releaseDir+'.war'
stopCmd = 'sudo service {0} stop'.format(serviceName)
startCmd = 'sudo service {0} start'.format(serviceName)
rmCmd = 'sudo rm -rf {0} {1}'.format(releaseDir,dstFile)
mvCmd = 'sudo mv {0} {1}'.format(uploadedFile,dstFile)
servers = data[groupName]['ip']

oldWar = releaseName+'.war'
selectedWar = basename(newWar)
if oldWar != selectedWar:
    logging.error("Fatal Error: You want to deploy {0},but select {1}".format(serviceName,selectedWar))
    sys.exit(250)

for ip in servers:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,port,pkey=pkey)
    except Exception,e:
        logging.error(e)
        sys.exit(200)

    try:
        tunnel = paramiko.Transport((ip,port))
        tunnel.connect(username=username,pkey=pkey)
        sftp = paramiko.SFTPClient.from_transport(tunnel)
    except Exception,e:
        logging.error(e)
        sys.exit(201)

    #stop tomcat
    logging.info("Stopping {0} service".format(serviceName))
    stdin,stdout,stdin = ssh.exec_command(stopCmd)
    time.sleep(10)
    #Delete old war files
    stdin,stdout,stderr = ssh.exec_command(rmCmd)
    err = stderr.read()
    if err:
        print err
        logging.error('Failed to rm old war files on {0}'.format(ip))
        sys.exit(202)
    #upload new war package to the destination server
    logging.info("Upload {0} to {1}".format(newWar,ip))
    sftp.put(newWar,uploadedFile)
    stdin,stdout,stderr = ssh.exec_command(mvCmd)
    err = stderr.read()
    if err:
        logging.error('Failed to exec {0}'.format(mvCmd))
        sys.exit(203)
    #start tomcat
    logging.info("Starting {0} service".format(serviceName))
    stdin,stdout,stderr = ssh.exec_command(startCmd)
    err = stderr.read()
    if err:
        logging.error('Failed to start {} service on {}'.format(serviceName,ip))
        logging.error(err)
        sys.exit(204)

    sftp.close()
    tunnel.close()
    ssh.close()
    logging.info('Successfully deployed {0} on {1}'.format(serviceName,ip))