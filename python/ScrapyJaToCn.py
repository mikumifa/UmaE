import json
import re
import os

from bs4 import BeautifulSoup
import requests


class GameDatabase:
    def __init__(self, source_path: str, cache_path: str = "namedict.json"):
        self.source_path = source_path
        self.cache_path = cache_path
        self.index_map = {}  # type:ignore
        self._build_cache()

    def _parse_line_to_dict(self, line: str) -> dict | None:
        try:
            pattern = re.compile(r'(\w+)=["\'](.*?)["\'](?=[,}])')
            pairs = pattern.findall(line)
            return dict(pairs) if pairs else None
        except:
            return None

    def _build_cache(self):
        with open(self.source_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip(",\n ")
                if not line or "{" not in line:
                    continue
                item = self._parse_line_to_dict(line)
                if item is None:
                    continue
                if "index" in item and "text_CN" in item and "category" in item:
                    key = f"{item['category']}_{item['index']}"
                    if key in self.index_map:
                        print(f"[Warning] Duplicate index: {key}")
                    else:
                        self.index_map[key] = item

        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.index_map, f, ensure_ascii=False, indent=2)

    def _load_cache(self):
        with open(self.cache_path, "r", encoding="utf-8") as f:
            self.index_map = json.load(f)

    def get_name(self, category: str, index: str) -> str:
        """传入 category 和 index，返回 text_CN 中文名"""
        key = f"{category}_{index}"
        return self.index_map.get(key, {}).get("text_CN", f"[Missing] {key}")

    def create_map_json(
        self, source="text_JP", target="text_CN", output_path="skill-cn.json"
    ):
        """根据 source 和 target 字段，构建映射字典并写入 JSON 文件"""
        result = {}
        for item in self.index_map.values():
            if source in item and target in item:
                if item[target]:
                    result[item[source]] = item[target]
        #  "季節ウマ娘◎": "Seasonal Girl◎",
        result["季節ウマ娘◎"] = "季节优俊少女◎"
        result["季節ウマ娘○"] = "季节优俊少女○"

        #  "天気の日◎": "Weather Days◎",
        result["天気の日◎"] = "天气◎"
        result["天気の日○"] = "天气○"

        #  "良バ場◎": "Good Track Condition ◎",
        result["良バ場◎"] = "场地◎"
        result["良バ場○"] = "场地○"

        #   "小回り◎": "Tight Turns◎",
        result["小回り◎"] = "跑法擅长◎"
        result["小回り○"] = "跑法擅长○"

        # "勝負師": "Gambler",
        # result["勝負師◎"] = "幸运◎"
        # result["勝負師○"] = "幸运○"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ 映射文件已保存为: {output_path}")


# 🧪 示例用法
if __name__ == "__main__":
    url = "https://wiki.biligame.com/umamusume/%E6%A8%A1%E5%9D%97:%E7%BF%BB%E8%AF%91%E6%95%B0%E6%8D%AE%E5%BA%93"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    pre = soup.find("pre", class_="mw-code mw-script", dir="ltr")
    text_copy = pre.get_text()
    with open("python/name.lua", "w", encoding="utf-8") as f:
        f.write(text_copy)
    db = GameDatabase("python/name.lua", "name.json")
    db.create_map_json(output_path="src/locales/skill-zh.json")
