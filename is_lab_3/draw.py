import networkx as nx
import matplotlib.pyplot as plt

# Создаём направленный граф
G = nx.DiGraph()

# --- 1. Базовый фрейм ---
G.add_node("Frame (базовый фрейм)", style='filled', fillcolor='orange')

# --- 2. Основные классы, наследуемые от Frame ---
G.add_node("Device", style='filled', fillcolor='#A5D8F3')
G.add_node("User", style='filled', fillcolor='#A5D8F3')
G.add_node("AutomationScenario", style='filled', fillcolor='#A5D8F3')

# Связи от базового фрейма
G.add_edge("Frame (базовый фрейм)", "Device")
G.add_edge("Frame (базовый фрейм)", "User")
G.add_edge("Frame (базовый фрейм)", "AutomationScenario")

# --- 3. Наследники Device: Sensor и Actuator ---
G.add_node("Sensor", style='filled', fillcolor='#CFEFFF')
G.add_node("Actuator", style='filled', fillcolor='#CFEFFF')

G.add_edge("Device", "Sensor")
G.add_edge("Device", "Actuator")

# --- 4. Наследники Sensor: TemperatureSensor, LightSensor ---
G.add_node("TemperatureSensor", style='filled', fillcolor='#CFEFFF')
G.add_node("LightSensor", style='filled', fillcolor='#CFEFFF')

G.add_edge("Sensor", "TemperatureSensor")
G.add_edge("Sensor", "LightSensor")

# --- 5. Наследники Actuator: Heater, SmartLight ---
G.add_node("Heater", style='filled', fillcolor='#CFEFFF')
G.add_node("SmartLight", style='filled', fillcolor='#CFEFFF')

G.add_edge("Actuator", "Heater")
G.add_edge("Actuator", "SmartLight")

# --- 6. Наследники User: AdminUser, RegularUser ---
G.add_node("AdminUser", style='filled', fillcolor='#CFEFFF')
G.add_node("RegularUser", style='filled', fillcolor='#CFEFFF')

G.add_edge("User", "AdminUser")
G.add_edge("User", "RegularUser")

# --- 7. Добавляем несколько конкретных объектов (экземпляров) ---
# Пример Heater
G.add_node("MyHeater\n(location=LivingRoom,\nis_on=False,\nmax_temp=30)",
           style='filled', fillcolor='#BFFFBF')
G.add_edge("Heater", "MyHeater\n(location=LivingRoom,\nis_on=False,\nmax_temp=30)", 
           label="экземпляр")

# Пример SmartLight
G.add_node("MainLight\n(location=Kitchen,\nis_on=True,\nbrightness=70)",
           style='filled', fillcolor='#BFFFBF')
G.add_edge("SmartLight", "MainLight\n(location=Kitchen,\nis_on=True,\nbrightness=70)", 
           label="экземпляр")

# Пример AutomationScenario
G.add_node("MyScenario\n(condition=temp<20,\naction=turn on heater)",
           style='filled', fillcolor='#BFFFBF')
G.add_edge("AutomationScenario", "MyScenario\n(condition=temp<20,\naction=turn on heater)",
           label="экземпляр")

# Пример AdminUser
G.add_node("John\n(username=john_adm,\nprivileges=full_access)",
           style='filled', fillcolor='#FFCFE0')
G.add_edge("AdminUser", "John\n(username=john_adm,\nprivileges=full_access)", 
           label="экземпляр")

# Пример RegularUser
G.add_node("Mary\n(username=mary_usr,\nprivileges=limited_access)",
           style='filled', fillcolor='#FFCFE0')
G.add_edge("RegularUser", "Mary\n(username=mary_usr,\nprivileges=limited_access)", 
           label="экземпляр")

# --- 8. Отобразим связи между объектами, если нужно ---
# Например, MyHeater "установлен" в MyScenario или как-то участвует
G.add_edge("MyScenario\n(condition=temp<20,\naction=turn on heater)",
           "MyHeater\n(location=LivingRoom,\nis_on=False,\nmax_temp=30)",
           label="включить при temp<20")

# MainLight или Heater может быть управляем пользователем (John, Mary) — пример
G.add_edge("John\n(username=john_adm,\nprivileges=full_access)",
           "MyHeater\n(location=LivingRoom,\nis_on=False,\nmax_temp=30)",
           label="управляет")

# --- 9. Настройка отрисовки ---
pos = nx.spring_layout(G, k=2, seed=42)
plt.figure(figsize=(12, 8))

# Подписи на рёбрах
edge_labels = nx.get_edge_attributes(G, 'label')

nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='white', edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, connectionstyle='arc3,rad=0.2')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, label_pos=0.5)

plt.title("Схема фреймов «Умный дом» (Smart Home) с примерами объектов", fontsize=10)
plt.axis('off')
plt.tight_layout()
plt.show()
