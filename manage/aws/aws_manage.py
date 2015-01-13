'''
============
aws manager
============

1. all you need is an AWS account

2. then with pip install:
* fabric
* boto

uses boto and fabric to easily manage aws instances

============
further info
============

standard ssh login works like this
#ssh -i mykey.pem ec2-user@ec2-23-20-241-197.compute-1.amazonaws.com


you might want to redirect port 80 to 8080 like this
#redirect port
#sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
'''

import os

from boto import ec2
import mysettings

from pprint import pprint

from fabric.api import env
from fabric.api import sudo, run, put
from fabric.exceptions import NetworkError

from fabric.api import *
from time import sleep

import argparse
import getopt
import sys
import time

import sys

try:
    from mysettings import AWS
    from mysettings import remote_dir
    from mysettings import APP
    from mysettings import github_user
    print 'remote_dir',remote_dir
except:
    print """Error: You need to create a myettings.py file
                 with your amazon secret variables!"""
    sys.exit(1)


def create_instance():
    """ Create an Amazon Instance """
    print 'firing up an instance'
    ec2conn = get_conn()

    reservation = ec2conn.run_instances('ami-aecd60c7', instance_type='t1.micro', key_name='bckey')


    #print mysettings.SERVER
    reservation = ec2conn.run_instances(mysettings.SERVER)
    print reservation
    instance = reservation.instances[0]
    time.sleep(1)
    while instance.state != 'running':
        time.sleep(5)
        instance.update()
        print "Instance state: %s" % (instance.state)

    # Sleep for a bit more before trying to connect
    print 'waiting some more to initalize'
    time.sleep(60)

    print "instance %s done!" % (instance.id)

    return instance



def set_env(ipa):
    env.hosts = [ipa]
    env.user = 'ubuntu'
    print mysettings.AWS["secrets"]["aws_key_path"]
    env.key_filename = mysettings.AWS["secrets"]["aws_key_path"]
    print env.key_filename
    env.host_string = env.user + "@%s" % (ipa)
    #hs = 'ec2-107-20-62-157.compute-1.amazonaws.com'
    #env.host_string = "ec2-user@%s" % (hs)


def install_web(ipa):
    set_env(ipa)

    #sudo('yum install git')
    #sudo('yum install numpy')
    #sudo('pip install scipy')
    #sudo('pip install f2py')


    #install pip first
    make_install = False
    if make_install:
      sudo('curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py')
      run('python get-pip.py')

      #now pip install all the requirements (you might want to install gunicorn/ nginx for real web apps)
      put('requirements.txt', remote_dir)
      sudo('pip install -r %s/requirements.txt' % (remote_dir))

    put(appname,remote_dir)


def checkout_github():
    ''' check out a github repo to the server '''
    github_fingerprint = "github.com,ABC ssh-rsa ..."

    sudo(""" echo '%s' >> .ssh/known_hosts """ % github_fingerprint , pty=True)
    put("ssh-config", ".ssh/config", mode=0600)
    put('keys/deploy_key', '.ssh/', mode=0600)
    run('git clone github:%s %s' % (settings.REPO, remote_code_dir) )


def runapp(ipa):
    ''' run the python app on the AWS server '''
    set_env(ipa)
    #redirect 8080 to 80
    #sudo('iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080')
    #appname = mysettings['APP']['appname']
    #appname = './possiplex/app.py'
    sudo('cd app/')
    appname = "app.py"
    sudo('nohup python ' + appname + ' >& /dev/null < /dev/null &')


def copy_file(ipa,from_file,to_file):
    ''' copy a file to the server '''
    #print mysettings
    set_env(ipa)
    put(from_file,to_file)

def copy(ipa,from_dir):
    ''' copy a file to the server '''
    #print mysettings
    set_env(ipa)

    #sudo('mkdir webwiz')

    global remote_dir


    from_dir_root_name = from_dir.split('/')[-2]
    to_dir = remote_dir + from_dir_root_name

    print 'from : ',from_dir
    print 'to: ',to_dir
    #from_dir_root_name

    #fromf = os.path.join(from_dir,'app.py')
    #tof = os.path.join(to_dir,'app.py')
    #print tof
    put(from_dir,to_dir)



