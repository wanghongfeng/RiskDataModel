import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    # 创建游标
    cur = conn.cursor()
    
    # 查询当前的关税规则生效时间
    print("当前关税规则的生效时间:")
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, effective_date, expiry_date FROM tariff_rule LIMIT 10")
    tariffs = cur.fetchall()
    
    print("ID | 起始国家 | 目的国家 | 产品类型 | 生效日期 | 到期日期")
    print("-" * 80)
    
    for tariff in tariffs:
        tariff_id, origin, dest, product_type, effective_date, expiry_date = tariff
        print(f"{tariff_id} | {origin} | {dest} | {product_type} | {effective_date} | {expiry_date}")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()