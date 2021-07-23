from logging import error
import requests
from bs4 import BeautifulSoup
import json
import googletrans
import log

class Hochschule() : 
  hochschuleJsonPath = './hochschule_info.json'
  slackJsonPath = './slack_info.json'

  with open(slackJsonPath, 'r', encoding='utf-8-sig') as slackJson :
    slackFile = json.load(slackJson)
    token = slackFile['token']

  with open(hochschuleJsonPath, 'r', encoding='utf-8-sig') as hochschuleJson :
    infoFile = json.load(hochschuleJson)
    

  def __init__(self) :
    pass

  # slack_info.json 
  def slackChannel_id(self, name) :
    '''
    slack 채널 id 가져오기\n
    매개변수 : name
    '''
    try :
      self.channel_id = self.slackFile['channel_id'][name]

      self.log.info(f'{self.__class__.__qualname__} slackInfo Fertig')

      return self.channel_id
    
    except Exception as ex :
      self.log.exception('slackToken Error' + str(ex))
      print()


  # slack message
  def slack_message(self, token, channel_id ,message) :
    '''
    slack으로 메세지 보내기
    '''
    try :
      if message == None :
        self.log.debug('message 가 없습니다')
        return False

      self.data = {'Content-Type': 'application/x-www-form-urlencoded',
          'token': token,
          'channel': channel_id, 
          'text': message
          }
      URL = "https://slack.com/api/chat.postMessage"
      res = requests.post(URL, data=self.data)
      
      if res.status_code == 200 :
        self.log.info('slack 메세지 전송 성공')
      else :
        self.log.info('slack 메세지 전송 실패')

    except Exception as ex :
      self.log.exception('slack_message Error' + str(ex))
      print()

  # slack message aus json File
  def slack_message_json(self) :
    '''
    Json 파일에 저장되어 있는 정보 slack 메세지 전송\n
    '''
    try :
      self.jsonFileList = self.returnAllgemeinList()

      self.message = f'----- {self.name} 음대 사이트 정보 -----\n\n'
      
      for self.i in self.jsonFileList :
        self.idx = self.i['No.']
        self.url = self.i['Url']
        self.info = self.i['info']
        
        if self.idx == None or self.url == '' or self.info == '' :
          break
        self.message += f'{self.idx}. {self.info} 페이지 :\n{self.url}\n\n'
      
      self.log.info('slack_message_json Fertig')
      return self.message

    except Exception as ex :
      self.log.exception('slack_message_json Error' + str(ex))
      print()



  # google trans : de -> ko
  def toKor(self, message, title) :
    '''
    독일어를 한국어로 구글 번역\n
    매개변수 message : string, 독일어\n
    return : de + ko text
    '''
    try :
      self.translator = googletrans.Translator()
      self.translatedText = ''
      self.deText = message
      self.koText = self.translator.translate(self.deText, dest='ko')
      self.translatedText += f'----- {self.name} {title} -----'
      self.translatedText += '\n\n'
      self.translatedText += self.deText + '\n'
      self.translatedText += self.koText.text + '\n'
      # slack 에서 공백(빈 줄) = \xa0
      self.translatedText += '\xa0'

      self.log.info('toKor Fertig')
      return self.translatedText

    except Exception as ex:
      self.log.exception('toKor Error' + str(ex))
      print()

  # 파파고 번역 : de -> ko 일일 글자 제한 10000
  def papagoToKor(self, text):
    self.client_id = "" # <-- client_id 기입
    self.client_secret = "" # <-- client_secret 기입

    self.data = {'text' : text,
            'source' : 'de',
            'target': 'ko'}

    self.url = "https://openapi.naver.com/v1/papago/n2mt"

    self.header = {"X-Naver-Client-Id":self.client_id,
              "X-Naver-Client-Secret":self.client_secret}

    response = requests.post(self.url, headers=self.header, data=self.data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)

  # json 정보 출력
  def printAllgeimeinInfo(self) :
    '''
    각 학교 사이트 정보를 담은 csv 내용을 출력한다\n
    매개변수, return : 없음\n
    index, url, 설명
    '''
    try :
      with open(self.hochschuleJsonPath, 'r', encoding='utf-8-sig') as hochschuleJson :
        self.allgemein = json.load(hochschuleJson)[self.name]['Allgemein']
      print()
      self.log.info(f'----- {self.name} info ----- ')
      print()
      for self.i in self.allgemein :
        self.idx = self.i['No.']
        self.url = self.i['Url']
        self.info = self.i['info']

        if self.idx == None or self.url == '' or self.info == '' :
          break
        
        self.log.info(f'index: {self.idx}')
        self.log.info(f'url  : {self.url}')
        self.log.info(f'info : {self.info}\n')
      self.log.info(f'----- {self.name}  끝  ----- ')
      print()
    except Exception as ex :
      self.log.exception('printAllgeimeinInfo Error' + str(ex))
      print()

  # json 사이트 주소 읽어오기
  def returnAllgemeinList(self) :
    '''
    json 파일에 있는 Allgemein return\n
    return : allgemein\n
    'No.', 'Url', '설명' 로 딕셔너리 접근
    '''
    try :
      with open(self.hochschuleJsonPath, 'r', encoding='utf-8-sig') as hochschuleJson :
        self.allgemein = json.load(hochschuleJson)[self.name]['Allgemein']
      self.log.info('returnAllgemeinList Fertig')
      return self.allgemein

    except Exception as ex :
      self.log.exception('returnAllgemeinList Error' + str(ex))
      print()


  # html 페이지 가져오기
  def htmlParser(self, url) :
    '''
    각 사이트 BeautifulSoup 으로 가져오기\n
    매개 변수 : url\n
    return : soup\n 
    매 년, 매 학기 바뀔 수 있으므로 크롤링하기
    '''

    response = requests.get(url)
    try :
      if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        self.log.info(f'htmlParser Fertig  {url}  연결 성공')
        return soup
      else : 
        self.log.info(f'htmlParser 연결 실패\nstatus_code: {response.status_code}')
        return False

    except Exception as ex :
      self.log.exception(f'htmlParser Error' + str(ex))
      self.log.exception(f'잘못된 url 입니다 {url}')