def get_conn():
    ec2conn = ec2.connection.EC2Connection(mysettings.AWS['secrets']['aws_key'], mysettings.AWS['secrets']['aws_secret'])
    return ec2conn

def get_instances():
    ec2conn = get_conn()
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    return instances

def showInstances():
    ''' show running instances '''
    instances = get_instances()

    ips = list()

    for i in instances:
        d = i.__dict__
        #pprint(i.__dict__)
        if i.state=='running':
            print d['dns_name'],' ',d['ip_address']
            #print ('AWS instance %s * ip %s * launched at %s'%(d['dns_name'],d['ip_address'],d['launch_time']))
            ips.append(d['ip_address'])

    print ('number of instances %i'%len(ips))
    #rs = ec2conn.get_all_security_groups()
    #print ('security groups')
    #print (rs)


def get_ips():
    ''' get ips of all running instances '''
    instances = get_instances()

    ips = list()

    for i in instances:
        d = i.__dict__
        if i.state=='running':
            ips.append(d['ip_address'])

    return ips


def get_single_ip():
    ''' get the ip of your running instance '''
    ips = get_ips()
    if len(ips)!=1: raise ValueError

    return ips[0]


def installhello():
    ips = get_ips()
    if len(ips)!=1: return

    ip = ips[0]
    deploy_web(ip)



def stop_all():
    ''' stop all instances '''
    ec2conn = get_conn()
    instances = get_instances()
    for instance in instances:
        iid = instance.__dict__['id']
        print 'deleting ',iid

        while instance.state == 'running':
            ec2conn.terminate_instances(instance_ids=[iid])
            time.sleep(5)
            instance.update()
            print "Instance state: %s" % (instance.state)


def main():

    try:
        optlist, args = getopt.getopt(sys.argv[1:], '')

        if args[0]=='show':
            print 'showing instances'
            showInstances()
        elif args[0]=='create':
            create_instance()
        elif args[0]=='printip':
            get_ip_running()
        elif args[0]=='stop':
            stop_all()
        elif args[0]=='install':
            ips = get_ips()
            if len(ips)==1:
                install_web(ips[0])
        elif args[0]=='run':
            ipa = get_single_ip()
            runapp(ipa)
        elif args[0]=='sudo':
            ipa = get_single_ip()
            instances = get_instances()
            set_env(ipa)
            sudo(args[1])
        elif args[0]=='copy':
            ipa = get_single_ip()
            if args[1]:
                print 'copying %s using ip %s'%(args[1],ipa)
                copy(ipa,args[1])
                #,args[2])
        elif args[0]=='copyfile':
            ipa = get_single_ip()
            if args[1]:
                print 'copying %s using ip %s'%(args[1],ipa)
                copy_file(ipa,args[1],args[2])



    except getopt.GetoptError as err:
        #usage()
        sys.exit(2)


def test_rsynch():
    import subprocess
    #args = ["rsync", "-avz", "--include", "*/", "--include", "*.jpg", "--exclude", "*", "-e", "ssh"]    
    args = ["rsync","-avL", "--progress","-e ssh -i /Users/blc/.ssh/bensh.pem", \
    "/Users/blc/polymarkets/app/", "ubuntu@ec2-107-21-136-83.compute-1.amazonaws.com:/home/ubuntu/app"]
    #args.append("jill@" + host + ":/home/jill/web/public/static/"])
    print "executing " + ' '.join(args)
    subprocess.call(args)

    #run app
    '''
    ipa = get_single_ip()
    set_env(ipa)
    sudo('cd /home/ubuntu/app/')
    #appname = "start.sh"
    sudo('/home/ubuntu/app/start.sh')
    #sudo('ls')
    '''

def copy_app():
    ipa = get_single_ip()
    copy(ipa,'/Users/blc/1market/webapp/')

if __name__=='__main__':
    #main()
    test_rsynch()
    #copy_app()
