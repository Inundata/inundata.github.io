import pymysql

def access_db(host, user, pw, target_db):
    charset, collation = "utf8mb4", "utf8mb4_0900_ai_ci"

    conn = pymysql.connect(host = host
                        , user = user
                        , password = pw
                        , database =target_db
                        , collation = collation
                        , charset = charset)
    cur = conn.cursor()
    
    return cur, conn