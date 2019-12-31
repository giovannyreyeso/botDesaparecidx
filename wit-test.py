# -*- coding: utf-8 -*-
from bot_wit import BotWit
bot_wit = BotWit("")
#fake_message = '¿Hay fotos del #TorneoDeVómito en el #SaquenPandarIgual? #Urge #AlertaAmber #SanLuisPotosí #ElToquínMásPincheLépero Citar Tweet'
real_message = '#AlertaAmber Reyna desapareció en la Miguel Hidalgo, su familia la busca. Estas son sus características:'
#bot_wit.get_intent(fake_message)
print(bot_wit.get_intent(real_message))