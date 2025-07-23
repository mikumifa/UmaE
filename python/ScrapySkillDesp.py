import requests
from bs4 import BeautifulSoup
import json


def fetch_add_save_new(save_path="src/components/data/skillDetail_cn.json"):
    url = "https://wiki.biligame.com/umamusume/%E7%AE%80%E4%B8%AD%E6%8A%80%E8%83%BD%E9%80%9F%E6%9F%A5%E8%A1%A8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "Referer": "https://wiki.biligame.com/umamusume/%E7%AE%80/%E7%87%83%E7%83%A7%E9%9D%92%E6%98%A5%C2%B7%E9%80%9F",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    json_div = soup.find("div", {"id": "jn-json"})
    clean_json = json_div.text
    start = clean_json.find("[")
    end = clean_json.rfind("]") + 1
    json_text = clean_json[start:end]
    index = json_text.rfind(",")
    if index != -1:
        json_text = json_text[:index] + json_text[index + 1 :]
    data = json.loads(json_text)
    field_map = {
        "1": "full_name",  # "简/精诚所至，金石为开"
        "3": "skill_name",  # "精诚所至，金石为开"
        "5": "rarity_cn",  # "独特"
        "6": "condition_cn",  # "通用"
        "8": "description",  # 技能描述
        "10": "trigger_desc",  # 触发条件描述
        "11": "skill_type_cn",  # 技能类型
        "12": "skill_value",  # 技能数值
        "13": "duration",  # 持续时间
        "17": "skill_id",  # 技能ID
        "18": "score",  # 评价分
        "19": "cooldown",  # 冷却时间
        "20": "cost_pt",  # 技能消耗PT
        "23": "display_name",  # 显示用名称
    }

    def convert_skill(raw_skill):
        skill = {}
        for k, v in raw_skill.items():
            key = field_map.get(k)
            if key:
                skill[key] = v
        return skill

    skills = {}
    for d in data:
        skill = convert_skill(d)
        skills[skill["skill_name"]] = skill
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fetch_add_save_new()
