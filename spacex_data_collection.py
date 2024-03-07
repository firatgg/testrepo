# SpaceX Falcon 9 İlk Aşama İniş Tahmini
# Lab 1: Verilerin toplanması

# Bu kapak çalışmasında, Falcon 9'un ilk aşamasının başarılı bir şekilde iniş yapıp yapmayacağını tahmin edeceğiz.
# SpaceX, Falcon 9 roket fırlatmalarını web sitesinde 62 milyon dolar maliyetle ilan ediyor;
# diğer sağlayıcıların her biri 165 milyon dolara mal oluyor, tasarrufun çoğu SpaceX'in ilk aşamayı yeniden
# kullanabilmesinden kaynaklanıyor. Dolayısıyla ilk aşamanın iniş yapıp yapmayacağını belirleyebilirsek, fırlatma
# maliyetini de belirleyebiliriz. Bu bilgi, alternatif bir şirketin roket fırlatmak için SpaceX'e karşı teklif vermek
# istemesi durumunda kullanılabilir. Bu çalışmada, bir API'den veri toplayacak ve verilerin doğru formatta olduğundan
# emin olacaksınız.

import requests
import pandas as pd
import numpy as np
import datetime
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

#Aşağıda, fırlatma verilerindeki kimlik numaralarını kullanarak bilgi çıkarmak için API'yi kullanmamıza yardımcı olacak
#bir dizi yardımcı fonksiyon tanımlayacağız.

#Roket sütunundan güçlendirici adını öğrenmek istiyoruz.
##Veri kümesini alır ve API'yi çağırır ve verileri listeye eklemek için roket sütununu kullanır
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])

# Fırlatma rampasından, kullanılan fırlatma sahasının adını, enlemini ve boylamını bilmek istiyoruz.
## Veri kümesini alır ve API'yi çağırır ve verileri listeye eklemek için launchpad sütununu kullanır.
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])

#Yükten, yükün kütlesini ve gideceği yörüngeyi öğrenmek istiyoruz.
##Veri kümesini alır ve API'yi çağırır ve verileri listelere eklemek için payloads sütununu kullanır.
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

#Çekirdeklerden inişin sonucunu, iniş tipini, o çekirdekle yapılan uçuş sayısını, gridfins kullanılıp kullanılmadığını,
#çekirdeğin tekrar kullanılıp kullanılmadığını, bacakların kullanılıp kullanılmadığını, kullanılan iniş pistini,
#çekirdeklerin versiyonlarını ayırmak için kullanılan bir sayı olan çekirdeğin bloğunu,
#bu belirli çekirdeğin kaç kez tekrar kullanıldığını ve çekirdeğin serisini öğrenmek istiyoruz.
#Veri kümesini alır ve API'yi çağırır ve verileri listelere eklemek için çekirdek sütununu kullanır
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])


static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
response = requests.get(static_json_url)
response.status_code

data = pd.json_normalize(response.json())
data.head(5)

# Sadece istediğimiz özellikleri, uçuş numarasını ve date_utc'yi tutarak veri çerçevemizin bir alt kümesini alalım.
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]


# Birden fazla çekirdek içeren satırları ve tek bir rokette birden fazla yük içeren satırları çıkaracağız çünkü bunlar,
# 2 ek roket takviyesine sahip Falcon roketleri ve tek bir rokette birden fazla yük taşıyan durumları temsil ediyor.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# payloads ve cores 1 boyutunda listeler olduğundan, listedeki tek değeri de çıkaracağız ve özelliği değiştireceğiz.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

#Ayrıca, date_utc sütununu datetime veri türüne dönüştürmek ve ardından tarihi saati bırakacak şekilde ayıklamak istiyoruz.
data['date'] = pd.to_datetime(data['date_utc']).dt.date

#Tarihi kullanarak lansmanların tarihlerini kısıtlayacağız
data = data[data['date'] <= datetime.date(2020, 11, 13)]

# Roketten güçlendiricinin adını öğrenmek istiyoruz
# Yükten, yükün kütlesini ve gideceği yörüngeyi öğrenmek istiyoruz

# Fırlatma rampasından, kullanılan fırlatma sahasının adını, boylamını ve enlemini bilmek isteriz.

# Çekirdeklerden inişin sonucunu, inişin türünü, o çekirdekle yapılan uçuş sayısını,
# gridfins kullanılıp kullanılmadığını, çekirdeğin tekrar kullanılıp kullanılmadığını,
# bacakların kullanılıp kullanılmadığını, kullanılan iniş pistini, çekirdeklerin versiyonlarını ayırmak için kullanılan
# bir sayı olan çekirdeğin bloğunu, bu belirli çekirdeğin kaç kez tekrar kullanıldığını ve
# çekirdeğin serisini öğrenmek istiyoruz.

# Bu taleplerden gelen veriler listelerde saklanacak ve yeni bir veri çerçevesi oluşturmak için kullanılacaktır.

#Global variables
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)


launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

launch_df = pd.DataFrame(launch_dict)
launch_df.info()
launch_df.head()

data_falcon9 = launch_df[launch_df['BoosterVersion'] != 'Falcon 1']
data_falcon9.head()

data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))

data_falcon9.isnull().sum()

payload_mass_mean = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].fillna(payload_mass_mean)

data_falcon9.to_csv('dataset_part_1.csv', index=False)

