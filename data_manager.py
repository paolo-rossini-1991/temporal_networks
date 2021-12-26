import pandas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

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
        return self.__source == edge.getTarget() and self.__target == edge.getSource() and self.__year == edge.getYear()

    def isEqual(self, edge):
        return self.__source == edge.getSource() and self.__target == edge.getTarget() and self.__year == edge.getYear()

    def hasNode(self, node):
        return self.__source == node or self.__target == node

    def print(self):
        print(['Edge #', self.__id])
        print(self.__source)
        print(self.__target)
        print(self.__year)



def plotDegree(degree_dict, node):
    years = np.array(list(degree_dict.keys()))

    individual_degree = dict()
    for i in range(years.min(), years.max() + 1):
        if i in degree_dict:
            if node in degree_dict[i]:
                individual_degree[i] = degree_dict[i][node]
            else:
                individual_degree[i] = [0, 0]
        else:
            individual_degree[i] = [0, 0]

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(list(individual_degree.keys()), list([item[0] for item in list(individual_degree.values())]))
    ax.plot(list(individual_degree.keys()), list([item[1] for item in list(individual_degree.values())]))
    plt.show()
    print(correspondence_per_year)


def individualCorrespondents(edge_list, node):

    individual_correspondents = dict()

    for edge in edge_list:
        check = True
        if edge.hasNode(node):
            if edge.getYear() in individual_correspondents:
                for edge_check in list(individual_correspondents[edge.getYear()].keys()):
                    if edge.isEqual(edge_check) or edge.isReciprocal(edge_check):
                        check = False
                        individual_correspondents[edge.getYear()][edge_check] += 1
                    if check:
                        individual_correspondents[edge.getYear()].update({edge: 1})
            else:
                individual_correspondents[edge.getYear()] = {edge: 1}

    return individual_correspondents

def correspondencePerYear(individual_correspondents, node1, node2):
    year_list = np.array(list(individual_correspondents))
    correspondence_per_year = dict()
    for year in range(year_list.min(), year_list.max()):
        correspondence_per_year[year] = 0
        if year in individual_correspondents:
            for edge in list(individual_correspondents[year].keys()):
                edge_check = Edge(node1, node2, 0, year)
                if edge_check.isEqual(edge) or edge_check.isReciprocal(edge):
                    correspondence_per_year[year] = individual_correspondents[year][edge]

    print(correspondence_per_year)



if __name__ == '__main__':
    # get current working directory
    cwd = os.getcwd()

    # read csv
    df = pandas.read_csv(cwd + '/data/Edges_Dynamic_Gephi.csv', sep=';')

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

    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(list(nodes_per_year.keys()), list(nodes_per_year.values()))

    # plotDegree(degree_dict=degree_per_year, node=27)

    individual_correspondents = individualCorrespondents(edge_list=edge_list, node=27)
    correspondencePerYear(individual_correspondents, node1=27, node2=56)
