import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Путь к файлу CSV
file_path = "/content/for_graph.csv"

# Загрузка данных
df = pd.read_csv(file_path, usecols=[
    'id', 'sex', 'opposition_support_ratio',
    'friend0-id', 'friend0-sex', 'friend0-opposition_support_ratio',
    'friend1-id', 'friend1-sex', 'friend1-opposition_support_ratio',
    'friend2-id', 'friend2-sex', 'friend2-opposition_support_ratio',
    'friend3-id', 'friend3-sex', 'friend3-opposition_support_ratio',
    'friend4-id', 'friend4-sex', 'friend4-opposition_support_ratio',
    'friend5-id', 'friend5-sex', 'friend5-opposition_support_ratio',
    'friend6-id', 'friend6-sex', 'friend6-opposition_support_ratio',
    'friend7-id', 'friend7-sex', 'friend7-opposition_support_ratio',
    'friend8-id', 'friend8-sex', 'friend8-opposition_support_ratio',
    'friend9-id', 'friend9-sex', 'friend9-opposition_support_ratio',
    'friend10-id', 'friend10-sex', 'friend10-opposition_support_ratio',
    'friend11-id', 'friend11-sex', 'friend11-opposition_support_ratio',
    'friend12-id', 'friend12-sex', 'friend12-opposition_support_ratio',
    'friend13-id', 'friend13-sex', 'friend13-opposition_support_ratio',
    'friend14-id', 'friend14-sex', 'friend14-opposition_support_ratio',
    'friend15-id', 'friend15-sex', 'friend15-opposition_support_ratio',
    'friend16-id', 'friend16-sex', 'friend16-opposition_support_ratio',
    'friend17-id', 'friend17-sex', 'friend17-opposition_support_ratio',
    'friend18-id', 'friend18-sex', 'friend18-opposition_support_ratio',
    'friend19-id', 'friend19-sex', 'friend19-opposition_support_ratio'
])

# Создание графа
G = nx.Graph()

# Добавляем основные узлы и их атрибуты, пропуская нулевые значения.
for index, row in df.iterrows():
    if row['id'] != 0:
        G.add_node(row['id'], 
                   sex=row['sex'], 
                   opposition_support_ratio=row['opposition_support_ratio'])

        for i in range(20):  # 20 друзей
            friend_id_col = f'friend{i}-id'
            if friend_id_col in row and pd.notna(row[friend_id_col]) and row[friend_id_col] != 0:
                friend_id = row[friend_id_col]
                friend_sex = row.get(f'friend{i}-sex')
                friend_opposition_support_ratio = row.get(f'friend{i}-opposition_support_ratio')

                # Добавляем каждого друга как узел, если его еще нет в графе
                if friend_id not in G:
                    G.add_node(friend_id, 
                            sex=friend_sex, 
                            opposition_support_ratio=friend_opposition_support_ratio)
                
                # Добавляем ребро между основным узлом и его другом
                G.add_edge(row['id'], friend_id)

# Определение цвета узлов
node_colors = []
for node in G.nodes:
    opposition_support_ratio = G.nodes[node].get('opposition_support_ratio', 0)
    sex = G.nodes[node].get('sex', 'unknown')

    # Устанавливаем цвет в зависимости от уровня поддержки оппозиции и пола
    if pd.notna(opposition_support_ratio) and opposition_support_ratio > 0.5:
        color = 'red'
    else:
        color = 'green'
    
    if sex == 'male':
        color = 'blue'
    elif sex == 'female':
        color = 'pink'
    
    node_colors.append(color)

# Визуализация графа
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G, k=0.1)  # параметр k регулирует расстояние между узлами
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=50)
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
plt.title("Network Graph - Spring Layout")
plt.show()