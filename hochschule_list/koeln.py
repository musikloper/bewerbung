
import log
from hochschule_list.hochschule import Hochschule
from bs4 import BeautifulSoup
import json


class Koeln(Hochschule) :
  def __init__(self):
    try :
      super().__init__()
      self.name = 'koeln'

      # log 
      self.log = log.Log(self.name).logger
      self.log.propagate = False
      
      # hochschule_info.json #
      self.infoFile = super().infoFile[self.name]
      self.allgemein = self.infoFile['Allgemein']
      self.bewerbungsFristInfo = self.infoFile['bewerbungsFristInfo']
      self.bewerbungMainInfo = self.infoFile['bewerbungMainInfo']

      # slack
      self.channel_id = super().slackChannel_id(self.name)

      self.log.info(f'{self.__class__.__name__} init Fertig')

    except Exception as ex :
      self.log.exception('init Error ' + str(ex))


  ##### 변동 사항 생기면 수정해야한다 #####

  # 메인 정보
  def bewerbungMain(self) :
    '''
    Köln Bewerbung Main (DE / KO)
    return : String, message
    '''
    self.soup = super().htmlParser(self.bewerbungMainInfo['url'])
    self.title = 'bewerbungMain'
    self.text = ''
    try :
      if self.soup != False :
        self.smallTitle = self.soup.select_one('#c9169 > h2')
        self.info1 = self.soup.select('#c9169 > p')
        self.info2 = self.soup.select('#c12861 > p, strong')
        
        self.text += self.smallTitle.text + '\n\n'
        for self.i in self.info1 :
          self.text += self.i.text.replace('\xa0', '').strip() + '\n\n'
        for self.i in self.info2 :
          self.text += self.i.text.replace('\xa0', '').strip() + '\n\n'
      else :
        self.log.info('bewerbungMain url 연결 실패\n' + self.bewerbungMainInfo['url'])
        print()
        return False

      self.messageText = super().toKor(self.text, self.title)
      self.log.info('bewerbungMain Fertig')
      return self.messageText

    except Exception as ex :
      self.log.exception('bewerbungMain Error' + str(ex))
      print()


  # 날짜 
  def bewerbungsFrist(self):
    '''
    Köln Bewerbungsfrist Information (DE / KO)
    return : String, message
    '''
    self.soup = super().htmlParser(self.bewerbungsFristInfo['url'])
    self.title = 'bewerbungsFrist'
    try :
      self.text = ''
      if self.soup != False :
        # #c9071 = 태그 아이디
        self.info = self.soup.select('#c9071 > h2, p')

        if self.info == None or self.info == '' :
          self.log.debug(f'self.info : {self.info}')
          self.log.debug(f'Url / Tag 를 확인하세요')
          return False

        else :
          for self.i in self.info :

            # 공백 제거
            # '\xa0' = &nbsp
            if self.i.text == '' or self.i.text == '\xa0' :
              continue
            
            # 제목인 경우
            if self.i.name == 'h2' :
              self.text += '\n'

            self.text += self.i.text + '\n'
          self.messageText = super().toKor(self.text, self.title)
          self.log.info('bewerbungsFrist Fertig')
          return self.messageText

      else :
        self.log.debug('url 연결 실패 ' + self.bewerbungsFristInfo['url'])
        return False

    except Exception as ex :
      self.log.exception(f'{self.name} bewerbungsFrist Error' + str(ex))
      print()

  






##### 공통 함수 #####

  def slack_message(self, message):
    super().slack_message(super().token, self.channel_id, message)

  def slack_message_json(self):
    self.message = super().slack_message_json()
    super().slack_message(super().token, self.channel_id, self.message)

  def printAllgeimeinInfo(self):
    return super().printAllgeimeinInfo()

  def returnAllgemeinList(self) :
    return super().returnAllgemeinList()
