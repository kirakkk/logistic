'''
1、处理中心点P到各个直连节点的巡回路径与往返路径的节约值；
    1.1、节点有四种类型：
        a,中心节点 p
        b,有直连路线的周围节点 a,b,c...
        c,无直连路线的周围节点 j
        d,中途节点（两个空白的节点）
    1.2、路线类型：
        a,直连线路；
        b,巡回线路；
        c,中转线路（通过中途节点到达下一个 无直连路线的周围节点）；
2、持久化节点信息；
3、计算逻辑：
    3.1、找到最短的“直连线路”
        3.1.1、如果只有一条，则为该线路；
        3.1.2、如果有中途节点，则计算配送中心P通过中途节点到达可连通的周围节点的距离，并生成直连线路；
        3.1.3、生成巡回线路（遍历各个“相邻对”），生成巡回线路列表，并进行排序；
        3.1.4、计算路线节约值，并按照节约值高低进行排序；
        3.1.5、排序后根据车辆的单程限制以及载重限制进行路线生成；
4、
'''

import shelve

info_path = "./info.db"

info = shelve.open(info_path,writeback=True)

NODE_TYPES = {1:"中心节点",
              2:"直通周围节点" ,
              3:"非直通周围节点",
              4:"中途节点" }

ROUTE_TYPES = {1:"直连线路",
               2:"巡回线路",
               3:"中转线路"}


car_load = [2,4]
distance_limit = 40


relative_dist = [[],]

class Node:
    Count = 0

    def __init__(self,node_name:str) -> None:
        Node.Count += 1
        self.name = node_name
        self.relation = {}
        pass

    def __del__(self):
        Node.Count -= 1
        print("EVENT-DELETE-Node {} deleted.".format(self.name))

    def add_relation(self,node_name:str,distance:float):
        self.relation[node_name]=distance   #添加临近节点
        pass

class Route:
    Count = 0
    def __init__(self,nodes:list):
        Route.Count += 1
        pass
        
    def __del__(self):
        Route.Count -= 1
        pass
    
    def add_route(self,node)