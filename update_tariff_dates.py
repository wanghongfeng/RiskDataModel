import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('update_tariff_dates.sql', 'r', encoding='utf-8') as f:
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
    
    # 重新查询关税规则的生效时间
    cur.execute("SELECT tariff_id, origin_country, destination_country, product_type, effective_date, expiry_date, rule_status FROM tariff_rule LIMIT 10")
    tariffs = cur.fetchall()
    
    print("ID | 起始国家 | 目的国家 | 产品类型 | 生效日期 | 到期日期 | 状态")
    print("-" * 90)
    
    for tariff in tariffs:
        tariff_id, origin, dest, product_type, effective_date, expiry_date, status = tariff
        print(f"{tariff_id} | {origin} | {dest} | {product_type} | {effective_date} | {expiry_date} | {status}")
    
    # 统计更新的记录数
    cur.execute("SELECT COUNT(*) FROM tariff_rule WHERE effective_date = '2026-04-02'")
    updated_count = cur.fetchone()[0]
    print(f"\n已更新 {updated_count} 条关税规则的生效时间")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()