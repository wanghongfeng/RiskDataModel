-- 风险映射表
CREATE TABLE risk_mapping (
    mapping_id SERIAL PRIMARY KEY,
    path_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    factory_id VARCHAR(50) NOT NULL,
    supplier_id VARCHAR(50),
    origin_country VARCHAR(50) NOT NULL,
    destination_country VARCHAR(50) NOT NULL,
    current_tariff DECIMAL(5,2),
    tariff_risk_level VARCHAR(10),
    product_risk_level VARCHAR(10),
    factory_risk_level VARCHAR(10),
    overall_risk_level VARCHAR(10),
    risk_score INT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (path_id) REFERENCES supply_path(path_id),
    FOREIGN KEY (product_id) REFERENCES product_master(product_id),
    FOREIGN KEY (factory_id) REFERENCES factory_master(factory_id)
);

-- 创建索引
CREATE INDEX idx_risk_mapping_path ON risk_mapping(path_id);
CREATE INDEX idx_risk_mapping_product ON risk_mapping(product_id);
CREATE INDEX idx_risk_mapping_factory ON risk_mapping(factory_id);
CREATE INDEX idx_risk_mapping_overall ON risk_mapping(overall_risk_level);