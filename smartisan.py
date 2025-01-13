#!/usr/bin/env python3

import os
import requests

def download_image(img_url, save_path, max_retries=3):
    """下载单张图片并保存到指定路径，支持重试"""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(img_url, timeout=10)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"成功下载: {img_url}")
            return  # 下载成功后直接返回
        except Exception as e:
            print(f"下载失败 [第{attempt}次尝试]: {img_url}, 错误信息: {e}")
    # 如果所有尝试都失败
    print(f"下载多次失败，放弃: {img_url}")

def main():
    base_dir = "/Users/arthur/Pictures/SmartisanOS"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    url = "http://api-app.smartisan.com/app/index.php?r=paperapi/index/list&client_version=2&limit=10000&paper_id=0"

    try:
        response = requests.get(url)
        data_json = response.json()
    except Exception as e:
        print("请求或解析 JSON 出错:", e)
        return

    if data_json.get("code", -1) != 0 or not data_json.get("data"):
        print("没有满足条件的数据或拉取失败，结束下载。")
        return

    data_list = data_json["data"]
    total_downloaded = 0

    for item in data_list:
        source = item.get("source", "Unknown")  # 图片来源
        img_url = item.get("url", "")
        img_id = item.get("id", "no_id")

        source_dir = os.path.join(base_dir, source)
        if not os.path.exists(source_dir):
            os.makedirs(source_dir, exist_ok=True)

        save_path = os.path.join(source_dir, f"{img_id}.jpg")

        if img_url:
            # 增加重试功能
            before_exist = os.path.exists(save_path)
            download_image(img_url, save_path, max_retries=3)
            # 如果成功下载，文件一定会存在
            if not before_exist and os.path.exists(save_path):
                total_downloaded += 1

    print(f"所有壁纸下载完成，共下载 {total_downloaded} 张。")

if __name__ == "__main__":
    main()