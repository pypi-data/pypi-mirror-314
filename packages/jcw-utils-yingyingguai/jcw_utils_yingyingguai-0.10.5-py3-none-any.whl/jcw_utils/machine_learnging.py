from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np


def custom_kmeans(texts):
    # 假设这是你的文本数据列表
    texts = ['dict for dict in filepaths_jsonl',
            'dict for dict in filepaths_jsonl',]

    # 文本预处理（这里省略了，可以添加停用词去除、词干提取等步骤）

    # 特征提取：使用TF-IDF向量化文本
    vectorizer = TfidfVectorizer(max_features=20)  # 假设我们只取前5个最重要的特征
    X = vectorizer.fit_transform(texts)

    # 选择聚类算法：这里使用K-Means
    kmeans = KMeans(n_clusters=3, random_state=1000)

    # 训练聚类模型
    kmeans.fit(X)

    # 聚类标签分配
    predicted_labels = kmeans.predict(X)

    # 评估模型：使用轮廓系数
    silhouette_avg = silhouette_score(X, predicted_labels)
    print("Silhouette Coefficient: ", silhouette_avg)

    # 打印聚类结果
    for i, label in enumerate(predicted_labels):
        print(f"Document {texts[i]} belongs to cluster {label}")
    
    
