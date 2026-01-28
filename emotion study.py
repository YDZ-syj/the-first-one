# -*- coding: utf-8 -*-
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        """初始化分析器，加载情感词典"""
        self.sentiment_words = self._load_sentiment_words()
        self.history = {'positive': 0, 'negative': 0, 'neutral': 0}
        self.tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        self.all_texts = []

    def _load_sentiment_words(self):
        """加载基础情感词典（实际应用中可扩展更大词典）"""
        words = {
            'positive': ['love', 'excellent', 'great', 'wonderful', 'amazing', 'best', 'happy'],
            'negative': ['hate', 'terrible', 'awful', 'horrible', 'worst', 'angry', 'sad'],
            'neutral': ['the', 'and', 'but', 'if', 'then', 'it', 'is']
        }
        return words

    def analyze_sentiment(self, text):
        """分析文本情感"""
        self.all_texts.append(text)

        # 使用TextBlob进行基础情感分析
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        # 确定情感类别
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        self.history[sentiment] += 1
        return sentiment, polarity

    def extract_keywords(self, text):
        """提取文本中的情感关键词"""
        # 使用TF-IDF提取重要词汇
        if len(self.all_texts) > 1:
            tfidf_matrix = self.tfidf.fit_transform(self.all_texts)
            feature_array = np.array(self.tfidf.get_feature_names_out())
            tfidf_sorting = np.argsort(tfidf_matrix[-1].toarray()).flatten()[::-1]
            top_keywords = feature_array[tfidf_sorting][:5]
        else:
            words = re.findall(r'\b\w+\b', text.lower())
            top_keywords = sorted(set(words), key=lambda x: len(x), reverse=True)[:5]

        # 识别情感词汇
        sentiment_keywords = defaultdict(list)
        for word in top_keywords:
            for sentiment, words_list in self.sentiment_words.items():
                if word in words_list:
                    sentiment_keywords[sentiment].append(word)

        return sentiment_keywords

    def visualize_sentiment(self):
        """创建情感可视化图表"""
        plt.figure(figsize=(12, 5))

        # 饼图
        plt.subplot(1, 2, 1)
        labels = ['Positive', 'Negative', 'Neutral']
        sizes = [self.history['positive'], self.history['negative'], self.history['neutral']]
        colors = ['#66c2a5', '#fc8d62', '#8da0cb']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Sentiment Distribution')

        # 柱状图
        plt.subplot(1, 2, 2)
        plt.bar(labels, sizes, color=colors)
        plt.title('Sentiment Count')
        plt.ylabel('Number of Texts')

        plt.tight_layout()
        plt.savefig('sentiment_analysis.png')
        plt.close()
        print("图表已保存为 'sentiment_analysis.png'")

    def analyze_and_visualize(self, text):
        """完整分析流程"""
        print("\n" + "=" * 50)
        print(f"分析文本: \"{text}\"")

        # 情感分析
        sentiment, polarity = self.analyze_sentiment(text)
        print(f"情感类别: {sentiment.capitalize()} (极性分数: {polarity:.2f})")

        # 关键词提取
        keywords = self.extract_keywords(text)
        print("\n情感关键词:")
        for sentiment_type, words in keywords.items():
            if words:
                print(f"  - {sentiment_type.capitalize()}: {', '.join(words)}")

        # 可视化
        self.visualize_sentiment()
        print("=" * 50 + "\n")


# 主程序
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    print("社交媒体情绪分析仪 - 输入文本进行情绪分析 (输入'exit'退出)")
    while True:
        text = input("\n请输入文本: ")
        if text.lower() == 'exit':
            break

        analyzer.analyze_and_visualize(text)