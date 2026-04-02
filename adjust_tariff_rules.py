import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('adjust_tariff_rules.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    # 创建游标
    cur = conn.cursor()
    
    # 先查询当前的关税规则数量
    cur.execute("SELECT COUNT(*) FROM tariff_rule")
    before_count = cur.fetchone()[0]
    print(f"调整前关税规则数量: {before_count}")
    
    # 执行SQL语句
    print("开始执行关税规则调整...")
    cur.execute(sql_content)
    print("关税规则调整执行成功")
    
    # 提交事务
    conn.commit()
    print("事务提交成功")
    
    # 验证调整结果
    print("\n验证调整结果:")
    
    # 查询调整后的关税规则数量
    cur.execute("SELECT COUNT(*) FROM tariff_rule")
    after_count = cur.fetchone()[0]
    print(f"调整后关税规则数量: {after_count}")
    print(f"删除了 {before_count - after_count} 条非美国目的国家的关税规则")
    
    # 查询剩余的关税规则
    cur.execute("""
    SELECT tariff_id, origin_country, destination_country, product_type, 
           current_tariff, future_tariff, effective_date, expiry_date, rule_status
    FROM tariff_rule
    ORDER BY origin_country, product_type
    """)
    
    tariffs = cur.fetchall()
    print("\n剩余关税规则:")
    print("ID | 起始国家 | 目的国家 | 产品类型 | 当前关税 | 未来关税 | 生效日期 | 到期日期 | 状态")
    print("-" * 120)
    
    for tariff in tariffs:
        tariff_id, origin, dest, prod_type, current, future, effective, expiry, status = tariff
        print(f"{tariff_id} | {origin} | {dest} | {prod_type} | {current}% | {future}% | {effective} | {expiry} | {status}")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    if 'conn' in locals():
        conn.rollback()
        conn.close()