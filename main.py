from hochschule_list.duesseldorf import duesseldorf
from hochschule_list.koeln import Koeln
import json

# path = './hochschule_info.json'
# with open(path,'r', encoding='utf-8-sig') as json_file:
#   test1 = json.load(json_file)
#   print(test1)
#   testKoeln = test1['koeln'][0]['Url']
#   print(testKoeln)
koeln = Koeln()
print(koeln.bewerbungMain())
# koeln.printAllgeimeinInfo()
# lst = koeln.returnAllgemeinList()
# message1 = koeln.bewerbungsFrist()
# message2 = koeln.bewerbungMain()
# koeln.slack_message_json()
# koeln.slack_message(message1)
# koeln.slack_message(message2)

dus = duesseldorf()
# dus.printAllgeimeinInfo()
# dus.slack_message_json()
# dusMessages = dus.bewerbungMain()
# dus.slack_message(dusMessages)
# for i in dusMessages :
  # dus.slack_message(i)
  # print(i)