import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('update_tariff.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    # 创建游标
    cur = conn.cursor()
    
    # 执行SQL语句
    print("开始执行SQL更新语句...")
    cur.execute(sql_content)
    print("SQL更新语句执行成功")
    
    # 提交事务
    conn.commit()
    print("事务提交成功")
    
    # 验证更新结果
    print("\n验证更新结果:")
    
    # 重新查询中国到美国的关税规则
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, current_tariff, future_tariff FROM tariff_rule WHERE origin_country = '中国' AND destination_country = '美国'")
    china_us_tariffs = cur.fetchall()
    
    print("中国到美国的关税规则（更新后）:")
    print("ID | 产品类型 | 当前关税 | 未来关税 | 变化")
    print("-" * 50)
    
    for tariff in china_us_tariffs:
        tariff_id, origin, dest, product_type, current, future = tariff
        change = future - current
        print(f"{tariff_id} | {product_type} | {current}% | {future}% | {'+' if change > 0 else ''}{change}%")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()