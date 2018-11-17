import numpy as np
import sys
from numba import jit

# state_final = ([1,2,3],
#                [8,0,4],
#                [7,6,5])
# state0=([2,8,3],
#         [1,0,4],
#         [7,6,5])
#
state_final=([1,2,3,4],
             [5,6,7,8],
             [9,10,11,12],
             [13,14,15,0])
state0=([11,9,4,15],
        [1,3,0,12],
        [7,5,8,6],
        [13,2,10,14])

# state0=([1,3,4,12],
#         [5,2,6,0],
#         [9,10,8,7],
#         [13,14,11,15])

class Node():
    @jit
    def __init__(self,parent,move):
        global state_final
        self.move=move
        self.parent = parent
        self.child = []
        if move=='e':
            self.state=np.array(state0)
            self.depth=0
            # self.path=[]
        else:
            self.depth=self.parent.depth+1
            # self.path=self.parent.path.append(move)
        self.state = self._do_move(move)
        self.state_final=np.array(state_final)

    @jit
    def calc_diff_bit(self):
        self.h_val=0
        for i in range(self.state_final.shape[0]):
            for j in range(self.state_final.shape[1]):
                # print(self.state[i,j])
                # print(state_final[i,j])
                if self.state[i,j]!=self.state_final[i,j]:
                    self.h_val+=1
        # if self.state[self.state.shape[0]//2,self.state.shape[0]//2]!=0:
        #     self.h_val-=1
        return self.h_val

    @jit
    def calc_dis_h(self):
        self.h_val=0
        for num in range(0,self.state_final.flatten().shape[0]):
            i=np.argwhere(self.state_final==num)[0,0]
            j=np.argwhere(self.state_final==num)[0,1]
            i_=np.argwhere(self.state==num)[0,0]
            j_=np.argwhere(self.state==num)[0,1]
            self.h_val+=abs(i-i_)+abs(j-j_)
        return self.h_val
    @jit
    def is_final(self):
        if self.calc_diff_bit()==0:
            return True
        return False
    @jit
    def _calc_legal_move(self):
        self.legal_move=['r','d','l','u']
        if self.move=='r':
            self.legal_move.remove('l')
        if self.move=='l':
            self.legal_move.remove('r')
        if self.move=='u':
            self.legal_move.remove('d')
        if self.move=='d':
            self.legal_move.remove('u')

        self.zero_position = [int(np.where(self.state == 0)[0]), int(np.where(self.state == 0)[1])]
        if self.zero_position[0]==0:
            self.legal_move.remove('d')
        if self.zero_position[0]==self.state_final.shape[0]-1:
            self.legal_move.remove('u')
        if self.zero_position[1]==0:
            self.legal_move.remove('r')
        if self.zero_position[1]==self.state_final.shape[1]-1:
            self.legal_move.remove('l')
        return self.legal_move
    @jit
    def calc_f_val(self):
        self.f_val = self.calc_dis_h() + self.depth
        return self.f_val
    @jit
    def _do_move(self,move):
        # 仅限s0使用
        if move=='e':
            return self.state

        self.zero_position_pre = [int(np.where(self.parent.state == 0)[0]), int(np.where(self.parent.state == 0)[1])]
        if move=='r':
            self.state=self.parent.state.copy()
            self.state[self.zero_position_pre[0],self.zero_position_pre[1]],\
            self.state[self.zero_position_pre[0],self.zero_position_pre[1] - 1]= \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1] - 1], \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1]]
        if move=='l':
            self.state=self.parent.state.copy()
            self.state[self.zero_position_pre[0],self.zero_position_pre[1]],\
            self.state[self.zero_position_pre[0],self.zero_position_pre[1] + 1]= \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1] + 1], \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1]]
        if move=='u':
            self.state=self.parent.state.copy()
            self.state[self.zero_position_pre[0],self.zero_position_pre[1]],\
            self.state[self.zero_position_pre[0]+1,self.zero_position_pre[1]]= \
            self.state[self.zero_position_pre[0]+1, self.zero_position_pre[1]], \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1]]
        if move=='d':
            self.state=self.parent.state.copy()
            self.state[self.zero_position_pre[0],self.zero_position_pre[1]],\
            self.state[self.zero_position_pre[0]-1,self.zero_position_pre[1]]= \
            self.state[self.zero_position_pre[0]-1, self.zero_position_pre[1]], \
            self.state[self.zero_position_pre[0], self.zero_position_pre[1]]
        return self.state


class Open():
    @jit
    def __init__(self,s0):
        self.l=[s0]
    @jit
    def is_empty(self):
        if len(self.l)==0:
            return True
        return False
    @jit
    def sort(self):
        if len(self.l)==1:
            return self.l
        for j in range(1,len(self.l)):
            key=self.l[j].calc_f_val()
            i = j-1
            while i>=0 and self.l[i].calc_f_val()>key:
                self.l[i+1]=self.l[i]
                i-=1
            self.l[i+1].h_val = key
    @jit
    def sort_t1(self):
        min_f=sys.maxsize
        for i in range(len(self.l)):
            if self.l[i].calc_f_val()<min_f:
                min_f=self.l[i].calc_f_val()
                min_num=i
        min_item=self.l.pop(min_num)
        self.l.insert(0,min_item)

    def add(self,node):
        self.l.append(node)

    def pop_first(self):
        return self.l.pop(0)

    def find(self,node):
        for i in self.l:
            if (node.state==i.state).all():
                return i,True
        return None,False


class Closed():
    def __init__(self):
        self.l=[]

    def add(self,node):
        self.l.append(node)
    @jit
    def find(self,node):
        for i in self.l:
            if (node.state==i.state).all():
                return True
        return False

s=[]
s.append(Node(parent=None,move='e'))
print(s[0]._calc_legal_move())
o=Open(s0=s[0])
print(o.find(s[0]))
c=Closed()


def main():
    counter=0
    while 1:
        if o.is_empty():
            print('Failed to solve this problem!')
            return
        cur_node=o.pop_first()
        counter+=1
        print('current node: ',counter)
        # print(cur_node.state)
        # print(cur_node.depth, '+', cur_node.calc_dis_h(), '=', cur_node.calc_f_val())
        c.add(cur_node)
        if cur_node.is_final():
            print('Success!')
            return
        # 替换成if cur_node.calc_legal_move():?
        if len(cur_node._calc_legal_move())==0:
            continue
        else:
            for i in cur_node.legal_move:
                n=Node(parent=cur_node,move=i)
                _,ofind=o.find(n)
                if not ofind and not c.find(n):
                    s.append(n)
                    o.add(n)
                    # print('child+  ',i)
                    # print(n.state)
                    # print(n.depth, '+', n._calc_diff_bit(), '=', n.calc_f_val())
                elif _!=None:
                    if _.depth>n.depth:
                        _.depth=n.depth
            o.sort_t1()
            # print('open table')
            # for j in o.l:
            #     print(j.state)
            #     print(j.depth,'+',j._calc_diff_bit(),'=',j.calc_f_val())

main()