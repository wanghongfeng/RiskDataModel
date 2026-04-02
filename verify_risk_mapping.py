import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    # 连接到数据库
    conn = psycopg2.connect(db_url)
    print("成功连接到数据库")
    
    cur = conn.cursor()
    
    # 查询风险映射表中的数据条数
    cur.execute("SELECT COUNT(*) FROM risk_mapping")
    count = cur.fetchone()[0]
    print(f"\n风险映射表中共有 {count} 条数据")
    
    # 查询风险映射结果预览
    print("\n风险映射结果预览 (前10条):")
    cur.execute("""
    SELECT 
        mapping_id, path_id, origin_country, destination_country,
        current_tariff, tariff_risk_level, product_risk_level, 
        factory_risk_level, overall_risk_level, risk_score
    FROM risk_mapping 
    ORDER BY risk_score DESC
    LIMIT 10
    """)
    
    results = cur.fetchall()
    print("ID | 路径ID | 原产国 | 目的国 | 关税 | 关税风险 | 产品风险 | 工厂风险 | 综合风险 | 风险分数")
    print("-" * 100)
    for row in results:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}% | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]}")
    
    # 统计风险分布
    print("\n风险等级分布统计:")
    cur.execute("SELECT overall_risk_level, COUNT(*) FROM risk_mapping GROUP BY overall_risk_level ORDER BY overall_risk_level")
    risk_dist = cur.fetchall()
    for level, count in risk_dist:
        print(f"{level}风险: {count} 条")
    
    # 查询高风险记录
    print("\n高风险记录详情:")
    cur.execute("""
    SELECT 
        mapping_id, path_id, origin_country, destination_country,
        current_tariff, product_risk_level, factory_risk_level, overall_risk_level, risk_score
    FROM risk_mapping 
    WHERE overall_risk_level = '高'
    ORDER BY risk_score DESC
    LIMIT 5
    """)
    
    high_risk = cur.fetchall()
    for row in high_risk:
        print(f"ID:{row[0]} 路径:{row[1]} {row[2]}->{row[3]} 关税:{row[4]}% 产品风险:{row[5]} 工厂风险:{row[6]} 综合:{row[7]} 分数:{row[8]}")
    
    # 关闭连接
    cur.close()
    conn.close()
    print("\n验证完成，数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    if 'conn' in locals():
        conn.close()
