import polars as pl
import os
# import pandas as pd
import importlib.resources as resources

def getfwdpos(pos, bidf):
    bi = []
    for i in range(len(bidf["POS1"])):
        if bidf["POS1"][i] == pos:
            # print(bidf['POS1'][i],bidf['POS2'][i],bidf['Prob'][i])
            bi.append([pos, bidf['POS1'][i], bidf['Prob'][i]])
    return bi


def getbwdpos(pos, bidf):
    bi = []
    for i in range(len(bidf["POS2"])):
        if bidf["POS2"][i] == pos:
            # print(bidf['POS1'][i],bidf['POS2'][i],bidf['Prob'][i])
            bi.append([pos, bidf['POS1'][i], bidf['Prob'][i]])
    return bi


def getwdpos(wrd, wpdf):
    wp = []
    for i in range(len(wpdf["Word"])):
        if wpdf["Word"][i] == wrd:
            #             print(wrd,wpdf['POS'][i],wpdf['Prob'][i])
            wp.append([wrd, wpdf['POS'][i], wpdf['Prob'][i]])
    return wp


def computepos(wrd, pos, prob, bidf):
    bstpos = ""
    bstscr = 0
    fpos = getfwdpos(pos, bidf)
    bpos = getbwdpos(pos, bidf)
    for ff in fpos:
        for bb in bpos:
            if ff[0] == bb[1]:
                temp = ff[2] * bb[2] * prob
                if temp > bstscr:
                    #                     print("{}\t{}\t{}\t{}\t".format(ff[2],bb[2],prob,temp))
                    bstpos = ff[0]
                    bstscr = temp
    #     print("{}\t{}".format(bstpos, bstscr))
    ll = [bstpos, bstscr]
    return ll


def computebestpos(lst):
    bstpos = ""
    bstscr = 0
    for l in lst:
        if l[1] > bstscr:
            bstpos = l[0]
            bstscr = l[1]
    return bstpos


def postag(sent):
    # path = os.getcwd()
    # bidf = pd.read_csv(os.path.join(path, "bipos.csv"), encoding="utf-8-sig")
    # wpdf = pd.read_csv(os.path.join(path, "wdpos.csv"), encoding="utf-8-sig")
    # bidf = pd.read_csv("bipos.csv", encoding="utf-8-sig")
    # wpdf = pd.read_csv("wdpos.csv", encoding="utf-8-sig")
    with resources.as_file(resources.files('hindiPOS').joinpath('bipos.csv')) as bidf_path:
        bidf = pl.read_csv(bidf_path, encoding='utf-8-sig')
    with resources.as_file(resources.files('hindiPOS').joinpath('wdpos.csv')) as wpdf_path:
        wpdf = pl.read_csv(wpdf_path, encoding='utf-8-sig')
    # wpdf = wpdf[:, 1:]
    # bidf = bidf[:, 1:]
    wpdf = wpdf.select(pl.col('*').exclude(wpdf.columns[0]))
    bidf = bidf.select(pl.col('*').exclude(bidf.columns[0]))

    lattice = []
    for word in sent.split():
        lct = []
        temp = getwdpos(word, wpdf)
        if temp == []:
            lattice.append(word + "|" + "NN")
            #       lattice.append(word+"|"+"UNK")
            continue
        for i in range(len(temp)):
            ll = computepos(temp[i][0], temp[i][1], temp[i][2], bidf)
            lct.append(ll)
        t = computebestpos(lct)
        lattice.append(temp[i][0] + "|" + t)

    return lattice