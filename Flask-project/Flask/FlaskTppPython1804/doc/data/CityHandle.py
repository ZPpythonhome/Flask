"""

    要写一个脚本，把Json数据导入到数据库中

    读取出数据
    数据写入到数据库

"""
import json

import pymysql


def json_to_db():
    # 建立数据库链接，  客户端
    client = pymysql.Connect(user="root", password="rock1204", host="localhost", port=3306, db="Python1804FlaskTpp", charset='utf8')
    # 使用代码操作数据库，  游标
    cursor = client.cursor()





    with open('City.json', "r") as cities_info:
        cities_content = cities_info.read()

        # print(type(cities_content))

        # print(cities_content)

        json_load = json.loads(cities_content)

        # print(json_load)

        # print(type(json_load))
        returnValue = json_load.get('returnValue')

        # print(returnValue)
        #
        # print(type(returnValue))

        keys = returnValue.keys()

        # print(keys)

        for key in keys:

            print(key)
            # 使用游标进行数据操作
            cursor.execute("INSERT INTO letter(letter) VALUE ('%s');" % key)

            client.commit()

            cursor.execute("SELECT * FROM letter WHERE letter='%s';" % key )

            result = cursor.fetchone()

            letter_id = result[0]

            # print(returnValue.get(key))

            city_list = returnValue.get(key)

            for city_info in city_list:
                # print(city_info)

                id = city_info.get("id")

                regionName = city_info.get("regionName")

                cityCode = city_info.get("cityCode")

                pinYin = city_info.get("pinYin")

                print(id, regionName, cityCode, pinYin)

                cursor.execute("INSERT INTO city(id, regionName, cityCode, pinYin, c_letter) VALUE (%d, '%s', %d, '%s', %d);" % (id, regionName, cityCode, pinYin, letter_id))

                client.commit()

    cursor.close()

    client.close()


if __name__ == '__main__':
    json_to_db()