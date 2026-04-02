# 风险数据模型文档

## 1. 数据模型概述

本数据模型设计用于管理海尔集团的供应链风险数据，包含以下核心数据表：

- 工厂主数据表
- 产品主数据表
- BOM主数据表
- 供应商主数据表
- 供应路径表
- 销售订单表

## 2. 表结构详细说明

### 2.1 工厂主数据表 (factory_master)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| factory_id | VARCHAR(50) | PRIMARY KEY | 工厂唯一标识 |
| factory_name | VARCHAR(100) | NOT NULL | 工厂名称 |
| country | VARCHAR(50) | NOT NULL | 工厂所在国家 |
| capacity | INT | NOT NULL | 工厂产能 |
| main_markets | VARCHAR(255) | | 主要市场 |
| established_date | DATE | | 建立日期 |
| status | VARCHAR(20) | | 工厂状态 |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 最后更新时间 |

### 2.2 产品主数据表 (product_master)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| product_id | VARCHAR(50) | PRIMARY KEY | 产品唯一标识 |
| product_name | VARCHAR(100) | NOT NULL | 产品名称 |
| factory_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | 生产工厂ID |
| target_markets | VARCHAR(255) | | 目标市场 |
| base_price | DECIMAL(10,2) | NOT NULL | 基础价格 |
| product_type | VARCHAR(50) | | 产品类型 |
| launch_date | DATE | | 上市日期 |

### 2.3 BOM主数据表 (bom_master)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| bom_id | VARCHAR(50) | PRIMARY KEY | BOM唯一标识 |
| product_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | 产品ID |
| key_component_id | VARCHAR(50) | NOT NULL | 关键零部件ID |
| key_component_name | VARCHAR(100) | NOT NULL | 关键零部件名称 |
| quantity | INT | NOT NULL | 数量 |
| price | DECIMAL(10,2) | NOT NULL | 价格 |
| supplier_id | VARCHAR(50) | | 供应商ID |

### 2.4 供应商主数据表 (supplier_master)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| supplier_id | VARCHAR(50) | PRIMARY KEY | 供应商唯一标识 |
| supplier_name | VARCHAR(100) | NOT NULL | 供应商名称 |
| country | VARCHAR(50) | NOT NULL | 供应商所在国家 |
| tier | INT | NOT NULL | 供应商层级 |
| supplier_type | VARCHAR(50) | | 供应商类型 |
| established_date | DATE | | 成立日期 |
| credit_rating | VARCHAR(10) | | 信用评级 |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 最后更新时间 |

### 2.5 供应路径表 (supply_path)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| path_id | VARCHAR(50) | PRIMARY KEY | 路径唯一标识 |
| key_component_id | VARCHAR(50) | NOT NULL | 关键零部件ID |
| supplier_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | 供应商ID |
| supply_country | VARCHAR(50) | NOT NULL | 供应国家 |
| factory_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | 工厂ID |
| path_type | VARCHAR(50) | | 路径类型 |
| lead_time | INT | | 前置时间 |
| transportation_mode | VARCHAR(50) | | 运输方式 |

### 2.6 销售订单表 (sales_order)

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|------|------|
| order_id | VARCHAR(50) | PRIMARY KEY | 订单唯一标识 |
| product_id | VARCHAR(50) | NOT NULL, FOREIGN KEY | 产品ID |
| quantity | INT | NOT NULL | 数量 |
| sales_country | VARCHAR(50) | NOT NULL | 销售国家 |
| price | DECIMAL(10,2) | NOT NULL | 价格 |
| order_date | DATE | NOT NULL | 订单日期 |
| delivery_date | DATE | | 交付日期 |
| status | VARCHAR(20) | | 订单状态 |

## 3. 关系图

```
+---------------+      +---------------+      +---------------+
| factory_master|      | product_master|      | sales_order   |
+---------------+      +---------------+      +---------------+
| factory_id    |<-----| factory_id    |<-----| product_id    |
| country       |      | product_id    |      | order_id      |
| capacity      |      | base_price    |      | quantity      |
+---------------+      +---------------+      +---------------+
        ^                      |
        |                      |
        |                      v
        |                +---------------+
        |                | bom_master    |
        |                +---------------+
        |                | product_id    |
        |                | key_component_id|
        |                +---------------+
        |                      |
        |                      |
        v                      v
+---------------+      +---------------+
| supplier_master|      | supply_path   |
+---------------+      +---------------+
| supplier_id   |<-----| supplier_id   |
| country       |      | factory_id    |<--+
| tier          |      | lead_time     |   |
+---------------+      +---------------+   |
                                            |
                                            +----------------+
```

## 4. 索引设计

为提高查询性能，已为以下字段创建索引：

- `factory_master.country` - 按国家查询工厂
- `product_master.factory_id` - 按工厂查询产品
- `bom_master.product_id` - 按产品查询BOM
- `supplier_master.country` - 按国家查询供应商
- `supply_path.factory_id` - 按工厂查询供应路径
- `supply_path.supplier_id` - 按供应商查询供应路径
- `sales_order.product_id` - 按产品查询订单
- `sales_order.sales_country` - 按国家查询订单

## 5. 数据模型使用说明

### 5.1 风险分析场景

1. **供应链风险分析**：
   - 通过供应路径表分析关键零部件的供应风险
   - 结合供应商层级和信用评级评估供应稳定性

2. **生产能力风险分析**：
   - 分析工厂产能与订单需求的匹配情况
   - 评估不同国家工厂的生产风险

3. **市场风险分析**：
   - 分析产品在不同国家的销售分布
   - 评估目标市场的风险集中度

4. **成本风险分析**：
   - 通过BOM表分析关键零部件成本占比
   - 评估供应商价格波动对产品成本的影响

### 5.2 数据加载建议

1. **主数据加载顺序**：
   - 先加载 `factory_master` 和 `supplier_master`
   - 然后加载 `product_master`
   - 接着加载 `bom_master`
   - 最后加载 `supply_path` 和 `sales_order`

2. **数据更新频率**：
   - 主数据表（工厂、供应商）：定期更新
   - 产品和BOM表：产品变更时更新
   - 供应路径表：供应链变更时更新
   - 销售订单表：实时更新

## 6. 扩展建议

1. **增加风险评估表**：用于存储各维度的风险评估结果
2. **增加历史数据表**：记录关键数据的历史变化
3. **增加预警规则表**：定义风险预警的规则和阈值
4. **增加应急预案表**：存储应对风险的预案

## 7. 技术实现建议

1. **数据库选择**：建议使用PostgreSQL或MySQL
2. **ETL流程**：建立自动化的数据抽取、转换和加载流程
3. **数据仓库集成**：考虑与企业数据仓库集成
4. **API设计**：为风险分析系统提供数据访问API

## 8. 安全考虑

1. **数据访问控制**：根据用户角色设置不同的访问权限
2. **数据加密**：对敏感数据进行加密存储
3. **审计日志**：记录数据变更的审计日志
4. **备份策略**：建立定期数据备份机制

---

本数据模型设计遵循规范化原则，确保数据完整性和一致性，同时考虑了查询性能和风险分析的需求。