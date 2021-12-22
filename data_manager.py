import pandas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Edge:
    def __init__(self, a, b, id, year):
        self.__source = a
        self.__target = b
        self.__id = id
        self.__year = year

    def setSource(self, source):
        self.__source = source

    def setTarget(self, target):
        self.__target = target

    def setYear(self, year):
        self.__year = year

    def getSource(self):
        return self.__source

    def getTarget(self):
        return self.__target

    def getYear(self):
        return self.__year

    def isReciprocal(self, edge):
        return self.__source == edge.getTarget() and self.__target == edge.getSource()

    def isEqual(self, edge):
        return self.__source == edge.getSource() and self.__target == edge.getTarget() and self.__year == edge.getYear()

    def print(self):
        print(['Edge #', self.__id])
        print(self.__source)
        print(self.__target)
        print(self.__year)

df = pandas.read_csv('/home/luca/Downloads/Edges_Dynamic_Gephi.csv', sep=';')

years = np.array(df['onset'])

edges_per_year = dict()
for i in range(years.min(), years.max()+1):
    edges_per_year[i] = np.count_nonzero(years == i)

year_list = list()
for key in edges_per_year:
    if edges_per_year[key] > 0:
        year_list.append(key)

edge_list = list()
for i in range(len(df['source'])):
    edge = Edge(int(df[i:i + 1]['source']), int(df[i:i + 1]['target']), int(df[i:i + 1]['edge.id']), int(df[i:i + 1]['onset']))
    edge_list.append(edge)

degree_per_year = dict()
for year in year_list:
    temp = dict()
    old_size = len(temp)
    num_source = 0
    num_target = 0
    for edge in edge_list:
        if edge.getYear() == year:
            if edge.getSource() in temp.keys():
                num_source = temp[edge.getSource()][0] + 1
                num_target = temp[edge.getSource()][1]
                temp.update({edge.getSource(): [num_source, num_target]})
            else:
                temp.update({edge.getSource(): [1, 0]})

            if edge.getTarget() in temp.keys():
                num_source = temp[edge.getTarget()][0]
                num_target = temp[edge.getTarget()][1] + 1
                temp.update({edge.getTarget(): [num_source, num_target]})
            else:
                temp.update({edge.getTarget(): [0, 1]})
    degree_per_year[year] = temp

# edges_per_year
fig, ax = matplotlib.pyplot.subplots()
ax.plot(list(edges_per_year.keys()), list(edges_per_year.values()))

# nodes_per_year
nodes_per_year = dict()
for key in degree_per_year:
    nodes_per_year[key] = len(degree_per_year[key])

print(degree_per_year)
print(nodes_per_year)

fig, ax = matplotlib.pyplot.subplots()
ax.plot(list(nodes_per_year.keys()), list(nodes_per_year.values()))
plt.show()