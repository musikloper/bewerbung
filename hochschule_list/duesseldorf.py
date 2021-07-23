import log
from hochschule_list.hochschule import Hochschule

import json


class duesseldorf(Hochschule) :
  def __init__(self):
    try:
      super().__init__()
      self.name = 'duesseldorf'

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

  # 날짜
  def bewerbungsFrist(self):
    '''
    Düsseldorf Bewerbungsfrist Information (DE / KO)
    return : String, message
    '''
    self.FristInfo = super().infoFile[self.name]['bewerbungsFristInfo']
    self.title = 'bewerbungsFrist'
    try :
      self.messageTextList = []

      # 뒤셀은 바첼러 마스터 태그가 같음
      for self.url in self.FristInfo :
        self.soup = super().htmlParser(self.url['url'])
        self.text = ''
        if self.soup != False :
          self.tagname = self.url['tagname'][0]
          self.info = self.soup.select(f'.{self.tagname} h1, p, .{self.tagname} p > br')
          if self.info == None or self.info == '' :
            self.log.debug(f'self.info : {self.info}')
            self.log.debug(f'Url / Tag 를 확인하세요')
            return False

          else :
            for self.i in self.info :
              if self.i.name == 'h1' :
                continue
              if self.i.name == 'br' :
                continue
              self.text += self.i.text + '\n\n'
            self.messageText = super().toKor(self.text, self.title)
            self.messageTextList.append(self.messageText)
            self.log.info('bewerbungsFrist Fertig')

        else :
          self.log.debug('url 연결 실패 ' + self.bewerbungsFristInfo['url'])
          return False
      return self.messageTextList

    except Exception as ex :
      self.log.exception(f'{self.name} bewerbungsFrist Error' + str(ex))
      print()
  
  # 메인 정보
  def bewerbungMain(self) :
    '''
    Düsseldorf Bewerbung Main (DE / KO)
    return : String, message
    '''
    self.title = 'bewerbungMain'
    self.soup = super().htmlParser(self.bewerbungMainInfo['url'])

    self.text = ''
    try :
      if self.soup != False :
        self.tagname = self.bewerbungMainInfo['tagname'][0]
        self.info = self.soup.select(f'.{self.tagname} button, .{self.tagname} p , .{self.tagname} a')
        
        if self.info == None or self.info == '' :
          self.log.debug(f'self.info : {self.info}')
          self.log.debug(f'Url / Tag 를 확인하세요')
          return False

        else :
          for self.i in self.info :
            if self.i.name == 'a' :
              self.href = self.i.attrs['href']
              self.n = self.i.text
              self.text += f'{self.n} : https://www.rsh-duesseldorf.de/{self.href} \n'
              continue
            
            if self.i.name == 'button' :
              self.text += '\n\n' + self.i.text + '\n\n'
              continue
            self.text += self.i.text + '\n\n'

          self.messageText = super().toKor(self.text, self.title)

      else :
        self.log.info('bewerbungMain url 연결 실패\n' + self.bewerbungMainInfo['url'])
        print()
        return False

      self.log.info('bewerbungMain Fertig')
      return self.messageText

    except Exception as ex :
      self.log.exception('bewerbungMain Error' + str(ex))
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