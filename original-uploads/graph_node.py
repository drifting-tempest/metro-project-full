#from nodes.py import same_line
import sys
sys.setrecursionlimit(5000)#usual 1000,shit heavcy
lines={ "tokyo sakura":['Minowabashi', 'Arakawa-itchumae',
    'Arakawakuyakushomae', 'Arakawa-nichome', 'Arakawa-nanachome',
    'Machiya-ekimae', 'Machiya-nichome', 'Higashi-ogu-sanchome',
    'Kumanomae', 'Miyanomae', 'Odai', 'Arakawa-yuenchimae',
    'Arakawa-shakomae', 'Kajiwara', 'Sakaecho', 'Oji-ekimae',
    'Asukayama', 'Takinogawa-itchome', 'Nishigahara-yonchome',
    'Shin-koshinzuka', 'Koshinzuka', 'Sugamoshinden', 'Otsuka-ekimae',
    'Mukohara', 'Higashi-ikebukuro-yonchome', 'Toden-zoshigaya',
    'Kishibojimmae', 'Gakushuinshita', 'Omokagebashi', 'Waseda'],
    "asakusa":['Nishi-magome', 'Magome', 'Nakanobu', 'Togoshi',
    'Gotanda', 'Takanawadai', 'Sengakuji', 'Mita', 'Daimon',
    'Shimbashi', 'Higashi-ginza', 'Takaracho', 'Nihombashi',
    'Ningyocho', 'Higashi-nihombashi', 'Asakusabashi', 'Kuramae',
    'Asakusa', 'Honjo-azumabashi', 'Oshiage'], "mita":['Meguro',
    'Shirokanedai', 'Shirokane-takanawa', 'Mita', 'Shibakoen',
    'Onarimon', 'Uchisaiwaicho', 'Hibiya', 'Otemachi', 'Jimbocho',
    'Suidobashi', 'Kasuga', 'Hakusan', 'Sengoku', 'Sugamo',
    'Nishi-sugamo', 'Shin-itabashi', 'Itabashi-kuyakushomae',
    'Itabashihoncho', 'Motohasunuma', 'Shimura-sakaue',
    'Shimura-sanchome', 'Hasune', 'Nishidai', 'Takashimadaira',
    'Shin-takashimadaira', 'Nishi-takashimadaira'],
    "nippori":['Nippori', 'Nishi-nippori', 'Akado-shogakkomae',
    'Kumanomae', 'Adachi-odai', 'Ogi-ohashi', 'Koya', 'Kohoku',
    'Nishiaraidaishi-nishi', 'Yazaike', 'Toneri-koen', 'Toneri',
    'Minumadai-shinsuikoen'], "oedo":['Tochomae', 'Shinjuku-nishiguchi',
    'Higashi-shinjuku', 'Wakamatsu-kawada', 'Ushigome-yanagicho',
    'Ushigome-kagurazaka', 'Iidabashi', 'Kasuga', 'Hongo-sanchome',
    'Ueno-okachimachi', 'Shin-okachimachi', 'Kuramae', 'Ryogoku',
    'Morishita', 'Kiyosumi-shirakawa', 'Monzen-nakacho', 'Tsukishima',
    'Kachidoki', 'Tsukijishijo', 'Shiodome', 'Daimon', 'Akabanebashi',
    'Azabu-juban', 'Roppongi', 'Aoyama-itchome', 'Kokuritsu-kyogijo',
    'Yoyogi', 'Shinjuku', 'Tochomae', 'Nishi-shinjuku-gochome',
    'Nakano-sakaue', 'Higashi-nakano', 'Nakai',
    'Ochiai-minami-nagasaki', 'Shin-egota', 'Nerima', 'Toshimaen',
    'Nerima-kasugacho', 'Hikarigaoka'], "shinjuku":['Shinjuku',
    'Shinjuku-sanchome', 'Akebonobashi', 'Ichigaya', 'Kudanshita',
    'Jimbocho', 'Ogawamachi', 'Iwamotocho', 'Bakuro-yokoyama',
    'Hamacho', 'Morishita', 'Kikukawa', 'Sumiyoshi', 'Nishi-ojima',
    'Ojima', 'Higashi-ojima', 'Funabori', 'Ichinoe', 'Mizue',
    'Shinozaki', 'Motoyawata'] }#MAster list for the current phase

def hub(x):#Shows the line of inp.sta
    station_to_lines = {}
    
    for line, stations in lines.items():
        for i in stations:
            if i not in station_to_lines:
                station_to_lines[i] = []
            station_to_lines[i].append(line)
    return station_to_lines[x]

def graph1(x):#shows a grapgh of sta.inputted
    graph={}
    for z in lines.values():

        for i in range(len(z)):
            station = z[i]

            if station not in graph:
                graph[station] = []
        
            if i > 0:
                graph[station].append(z[i-1])
        
            if i < (len(z)-1):
                graph[station].append(z[i+1])
    return graph[x]

def dfs(graph1, current, end,visited,path):
    visited.append(current)
    path.append(current)

    if current == end:
        return path
    
    jew=list(graph1(current))
    for x in jew:

        if x not in visited:

            result = dfs(graph1, x, end, visited, path)

            if result is not None:
                return result
    path.pop()
    return None

print(dfs(graph1,"Roppongi","Asakusa",[],[]))