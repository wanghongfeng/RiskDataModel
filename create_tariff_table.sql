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
CREATE INDEX idx_tariff_origin ON tariff_rule(origin_country);
CREATE INDEX idx_tariff_destination ON tariff_rule(destination_country);
CREATE INDEX idx_tariff_product ON tariff_rule(product_type);