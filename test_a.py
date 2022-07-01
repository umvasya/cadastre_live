import os
import json
import psycopg2
import pygeoj

cadnum = '3223387200:06:027:0157'
category = 'category'
purpose = '10.07 Для рибогосподарських потреб Для організації риболовецького стану'
area = '2.04578'
ownership = 'Державна власність'

gjson = {"type":"Polygon","coordinates":[[[30.42234420776367,50.45061835789743],[30.477619171142575,50.417706358529024],[30.50422668457031,50.46209390533412],[30.446376800537106,50.48033975575682],[30.42234420776367,50.45061835789743]]]}
coordinates = gjson["coordinates"]
coord_text = ''
coord = ''
for i in coordinates[0]:
    item_in_list = str(i[0]) + ' ' + str(i[1])
    coord_text = coord_text + item_in_list + ','
coord = gjson["type"] + '((' + str(coord_text) + '))'
print(coord)
coord = 'POLYGON((31.754608154296875 51.17417731875822, 32.10205078125 54.85131525968606, 29.15771484375 54.87660665410869, 26.87255859375 52.02545860348814, 29.003906249999996 49.79544988802771, 32.51953125 50.544853857152326, 32.589569091796875 50.84150302516789, 32.509918212890625 51.24902276043772, 31.754608154296875 51.17417731875822))'
# #loadjsontable

#connect to the db
con = psycopg2.connect(
            host = "localhost",
            database="postgis_31_sample",
            user = "postgres",
            password = "postgres")

# cursor
cur = con.cursor()
cur.execute("INSERT INTO loadjsontable(cadnum, category, purpose, area, ownership, coordinates) VALUES (%s, %s, %s, %s, %s, %s)",
                                (cadnum, category, purpose, area, ownership, coord))


con.commit()
cur.execute("UPDATE loadjsontable SET parcel_geom = ST_PolyFromText(coordinates, 4326)")
print(str(cadnum) + ' ----------- DONE')

#
# cur.execute("SELECT ST_SetSRID(ST_GeomFromGeoJSON(%s),4326)", (gjson))
# con.commit()


# commit the transcation
con.commit()

# close the cursor
cur.close()

# close the connection
con.close()