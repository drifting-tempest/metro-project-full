lines={
    "tokyo sakura":['Minowabashi', 'Arakawa-itchumae', 'Arakawakuyakushomae', 'Arakawa-nichome', 'Arakawa-nanachome', 'Machiya-ekimae', 'Machiya-nichome', 'Higashi-ogu-sanchome', 'Kumanomae', 'Miyanomae', 'Odai', 'Arakawa-yuenchimae', 'Arakawa-shakomae', 'Kajiwara', 'Sakaecho', 'Oji-ekimae', 'Asukayama', 'Takinogawa-itchome', 'Nishigahara-yonchome', 'Shin-koshinzuka', 'Koshinzuka', 'Sugamoshinden', 'Otsuka-ekimae', 'Mukohara', 'Higashi-ikebukuro-yonchome', 'Toden-zoshigaya', 'Kishibojimmae', 'Gakushuinshita', 'Omokagebashi', 'Waseda'],
    "asakusa":['Nishi-magome', 'Magome', 'Nakanobu', 'Togoshi', 'Gotanda', 'Takanawadai', 'Sengakuji', 'Mita', 'Daimon', 'Shimbashi', 'Higashi-ginza', 'Takaracho', 'Nihombashi', 'Ningyocho', 'Higashi-nihombashi', 'Asakusabashi', 'Kuramae', 'Asakusa', 'Honjo-azumabashi', 'Oshiage'],
    "mita":['Meguro', 'Shirokanedai', 'Shirokane-takanawa', 'Mita', 'Shibakoen', 'Onarimon', 'Uchisaiwaicho', 'Hibiya', 'Otemachi', 'Jimbocho', 'Suidobashi', 'Kasuga', 'Hakusan', 'Sengoku', 'Sugamo', 'Nishi-sugamo', 'Shin-itabashi', 'Itabashi-kuyakushomae', 'Itabashihoncho', 'Motohasunuma', 'Shimura-sakaue', 'Shimura-sanchome', 'Hasune', 'Nishidai', 'Takashimadaira', 'Shin-takashimadaira', 'Nishi-takashimadaira'],
    "nippori":['Nippori', 'Nishi-nippori', 'Akado-shogakkomae', 'Kumanomae', 'Adachi-odai', 'Ogi-ohashi', 'Koya', 'Kohoku', 'Nishiaraidaishi-nishi', 'Yazaike', 'Toneri-koen', 'Toneri', 'Minumadai-shinsuikoen'],
    "oedo":['Tochomae', 'Shinjuku-nishiguchi', 'Higashi-shinjuku', 'Wakamatsu-kawada', 'Ushigome-yanagicho', 'Ushigome-kagurazaka', 'Iidabashi', 'Kasuga', 'Hongo-sanchome', 'Ueno-okachimachi', 'Shin-okachimachi', 'Kuramae', 'Ryogoku', 'Morishita', 'Kiyosumi-shirakawa', 'Monzen-nakacho', 'Tsukishima', 'Kachidoki', 'Tsukijishijo', 'Shiodome', 'Daimon', 'Akabanebashi', 'Azabu-juban', 'Roppongi', 'Aoyama-itchome', 'Kokuritsu-kyogijo', 'Yoyogi', 'Shinjuku', 'Tochomae', 'Nishi-shinjuku-gochome', 'Nakano-sakaue', 'Higashi-nakano', 'Nakai', 'Ochiai-minami-nagasaki', 'Shin-egota', 'Nerima', 'Toshimaen', 'Nerima-kasugacho', 'Hikarigaoka'],
    "shinjuku":['Shinjuku', 'Shinjuku-sanchome', 'Akebonobashi', 'Ichigaya', 'Kudanshita', 'Jimbocho', 'Ogawamachi', 'Iwamotocho', 'Bakuro-yokoyama', 'Hamacho', 'Morishita', 'Kikukawa', 'Sumiyoshi', 'Nishi-ojima', 'Ojima', 'Higashi-ojima', 'Funabori', 'Ichinoe', 'Mizue', 'Shinozaki', 'Motoyawata']
}#MAster list for the current phase

def hub(x):#Shows the line of teh inputted station
    station_to_lines = {}
    
    for line, stations in lines.items():
        for i in stations:
            if i not in station_to_lines:
                station_to_lines[i] = []
            station_to_lines[i].append(line)
    return station_to_lines[x]

fcc=hub("Morishita") #dunction call
print(fcc)

""" def same_line(x,y):#Checks if sta1&sta2 is same line
    line1=hub(x)
    line2=hub(y)
    if line1==line2:
        return True #Works even if sta1 is in more than 1 line
    else:
        return False 

s1=input("Enter a station:[Be careful of spelling]")
s2=input("Enter a station:[Be careful of spelling]")
fc=same_line(s1,s2)#function call
print("Station 1:",s1," and station2:",s2,"is in the same line?",fc) """


graph = {}#shows all the sta bef ad af inputed sta.
for stations in lines.values():

    for i in range(len(stations)):

        station = stations[i]

        if station not in graph:
            graph[station] = []

        if i > 0:
            graph[station].append(stations[i-1])

        if i < len(stations)-1:
            graph[station].append(stations[i+1])
print(graph["Morishita"])