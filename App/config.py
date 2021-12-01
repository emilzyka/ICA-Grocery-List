def user_define():
    print("""Ange hur många recept du vill lägga till i din inköpslista:
- Alla recept som väljs räcker för en måltid för 4 personer""")

    ANTAL_MÅLTIDER = int(input())

    print("""Ange hur många recept som programmet ska välja mellan:
- Rekommenderas att välja mellan 30 till 100 
- OBS MINSTA GILTLIGA VÄRDE ÄR 14!""")

    URVAL_MÅLTIDER = int(input()) // 14

    print("""Ange en siffra för att bestämma från vilken kategori du vill välja ditt recept:
    1: Antal röster - REKOMMENDERAD -
    2: Bäst betyg
    3: Klimatpåverkan
    4: Antal kommentarer
    5: Sparad antal gånger
    6: Kalorier
    """)

    kategori = input()

    print('LOADING...')

    if kategori == '1' or kategori == 'Antal röster':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Votes'
    elif kategori == '2' or kategori == 'Bäst betyg':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Grade'
    elif kategori == '3' or kategori == 'Klimatpåverkan':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Climate'
    elif kategori == '4' or kategori == 'Antal kommentarer':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Comments'
    elif kategori == '5' or kategori == 'Sparad antal gågner':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Saves'
    elif kategori == '6' or kategori == 'Kalorier':
        return ANTAL_MÅLTIDER, URVAL_MÅLTIDER, 'Nutrition'
    else:
        print({'ERROR': 'ogiltligt input försök igen' })











