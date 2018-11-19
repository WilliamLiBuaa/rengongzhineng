import numpy as np
import time
import copy
#
# state_final = ([1,2,3],
#                [8,0,4],
#                [7,6,5])
# state0 = ([0,1,8],
#           [4,2,3],
#           [5,6,7])
# state0=([2,8,3],
#         [1,0,4],
#         [7,5,6])
move_dict={'up':[-1,0],'down':[1,0],'right':[0,1],'left':[0,-1]}
state_final=([1,2,3,4],
             [5,6,7,8],
             [9,10,11,12],
             [13,14,15,0])
state0=([11,9,4,15],
        [1,3,0,12],
        [7,5,8,6],
        [13,2,10,14])
# state0=([1,4,3,2],
#         [9,6,8,7],
#         [5,10,0,12],
#         [13,14,11,15])

size=len(state0[0])
node_num_counter=0


class Node():
    def __init__(self,parent,move):
        global node_num_counter
        self.num=node_num_counter
        node_num_counter+=1
        self.move=move
        self.parent=parent
        if self.move=='init':
            self.state=np.array(state0)
            self.depth=0
        else:
            self.state=copy.deepcopy(self.parent.state)
            self.state=self.do_move(self.move)
            self.depth=self.parent.depth+1
        self.f=self.fx()
        self.bit_diff_val=self.bit_diff()
        self.legal_moves=self.legal_move()
        # 初始节点初始化专用


    # 所有移动的主语都是0元素，left表示0元素左移
    def do_move(self,move):
        move_=move_dict[move]
        state_pre=copy.deepcopy(self.state)
        # zpp是指zero_pos_pre
        # zpa是指zero_pos_aft
        zpp=np.where(state_pre==0)
        zpp=(zpp[0][0],zpp[1][0])
        zpa=(zpp[0]+move_[0],zpp[1]+move_[1])
        state_pre[zpp],state_pre[zpa]=state_pre[zpa],state_pre[zpp]
        return state_pre

    def legal_move(self):
        state_pre=copy.deepcopy(self.state)
        legal_moves = ['up', 'down', 'right', 'left']
        # zpp=zero_pos_pre
        # zpa=zero_pos_aft
        zpp=np.where(state_pre==0)
        zpp=(zpp[0][0],zpp[1][0])
        if self.move!='init':
            if self.move=='up':
                legal_moves.remove('down')
            elif self.move=='down':
                legal_moves.remove('up')
            elif self.move == 'left':
                legal_moves.remove('right')
            elif self.move == 'right':
                legal_moves.remove('left')
        if zpp[0]==0:
            legal_moves.remove('up')
        elif zpp[0]==size-1:
            legal_moves.remove('down')
        if zpp[1]==0:
            legal_moves.remove('left')
        elif zpp[1]==size-1:
            legal_moves.remove('right')
        return legal_moves

    def bit_diff(self):
        bit_diff_val=np.sum(self.state==state_final)
        return bit_diff_val

    def manhattan(self):
        manh_dis=0
        state_final_=np.array(state_final)
        for num in range(1,size**2):
            # i=np.argwhere(self.state==num)
            i=np.argwhere(self.state==num)[0]
            j=np.argwhere(state_final_==num)[0]
            manh_dis+=sum(abs(i-j))
        return manh_dis

    def manhattan_w(self):
        manh_dis_w=0
        state_final_=np.array(state_final)
        for num in range(1,size**2):
            # i=np.argwhere(self.state==num)
            i=np.argwhere(self.state==num)[0]
            j=np.argwhere(state_final_==num)[0]
            if sum(abs(j))==0:
                manh_dis_w+=sum(abs(i-j))*1.5
            elif sum(abs(j))<=1:
                manh_dis_w+=sum(abs(i-j))*1.3
            elif sum(abs(j))<=2:
                manh_dis_w+=sum(abs(i-j))*1.1
            else:
                manh_dis_w+=sum(abs(i-j))
        return manh_dis_w

    def fx(self):
        return self.manhattan_w()# + self.depth


class Open():
    def __init__(self,s0):
        self.l=[s0]

    def is_empty(self):
        if len(self.l)==0:
            return True
        return False

    def add_sort(self,node):
        for i in range(len(self.l)):
            if node.f<self.l[i].f:
                self.l.insert(i,node)
                return
        self.l.append(node)

    def find_replace_add(self,node):
        for i in range(len(self.l)):
            # 如果找到了状态一样的节点
            if (node.state==self.l[i].state).all():
                # 如果新的节点比老的深度小
                if node.f<self.l[i].f:
                    self.l.pop(i)
                    self.add_sort(node)
                    return
        # 如果没找到状态一样的节点，直接加进去
        self.add_sort(node)

    def pop_first(self):
        return self.l.pop(0)


class Closed():
    def __init__(self):
        self.l=[]

    def add(self,node):
        self.l.append(node)

    def add_sort(self,node):
        for i in range(len(self.l)):
            if node.f<self.l[i].f:
                self.l.insert(i,node)
                return
        self.l.append(node)

    def find(self,node):
        for i in range(len(self.l)):
            # 如果找到了状态一样的节点
            if (node.state==self.l[i].state).all():
                if node.depth<self.l[i].depth:
                    self.l[i].parent=node.parent
                return True
        return False

    def find_replace_add(self,node):
        for i in range(len(self.l)):
            # 如果找到了状态一样的节点
            if (node.state==self.l[i].state).all():
                # 如果新的节点比老的深度小
                if node.f<self.l[i].f:
                    # self.l.pop(i)
                    # self.add_sort(node)
                    self.l[i]=node
                    return
        # 如果没找到状态一样的节点，直接加进去
        self.add_sort(node)

# s0=Node(parent=None,move='init')
# print(s0.state)
# print(s0.legal_move())
# print(s0.manhattan())
# legal_move=s0.legal_move()
# s1=Node(parent=s0,move=legal_move[0])
# print(s1.state)
# print(s1.legal_move())
# print(s1.num)

def print_trace_back(node):
    lp=[node]
    while node.parent!=None:
        lp.insert(0,node.parent)
        node=node.parent
    for i in range(len(lp)):
        print('Step:',i)
        print(lp[i].state)

def main():
    start=time.time()
    s0=Node(parent=None,move='init')
    o=Open(s0=s0)
    c=Closed()
    while not o.is_empty():
        cur_node=o.pop_first()
        print('cur_node num:',cur_node.num,'d:',cur_node.depth,'f:',cur_node.f)
        print(cur_node.state)
        c.add(cur_node)
        # if cur_node.bit_diff==0:
        # if cur_node.depth==cur_node.f:
        if cur_node.f==0:
            print('Success!')
            end=time.time()
            print('time cost:',end-start,'seconds')
            print_trace_back(cur_node)
            return
        if len(cur_node.legal_move())==0:
            continue
        else:
            for i in cur_node.legal_moves:
                n=Node(parent=cur_node,move=i)
                if not c.find(n):
                    o.find_replace_add(n)
main()