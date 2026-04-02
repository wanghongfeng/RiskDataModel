import psycopg2
import os

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('risk_data_model.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    # 创建游标
    cur = conn.cursor()
    
    # 执行SQL语句
    print("开始执行SQL语句...")
    cur.execute(sql_content)
    print("SQL语句执行成功")
    
    # 提交事务
    conn.commit()
    print("事务提交成功")
    
    # 验证表是否创建成功
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    print("\n已创建的表:")
    for table in tables:
        print(f"- {table[0]}")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()