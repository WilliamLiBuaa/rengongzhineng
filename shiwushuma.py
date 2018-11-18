import numpy as np
import sys
import copy

state_final = ([1,2,3],
               [8,0,4],
               [7,6,5])
state0=([2,8,3],
        [1,0,4],
        [7,6,5])
move_dict={'up':[-1,0],'down':[1,0],'right':[0,1],'left':[0,-1]}
# state_final=([1,2,3,4],
#              [5,6,7,8],
#              [9,10,11,12],
#              [13,14,15,0])
# state0=([11,9,4,15],
#         [1,3,0,12],
#         [7,5,8,6],
#         [13,2,10,14])

size=len(state0[0])


class Node():
    def __init__(self,parent,move):
        self.move=move
        self.parent=parent
        # 初始节点初始化专用
        if self.move=='init':
            self.state=np.array(state0)
            self.depth=0
        else:
            self.state=self.parent.do_move(self.move)
            self.depth=self.parent.depth+1

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
        self.state=state_pre
        return self.state

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
        for num in range(size**2-1):
            i=np.argwhere(self.state==num)[0]
            j=np.argwhere(state_final_==num)[0]
            manh_dis+=sum(abs(i-j))
        return manh_dis

s0=Node(parent=None,move='init')
print(s0.state)
print(s0.legal_move())
print(s0.manhattan())
legal_move=s0.legal_move()
s1=Node(parent=s0,move=legal_move[0])
print(s1.state)
print(s1.legal_move())
