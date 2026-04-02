-- 更新中国到美国的关税规则，将未来关税设置为高于当前关税
UPDATE tariff_rule
SET future_tariff = 
    CASE 
        WHEN product_type = '高端冰箱' THEN 30.00
        WHEN product_type = '中高端冰箱' THEN 30.00
        WHEN product_type = '中端冰箱' THEN 25.00
        WHEN product_type = '经济型冰箱' THEN 20.00
        ELSE future_tariff
    END
WHERE origin_country = '中国' AND destination_country = '美国';

-- 验证更新结果
SELECT tariff_id, origin_country, destination_country, product_type, current_tariff, future_tariff
FROM tariff_rule
WHERE origin_country = '中国' AND destination_country = '美国';