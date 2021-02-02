import csv
import json
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import LSTM, GRU,Bidirectional, Flatten, Dense
from keras_self_attention import SeqSelfAttention
import csv, re
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras import optimizers
import numpy as np
from keras.preprocessing.text import  Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import  EarlyStopping, ModelCheckpoint
from keras_self_attention import SeqSelfAttention, SeqWeightedAttention
from app.models import Champion, Conversation
from app import db 

dict_intent={
    'build_item':0,
    'support_socket':1,
    'counter':2,
    'be_countered':3,
    'skill_up':4,
    'how_to_play':5,
    'combo':6,
    'combine_with':7,
    'how_to_use_skill':8,
    'introduce':9
}
CHAMPIONS = []
dict_digit2intent = {}
key = 0
for i in dict_intent.keys():
    dict_digit2intent[key] = i
    key += 1
f = open('app/api_service/my_upload/champions.txt', "r")
reg = ""
for cham in f:
    reg += cham.split ('\n')[0] + '|'
    CHAMPIONS.append(cham.split ('\n')[0])
reg = reg[:-1]
f.close()

skills = ['Q', 'W', 'E' , 'R', 'q','w','e','r']
def get_entity(content): 
    
    hero = re.search(reg.lower(), content.lower())
    if hero != None:
        hero = hero.group()
    else: hero = ""
    if hero == "":
        hero = re.search(reg, content)
        if hero != None:
            hero = hero.group()
        else: hero = ""
    spl = content.split(" ")
    skill = ""
    for i in spl:
        if i in skills:
            skill = i
            break

    if hero != "":
        for c in CHAMPIONS:
            if c.lower() == hero.lower():
                hero = c 
                break
    if 'jarvan' in content.lower():
        hero = 'Jarvan IV'
    if 'mundo' in content.lower():
        hero = 'Dr. Mundo'

    return hero, skill.upper()

