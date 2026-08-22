#load lists 
#if sta1 and sta2 lines are similar;make it a function 
#if not show all possible path using graph node

tokyo=['Minowabashi', 'Arakawa-itchumae', 'Arakawakuyakushomae', 'Arakawa-nichome', 'Arakawa-nanachome', 'Machiya-ekimae', 'Machiya-nichome', 'Higashi-ogu-sanchome', 'Kumanomae', 'Miyanomae', 'Odai', 'Arakawa-yuenchimae', 'Arakawa-shakomae', 'Kajiwara', 'Sakaecho', 'Oji-ekimae', 'Asukayama', 'Takinogawa-itchome', 'Nishigahara-yonchome', 'Shin-koshinzuka', 'Koshinzuka', 'Sugamoshinden', 'Otsuka-ekimae', 'Mukohara', 'Higashi-ikebukuro-yonchome', 'Toden-zoshigaya', 'Kishibojimmae', 'Gakushuinshita', 'Omokagebashi', 'Waseda']
asakusa=['Nishi-magome', 'Magome', 'Nakanobu', 'Togoshi', 'Gotanda', 'Takanawadai', 'Sengakuji', 'Mita', 'Daimon', 'Shimbashi', 'Higashi-ginza', 'Takaracho', 'Nihombashi', 'Ningyocho', 'Higashi-nihombashi', 'Asakusabashi', 'Kuramae', 'Asakusa', 'Honjo-azumabashi', 'Oshiage']
mita=['Meguro', 'Shirokanedai', 'Shirokane-takanawa', 'Mita', 'Shibakoen', 'Onarimon', 'Uchisaiwaicho', 'Hibiya', 'Otemachi', 'Jimbocho', 'Suidobashi', 'Kasuga', 'Hakusan', 'Sengoku', 'Sugamo', 'Nishi-sugamo', 'Shin-itabashi', 'Itabashi-kuyakushomae', 'Itabashihoncho', 'Motohasunuma', 'Shimura-sakaue', 'Shimura-sanchome', 'Hasune', 'Nishidai', 'Takashimadaira', 'Shin-takashimadaira', 'Nishi-takashimadaira']
nippori=['Nippori', 'Nishi-nippori', 'Akado-shogakkomae', 'Kumanomae', 'Adachi-odai', 'Ogi-ohashi', 'Koya', 'Kohoku', 'Nishiaraidaishi-nishi', 'Yazaike', 'Toneri-koen', 'Toneri', 'Minumadai-shinsuikoen']
oedo=['Tochomae', 'Shinjuku-nishiguchi', 'Higashi-shinjuku', 'Wakamatsu-kawada', 'Ushigome-yanagicho', 'Ushigome-kagurazaka', 'Iidabashi', 'Kasuga', 'Hongo-sanchome', 'Ueno-okachimachi', 'Shin-okachimachi', 'Kuramae', 'Ryogoku', 'Morishita', 'Kiyosumi-shirakawa', 'Monzen-nakacho', 'Tsukishima', 'Kachidoki', 'Tsukijishijo', 'Shiodome', 'Daimon', 'Akabanebashi', 'Azabu-juban', 'Roppongi', 'Aoyama-itchome', 'Kokuritsu-kyogijo', 'Yoyogi', 'Shinjuku', 'Tochomae', 'Nishi-shinjuku-gochome', 'Nakano-sakaue', 'Higashi-nakano', 'Nakai', 'Ochiai-minami-nagasaki', 'Shin-egota', 'Nerima', 'Toshimaen', 'Nerima-kasugacho', 'Hikarigaoka']
shinjuku=['Shinjuku', 'Shinjuku-sanchome', 'Akebonobashi', 'Ichigaya', 'Kudanshita', 'Jimbocho', 'Ogawamachi', 'Iwamotocho', 'Bakuro-yokoyama', 'Hamacho', 'Morishita', 'Kikukawa', 'Sumiyoshi', 'Nishi-ojima', 'Ojima', 'Higashi-ojima', 'Funabori', 'Ichinoe', 'Mizue', 'Shinozaki', 'Motoyawata']
line_name=[tokyo,asakusa,mita,nippori,oedo,shinjuku]

line_=["tokyo","asakusa","mita","nippori","oedo","shinjuku"]
# fix problem and can it be used on diff file as a func.py?
def same_line(x,y):
    #x=sta1
    #y=sta2
    for i in line_name:
        for j in i:
            if j==x:
                #print(line_[i]) fix it to show the line name
                line1=i
    for i in line_name:
        for j in i:
            if j==y:
                #print(i) same as above
                line2=i
    if line1==line2:
        return True
    else:
        return False

s1=input("Enter a station:")
s2=input("Enter a station:")
fc=same_line(s1,s2) #fun.call
print("Station 1:",s1," and station2:",s2,"is in the same line?",fc)
