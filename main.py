import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Slider
import pandas as pd


data = pd.read_csv('imports-exports-commerciaux.csv')

tabDate=[]

G = nx.Graph()

for index in ['cwe', 'es', 'it', 'gb', 'ch']:
    source = 'fr'
    G.add_edge(source, index)

pos = nx.spring_layout(G)

fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.2)

color_map = {'fr': 'blue', 'cwe': 'yellow', 'es': 'orange', 'it': 'green', 'gb': 'grey', 'ch': 'red'}
labels = {node: node for node in G.nodes()}

nx.draw(G, pos, ax=ax, node_color=[color_map[node] for node in G.nodes()], labels=labels)

axcolor = 'lightgoldenrodyellow'

#Permet de placer le slider
axslid = plt.axes([0.25, 0.05, 0.50, 0.03])
#Création du slider de 0 à 6209 jours (nb de ligne du fichier csv)
slider=Slider(axslid, 'NB jours', 0.0, 6209.0, 1.0)
title=plt.text(1.15, 2.05, 'Dates', fontsize=12, ha='center', va='center')


#Tri fusion pour trier le tableau de date de la date la plus ancienne à la plus récente
def tri_fusion(tab):
    if len(tab) > 1:
        milieu = len(tab) // 2
        gauche = tab[:milieu]
        droite = tab[milieu:]

        tri_fusion(gauche)
        tri_fusion(droite)

        i = j = k = 0

        while i < len(gauche) and j < len(droite):
            if gauche[i] < droite[j]:
                tab[k] = gauche[i]
                i += 1
            else:
                tab[k] = droite[j]
                j += 1
            k += 1

        while i < len(gauche):
            tab[k] = gauche[i]
            i += 1
            k += 1

        while j < len(droite):
            tab[k] = droite[j]
            j += 1
            k += 1
        
    return tab

#Convertir la colonne 'date' en objet Date
date=pd.to_datetime(data['date'], format="%Y-%m-%d")

#Boucle pour avoir un format YYYY-MM-DD et rentrer les valeurs dans le tableau 
for row in date:
    date_str=row.date().isoformat()
    tabDate.append(date_str)

tab_tmp=[]
tab_tmp=tri_fusion(tabDate)
print("Début : ", tab_tmp[0])
print("Fin : ", tab_tmp[len(tab_tmp) - 1])



prev_val = 0

#Fonction qui se déclence à chaque changement de valeur du slider
def update(val):
    indice=0
    global prev_val
    global slider_value
    data2 = pd.read_csv('imports-exports-commerciaux.csv')
    slider_value = int(slider.val) # convertir la valeur du slider en entier
    title.set_text('Date: {}'.format(tab_tmp[slider_value])) # mettre à jour le texte avec la date correspondante
    num_row=slider_value

    for i in data2['date']:
        indice=indice+1
        if i == tab_tmp[slider_value]:
            num_row=indice

    print("La date est", tab_tmp[slider_value])
    
    if val != prev_val:
        prev_val = val

        # Modifier la largeur des arêtes en fonction de la valeur de l'export entre la france et ses pays voisins
        for index in ['cwe', 'es', 'it', 'gb', 'ch']:
            source = 'fr'
            exportFr=int(data2['fr_'+ index][num_row-1])
            importFr= int(data2[index +"_fr"][num_row-1])
            #Pour une meilleur visibilité des arêtes, on augmente les valeurs lorsqu'elles sont proches de 0
            if exportFr >= 0 and exportFr <300:
                exportFr=300

            if importFr < 0:
                importFr=importFr*(-1)
            
            if importFr >= 0 and importFr < 600:
                importFr=600

            G.add_edge(source, index, width=exportFr/450, alpha=importFr/4000)
            print(index+" -> export & import = ", int(data2['fr_'+ index][num_row-1]), " & ", int(data2[index +"_fr"][num_row-1]))

        ax.clear()
        edges = nx.draw_networkx_edges(
                                            G,
                                            pos,
                                            ax=ax,
                                            width=[G[u][v].get('width', 1.0) for u, v in G.edges()],
                                            alpha= [G[u][v].get('alpha', 1.0) for u, v in G.edges()]
                                       )
        nx.draw_networkx_labels(G, pos, labels, font_size=10, ax=ax)
        plt.draw()


slider.on_changed(update)

plt.show()
