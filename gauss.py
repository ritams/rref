import numpy as np
import sympy as sp


def multiply(i, a):
    return "R_{{ {} }} \\rightarrow R_{{ {} }} \\times ({}) \\\\ ".format(i + 1, i + 1, sp.latex(a))


def add(i, j, a):
    return "R_{{ {} }} \\rightarrow R_{{ {} }} + R_{{ {} }} \\times ({}) \\\\".format(j + 1, j + 1,
                                                                                      i + 1, sp.latex(a))


def swap(i, j):
    return "R_{{ {} }} \\leftrightarrow R_{{ {} }} \\\\".format(i + 1, j + 1)


def augmented(a):
    text = ""
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            text += sp.latex(a[i, j]) + "&"
        text = text[:-1] + "\\\\"

    tex = "\\left[\\begin{array}" + "{" + "c" * (a.shape[1] - 1) + "|c}"
    tex = tex + text[:-2]
    tex = tex + "\\end{array}\\right]"
    return tex


def rref(b, aug=False):
    a = sp.Matrix(b)
    if aug:
        tex = augmented(a)
    else:
        tex = sp.latex(a)
    pivot = 0
    flag2 = False
    for i in range(a.shape[0]):

        if aug:
            if pivot == a.shape[1] - 1: break
        else:
            if pivot == a.shape[1]: break

        text = []
        # find pivotal position
        while a.shape[1] - pivot > 0:
            if a[i, pivot] != 0:
                # do stuff
                if a[i, pivot] != 1:
                    text.append(multiply(i, 1 / a[i, pivot]))
                    a[i, :] = a[i, :] / a[i, pivot]
                for j in range(a.shape[0]):
                    if i != j:
                        if a[j, pivot] != 0:
                            text.append(add(i, j, -a[j, pivot]))
                            a[j, :] = a[j, :] - a[i, :] * a[j, pivot]
                pivot += 1       
                break
            else:
                flag = True
                for j in range(i + 1, a.shape[0]):
                    if a[j, pivot] != 0:
                        # swap
                        text.append(swap(i, j))
                        temp = a[i, :]
                        a[i, :] = a[j, :]
                        a[j, :] = temp
                        flag = False
                        break
                if flag:
                    pivot += 1
                    if aug and pivot == a.shape[1] - 1:
                        flag2 = True
                        break
        if flag2: break

        n = len(text)
        up_stack = "\substack { "
        down_stack = "\substack { "
        for i in range(n):
            if i < round(n / 2):
                up_stack += text[i]
            else:
                down_stack += text[i]
        up_stack += " }"
        down_stack += " }"

        op = "\\xrightarrow[ {} ]{{ {} }}".format(down_stack, up_stack)
        if aug:
            tex = tex + op + augmented(a)
        else:
            tex = tex + op + sp.latex(a)
    print(tex)
    return sp.Matrix(b).rref()[0]
