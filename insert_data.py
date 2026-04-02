import psycopg2

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 读取SQL文件
with open('insert_sample_data.sql', 'r', encoding='utf-8') as f:
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
    
    # 验证工厂数据
    cur.execute("SELECT COUNT(*) FROM factory_master")
    factory_count = cur.fetchone()[0]
    print(f"工厂数据: {factory_count} 条")
    
    # 验证供应商数据
    cur.execute("SELECT COUNT(*) FROM supplier_master")
    supplier_count = cur.fetchone()[0]
    print(f"供应商数据: {supplier_count} 条")
    
    # 验证产品数据
    cur.execute("SELECT COUNT(*) FROM product_master")
    product_count = cur.fetchone()[0]
    print(f"产品数据: {product_count} 条")
    
    # 验证HRF-500产品
    cur.execute("SELECT product_id, product_name FROM product_master WHERE product_name = 'HRF-500'")
    hrf500 = cur.fetchone()
    if hrf500:
        print(f"HRF-500产品: ID={hrf500[0]}, 名称={hrf500[1]}")
    else:
        print("HRF-500产品未找到")
    
    # 验证BOM数据
    cur.execute("SELECT COUNT(*) FROM bom_master")
    bom_count = cur.fetchone()[0]
    print(f"BOM数据: {bom_count} 条")
    
    # 验证供应路径数据
    cur.execute("SELECT COUNT(*) FROM supply_path")
    supply_path_count = cur.fetchone()[0]
    print(f"供应路径数据: {supply_path_count} 条")
    
    # 验证销售订单数据
    cur.execute("SELECT COUNT(*) FROM sales_order")
    sales_order_count = cur.fetchone()[0]
    print(f"销售订单数据: {sales_order_count} 条")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    print("\n数据库连接已关闭")
    
except Exception as e:
    print(f"错误: {e}")
    if 'conn' in locals():
        conn.rollback()
        conn.close()