-- 删除目的国家不是美国的关税规则
DELETE FROM tariff_rule 
WHERE destination_country != '美国';

-- 更新剩余关税规则的生效时间为2026年4月3日（2026年4月2日之后）
UPDATE tariff_rule
SET effective_date = '2026-04-03',
    expiry_date = '2027-12-31',
    rule_status = '有效'
WHERE destination_country = '美国';

-- 验证更新结果
SELECT tariff_id, origin_country, destination_country, product_type, 
       current_tariff, future_tariff, effective_date, expiry_date, rule_status
FROM tariff_rule
ORDER BY origin_country, product_type;