def load_model():
    model = Sequential()
    model.add(Embedding(208, 5248, input_length=17))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    # model.add(LSTM(128, return_sequences = True))
    model.add(Flatten())
    model.add(Dense(10, activation='softmax'))
    model.compile(loss= 'categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.load_weights('app/api_service/my_upload/hoaf13-nlp.h5')
    # model.summary()
    return model
def process_content(reg, content): 
    # content = content.lower()
    x = re.search(reg, content)
    
    if x != None:
        content = content.replace(x.group(), "{hero}")
    return content
def process_data(model, content):
    f = open('app/api_service/my_upload/bow.txt', 'r')
    dictionary = ''
    for word in f:
        dictionary += word + " "
    f.close()
    data = [dictionary]
    token_obj = Tokenizer()
    token_obj.fit_on_texts(data)
    max_len = 17
    X_train_token = token_obj.texts_to_sequences([content])
    X_pad = pad_sequences(X_train_token, maxlen=max_len, padding='post')

    result = model.predict(X_pad)
    intent = np.argmax(result)
    hero, skill = get_entity(content)

    return dict_digit2intent[intent], result[0][intent], hero, skill


def get_raw_answer(intent, champion):
    message_answer = None
    if intent == 'build_item': message_answer = champion.build_item
    if intent == 'support_socket': message_answer = champion.support_socket
    if intent == 'counter': message_answer = champion.counter
    if intent == 'be_countered': message_answer = champion.be_countered
    if intent == 'skill_up': message_answer = champion.skill_up
    if intent == 'how_to_play': message_answer = champion.how_to_play
    if intent == 'combo': message_answer = champion.combo
    if intent == 'combine_with': message_answer = champion.combine_with
    if intent == 'how_to_use_skill': message_answer = champion.how_to_use_skill
    if intent == 'introduce': message_answer = champion.introduce
    return message_answer

def normalize_message(intent, message_answer, entities, champion,conversation_id):
    ans = None
    action = None
    try:
        skill_message = entities['skill']
    except Exception:
        skill_message = None
    try:
        champion_message = entities['champion']
    except Exception:
        champion_message = None
    action = "action_"+intent
    if intent == 'build_item': # "['Nguyệt Đao', 'Vô Cực Kiếm', 'Vũ Điệu Tử Thần', 'Áo Choàng Bóng Tối', 'Kiếm Ma Youmuu', 'Dao Găm Nham Thạch']"
        list_items = eval(message_answer)
        items = ', '.join(list_items)
        ans = "{} lên đồ như sau: {}".format(champion.name, items)
    if intent == 'support_socket': # ImageField 
        ans = champion.support_socket
    if intent == 'counter': # ['Darius', 'Yasuo', 'Zed', 'Master Yi', 'Katarina', 'Hecarim', 'Akali', 'Renekton', 'LeBlanc', 'Jinx', 'Kassadin', 'Jax']        ans = MEDIA_URL + ans.url
        message_answer = message_answer.replace('"','')
        message_answer = message_answer.replace("'",'')
        list_champions = message_answer.strip('][').split(', ')
        champions = ', '.join(list_champions)
        ans = "{} khắc chế được các tướng: {}".format(champion.name,champions)
    if intent == 'be_countered': # ['Jax', 'Riven', 'Teemo', 'Fiora', 'Renekton', 'Tryndamere', 'Pantheon', 'Nasus', 'Lee Sin', 'Irelia', 'Ngộ Không', 'Jayce']
        message_answer = message_answer.replace('"','')
        message_answer = message_answer.replace("'",'')
        list_champions = message_answer.strip('][').split(', ')
        champions = ', '.join(list_champions)
        ans = "{} bị khắc chế bởi các tướng: {}".format(champion.name, champions)
    if intent == 'skill_up': # ['E', 'Q', 'E', 'Q', 'E', 'R', 'Q', 'Q', 'R', 'Q', 'R', 'E', 'E', 'W', 'W', 'W', 'W', 'W']
        message_answer = message_answer.replace("'",'')
        list_skills = message_answer.strip('][').split(', ')
        skills = ', '.join(list_skills)
        ans = "Thứ tự lên skill của {}: {}".format(champion.name, skills)
    if intent == 'combo': # ['Q', 'R', 'W', 'Attack', 'E']
        message_answer = message_answer.replace("'",'')
        list_combos = message_answer.strip('][').split(', ')
        combos = ', '.join(list_combos)
        ans = "{} combo như sau: {}".format(champion.name, combos)
    if intent == 'combine_with': # ['Yasuo', 'Zilean', 'Tryndamere', 'Lee Sin', 'Fizz', 'Ahri', 'Orianna', 'Renekton', 'Vayne', 'Akali', 'Jax', 'Ezreal']
        message_answer = message_answer.replace('"','')
        message_answer = message_answer.replace("'",'')
        list_champions = message_answer.replace('[','')
        list_champions = list_champions.replace(']','') 
        # print("list champions: ", list_champions)
        ans = "{} phối hợp tốt với: {}".format(champion.name, list_champions)
    if intent == 'how_to_use_skill': # {'E': Luoi guom doa day}
        skill_champion = eval(champion.how_to_use_skill)
        skill = skill_champion[skill_message]
        ans = "Skill {}: ".format(skill_message) + skill
    if intent == 'introduce': # Từng là những người bảo hộ cao quý của Shurima ...
        ans = champion.introduce
    if intent == 'how_to_play':
        ans = champion.how_to_play
    if intent == 'what_about':
        conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))
        print("length ", len(conversations))
        conversation = None
        for c in conversations[::-1]:
            if c.intent != 'what_about':
                conversation = c
                break
        print(conversation)
        last_entities = eval(conversation.entities)
        last_intent = conversation.intent
        last_message_answer = conversation.message_answer
        print("last intent: ",last_intent)
        try:
            last_champion = last_entities['champion']
        except Exception:
            last_champion = None
        try:
            last_skill = last_entities['skill']
        except Exception:
            last_skill = None

        if champion_message != None and skill_message == None:
            champion = Champion.query.filter_by(name=champion_message).first()
            this_entities = dict()
            this_entities['champion'] = champion.name
            this_entities['skill'] = last_skill
            this_answer = get_raw_answer(last_intent, champion)
            ans,action = normalize_message(last_intent, this_answer, this_entities, champion, conversation_id)
            return ans,action 
        if champion_message == None and skill_message != None:
            champion = Champion.query.filter_by(name=last_champion).first()
            this_entities = dict()
            this_entities['champion'] = champion.name
            this_entities['skill'] = skill_message
            last_intent = 'how_to_use_skill'
            this_answer = get_raw_answer(last_intent, champion)
            ans,action = normalize_message(last_intent, this_answer, this_entities, champion, conversation_id)
            return ans,action
        if champion_message == None and skill_message == None:
            ans = "Tôi không hiểu ý của bạn. Mời bạn nhập lại câu hỏi rõ ràng hơn."
            action = "action_ask_hero_and_skill"
            return ans,action
    return ans,action

def is_valid_what_about(conversation_id):
        conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))
        if len(conversations) == 0:
            return False
        conversation = None
        for c in conversations[::-1]:
            if c.intent != 'what_about':
                conversation = c
                break
        if conversation == None:
            return False
        return True

def string_to_dict(entities):
    ans = eval(entities)
    return ans 

