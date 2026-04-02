-- 工厂主数据表
CREATE TABLE factory_master (
    factory_id VARCHAR(50) PRIMARY KEY,
    factory_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    main_markets VARCHAR(255),
    established_date DATE,
    status VARCHAR(20),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 产品主数据表
CREATE TABLE product_master (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    factory_id VARCHAR(50) NOT NULL,
    target_markets VARCHAR(255),
    base_price DECIMAL(10,2) NOT NULL,
    product_type VARCHAR(50),
    launch_date DATE,
    FOREIGN KEY (factory_id) REFERENCES factory_master(factory_id)
);

-- BOM主数据表
CREATE TABLE bom_master (
    bom_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    key_component_id VARCHAR(50) NOT NULL,
    key_component_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    supplier_id VARCHAR(50),
    FOREIGN KEY (product_id) REFERENCES product_master(product_id)
);

-- 供应商主数据表
CREATE TABLE supplier_master (
    supplier_id VARCHAR(50) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    tier INT NOT NULL,
    supplier_type VARCHAR(50),
    established_date DATE,
    credit_rating VARCHAR(10),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 供应路径表
CREATE TABLE supply_path (
    path_id VARCHAR(50) PRIMARY KEY,
    key_component_id VARCHAR(50) NOT NULL,
    supplier_id VARCHAR(50) NOT NULL,
    supply_country VARCHAR(50) NOT NULL,
    factory_id VARCHAR(50) NOT NULL,
    path_type VARCHAR(50),
    lead_time INT,
    transportation_mode VARCHAR(50),
    FOREIGN KEY (supplier_id) REFERENCES supplier_master(supplier_id),
    FOREIGN KEY (factory_id) REFERENCES factory_master(factory_id)
);

-- 销售订单表
CREATE TABLE sales_order (
    order_id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    sales_country VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (product_id) REFERENCES product_master(product_id)
);

-- 关税规则表
CREATE TABLE tariff_rule (
    tariff_id VARCHAR(50) PRIMARY KEY,
    origin_country VARCHAR(50) NOT NULL,
    destination_country VARCHAR(50) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    current_tariff DECIMAL(5,2) NOT NULL,
    future_tariff DECIMAL(5,2),
    effective_date DATE NOT NULL,
    expiry_date DATE,
    rule_status VARCHAR(20),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 为频繁查询的字段创建索引
CREATE INDEX idx_factory_country ON factory_master(country);
CREATE INDEX idx_product_factory ON product_master(factory_id);
CREATE INDEX idx_bom_product ON bom_master(product_id);
CREATE INDEX idx_supplier_country ON supplier_master(country);
CREATE INDEX idx_supply_path_factory ON supply_path(factory_id);
CREATE INDEX idx_supply_path_supplier ON supply_path(supplier_id);
CREATE INDEX idx_sales_order_product ON sales_order(product_id);
CREATE INDEX idx_sales_order_country ON sales_order(sales_country);
CREATE INDEX idx_tariff_origin ON tariff_rule(origin_country);
CREATE INDEX idx_tariff_destination ON tariff_rule(destination_country);
CREATE INDEX idx_tariff_product ON tariff_rule(product_type);