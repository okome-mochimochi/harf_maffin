import os,re,csv,pandas as pd,numpy as np,itertools

year=2012
key= (year-2012)*(1)+1
m_key =[0,45,46,42,43,48,43,52]
dir_path ='./'+f'{year}_j2/'
os.makedirs(dir_path, exist_ok=True)


#　1: 用意したテキストの修正
with open(f'{year}_source.txt','r',encoding='UTF-8') as f:
    reg = f.read()
#  1-1:source file backup
with open(f'./{year}_j2/source{year}_j2.txt','w',encoding='UTF-8') as w:
    w.write(reg)

    reg = re.sub(r'チ.*','',reg,)
    reg = re.sub(r'(\d+)\t',r'\1',reg,)
    reg = re.sub(r'(\w+)\t',r'★\1',reg, )
    reg = re.sub(r'\n','',reg,)
    reg = re.sub(r'\r\n',r'\n',reg, )
    reg = re.sub(r'★',r'\n★',reg,)
    reg = re.sub(r'(△|○|●|A|H)',r'\t\1\t',reg,)
    reg = re.sub(r's.:.(\d+)',r's-\1\t',reg, )
    reg = re.sub(r'p.:.(\d+)',r'p-\1',reg, )
    reg = re.sub(r'(\d)(s)',r'\1\t\2',reg,)
    reg = re.sub(r'(p-\d+)(\s+|\t+)(s)',r'\1\t\t\t\t\2',reg,)
    reg = re.sub(r'(s|p)-','',reg,)
    reg = re.sub(r'-',r'\t',reg,)
    reg = re.sub(r'(★\w+)\s+(\d+\t)',r'\1\t\t\t\t\2',reg,)
    reg = re.sub(r' ','',reg,)

    with open('reg.txt','w',encoding='utf-8') as f:
        f.write(reg)

#　2:クラブリストの取得（22クラブなので決め打ちでOK）
    l = re.sub(r'(★.+?)\t.*(\n|$)',r'\1,',reg)
    l  = re.sub(r'^\n','',l)
    club = l.split(',')
    club = club[0:22]

with open(f'./{year}_j2/{year}_j2_club.csv','w', encoding='utf-8',) as f:
    writer = csv.writer(f,delimiter='\t',)
    writer.writerow(club)

 ]:
#　3:クラブごと抽出し、一行にまとめる
#  箱の準備
tmp =pd.DataFrame()
result =pd.DataFrame()
rank =[]

クラブ名で、テキスト全文検索→1行にまとめて、整形
for name in club:
    x = re.findall(r'%s.+' % name,reg) #★クラブ名で行抽出
    x = ''.join(x)
    x = re.sub(r'%s\t' % name,r'',x) #ヘッド重複を処理
    x = re.sub(r'(\d+)(A|H)',r'\1\t\2',x,)
    x = re.sub(r'(\d)\t{3}(\d)',r'\1\t\t\t\t\t\t\2',x,)
    x = re.sub(r'(\w)\t{4}(\d)',r'\1\t\t\t\t\t\2',x,)
    x = re.sub(r'^\n','',x)
    x = re.sub(r'\t{6}',r'\t\t\t\t0\t0\t',x,)
    with open('reg_01.txt','w',encoding='utf-8') as f:
        f.write(x)

    rank_n1 = re.sub(r'.+?(\d+)\t\d+$',r'\1',x)
    print(rank_n1)
    rank.append(rank_n1)

    # Type-B 出力部分
    y = re.sub(r'\t{4}0\t0\t\d+\t\d+',r'',x,)
    with open('reg_02.txt','w',encoding='utf-8') as f:
        f.write(y)

#重複削除（34節らへん、ここは年ごとに決め打ち）
#18-301:315 17-254:268 16-274:316 15-239:252 14-232:252 13-316:371 12-cut なし
    y = y.split('\t')
    if year==2018 and len(y)==301:    del y[252:259]
    elif year==2018 and len(y)==308:    del y[252:266]
    elif year ==2017: del y[254:268]
    elif year ==2016: del y[274:316]
    elif year ==2015: del y[238:252]
    elif year ==2014: del y[231:252]
    elif year ==2013: del y[238:287]
    else : pass

#  クラブ別集計
    b =np.array(y,dtype='unicode')
    b =b.reshape(42,7)
    b =pd.DataFrame(b,columns = ['H/A','対戦相手','試合結果','得点','失点','順位','勝ち点'],)

    for i in y :
        g_g =y[3::7]
        g_a =y[4::7]
        m_res = y[2::7]

    res=[]
    for s in m_res:
        if '○' in s:
            res.extend([1,0,0])
        elif '△' in s:
            res.extend([0,1,0])
        elif '●' in s:
            res.extend([0,0,1])
        else:pass


    res = [int(s) for s in res]
        res = np.array(res)
        res = res.reshape(42,3)
        res = np.cumsum(res,axis=0)
        res = pd.DataFrame(res,columns =['勝利数','引分数','敗北数'],)


    g_g = [int(s) for s in g_g]
    g_g = np.array(g_g,)
    g_g = np.cumsum(g_g)
    g_a = [int(s) for s in g_a]
    g_a = np.array(g_a,)
    g_a = np.cumsum(g_a)
    g_d = g_g-g_a
    gd_ = np.concatenate((g_g,g_a,g_d),)
    gd_ = gd_.reshape(3,42)
    gd_ = gd_.T
    gd_ = pd.DataFrame(gd_,columns =['得点計','失点計','得失点差'],)


#　データ統合
    b = pd.concat([b,gd_,res], axis=1)
    b = b[['H/A','対戦相手','試合結果','得点','失点','得点計','失点計','得失点差','勝利数','引分数','敗北数','勝ち点','順位']]
    b.to_csv(f'./{year}_j2/{year}_{rank_n1}_{name}.csv',index=False , float_format='%.0f',)]:
#　全クラブ分出力
    b =b.values.tolist()
    b =list(itertools.chain.from_iterable(b))
    b =pd.Series(b, name=f'{rank_n1},{name}')
    tmp =tmp.append(b)


tmp.to_csv(f'./{year}_j2/{year}_all.csv', sep='\t', header= False)