def to_json(intent, action, message_answer):
    ans = dict()
    ans['intent'] = intent 
    ans['action'] = action
    ans['message_answer'] = message_answer
    return ans

def is_ask_more(conversation_id):
    conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))
    if len(conversations) == 0:
        return False
    print("conversations[-1].action: ", conversations[-1].action)
    if conversations[-1].action in ['action_ask_hero','action_ask_skill','action_ask_hero_and_skill','action_ask_intent']:
        return True
    return False

def get_action_ask_more(conversation_id):
    conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))
    if conversations[-1].action in ['action_ask_hero','action_ask_skill','action_ask_hero_and_skill','action_ask_intent']:
        return conversations[-1].action
    return None

def get_conversation_ask_more(conversation_id):
    conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))[::-1]
    conversation = None
    for c in conversations:
        if c.action in ['action_ask_hero','action_ask_skill','action_ask_hero_and_skill','action_ask_intent']:
            conversation = c
            break
    if conversation == None:
        return list(Conversation.query.filter_by(conversation_id=conversation_id))[-1]
    return conversation

def get_conversation_what_about(conversation_id):
    conversation = None
    conversations = list(Conversation.query.filter_by(conversation_id=conversation_id))
    for c in conversations[::-1]:
        if c.intent != 'what_about':
            conversation = c 
            break
    return conversation

def tolower_message(message_question):
    ans = message_question.lower()
    return ans 

