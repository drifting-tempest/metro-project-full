#for calculating the fair between stations.
"""Rule 1: The fair is always calculated on the shortest path
            except: trasnfer at Kuramae,Bakuroyokoyama,Higashi-Nihonbashi sta.
    Rule 2: For Sakura tram, the fair is fixed regradless of distance
"""

def fare(km):
    adult_ic={"4":178,"9":220,"15":272,"21":325,"27":377, "46":430}
    adult_ticket={"4":180,"9":220,"15":280,"21":330,"27":380,"46":430}

    children_ic={"4":89,"9":110,"15":136,"21":162,"27":188, "46":215}
    children_ticket={"4":90,"9":110,"15":140,"21":170,"27":190, "46":220}

    fare_all = []
    master_dic = [adult_ic, adult_ticket, children_ic, children_ticket]
    master_name = ["adult_ic", "adult_ticket", "children_ic", "children_ticket"]

    for current_dic, name in zip(master_dic, master_name):
        fare_val = None
        
        for dis, price in current_dic.items():
            if km <= int(dis):
                fare_val = price
                break  
        
        if fare_val is None:#more than  46km
            fare_val = current_dic["46"]
            
        #print(f"Distance: {km} km | Fare: {fare_val} yen | Type: {name}")
        fare_all.append(fare_val)

    return fare_all

def fare_sakura(km_sakura,km):
    total=(km+km_sakura)
    sakura_adult_ic="168"
    sakura_adult_ticket="170"

    sakura_children_ic="84"
    sakura_children_ticket="90"
    km=fare(km)#fc for normal km, returned in a list [1,2,3,4]
    #add [a,b,c,d]
    #final shd be [1+a,2+b,3+c,4+d]


    fare_all = []
    master_dic = [sakura_adult_ic, sakura_adult_ticket, sakura_children_ic, sakura_children_ticket]
    master_name = ["sakura_adult_ic", "sakura_adult_ticket", "sakura_children_ic", "sakura_children_ticket"]

    for i in range(0,len(master_dic)):
        tram_a=int(master_dic[i])
        toei_a=int(km[i])
        a=int(master_dic[i])+int(km[i])
        fare_all.append(a)
        
        #print(f"Total Distance: {total} km | Fare(Toei): {toei_a} yen | Fare(Tram): {tram_a} yen | Type: {master_name[i]}")
    print(fare_all)
    return fare_all


def fare_transfer(km_till_trasnfer,km_after_trasnfer):
    total=float(km_till_trasnfer+km_after_trasnfer)
    master_name = ["adult_ic", "adult_ticket", "children_ic", "children_ticket"]

    fare_all=[]
    km1=fare(km_till_trasnfer)#its a list
    km2=fare(km_after_trasnfer)#also a list
    km_total=[]

    for i in range(0,len(km1)):
        fare1=km1[i]
        fare2=km2[i]
        km_total=fare1+fare2
        fare_all.append(km_total)
        print(f"Total Distance: {total} km | Fare(bef trasnfer): {fare1} yen | Fare(aft transfer): {fare2} yen | Type: {master_name[i]}")
    print(fare_all)
a=fare_transfer(12.5,12.5)