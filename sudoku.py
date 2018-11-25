# -*- coding: utf-8 -*-
import os
import sys

sudoku = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 3, 6, 0, 0, 0, 0, 0],
          [0, 7, 0, 0, 9, 0, 2, 0, 0],
          [0, 5, 0, 0, 0, 7, 0, 0, 0],
          [0, 0, 0, 0, 4, 5, 7, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 3, 0],
          [0, 0, 1, 0, 0, 0, 0, 6, 8],
          [0, 0, 8, 5, 0, 0, 0, 1, 0],
          [0, 9, 0, 0, 0, 0, 4, 0, 0]]
update_times = 0
grids = []
process = ""


class Grid:

    def __init__(self, id, r, c, b, value, candidates):
        self.id = id
        self.r = r
        self.c = c
        self.b = b
        self.value = value
        self.candidates = candidates

    def __str__(self):
        s = ""
        s += "row: " + str(self.r) + "  "
        s += "col: " + str(self.c) + "  "
        s += "block: " + str(self.b) + "  "
        s += "value: " + str(self.value) + "  "
        s += "candidates: " + str(self.candidates)
        return s


# @function: 产生候选数字
def generate_candidates():
    for id in range(0, 81):
        r = int(id/9)
        c = id % 9
        b = int(r/3)*3+int(c/3)
        if sudoku[r][c] != 0:
            grids.append(Grid(id, r, c, b, sudoku[r][c], []))
        else:
            candidates = []
            for num in range(1, 10):
                row_list = sudoku[r][:]
                col_list = [sudoku[i][c] for i in range(0, 9)]
                block_list = []
                for i in range(int(r/3)*3, int(r/3)*3+3):
                    for j in range(int(c/3)*3, int(c/3)*3+3):
                        block_list.append(sudoku[i][j])
                flag1 = num not in row_list
                flag2 = num not in col_list
                flag3 = num not in block_list
                if flag1 and flag2 and flag3:
                    candidates.append(int(num))
            grids.append(Grid(id, r, c, b, 0, candidates))


def show():
    s = "       "
    for i in range(0, 9):
        s += "C" + str(i+1) + "      "
    s += "\n   *************************************************************************\n"
    for r in range(0, 9):
        for j in range(0, 3):
            if j == 1:
                s += "R" + str(r+1) + " $ "
            else:
                s += "   $ "
            for c in range(0, 9):
                if sudoku[r][c] != 0:
                    if j == 1:
                        s += "  " + str(sudoku[r][c]) + "   "
                    else:
                        s += "      "
                else:
                    for l in range(j*3+1, j*3+4):
                        if l in grids[9*r+c].candidates:
                            s += str(l) + " "
                        else:
                            s += "  "
                if (c + 1) % 3 == 0:
                    s += "$ "
                else:
                    s += "| "
            if j == 1:
                s += "R" + str(r+1) + "\n"
            else:
                s += "\n"
        if (r + 1) % 3 == 0:
            s += "   *************************************************************************\n"
        else:
            s += "   —————————————————————————————————————————————————————————————————————————\n"
    s += "       "
    for i in range(0, 9):
        s += "C" + str(i+1) + "      "
    s += "\n\n\n"
    # print(s)
    return s


# @function: 判断数独是否填充完毕，填充完毕返回True，否则返回False
def end():
    for i in range(0, 81):
        if grids[i].value == 0:
            return False
    return True


# 唯一候选数法
# http://www.llang.net/sudoku/skill/2-1.html
def only_candidate():
    global process
    for i in range(0, 81):
        if len(grids[i].candidates) == 1:
            process += ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
            process += ("因为( R"+str(grids[i].r+1)+", C"+str(grids[i].c+1) +
                        " )格中只有1个候选数字 "+str(grids[i].candidates[0])+"\n")
            process += ("所以( R"+str(grids[i].r+1)+", C"+str(grids[i].c+1) +
                        " )格中应当填入数字 "+str(grids[i].candidates[0])+"\n"+"\n")
            # update grid
            grids[i].value = grids[i].candidates[0]
            grids[i].candidates = []
            # update sudoku
            sudoku[grids[i].r][grids[i].c] = grids[i].value
            update_candidate(
                [grids[i].r], [_ for _ in range(0, 9)], [grids[i].value])
            update_candidate([_ for _ in range(0, 9)], [
                             grids[i].c], [grids[i].value])
            update_candidate([_ for _ in range(int(grids[i].r/3)*3, int(grids[i].r/3)*3+3)], [
                             _ for _ in range(int(grids[i].c/3)*3, int(grids[i].c/3)*3+3)], [grids[i].value])
            process += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n"
            return True


