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
    for i in range(a.shape[0]):
        text = []
        # find pivotal position
        if a[i, i] != 0:
            # do stuff
            if a[i, i] != 1:
                text.append(multiply(i, 1 / a[i, i]))
                a[i, :] = a[i, :] / a[i, i]
            for j in range(a.shape[0]):
                if i != j:
                    if a[j, i] != 0:
                        text.append(add(i, j, -a[j, i]))
                        a[j, :] = a[j, :] - a[i, :] * a[j, i]
        else:
            # swap
            flag = True
            for j in range(i + 1, a.shape[0]):
                if a[j, i] != 0:
                    # swap
                    text.append(swap(i, j))
                    temp = a[i, :]
                    a[i, :] = a[j, :]
                    a[j, :] = temp
                    flag = False
                    break
            if flag:
                break
            else:
                # then do stuff
                if a[i, i] != 1:
                    text.append(multiply(i, 1 / a[i, i]))
                    a[i, :] = a[i, :] / a[i, i]
                for j in range(a.shape[0]):
                    if i != j:
                        if a[j, i] != 0:
                            text.append(add(i, j, -a[j, i]))
                            a[j, :] = a[j, :] - a[i, :] * a[j, i]

        n = len(text)
        up_stack = "\substack { "
        down_stack = "\substack { "
        for i in range(n):
            if i < int(n / 2):
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
