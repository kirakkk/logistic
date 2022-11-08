'''
1、处理中心点P到各个直连节点的巡回路径与往返路径的节约值；
    1.1、节点有四种类型：
        a,中心节点 p
        b,有直连路线的周围节点 a,b,c...
        c,无直连路线的周围节点 j （即需要经过其他周围节点才能和中心节点联通的节点）
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
    3.2、路径匹配模式：
        3.2.1、直连线路：121，12421
        3.2.2、有中途节点的直连线路：14241
        3.2.3、巡回路线：
            3.2.3.1、直连巡回路线：1221
            3.2.3.2、有中途节点的巡回路线：14221，12241，14221，142421【考虑是否穷举，或者更抽象化】
            3.2.3.3、中转线路：12321
    3.3、节约值：
        匹配好所谓的“节点对”，以 巡回路线里程 - 直连里程 = 节约值 为计算公式进行计算。
            --> 3.3.1、常规情况是 2个周围节点 及 1个中心节点；
            --> 3.3.2、特殊情况是 其中一个周围节点是无直连路线的周围节点；在这种情况下，应该遵循这样的模式 1->2->3->(若干个3类节点)->2->1
4、
'''

import shelve
from collections import namedtuple
import logging,datetime
import atexit
import sys
import os
import datetime
#from functools import reduce

#日志基本配置.
today=datetime.date.today()
print(datetime.date.strftime(today,'%Y%m%d'))
fn=os.path.join(os.path.curdir,"logs",datetime.date.strftime(today,'%Y%m%d')+".log")

if not os.path.exists(os.path.dirname(fn)):
    os.mkdir(os.path.abspath(os.path.dirname(fn)))
else:
    logging.basicConfig(level=logging.DEBUG,filename=fn,filemode='a')

info_path = "./info.db"

info = shelve.open(info_path,writeback=True)

try:
    info['Trial Times'] = +1
except KeyError:
    info['Trial Times'] = 1
finally:
    logging.debug("【系统运行记录】第 %d 次测试运行脚本。"%(info['Trial Times']))


#节点属性.
#Node = namedtuple(typename="Node_tuple",field_names=("node_name","node_type","node_load","relative_nodes", "relative_distance"))

#节点类型.
NODE_TYPES = {1:"中心节点",
              2:"直通周围节点" ,
              3:"非直通周围节点",
              4:"中途节点" }

ROUTE_TYPES = {1:"直连线路",
               2:"巡回线路",
               3:"中转线路"}

class Node:
    Count = 0
    def __init__(self,node_name:str,node_type:int,load:float = 0) -> None:
        Node.Count += 1
        print("EVENT-ADD-Node {} deleted.".format(self.name))
        self.name = node_name
        self.relation = {}
        self.load = load
        self.type = node_type

    def __del__(self):
        Node.Count -= 1
        print("EVENT-DELETE-Node {} deleted.".format(self.name))

    def add_relation(self,relative_node_name:str,distance:float):
        self.relation[relative_node_name]=distance   #添加临近节点
        pass

class Route:
    Count = 0
    def __init__(self,nodes:list):
        Route.Count += 1
        pass
        
    def __del__(self):
        Route.Count -= 1
        pass
    
    def add_route(self,node):
        pass

def saving(nodes_matrix:dict):
    nodes = nodes_matrix
    def generate_nodes(nodes):
        for k,v in nodes:    
            pass
    
    def generate_straight_routes(nodes):
        pass
    def generate_round_routes(nodes):
        pass

    def calculate_savings(nodes):
        pass

    def generate_ovarall_routes(nodes):
        pass

    return None

def data_check(node_data):
    logging.debug("【初始数据检查】初始数据检查开始..")
    from collections import Counter
    nodes = node_data.keys()
    
    for key,data in node_data:
        dist_dict = dict(zip(data[3],data[4]))
        #节点数量与对应距离数据点个数检查.
        if len(data[3])!=len(data[4]):
            logging.error("【初始数据检查】: Node %s 关联节点数量与节点距离数量不一致，请检查后重新录入数据！"% key)
        #相邻节点名称唯一性检查.
        unique_counter = Counter(data[3])
        if sum(map(lambda x: x-1,unique_counter.values())):
            logging.error("【初始数据检查】: Node %s 关联节点不唯一，请检查后重新录入数据！"% key)
            #sys.exit()
        for rel_node in data[3]:
            rel_dist_dict = dict(zip(node_data[rel_node][3],node_data[rel_node][4]))
            assert rel_node in nodes
            if key not in nodes[rel_node][3]:
                logging.error("【初始数据检查】: Node %s 关联节点 %s 不存在对应数据，请检查！"% (key,rel_node))
                #sys.exit()
            if dist_dict[rel_node]!= rel_dist_dict[key]:
               logging.error("【初始数据检查】: Node %s 关联节点 %s 所记录的距离不一致，请检查！"% (key,rel_node))
               #sys.exit()
            pass

