from fabric.api import *
import os
import re
import time
env.use_ssh_config = True
env.user = 'ubuntu'
env.key_filename = '/home/traveloka/.ssh/id_rsa'

devConfig = dict()
devConfig['DATABASE_URL']='postgresql://postgres:postgres@localhost:5432/accounting'
devConfig['HOST_URL']='localhost:5000'

productionConfig = dict()
productionConfig['DATABASE_URL']='postgresql://postgres:postgres@localhost:5432/accounting'
productionConfig['HOST_URL']='http://pxj.herokuapp.com'

def pushCode():
	print('Pushing to production server')
	local('git push heroku master')
	local('heroku ps:scale web=1')
	local('heroku ps')
	print('Finished')

def pushProductionConfig(key,value):
	local('heroku config:set {0}={1}'.format(key,value))

def pushLocalConfig():
	local('export {0}={1}'.format(key,value))

def pushConfig(aConfig,pushMethod):
	print('Pushing config...')
	for key in aConfig.keys():
		pushMethod(key,aConfig[key])
	print('Finished')


def deployDev():
	pushConfig(devConfig,pushLocalConfig)
	pass

def release():
	pushConfig(productionConfig,pushProductionConfig)
	pushCode()
	pass