import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('insert_tariff_data.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    # 创建游标
    cur = conn.cursor()
    
    # 执行SQL语句
    print("开始执行SQL插入语句...")
    cur.execute(sql_content)
    print("SQL插入语句执行成功")
    
    # 提交事务
    conn.commit()
    print("事务提交成功")
    
    # 验证数据是否插入成功
    print("\n验证插入的数据:")
    
    # 验证关税规则数据
    cur.execute("SELECT COUNT(*) FROM tariff_rule")
    tariff_count = cur.fetchone()[0]
    print(f"关税规则数据: {tariff_count} 条")
    
    # 验证中国到美国的关税规则
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, current_tariff FROM tariff_rule WHERE origin_country = '中国' AND destination_country = '美国' LIMIT 3")
    china_us_tariffs = cur.fetchall()
    print("\n中国到美国的关税规则:")
    for tariff in china_us_tariffs:
        print(f"ID: {tariff[0]}, 产品类型: {tariff[3]}, 当前关税: {tariff[4]}%")
    
    # 验证越南到东南亚的关税规则
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, current_tariff FROM tariff_rule WHERE origin_country = '越南' AND destination_country = '东南亚' LIMIT 2")
    vietnam_asean_tariffs = cur.fetchall()
    print("\n越南到东南亚的关税规则:")
    for tariff in vietnam_asean_tariffs:
        print(f"ID: {tariff[0]}, 产品类型: {tariff[3]}, 当前关税: {tariff[4]}%")
    
    # 验证德国到欧盟国家的关税规则
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, current_tariff FROM tariff_rule WHERE origin_country = '德国' AND (destination_country = '英国' OR destination_country = '法国') LIMIT 2")
    germany_eu_tariffs = cur.fetchall()
    print("\n德国到欧盟国家的关税规则:")
    for tariff in germany_eu_tariffs:
        print(f"ID: {tariff[0]}, 目的地: {tariff[2]}, 产品类型: {tariff[3]}, 当前关税: {tariff[4]}%")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()