def route_exists(dictkeys,target_node:str):
    if dictkeys:
        status_map = map(lambda x:x[-1]==target_node,dictkeys)
        return sum(list(status_map))
    else:
        return 0


def main():
    #用字典储存节点图，两个中途节点分别标记为x,y;
    #逆时针记录临近节点；
    node_matrix = {'p':[1,0,'abcxyghi',[10,9,7,6,5,3,4,10]],
                'a':[2,0.2,'bpji',[4,10,9,11]],
                'b':[2,1.5,'cpa',[5,9,4]],
                'x':[4,0,'pcde',[6,4,2,5]],
                'c':[2,1.4,'bdxp',[5,5,4,7]],
                'd':[3,1.0,'cex',[5,6,2]],
                'e':[3,1.5,'xdyf',[5,6,6,7]],
                'y':[4,0,'pefg',[5,6,3,4]],
                'f':[3,0.5,'gye',[6,3,7]],
                'g':[2,0.6,'hpyf',[2,3,4,6]],
                'h':[2,0.8,'ipg',[9,4,2]],
                'i':[2,0.6,'ajph',[11,8,10,9]],
                'j':[3,1.6,'ai',[9,8]]} 
    car_load = [2,4]
    distance_limit = 40
    
    #①检查数据有效性.
    data_check(node_matrix)

    #②数据有效性检查通过后，直连路线生成.
    #routes_direct_dict = {'connected_nodes':['线路类型',线路长度]}
    routes_direct_dict = {}
    
    def generate_direct_routes(nodes):
        nonlocal routes_direct_dict
        assert nodes['p']
        for node in nodes['p'][2]:
            index = nodes['p'][2].index(node)
            #①对于“直通周围节点”，直接生成“直连线路”，并记录 1、线路类型， 2、线路长度；
            if nodes[node][0] == 2:
                distance = nodes['p'][3][index]
                routes_direct_dict['p'+node]= [1,distance]
                logging.debug("【生成线路】【直通线路】 p ---> %s, 距离 %d ."%(node,distance))
            #②对于“中途节点”，探索它的下一个节点，当它是“非直通周围节点”则进行路径生成；
            if nodes[node][0] == 4:
                for indirect_node in nodes[node][2]:
                    #如果跳转后节点为非直通周围节点，则进行路线生成；
                    if nodes[indirect_node][0] == 3:
                        #距离= 中途节点-->p + 节点-->中途节点 的距离之和；
                        #只支持单层中途节点的情况，多层的情况应该需要递归判断；
                        distance = nodes[indirect_node][3][nodes[indirect_node][2].index("p")]\
                                    + nodes[node][3][nodes[node][2].index(indirect_node)]
                        #如果路径中已经存在了同一个路线，则选择短的路线作为最终选定的生成路径；（？路线标记需要中途节点名么？）
                        if 'p'+indirect_node in routes_direct_dict.keys():
                            distance_old = routes_direct_dict['p'+indirect_node][1]
                            distance = min(distance_old,distance)
                        routes_direct_dict['p'+indirect_node] = [3,distance]
                        logging.debug("【生成线路】【中转线路】 p ---> %s, 距离 %d ."%(indirect_node,distance))
                    else:
                        #如果跳转后的节点为其他类型的节点则不作处理（比如直通的周围节点、中途节点（本例中不存在，暂不予考虑））；
                        pass
            #③对于非直连周围节点，再检查一次是否已经都生成了路线（例题中的j节点），如果没有生成路线，则补充生成；
            if nodes[node][0]==3:
                #如果已经生成过路线了就不做操作；
                if route_exists(routes_direct_dict.keys(),node):
                    continue
                #如果没有生成过路线，就找到达node节点的最短线路；
                else:
                    for indirect_node in nodes[node][2]:
                        if 'p' in nodes[indirect_node][2]:
                            distance = nodes[indirect_node][3][nodes[indirect_node][2].index("p")] \
                                        + nodes[node][3][nodes[node][2].index(indirect_node)]
                            routes_direct_dict['p'+indirect_node+node] = [1,distance]
                            logging.debug("【生成线路】【中转线路】 p ---> %s, 距离 %d ."%(node,distance))
                            
                            for k in routes_direct_dict.keys():
                                if node in k:
                                    distance_old = routes_direct_dict[k][1]
                                    if distance <= distance_old:
                                        logging.debug("【删除线路】【中转线路】 p ---> %s, 距离 %d ."%(k[-1],routes_direct_dict.pop(k)))
                                    elif distance > distance_old:
                                        routes_direct_dict.pop('p'+indirect_node+node)
                                        pass
                            
                        else:
                            continue

#测试推送git



