from entity_spider.Client import Retry
from .exceptions import LinkHandlerException
from entity_spider.Parsers.exceptions import LinkParserException
from entity_spider.config.log import logger

class BaseLinkHandler(object):
    def __init__(self, parser=None, client=None):
        self._parser = parser
        self._client = client

    def can_handle(self, linkObj):
        return False

    def get_linkObj(self):
        return self._linkObj

    def handle(self, linkObj):
        self._linkObj = linkObj
        self.handle_new_state(self.get_entity_state(linkObj))

    def handle_new_state(self, entity_dic):
        raise Exception('not implemented')
        return None


    def get_entity_state(self, linkObj):
        #todo handle client exception here
        try :
            data = self._client.get_entity_data(linkObj)

            state = self._parser.parse(data)
            return state
        except LinkParserException as e:
            raise LinkParserException(e.message)
        except Retry as e :
            raise Retry()
        except Exception as e:
            logger.warning('get entity state exception for : %s' %linkObj)
            raise LinkHandlerException(message='get entity state exception for linkObj %s' %linkObj)

        #TODO : raise get_entity_state error here

