import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


def get_hot_topics():
    # 百度贴吧热议话题的URL
    url = "https://tieba.baidu.com/hottopic/browse/topicList"

    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有热门话题的div
        topics = soup.find_all('div', class_='topic-content')

        # 创建保存结果的文件夹
        if not os.path.exists('../../hot_topics'):
            os.makedirs('../../hot_topics')

        # 获取当前时间作为文件名
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'hot_topics/tieba_hot_topics_{current_time}.txt'

        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"百度贴吧热议话题 - 抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")

            # 只获取前20个话题
            for i, topic in enumerate(topics[:20], 1):
                # 获取话题标题
                title = topic.find('div', class_='topic-name').text.strip()
                # 获取话题描述（如果有的话）
                desc = topic.find('div', class_='topic-desc')
                desc_text = desc.text.strip() if desc else "无描述"

                # 写入话题信息
                f.write(f"{i}. {title}\n")
                f.write(f"   描述: {desc_text}\n\n")

        print(f"热门话题已保存到文件: {filename}")

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    get_hot_topics()