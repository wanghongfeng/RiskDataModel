-- 更新关税规则的生效时间和到期时间，以2026年4月2日为基准
UPDATE tariff_rule
SET 
    effective_date = '2026-04-02',
    expiry_date = '2027-12-31',
    rule_status = '有效'
WHERE effective_date < '2026-04-02';

-- 验证更新结果
SELECT tariff_id, origin_country, destination_country, product_type, effective_date, expiry_date, rule_status
FROM tariff_rule
LIMIT 10;