# @function: 根据行数和列数更新候选数字数组
def update_candidate(row_list, col_list, num_list):
    global process
    for i in range(0, 81):
        if grids[i].r in row_list and grids[i].c in col_list:
            for num in num_list:
                if num in grids[i].candidates:
                    grids[i].candidates.remove(num)
                    process += ("( R"+str(grids[i].r+1)+", C" +
                                str(grids[i].c+1)+" ) 格中删除候选数字 "+str(num)+"\n")
                    global update_times
                    update_times += 1
    process += "\n\n"
    # return True


# 隐性唯一候选数法
# http://www.llang.net/sudoku/skill/2-2.html
def implicit_only_candidate():
    global process
    # row
    for row in range(0, 9):
        t = [0 for _ in range(0, 10)]
        for i in range(0, 81):
            if grids[i].r == row and grids[i].candidates:
                for num in grids[i].candidates:
                    t[num] += 1
        for num in range(1, 10):
            if t[num] == 1:
                for i in range(0, 81):
                    if grids[i].r == row and num in grids[i].candidates:
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                        process += ("因为 R"+str(grids[i].r+1)+" 行中候选数字 "+str(
                            num)+" 只在 ( R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 格中出现了一次\n")
                        process += ("所以 ( R"+str(grids[i].r+1)+", C"+str(
                            grids[i].c+1)+" ) 格中应当填入数字 "+str(num)+"\n\n")
                        grids[i].value = num
                        grids[i].candidates = []
                        sudoku[grids[i].r][grids[i].c] = num
                        update_candidate(
                            [_ for _ in range(0, 9)], [grids[i].c], [num])
                        update_candidate([_ for _ in range(int(grids[i].r/3)*3, int(grids[i].r/3)*3+3)], [
                                         _ for _ in range(int(grids[i].c/3)*3, int(grids[i].c/3)*3+3)], [num])
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                        return True
    # col
    for col in range(0, 9):
        t = [0 for _ in range(0, 10)]
        for i in range(0, 81):
            if grids[i].c == col and grids[i].candidates:
                for num in grids[i].candidates:
                    t[num] += 1
        for num in range(1, 10):
            if t[num] == 1:
                for i in range(0, 81):
                    if grids[i].c == col and num in grids[i].candidates:
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                        process += ("因为 C"+str(grids[i].c+1)+" 列中候选数字 "+str(
                            num)+" 只在 ( R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 格中出现了一次\n")
                        process += ("所以 ( R"+str(grids[i].r+1)+", C"+str(
                            grids[i].c+1)+" ) 格中应当填入数字 "+str(num)+"\n\n")
                        grids[i].value = num
                        grids[i].candidates = []
                        sudoku[grids[i].r][grids[i].c] = num
                        update_candidate(
                            [grids[i].r], [_ for _ in range(0, 9)], [num])
                        update_candidate([_ for _ in range(int(grids[i].r/3)*3, int(grids[i].r/3)*3+3)], [
                                         _ for _ in range(int(grids[i].c/3)*3, int(grids[i].c/3)*3+3)], [num])
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                        return True
    # block
    for block in range(0, 9):
        t = [0 for _ in range(0, 10)]
        for i in range(0, 81):
            if grids[i].b == block and grids[i].candidates:
                for num in grids[i].candidates:
                    t[num] += 1
        for num in range(1, 10):
            if t[num] == 1:
                for i in range(0, 81):
                    if grids[i].b == block and num in grids[i].candidates:
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                        process += ("因为 "+str(grids[i].b+1)+" 宫中候选数字 "+str(
                            num)+" 只在 ( R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 格中出现了一次\n")
                        process += ("所以 ( R"+str(grids[i].r+1)+", C"+str(
                            grids[i].c+1)+" ) 格中应当填入数字 "+str(num)+"\n\n")
                        grids[i].value = num
                        grids[i].candidates = []
                        sudoku[grids[i].r][grids[i].c] = num
                        update_candidate(
                            [grids[i].r], [_ for _ in range(0, 9)], [num])
                        update_candidate([_ for _ in range(0, 9)], [
                                         grids[i].c], [num])
                        process += (
                            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^隐性唯一候选数法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                        return True


# 候选数区块删减法
# http://www.llang.net/sudoku/skill/2-3.html
def candidate_block_subtraction():
    global process
    for num in range(1, 10):
        for block in range(0, 9):
            row = []
            col = []
            for i in range(0, 81):
                if grids[i].b == block and num in grids[i].candidates:
                    row.append(grids[i].r)
                    col.append(grids[i].c)
            global update_times
            if len(list(set(row))) == 1:
                process += ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数区块删除法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                process += ("因为 "+str(block+1)+" 宫中数字 " +
                            str(num)+" 只出现在 R"+str(row[0]+1)+" 行中\n")
                process += ("所以 R"+str(row[0]+1)+" 行中的格，除 " +
                            str(block+1)+" 宫中的格之外，其余的格中均不能存在数字 "+str(num)+"\n\n")
                t = [_ for _ in range(0, 9)]
                for _ in range(block % 3*3, block % 3*3+3):
                    t.remove(_)
                _ = update_times
                update_candidate([row[0]], t, [num])
                process += ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数区块删除法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                if update_times != _:
                    return True
            if len(list(set(col))) == 1:
                process += ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数区块删除法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                process += ("因为 "+str(block+1)+" 宫中数字 " +
                            str(num)+" 只出现在 C"+str(col[0]+1)+" 列中\n")
                process += ("所以 C"+str(col[0]+1)+" 列中的格，除 " +
                            str(block+1)+" 宫中的格之外，其余的格中均不能存在数字 "+str(num)+"\n\n")
                t = [_ for _ in range(0, 9)]
                for _ in range(int(block/3)*3, int(block/3)*3+3):
                    t.remove(_)
                _ = update_times
                update_candidate(t, [col[0]], [num])
                process += ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数区块删除法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                if update_times != _:
                    return True


# 候选数对删减法
# http://www.llang.net/sudoku/skill/2-4.html
def candidate_pair_subtraction():
    global update_times, process
    for row in range(0, 9):
        for i in range(0, 81):
            for j in range(i+1, 81):
                if grids[i].r == row and grids[j].r == row and grids[i].candidates == grids[j].candidates and len(grids[i].candidates) == 2:
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                    process += ("因为数字 "+str(grids[i].candidates)+" 只出现在 R"+str(grids[i].r+1)+" 行中的 (R"+str(
                        grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格中\n")
                    process += ("所以 R"+str(grids[i].r+1)+" 行中，除 (R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(
                        grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格外，均不能存在数字 "+str(grids[i].candidates)+"\n\n")
                    _ = update_times
                    t = [_ for _ in range(0, 9)]
                    t.remove(grids[i].c)
                    t.remove(grids[j].c)
                    update_candidate([row], t, grids[i].candidates)
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                    if _ != update_times:
                        return True
    for col in range(0, 9):
        for i in range(0, 81):
            for j in range(i+1, 81):
                if grids[i].c == col and grids[j].c == col and grids[i].candidates == grids[j].candidates and len(grids[i].candidates) == 2:
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                    process += ("因为数字 "+str(grids[i].candidates)+" 只出现在 C"+str(grids[i].c+1)+" 列中的 (R"+str(
                        grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格中\n")
                    process += ("所以 C"+str(grids[i].c+1)+" 列中，除 (R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(
                        grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格外，均不能存在数字 "+str(grids[i].candidates)+"\n\n")
                    _ = update_times
                    t = [_ for _ in range(0, 9)]
                    t.remove(grids[i].r)
                    t.remove(grids[j].r)
                    update_candidate(t, [col], grids[i].candidates)
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                    if _ != update_times:
                        return True
    for block in range(0, 9):
        for i in range(0, 81):
            for j in range(i+1, 81):
                if grids[i].b == block and grids[j].b == block and grids[i].candidates == grids[j].candidates and len(grids[i].candidates) == 2:
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n")
                    process += ("因为数字 "+str(grids[i].candidates)+" 只出现在 "+str(grids[i].b+1)+" 宫中的 (R"+str(
                        grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格中\n")
                    process += ("所以 "+str(grids[i].c+1)+" 宫中，除 (R"+str(grids[i].r+1)+", C"+str(grids[i].c+1)+" ) 和 ( R"+str(
                        grids[j].r+1)+", C"+str(grids[j].c+1)+" ) 格外，均不能存在数字 "+str(grids[i].candidates)+"\n\n")
                    _ = update_times
                    for k in range(0, 81):
                        if grids[k].b == block and grids[k] is not grids[i] and grids[k] is not grids[j]:
                            update_candidate(
                                [grids[k].r], [grids[k].c], grids[i].candidates)
                    process += (
                        "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^候选数对删减法^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n")
                    if _ != update_times:
                        return True


if __name__ == "__main__":
    generate_candidates()
    process += "\noriginal sudoku with candidates: \n\n"
    process += show()
    while not end():
        _ = update_times
        if only_candidate():
            process += show()
            continue
        if implicit_only_candidate():
            process += show()
            continue
        if candidate_pair_subtraction():
            process += show()
            continue
        if candidate_block_subtraction():
            process += show()
            continue
        if _ == update_times:
            break
        """ 
        if implicit_candidate_pair_subtraction():
            continue
        if candidate_rectangle_subtraction():
            continue
        if chain_candidate_reduction():
            continue
        if XY():
            continue
        if XYZ():
            continue
        if WXYZ():
            continue
        if ABXYZ():
            continue
        """
    process += ("\nanswer: \n\n")
    process += show()
    # print(process)
    with open(os.path.dirname(os.path.realpath(__file__))+"/process", "w+", encoding="utf-8") as f:
        f.write(process)
