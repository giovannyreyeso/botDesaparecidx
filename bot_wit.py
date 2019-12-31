from wit import Wit

class BotWit:
    client = None
    def __init__(self, access_token):
        self.client = Wit(access_token)
    
    def get_wit_response(self,message):
        if self.client is None:
            return
        resp = self.client.message(message)
        print(str(resp))
        return resp

    def get_intent(self,message):
        if self.client is None:
            return
        print("Tweet: "+ message)            
        response = self.client.message(message)
        entities = response['entities']
        lost_intent = self.first_entity_value(entities, 'lost_intent')
        search_type = self.first_entity_value(entities, 'search_type')
        lost_adj = self.first_entity_value(entities, 'lost_adj')
        bot_name = self.first_entity_value(entities, 'bot_name')
        print(lost_intent,search_type,lost_adj)
        if lost_intent is None and search_type is None and lost_adj is None:
            return False
        if lost_intent is None and search_type is None:
            return False
        if search_type is None and lost_adj is None:
            return False
        if lost_intent is None and search_type is not None or lost_adj is not None:
            return True
        if bot_name is not None:
            return True
        return True
        
    def first_entity_value(self,entities, entity):
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val        

    