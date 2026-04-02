import psycopg2
from datetime import datetime

# 数据库连接参数
db_url = "postgresql://neondb_owner:npg_tiBzN8keDJf4@ep-cool-night-amag8gwx-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_tariff_risk_level(current_tariff, future_tariff):
    """根据当前关税和未来关税的差异评估关税风险等级"""
    if current_tariff is None:
        return "中"
    
    # 计算关税变化幅度
    tariff_increase = 0
    if future_tariff and future_tariff > current_tariff:
        tariff_increase = future_tariff - current_tariff
    
    # 综合当前关税水平和增加幅度判断风险
    if current_tariff >= 20 or (current_tariff >= 10 and tariff_increase >= 10):
        return "高"
    elif current_tariff >= 10 or (current_tariff >= 5 and tariff_increase >= 5):
        return "中"
    else:
        return "低"

def get_product_risk_level(product_type, base_price, tariff_impact):
    """根据产品类型、价格和关税影响评估产品风险等级"""
    # 基础风险等级
    if product_type in ["旗舰冰箱", "高端冰箱"]:
        base_risk = "高" if base_price >= 5000 else "中"
    elif product_type in ["中高端冰箱"]:
        base_risk = "中"
    else:
        base_risk = "低"
    
    # 考虑关税影响
    if tariff_impact == "高":
        if base_risk == "低":
            return "中"
        elif base_risk == "中":
            return "高"
    elif tariff_impact == "中" and base_risk == "高":
        return "高"
    
    return base_risk

def get_factory_risk_level(factory_country, destination_country, current_tariff, future_tariff):
    """根据工厂所在国家的产品销售区域受关税变化的影响幅度评估工厂风险等级"""
    if current_tariff is None:
        return "中"
    
    # 计算关税变化幅度
    tariff_increase = 0
    if future_tariff and future_tariff > current_tariff:
        tariff_increase = future_tariff - current_tariff
    
    # 重点关注中国到美国的关税变化
    if factory_country == "中国" and destination_country == "美国":
        if current_tariff >= 20 or (current_tariff >= 10 and tariff_increase >= 10):
            return "高"
        elif current_tariff >= 10 or (current_tariff >= 5 and tariff_increase >= 5):
            return "中"
    
    # 其他国家组合
    if tariff_increase >= 10:
        return "高"
    elif tariff_increase >= 5:
        return "中"
    
    return "低"

def calculate_overall_risk(tariff_risk, product_risk, factory_risk):
    """计算综合风险等级"""
    risk_scores = {"高": 3, "中": 2, "低": 1}
    total_score = risk_scores.get(tariff_risk, 2) + risk_scores.get(product_risk, 2) + risk_scores.get(factory_risk, 2)
    
    if total_score >= 7:
        return "高"
    elif total_score >= 5:
        return "中"
    else:
        return "低"

