import os
import time

import psycopg2
import requests
import json
import urllib3
import warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings()

main_koatuu_url = "https://kadastr.live/api/parcels/?cadnum__startswith="
main_parcel_url = "https://kadastr.live/api/parcels/?cadnum=7122583400:02:006:0016"
url = "https://kadastr.live/api/parcels/?cadnum=7122583400:02:006:0016"

#connect to the db
con = psycopg2.connect(
            host="localhost",
            database="cadastre_live_bd",
            user="postgres",
            password="postgres")

#cursor
cur = con.cursor()
program_start = time.time()
counter = 0
with open("koatuu_list.txt", "r") as a_file:
    for koatuu_line in a_file:
        koatu = koatuu_line.strip()
        try:
            start = time.time()
            for i in range(1, 100000000):
                # print(i)
                full_url = main_koatuu_url + koatu + '&page=' + str(i)
                print(full_url)
                response = requests.request("GET", full_url)
                json_response = json.loads(response.text)
                if json_response['results']:
                    print('OK - результат на сторінці є')
                    # print(response.text)
                    # print(json_response['results'])
                    print(len(json_response['results']), ' - ділянок на сторінці')
                    for parcel in json_response['results']:
                        counter += 1
                        # print(counter, parcel['cadnum'])

                        cadnum = parcel['cadnum']
                        category = parcel['category']
                        area = parcel['area']
                        unit_area = parcel['unit_area']
                        koatuu = parcel['koatuu']
                        use = parcel['use']
                        purpose = parcel['purpose']
                        purpose_code = parcel['purpose_code']
                        ownership = parcel['ownership']
                        ownershipcode = parcel['ownershipcode']
                        # geometry = parcel['geometry'].replace("'", '"')
                        jss = json.dumps(parcel['geometry'])
                        geometry = jss.replace("'", '"')

                        cur.execute(
                            "INSERT INTO parcels(cadnum, category, area, unit_area, koatuu, use, purpose, purpose_code, ownership, ownershipcode, geometry) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (cadnum, category, area, unit_area, koatuu, use, purpose, purpose_code, ownership, ownershipcode, geometry)
                            )


                        end = time.time()
                        duration = end - start
                        program_duration = end - program_start
                        speed = counter * 3600 / program_duration




                    # commit the transcation
                    con.commit()

                    print(counter, "- Parcel loaded in base,", str(round(speed)), 'prc/hour, duration -', time.strftime("%d:%H:%M:%S", time.gmtime(program_duration)))
                    print("SLEEP 5sec")
                    time.sleep(5)

                else:
                    print(f'Сторінка {i} відсутня в {koatu}')
                    break

            cur.execute("UPDATE parcels SET geom = ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326)")

        except Exception:
            print('Інформація по коду КОАТУУ - ' + koatu + ' відсутня')



#commit the transcation
con.commit()

#close the cursor
cur.close()

#close the connection
con.close()