def getDictPostResponse(conversation_id, message_question, entities, prob, intent):
    try:
        if "chào" in message_question.lower() or "hello" in message_question.lower() or "hi" in message_question.lower():
            intent = "say_hi"
            action = "action_say_hi"
            message_answer = "chào bạn, đây là chatbot lol."
            print(message_question.lower())
            res = to_json(intent, action, message_answer)
            return res
        if prob > 0.80:
            if ('champion' in entities and intent != 'how_to_use_skill') or ('champion' in entities and 'skill' in entities and intent == 'how_to_use_skill'):
                champion = Champion.query.filter_by(name=entities['champion']).first()
                message_answer = get_raw_answer(intent, champion)
                message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
                conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
                res = to_json(intent, action, message_answer)
                # res['probability'] = str(prob)          
                #return intent, action, message
                return res 
            
        if is_ask_more(conversation_id) == False:
            if intent == 'what_about':
                conversation_what_about = get_conversation_what_about(conversation_id)

                if 'champion' not in entities and 'skill' not in entities:
                    action = 'action_ask_hero_and_skill'
                    message_answer = 'Khong xac dinh duoc hero va skill, moi ban nhap hero va skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=conversation_what_about.intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    #return intent, action, message
                    return res

                if 'champion' not in entities:
                    action = 'action_ask_hero'
                    message_answer = 'Khong xac dinh duoc hero, moi ban nhap hero'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=conversation_what_about.intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    #return intent, action, message
                    return res

                if 'skill' not in entities and conversation_what_about.intent == 'how_to_use_skill':
                    action = 'action_ask_skill'
                    message_answer = 'Khong xac dinh duoc skill, moi ban nhap skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=conversation_what_about.intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    #return intent, action, message
                    return res


                entities_what_about = string_to_dict(conversation_what_about.entities)
                if 'champion' in entities_what_about:
                    entities['champion'] = entities_what_about['champion']
                if 'skill' in entities_what_about:
                    entities['skill'] = entities_what_about['skill']
                    
                champion = Champion.query.filter_by(name=entities['champion']).first()  
                message_answer = get_raw_answer(intent, champion)
                message_answer,action = normalize_message(conversation_what_about.intent,message_answer,entities,champion,conversation_id)
                conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=conversation_what_about.intent,entities=entities, action="action_"+intent)
                res = to_json(intent, action, message_answer)
                # res['probability'] = str(prob)          
                #return intent, action, message
                return res

            if prob < 0.5: 
                action = 'action_ask_intent'
                message_answer = 'Khong xac dinh duoc intent, moi ban nhap lai cau ro rang hon'
                conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                res = to_json(intent, action, message_answer)
                # res['probability'] = str(prob) 
                return res

            if intent == 'how_to_use_skill':
                print("entities:", entities)
                if 'champion' not in entities and 'skill' not in entities:
                    action = 'action_ask_hero_and_skill'
                    message_answer = 'Khong xac dinh duoc hero va skill, moi ban nhap hero va skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
        
                if 'champion' not in entities:
                    action = 'action_ask_hero'
                    message_answer = 'Khong xac dinh duoc hero, moi ban nhap hero'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
        
                if 'skill' not in entities:
                    action = 'action_ask_skill'
                    message_answer = 'Khong xac dinh duoc skill, moi ban nhap skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
        
            if intent != 'how_to_use_skill':
                if 'champion' not in entities:
                    action = 'action_ask_hero'
                    message_answer = 'Khong xac dinh duoc hero, moi ban nhap hero'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
        
            champion = Champion.query.filter_by(name=entities['champion']).first()
            message_answer = get_raw_answer( intent, champion)
            message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
            conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                            message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
            res = to_json(intent, action, message_answer)
            # res['probability'] = str(prob)          
            #return intent, action, message
            return res
        


        if is_ask_more(conversation_id):
            conversation_ask_more = get_conversation_ask_more(conversation_id)
            if conversation_ask_more.action == 'action_ask_hero':
                if 'champion' in entities:
                    name = entities['champion']
                    intent = conversation_ask_more.intent
                    champion = Champion.query.filter_by(name=name).first()
                    entities_ask_more = string_to_dict(conversation_ask_more.entities)
                    if 'skill' in entities_ask_more:
                        entities['skill'] = entities_ask_more['skill']  
                    message_answer = get_raw_answer( intent, champion)
                    message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    return res
                else:
                    action = 'action_ask_hero'
                    message_answer = 'Khong xac dinh duoc hero, moi ban nhap hero'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
            
            if conversation_ask_more.action == 'action_ask_skill':
                print(conversation_ask_more.message_question)
                if 'skill' in entities:
                    entities_ask_more = string_to_dict(conversation_ask_more.entities)
                    if 'champion' in entities_ask_more:
                        entities['champion'] = entities_ask_more['champion']
                    print("entities", entities)
                    name = entities['champion']
                    intent = conversation_ask_more.intent
                    champion = Champion.query.filter_by(name=name).first()
                    message_answer = get_raw_answer(intent, champion)
                    message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    return res
                else:
                    action = 'action_ask_skill'
                    message_answer = 'Khong xac dinh duoc skill, moi ban nhap skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res
            
            if conversation_ask_more.action == 'action_ask_hero_and_skill':
                
                if 'skill' in entities and 'champion' in entities:
                    entities_ask_more = string_to_dict(conversation_ask_more.entities)
                    name = None
                    new_entities = dict()
                    if 'champion' in entities:
                        new_entities['champion'] = entities['champion']
                    if 'skill' in entities:
                        new_entities['champion']     = entities['skill']
                    if 'champion' in entities_ask_more:
                        new_entities['champion'] = entities_ask_more['champion']
                    if 'skill' in entities:
                        new_entities['champion'] = entities_ask_more['skill']
                    
                    champion = Champion.query.filter_by(name=new_entities['champion']).first()
                    intent = conversation_ask_more.intent
                    message_answer = get_raw_answer(intent, champion)
                    message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)
                    db.session.add(conversation)
                    db.session.commit()
                    return res
                else:
                    action = 'action_ask_hero_and_skill'
                    message_answer = 'Khong xac dinh duoc hero va skill, moi ban nhap hero va skill'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    db.session.add(conversation)
                    db.session.commit()
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res

            if conversation_ask_more.action == 'action_ask_intent':
                if ('champion' in entities and intent != 'how_to_use_skill') or ('champion' in entities and 'skill' in entities and intent == 'how_to_use_skill'):
                    champion = Champion.query.filter_by(name=entities['champion']).first() 
                    message_answer = get_raw_answer( intent, champion)
                    message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                    message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
                    db.session.add(conversation)
                    db.session.commit()
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)          
                    #return intent, action, message
                    return res 
                else:
                    action = 'action_ask_intent'
                    message_answer = 'Khong xac dinh duoc intent'
                    conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                                message_answer=message_answer,intent=intent,entities=entities, action=action)
                    db.session.add(conversation)
                    db.session.commit()
                    res = to_json(intent, action, message_answer)
                    # res['probability'] = str(prob)  
                    return res

    except Exception:
        intent = "action_ask_intent"
        message_answer = 'Toi khong hieu ban noi gi. Moi ban nhap lai ro rang'
    
        if 'champion' not in entities:
            entities['champion'] = 'Aatrox'
        if 'skill' not in entities:
            entities['skill'] = 'Q'
        intent = 'how_to_use_skill'
        champion = Champion.query.filter_by(name=entities['champion']).first() 
        message_answer = get_raw_answer( intent, champion)
        message_answer,action = normalize_message(intent,message_answer,entities,champion,conversation_id)
        conversation = Conversation(conversation_id=conversation_id,message_question=message_question,
                        message_answer=message_answer,intent=intent,entities=entities, action="action_"+intent)
        db.session.add(conversation)
        db.session.commit()
        res = to_json(intent, action, message_answer)
        return res 