def generate_risk_mapping():
    try:
        # 连接到数据库
        conn = psycopg2.connect(db_url)
        print("成功连接到数据库")
        
        cur = conn.cursor()
        
        # 检查风险映射表是否存在，不存在则创建
        print("检查风险映射表...")
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'risk_mapping'
            )
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("创建风险映射表...")
            with open('risk_mapping.sql', 'r', encoding='utf-8') as f:
                cur.execute(f.read())
            conn.commit()
            print("风险映射表创建成功")
        else:
            print("风险映射表已存在，跳过创建")
        
        # 清空现有数据
        cur.execute("DELETE FROM risk_mapping")
        conn.commit()
        print("清空现有风险映射数据")
        
        # 查询供应路径和相关数据
        query = """
        SELECT 
            sp.path_id,
            sp.factory_id,
            sp.supplier_id,
            sp.key_component_id,
            f.country as origin_country,
            f.capacity as factory_capacity,
            p.product_id,
            p.product_name,
            p.product_type,
            p.base_price,
            p.target_markets,
            s.tier as supplier_tier,
            s.credit_rating as supplier_credit
        FROM supply_path sp
        JOIN factory_master f ON sp.factory_id = f.factory_id
        JOIN product_master p ON sp.factory_id = p.factory_id
        LEFT JOIN supplier_master s ON sp.supplier_id = s.supplier_id
        """
        
        cur.execute(query)
        supply_paths = cur.fetchall()
        print(f"获取到 {len(supply_paths)} 条供应路径数据")
        
        # 查询销售订单数据获取目的国家
        cur.execute("SELECT DISTINCT product_id, sales_country FROM sales_order")
        sales_data = cur.fetchall()
        
        # 构建产品到销售国家的映射
        product_sales_map = {}
        for product_id, sales_country in sales_data:
            if product_id not in product_sales_map:
                product_sales_map[product_id] = []
            product_sales_map[product_id].append(sales_country)
        
        # 查询关税规则
        cur.execute("SELECT origin_country, destination_country, product_type, current_tariff, future_tariff FROM tariff_rule WHERE rule_status = '有效'")
        tariff_rules = cur.fetchall()
        
        # 构建关税规则字典
        tariff_dict = {}
        for origin, dest, prod_type, current_tariff, future_tariff in tariff_rules:
            key = (origin, dest, prod_type)
            tariff_dict[key] = (current_tariff, future_tariff)
        
        print(f"获取到 {len(tariff_rules)} 条关税规则")
        
        # 生成风险映射数据
        risk_mappings = []
        mapping_id = 1
        
        print(f"开始处理 {len(supply_paths)} 条供应路径数据...")
        
        for i, path in enumerate(supply_paths):
            if i % 5 == 0:
                print(f"  处理第 {i+1}/{len(supply_paths)} 条供应路径...")
            path_id, factory_id, supplier_id, component_id, origin_country, factory_capacity, product_id, product_name, product_type, base_price, target_markets, supplier_tier, supplier_credit = path
            
            # 获取产品的销售国家
            destination_countries = product_sales_map.get(product_id, [])
            if not destination_countries:
                # 如果没有销售订单，使用目标市场
                destination_countries = target_markets.split(", ") if target_markets else ["未知"]
            
            for dest_country in destination_countries:
                # 查找关税
                tariff_key = (origin_country, dest_country, product_type)
                tariff_info = tariff_dict.get(tariff_key)
                
                # 初始化关税值
                current_tariff = None
                future_tariff = None
                
                if tariff_info:
                    current_tariff, future_tariff = tariff_info
                else:
                    # 如果没有精确匹配，尝试模糊匹配
                    if dest_country in ["德国", "法国", "英国"]:
                        tariff_key = (origin_country, "欧盟", product_type)
                        tariff_info = tariff_dict.get(tariff_key)
                    elif dest_country in ["越南", "泰国", "印度"]:
                        tariff_key = (origin_country, "东南亚", product_type)
                        tariff_info = tariff_dict.get(tariff_key)
                    
                    if tariff_info:
                        current_tariff, future_tariff = tariff_info
                
                # 评估风险等级
                tariff_risk = get_tariff_risk_level(current_tariff, future_tariff)
                product_risk = get_product_risk_level(product_type, base_price, tariff_risk)
                factory_risk = get_factory_risk_level(origin_country, dest_country, current_tariff, future_tariff)
                overall_risk = calculate_overall_risk(tariff_risk, product_risk, factory_risk)
                
                # 计算风险分数 (0-100)
                risk_score = 0
                if current_tariff:
                    risk_score += min(current_tariff * 2, 40)  # 关税贡献最多40分
                risk_score += {"高": 30, "中": 20, "低": 10}.get(product_risk, 20)
                risk_score += {"高": 30, "中": 20, "低": 10}.get(factory_risk, 20)
                
                risk_mappings.append((
                    path_id, product_id, factory_id, supplier_id,
                    origin_country, dest_country, current_tariff,
                    tariff_risk, product_risk, factory_risk, overall_risk, risk_score
                ))
                mapping_id += 1
        
        # 插入风险映射数据
        insert_query = """
        INSERT INTO risk_mapping 
        (path_id, product_id, factory_id, supplier_id, origin_country, destination_country,
         current_tariff, tariff_risk_level, product_risk_level, factory_risk_level, overall_risk_level, risk_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        print(f"准备插入 {len(risk_mappings)} 条风险映射数据...")
        cur.executemany(insert_query, risk_mappings)
        conn.commit()
        print(f"成功插入 {len(risk_mappings)} 条风险映射数据")
        
        # 查询并展示结果
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
        
        # 关闭连接
        cur.close()
        conn.close()
        print("\n风险映射生成完成，数据库连接已关闭")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    generate_risk_mapping()