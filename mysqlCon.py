import pymysql

timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="jack",
    host="libs-mang-pace-a6bb.h.aivencloud.com",
    password="AVNS_kJAYQ8B-B72d_qVa0lR",
    read_timeout=timeout,
    port=11632,
    user="avnadmin",
    write_timeout=timeout,
)

try:
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sample")
    print(cursor.fetchall())
finally:
    connection.close()
