import json
import random
import pickle
import numpy as np
from langchain.tools import BaseTool

JSON_PATH = 'static/sensor_response_data.json'
MODEL_PATH = 'static/sentence_transformer_model.pkl'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

class PlantSensor(BaseTool):
    name = "Plant_For_Sensor"
    description = """조건에 맞는 응답을 가져올 때 사용하는 도구이다. 이때, 배열에 있는 응답 중 하나를 랜덤으로 추출하고 그대로 응답한다."""  
    data : list
    
    def __init__(self, data : list = [0,0,0,0]) :
      super(PlantSensor, self).__init__(data = data)
      print(data)

    def _run(self, query: str) -> str:
        return get_response(query, arduino_data=self.data)
    
    async def _arun(self, query: str) -> str:
        raise NotImplementedError("질문에 답할 수 없어요.")


def get_response(query, arduino_data):
    
    def get_most_similar_question(query):
        query_embedding = model.encode(query)
        similarities = {}
        for plant_name in data['plants'].keys():
            plant_embedding = model.encode(plant_name)
            similarity = np.dot(query_embedding, plant_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(plant_embedding))
            similarities[plant_name] = similarity
        most_similar_plant = max(similarities, key=similarities.get)
        return most_similar_plant
        
    current_conditions = {
      "temperature": arduino_data[0], 
      "humidity": arduino_data[1], 
      "illumination": arduino_data[2], 
      "moisture": arduino_data[3]
      }
    # print(current_conditions)
    responses = data["plants"].get(get_most_similar_question(query), {}).get("environment_responses", [])
    
    valid_responses = []
    for response in responses:
        conditions = response["conditions"]
        is_valid = all(
            conditions[condition]["low"] <= current_conditions[condition] <= conditions[condition]["high"]
            for condition in conditions
        )
        if is_valid:
            valid_responses.extend(response["response"].values())

    all_responses = []
    for resp in valid_responses:
        for condition, value in current_conditions.items():
            resp = resp.replace(f"${{{condition}}}", str(value))
        all_responses.append(resp)
    
    if all_responses:
        return all_responses
    
    return ["지금은 응답을 해드릴 수 없어요."]



