#---------------------------------------------------------------------
# Python example to show how API is used with Micro GC Fusion
# 
# Copyright(c) 2014 INFICON This open source example may be freely
# used and modified for any purpose under terms of the MIT Licence
# http://opensource.org/licenses/MIT
#

#---------------------------------------------------------------------

import requests
import time
import json
import struct
import numpy as np
import importlib.resources

class Fusion(object):
    def __init__(self,ipaddress):
        try:
            self.ip = f'http://{ipaddress}'
            self.s = requests.Session()
            self.info=self.__Info__(self.ip,self.s)
            numberOfModules = self.info.__numberOfModules__()
        except Exception as e:
            print('Error connecting to Micro GC Fusion, check IP address')
        if numberOfModules == 3:
            self.moduleA = self.__Module__('A',self.ip, self.s)
            self.moduleB = self.__Module__('B',self.ip, self.s)
            self.moduleC = self.__Module__('C',self.ip, self.s)
            self.moduleD = self.__Module__('D',self.ip, self.s)
        elif numberOfModules ==2:
            self.moduleA = self.__Module__('A',self.ip, self.s)
            self.moduleB = self.__Module__('B',self.ip, self.s)
            self.moduleC = self.__Module__('C',self.ip, self.s)
        elif numberOfModules == 1:
            self.moduleA = self.__Module__('A',self.ip, self.s)
            self.moduleB = self.__Module__('B',self.ip, self.s)
        elif numberOfModules == 0:
            self.moduleA = self.__Module__('A',self.ip, self.s)
        
        self.data=self.__Databrowser__(self.ip, self.s)
        self.methods=self.__Methods__(self.ip, self.s)
        self.control=self.__Control__(self.ip, self.s)
        self.valco=self.__Valco__(self.ip, self.s)
        self.network=self.__Network__(self.ip, self.s)
        self.notifications=self.__Notifications__(self.ip, self.s)
    
    def close(self):
        self.s.close()

    def connected(self):
        try:
            response = self.s.get(f'{self.ip}')
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False

    def status(self):
        status = self.s.get(f'{self.ip}/v1/scm/sessions/system-manager/publicConfiguration').json()
        return {'sequence':status[0],'system':status[1]}

    class __Info__:
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
        def serialNumber(self):
            sn = self.s.get(f'{self.ip}/system/systemInfo/systemSerialNumber').json()
            return sn

        def partNumber(self):
            chassisPN = self.s.get(f'{self.ip}/system/systemInfo/systemPartNumber').json()
            allModules = self.s.get(f'{self.ip}/system/modules').json()
            modules = []
            for module in allModules:
                if 'module' in module:
                    modules.append(module)
            modules.sort()
            for module in modules:
                modulePN = allModules[module]['moduleInfo']['modulePartNumber']
                chassisPN = chassisPN+modulePN
            return chassisPN

        def hostname(self):
            hostname = self.s.get(f'{self.ip}/system/systemInfo/hostname').json()
            return hostname

        def storageLimit(self):
            limit = self.s.get(f'{self.ip}/v1/runData/storageLimit').json()
            return limit

        def __numberOfModules__(self):
            modules = self.s.get(f'{self.ip}/system/systemInfo/systemSpec/numberOfModules', timeout = 3).json()
            return modules
        
    class __Network__:
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def info(self):
            networkInfo = self.s.get(f'{self.ip}/networkConfig').json()
            return networkInfo

        def toggleWifi(self):
            wifi = self.s.get(f'{self.ip}/networkConfig/wifiEnable').json()
            if wifi == True:
                self.s.put(f'{self.ip}/networkConfig/wifiEnable',json=False)
            else:
                self.s.put(f'{self.ip}/networkConfig/wifiEnable',json=True)
            time.sleep(0.5)
            wifiAgain = self.s.get(f'{self.ip}/networkConfig/wifiEnable').json()
            return wifiAgain

        def getWifiPassword(self):
            password = self.s.get(f'{self.ip}/networkConfig/wifiPassword').json()
            return password

        def setWifiPassword(self,password):
            self.s.put(f'{self.ip}/networkConfig/wifiPassword',json=password)

        def setHostname(self, hostname):
            self.s.put(f'{self.ip}/networkConfig/hostname',json=hostname)

        def syncTime(self):
            t = str(time.time())
            self.s.put(f'{self.ip}/networkConfig/date',json=t)

    class __Control__:
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def run(self):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.run?runWhenReady=true')

        def runWithName(self,name,tags=[]):
            runCommandBody = {"runWhenReady":True, 
                                "annotations":{
                                            "name":name,
                                            "tags":tags
                                                },
                                            }
            self.s.post(f'{self.ip}/v1/scm/sessions/system-manager!cmd.run',json=runCommandBody)
                                
        def stopSequence(self):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.stop')
            
        def abortCurrentRun(self):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.abort')

        def loadMethod(self,methodName):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.loadMethod?methodLocation=/v1/methods/userMethods/{methodName}')

        def loadSequence(self,sequenceName):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.loadSequence?sequenceLocation=/sequences/{sequenceName}')

        def reboot(self):
            self.s.get(f'{self.ip}/cgi-bin/rebooterCgi.sh?now')
            
        def bakeout(self,minutes=30):
            self.s.get(f'{self.ip}/v1/scm/sessions/system-manager!cmd.bakeout?duration={minutes*60}s')
            
        def getStringCommand(self,string):
            response = self.s.get(f'{self.ip}{string}').json()
            return response
 
    class __Module__:
        def __init__(self,module, ipaddress, session):
            self.__module__=module
            fpgaLookup = {'A':1,'B':2,'C':3,'D':4}
            self.__fpgaNumber__ = fpgaLookup[self.__module__]
            self.ip=ipaddress 
            self.s=session 
       
        def info(self):
            return self.s.get(f'{self.ip}/system/modules/module{self.__module__}/moduleInfo/moduleSpecText').json()

        def serialNumber(self):
            return self.s.get(f'{self.ip}/system/modules/module{self.__module__}/moduleInfo/moduleSerialNumber').json() 

        def partNumber(self):
            return self.s.get(f'{self.ip}/system/modules/module{self.__module__}/moduleInfo/modulePartNumber').json()

        def heaters(self):
            value = self.s.get(f'{self.ip}/fpgaManager/fpga{self.__fpgaNumber__}/math/refConv').json()
            heaters = {'tcdHeater':round(value[17]['result'],2),
                        'injectorDieHeater':round(value[1]['result'],2),
                        'flowManifoldHeater':round(value[0]['result'],2),
                        'columnHeater':round(value[10]['result'],2),
                        'externalColumnHeater':round(value[2]['result'],2),
                            }
            return heaters
        
        def pressures(self,vso=''):
            values = self.s.get(f'{self.ip}/fpgaManager/fpga{self.__fpgaNumber__}/math/refConv').json()
            pressure = {
                    'carrier':round(values[13]['result'],2),
                    'inject':round(values[12]['result'],2),
                }
            if vso != '':
                if vso in pressure:
                    return pressure[vso]
            return pressure
        
        def tcdSignal(self):
            signal = self.s.get(f'{self.ip}/fpgaManager/fpga{self.__fpgaNumber__}/det/core/0/data').json()
            if(isinstance(signal, str)):
                        signal = struct.unpack('!f', bytes.fromhex(signal[2:]))[0]
            signal=signal*100000
            return signal

        def valves(self):
            value = self.s.get(f'{self.ip}/fpgaManager/fpga{self.__fpgaNumber__}/pwm/data').json()
            pn = self.partNumber()[0]
            v = {'W':{'backflush':value[8]['dutyCycle'],
                        'sample':value[5]['dutyCycle'],
                        'forflush':value[6]['dutyCycle'],
                        'switch':value[7]['dutyCycle'],
                        'inject':value[4]['dutyCycle'],
                        },
                'R':{'sample':value[5]['dutyCycle'],
                        'forflush':value[6]['dutyCycle'],
                        'switch':value[7]['dutyCycle'],
                        'inject':value[4]['dutyCycle'],
                        },
                'V':{'backflush':value[8]['dutyCycle'],
                        'sample':value[5]['dutyCycle'],
                        'forflush':value[6]['dutyCycle'],
                        'switch':value[7]['dutyCycle'],
                        'inject':value[4]['dutyCycle'],
                        },
                'T':{'sample':value[6]['dutyCycle'],
                        'switch':value[7]['dutyCycle'],
                        'inject':value[4]['dutyCycle'],
                        },
                'U':{'sample':value[6]['dutyCycle'],
                        'switch':value[7]['dutyCycle'],
                        'inject':value[4]['dutyCycle'],
                        },
                }  
            return v[pn]
        
        def fan(self):
            fanSpeed = self.s.get(f'{self.ip}/fpgaManager/fpga{self.__fpgaNumber__}/pwm/data/9/dutyCycle').json()
            fanSpeed = round(fanSpeed,2)
            return fanSpeed   

    class __Databrowser__:
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def lastRun(self):
            lastRunLocation = self.s.get(f"{self.ip}/v1/lastRun").json()['dataLocation']
            lastRunData = self.s.get(f'{self.ip}/runData/{lastRunLocation}').json()
            return lastRunData

        def lastRunID(self):
            runData = self.lastRun()
            return runData['$id']

        def getLastX(self,limit):
            runs = self.s.get(f'{self.ip}/runData?limit={limit}&sortByDate=DESC&allData=True').json()['runs']
            return runs
        
        def queryText(self, query):
            runs = self.s.get(f'{self.ip}/runData?{query}').json()[runs]
            return runs
        
        def getData(self,runID):
            runData = self.s.get(f'{self.ip}/runData/{runID}').json()
            return runData

        def addNewData(self,datafile):
            runID = datafile['$id']
            self.s.put(f'{self.ip}/v1/runData/{runID}',json=datafile)
            self.reprocess(runID)

        def replaceData(self,datafile):
            runID = datafile['$id']
            try:
                self.s.delete(f'{self.ip}/v1/runData/{runID}')
                self.s.put(f'{self.ip}/v1/runData/{runID}',json=datafile)
            except Exception as e:
                print('Error replacing datafile, attempting to create new file')
                print(e)
                self.addNewData(datafile)

        def reprocess(self,runID):
            reprocessData={'peakParameters':self.s.get(f'{self.ip}/runData/{runID}').json()['method']['peakParameters'],
                           'query': runID,
                           'target':'/runData'
                           }
            self.s.post(f'{self.ip}/peakUtilities/reprocessor!start',json=reprocessData)
            reprocessState = self.s.get(f'{self.ip}/peakUtilities/reprocessor/status').json()['running']
            while reprocessState == True:
                reprocessState = self.s.get(f'{self.ip}/peakUtilities/reprocessor/status').json()['running']
                time.sleep(1)

        def reprocessMany(self,runIDList):
            parsedList = ''
            for run in runIDList:
                parsedList +=run+'|'
            parsedList=parsedList[:-1]
            reprocessData={'peakParameters':self.s.get(f'{self.ip}/runData/{runIDList[0]}').json()['method']['peakParameters'],
                           'query': parsedList,
                           'target':'/runData'
                           }
            self.s.post(f'{self.ip}/peakUtilities/reprocessor!start',json=reprocessData)

        def compoundResults(self):
            lastRunLocation = self.s.get(f"{self.ip}/v1/lastRun").json()['dataLocation']
            runData = self.s.get(f'{self.ip}/runData/{lastRunLocation}').json()
            results = {'id':runData['$id'],
                        'timestamp':runData['runTimeStamp'],
                        'methodName':runData['methodName'],
                        }
            try:
                annotations = {'name':runData['annotations']['name'],
                                'tags':runData['annotations']['tags']
                                }
            except:
                pass
            compound = []
            for detector in runData['detectors']:
                try:
                    peaks = runData['detectors'][detector]['analysis']['peaks']
                    for peak in peaks:
                        
                        if 'label' in peak:
                            try:
                                label = peak['label'] #name this peak via the user input value
                                height = round(peak['height'],0) #Get the peak height, round the value
                                area = round(peak['area'],0) # Get the peak area, round the value
                                rt = peak['top'] #Get the "top", which represent the retention time of the peak
                                try:
                                    concentration = round(peak['concentration'],6) #Try to get the calculated peak concentration, round the value
                                except:
                                    concentration = '-'              #If the peak concentration is missing (not calibrated properly), enter a "-" as the value                          
                                try:
                                    normConc = round(peak['normalizedConcentration'],6) #Try to get the unNormalized Concentration, round the value
                                except:
                                    normConc = '-'
                                compound.append({label:{
                                                    'height':height,
                                                    'area':area,
                                                    'rt':rt,
                                                    'concentration':concentration,
                                                    'normalizedConcentration':normConc
                                                    }
                                            })
                            except Exception as e:
                                compound.append({label:'error gathering data'})
                            results.update({'compounds':compound})                                
                except Exception as e:
                    print(f'No peaks were found for {detector}')
            return results

        def __averageXRuns__(self,numberOfRunsToAverage,sequenceCheck=False):
            lastX = self.getLastX(numberOfRunsToAverage)
            averagedData = {}
            runIDs=[]
            methodName=lastX[0]['methodName']
            sequence = lastX[0]['sequence']
            detectors = [detector for detector in lastX[0]['detectors']]
            for detector in detectors:
                averagedData.update({detector:[]})
            for runData in lastX:
                runIDs.append(runData['$id'])
                if methodName != runData['methodName']:
                    print('Methods do not match, exiting averaging')
                    return False
                if sequenceCheck:
                    if sequence != runData['sequence']:
                        print('Sequence Check enabled: Sequence info does not match. Exiting averaging')
                        return False
                for detector in detectors:
                    if 'originalValues' in runData['detectors'][detector]:
                        averagedData[detector].append(runData['detectors'][detector]['originalValues'])
                    else:
                        originalValues = runData['detectors'][detector]['values']
                        averagedData[detector].append(originalValues)
                        runData['detectors'][detector]['originalValues'] = originalValues

            for detector in lastX[0]['detectors']:
                try:
                    lastX[0]['detectors'][detector]['values'] = list(np.mean(np.array(averagedData[detector]),axis=0))
                    try:
                        lastX[0]['annotations']['tags'].append(f'Averaged_{numberOfRunsToAverage}')
                    except:
                        lastX[0].update({'annotations':{'name':methodName,'tags':[f'Aveaged_{numberOfRunsToAverage}']}})
                except Exception as e:
                    print('Error Averaging Data')
                    print(e)
                    return False
            self.replaceData(lastX[0])
            self.reprocess(lastX[0]['$id'])
            return True
            
    class __Methods__:
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def getAll(self):
            return self.s.get(f'{self.ip}/methods/userMethods').json()

        def get(self,methodName):
            return self.s.get(f'{self.ip}/methods/userMethods/{methodName}').json()

        def methodByPN(self,condition=False,zero=False,clearPreset=False):
            jsonFileLocation = 'ModuleMethods.json'
            methodTypes = ['analyticalMethods'] #analyticalMethods, 0-InjectMethods, conditioningMethods, HeaterTests
            if condition==True:
                methodTypes.append('conditioningMethods')
            if zero == True:
                methodTypes.append('0-InjectMethods')
            
            with importlib.resources.open_text("MicroGCFusionAPI",jsonFileLocation) as file:
                moduleMethods = json.load(file)

            modelMethod = self.s.get(f'{self.ip}/methods/systemMethods/modelMethod').json()
            modules = []
            for mod in modelMethod['modules']:
                modules.append(mod)

            if clearPreset:
                userMethods = self.s.get(f'{self.ip}methods/userMethods')
                for method in userMethods:
                    userMethods[method]['isPreset'] = False
                self.s.put(f'{self.ip}methods/userMethods', json=userMethods)
                
            for methodType in methodTypes:
                methodName=''
                for module in modules:
                    modulePN = modelMethod['modules'][module]['modulePartNumber'].upper()  #Determine what modules are in the system
                    modelMethod['modules'].update({module:moduleMethods[methodType][modulePN]})    #Change the method of the module using the method from the json file
                    methodName += modulePN
                                                                 
                modelMethod.update({'options':{'lowTemperatureMode': True}})   #modify all methods to set "lowTemperatureMode" to true, which turns fan on at 20%
                modelMethod.update({'isPresent':True})
                if methodType == 'conditioningMethods':
                    methodName += '_CONDITION'
                elif methodType == '0-InjectMethods':
                    methodName+= '_0-Inject'

                msg = {'type':'WARN',
                            'messageID':f'Adding method: {methodName} to instrument'}
                
                requests.put(f'{self.ip}/system/notifications',json=msg)
                self.s.put(f'{self.ip}/methods/userMethods/'+methodName, json=modelMethod)    #put new method into methods/userMethods location
                return methodName

    class __Valco__:
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def enabled(self):
            valco = self.s.get(f'{self.ip}/valcoSelector').json()
            if not valco:
                return False
            else:
                return True

        def getPos(self):
            return self.s.get(f'{self.ip}/valcoSelector/position').json()

        def setPos(self,pos):
            self.s.put(f'{self.ip}/valcoSelector/position',json=pos)

        def info(self):
            return self.s.get(f'{self.ip}/valcoSelector').json()

    class __Notifications__():
        
        def __init__(self,ipaddress,session):
            self.ip = ipaddress
            self.s = session
            
        def info(self,message):
            msg = {'type':'INFO',
                    'messageID':message}
            self.s.post(f'{self.ip}/system/notifications',json=msg)

        def warn(self,message):
            msg = {'type':'WARN',
                    'messageID':message}
            self.s.post(f'{self.ip}/system/notifications',json=msg) 

        def error(self,message):
            msg = {'type':'ERROR',
                    'messageID':message}
            self.s.post(f'{self.ip}/system/notifications',json=msg)