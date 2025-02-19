import mysql.connector
from datetime import datetime

# 数据库连接配置
def save_mysql(img_io, emo):
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'image'
    }

    # 建立数据库连接
    mydb = mysql.connector.connect(**config)
    # 创建游标对象
    mycursor = mydb.cursor()

    # 创建表（如果表不存在）
    create_table_query = """
        CREATE TABLE IF NOT EXISTS images (
            序号 INT AUTO_INCREMENT PRIMARY KEY,
            图片编码 BLOB,
            存储日期 DATETIME,
            心情描述 VARCHAR(255)
        )
        """
    mycursor.execute(create_table_query)

    # 准备要插入的数据
    image_code = img_io
    record_time = datetime.now()
    emotion = emo
    # 插入数据的 SQL 语句
    insert_query = "INSERT INTO images(图片编码, 存储日期, 心情描述) VALUES (%s, %s ,%s)"
    data = (image_code, record_time, emotion)

    # 执行插入操作
    mycursor.execute(insert_query, data)
    # 提交事务
    mydb.commit()

    print(mycursor.rowcount, "条记录插入成功。")

    # 关闭游标和数据库连接
    mycursor.close()
    mydb.close()


def get_history_images():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="image"
        )
        cursor = conn.cursor()
        select_query = "SELECT 序号, 心情描述 FROM images"
        cursor.execute(select_query)
        result = cursor.fetchall()
        images = [{"id": row[0], "name": row[1]} for row in result]
        cursor.close()
        conn.close()
        return images
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []


# 根据图片 ID 获取图片数据
def get_image_by_id(image_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="image"
        )
        cursor = conn.cursor()
        # 修改为正确的字段名
        select_query = "SELECT 图片编码 FROM images WHERE 序号 = %s"
        cursor.execute(select_query, (image_id,))
        result = cursor.fetchone()
        if result:
            image_data = result[0]
        else:
            image_data = None
        cursor.close()
        conn.close()
        return image_data
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None


# 保存编辑后的图片到数据库
def save_edited_image(edited_image_data, image_name):
    try:
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'image'
        }
        # 建立数据库连接
        mydb = mysql.connector.connect(**config)
        # 创建游标对象
        mycursor = mydb.cursor()

        # 创建表（如果表不存在）
        create_table_query = """
            CREATE TABLE IF NOT EXISTS images (
                序号 INT AUTO_INCREMENT PRIMARY KEY,
                图片编码 BLOB,
                存储日期 DATETIME,
                心情描述 VARCHAR(255)
            )
            """
        mycursor.execute(create_table_query)

        # 准备要插入的数据
        image_code = edited_image_data
        record_time = datetime.now()
        # 这里将图片名字作为心情描述存储
        emotion = image_name

        # 插入数据的 SQL 语句
        insert_query = "INSERT INTO images(图片编码, 存储日期, 心情描述) VALUES (%s, %s, %s)"
        data = (image_code, record_time, emotion)

        # 执行插入操作
        mycursor.execute(insert_query, data)
        # 提交事务
        mydb.commit()

        print(mycursor.rowcount, "条编辑后的图片记录插入成功。")

        # 关闭游标和数据库连接
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print(f"保存编辑后的图片到数据库时出错: {err}")


# 新增的删除图片记录的方法
def delete_image_by_id(image_id):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="image"
        )
        cursor = conn.cursor()
        delete_query = "DELETE FROM images WHERE 序号 = %s"
        cursor.execute(delete_query, (image_id,))
        conn.commit()
        print(cursor.rowcount, "条记录删除成功。")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"删除记录时出错: {err}")
