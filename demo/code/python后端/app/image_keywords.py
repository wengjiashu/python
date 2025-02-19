import random
#stick figure 
animal=["rabbit","monkey","elephant","panda","fox"]
detail=["cartoon style","with an outline","Animals anthropomorphic"]
        
    #    "Animals have human expressions and human - like body movements","anthropomorphic"
    #    "The proportion of animals in the picture does not exceed one - fourth"
def choose_keywords(emo):
    if emo == "thankful" or emo=="happy" or emo=="like":
        weather=["sunny"]
        other=["sun","white cloud","clear stream","green trees","beautiful flowers"]
        facial_expression=["smile","laugh heartily"]
        # action=["cheer and jump for joy",""]
        element1=random.choice(animal)
        element2=random.choice(weather)        
        element3=random.sample(other,3)
        element4=random.choice(facial_expression)

        keywords=[element1] + [element2] + element3 + [element4] + detail
        return keywords
    elif emo == "sad" or emo =="complaining":
        weather=["rainy"]
        other=["dark clouds","a dirty stream","leafless tree","withered flowers"]
        facial_expression=["cry","sign"]
        # action=["cheer and jump for joy",""]
        element1=random.choice(animal)
        element2=random.choice(weather)        
        element3=random.sample(other,3)
        element4=random.choice(facial_expression)
        keywords=[element1] + [element2] + element3 + [element4] + detail
        return keywords
    elif emo == "angry" or emo == "disgusting":
        weather=["thunderstorm","fierce wind","heavy rain"]
        other=["white cloud","rolling stream","swaying tree","fallen leaves"]
        facial_expression=["angry"]
        # action=["cheer and jump for joy",""]
        element1=random.choice(animal)
        element2=random.choice(weather)        
        element3=random.sample(other,3)
        element4=random.choice(facial_expression)
        keywords=[element1] + [element2] + element3 + [element4] + detail        
        return keywords
    elif emo == "fearful":
        weather=["late at night"]
        other=["black cloud","calm stream","leafless tree"]
        facial_expression=["fear"]
        # action=["cheer and jump for joy",""]


        element1=random.choice(animal)
        element2=random.choice(weather)        
        element3=random.sample(other,3)
        element4=random.choice(facial_expression)
        keywords=[element1] + [element2] + element3 + [element4] + detail
        return keywords
    else:
        return "neutral"

# 情绪二级分类标签；
# 客服模型正向（thankful感谢、happy愉快）、
# 客服模型负向（complaining抱怨、angry愤怒）；
# 闲聊模型正向（like喜爱、happy愉快）、闲聊模型负向（angry愤怒、disgusting厌恶、fearful恐惧、sad悲伤）
# print(','.join(choose_keywords("sad")))