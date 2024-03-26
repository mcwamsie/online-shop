import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def get_important_features(data):
    important_features = []
    for i in range(0, data.shape[0]):
        important_features.append(
            data['product_name'][i] + " " +
            data['gender'][i] + " " +
            data['brand_name'][i] + " " +
            data['style_name'][i] + " " +
            data['category_name'][i]
        )

    return important_features


def sum_up(ids, cs):
    lists = []
    results = []
    for id in ids:
        lists.append(list(cs[id]))

    for i in range(len(lists[0])):
        results.append(0)

    for j in range(len(lists)):

        for i in range(len(lists[j])):
            results[i] += lists[j][i]
    return results


def get_similar_ids(product_ids):
    connection = sqlite3.connect('online.sqlite3')
    query = "SELECT core_product.id AS product_id, core_product.`name` AS product_name, core_style.`gender`, " \
            "core_style.`name` AS style_name, core_category.`name` AS category_name, core_brand.`name` AS brand_name, " \
            "core_style.id AS style_id, core_brand.id AS brand_id, core_category.id AS category_id FROM core_product " \
            "LEFT JOIN core_brand ON core_product.brand_id = core_brand.id LEFT JOIN core_style ON " \
            "core_product.style_id = core_style.id LEFT JOIN core_category ON core_style.category_id = " \
            "core_category.id "

    df = pd.read_sql(query, connection)
    print(df.head())

    df['important_features'] = get_important_features(df)
    print(df.head(3))
    cm = CountVectorizer().fit_transform(df['important_features'])
    cs = cosine_similarity(cm)
    index = []
    for product_id in product_ids:
        #print(product_id)
        #print(df)
        index.append(df[df.product_id == product_id].index.values.astype(int)[0])
    # print(index)
    scores = list(enumerate(sum_up(index, cs)))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    sorted_scores = sorted_scores[0:]

    similar_id = []

    j = 0
    for item in sorted_scores:
        # print(item[0])
        product_name = df[df.index == item[0]]['product_name'].values[0]
        product_id = df[df.index == item[0]]['product_id'].values.astype(int)[0]
        # print(j + 1, product_name, "(", product_id, ")")
        j = j + 1
        similar_id.append(product_id)
    return similar_id
