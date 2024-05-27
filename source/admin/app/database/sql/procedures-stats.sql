/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


--
-- PROCEDURES STATS - Procedures for generatins stats, they run on a schedule
--


CREATE PROCEDURE stats_insertDailyStatsOverall (
    IN p_date DATE
)
BEGIN
    DECLARE total_orders INT;
    DECLARE total_canceled_orders INT;
    DECLARE revenue_total DECIMAL(10, 2);
    DECLARE revenue_cash DECIMAL(10, 2);
    DECLARE revenue_wallet DECIMAL(10, 2);
    DECLARE new_acc_created INT;
    DECLARE total_wallet_refills INT;
    DECLARE total_wallet_refills_amount DECIMAL(10, 2);
    DECLARE average_order_price DECIMAL(10, 2);
    DECLARE most_purchased_productId INT;

    DECLARE selected_date DATE;
    SET selected_date = DATE(p_date);
    
    SELECT
        COUNT(orderId) INTO total_orders
    FROM 
        orders
    WHERE
        orders.status != "CANCELED"
        AND DATE(orders.createdTime) = selected_date;


    SELECT
        COUNT(orderId) INTO total_canceled_orders
    FROM 
        orders
    WHERE
        orders.status = "CANCELED"
        AND DATE(orders.createdTime) = selected_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_total
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND DATE(orders.createdTime) = selected_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_cash
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND orders.paymentType = "CASH"
        AND DATE(orders.createdTime) = selected_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_wallet
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND orders.paymentType = "WALLET"
        AND DATE(orders.createdTime) = selected_date;


    SELECT
        COUNT(accountId) INTO new_acc_created
    FROM
        accounts
    WHERE
        DATE(since) = selected_date;


    SELECT
        COUNT(refillId) INTO total_wallet_refills
    FROM
        accounts_wallet_refills
    WHERE
        DATE(date) = selected_date;


    SELECT
        SUM(amount) INTO total_wallet_refills_amount
    FROM
        accounts_wallet_refills
    WHERE
        DATE(date) = selected_date;


    SELECT
        orders_products.productId INTO most_purchased_productId
    FROM
        orders_products
    JOIN
        orders ON orders.orderId = orders_products.orderId
    WHERE
        DATE(orders.createdTime) = selected_date
        AND orders.status != "CANCELED"
    GROUP BY
        orders_products.productId
    ORDER BY
        SUM(orders_products.quantity) DESC
    LIMIT 1;


    SET average_order_price = revenue_total / total_orders;


    INSERT INTO
        stats_daily_overall
        (
            `date`,
            `total_orders`,
            `total_canceled_orders`,
            `revenue_total`,
            `revenue_cash`,
            `revenue_wallet`,
            `new_acc_created`,
            `total_wallet_refills`,
            `total_wallet_refills_amount`,
            `average_order_price`,
            `most_purchased_productId`,
            `lastUpdate`

        )
    VALUES 
        (
            selected_date,
            total_orders,
            total_canceled_orders,
            revenue_total,
            revenue_cash,
            revenue_wallet,
            new_acc_created,
            total_wallet_refills,
            total_wallet_refills_amount,
            average_order_price,
            most_purchased_productId,
            CURRENT_TIMESTAMP
        )
    ON DUPLICATE KEY UPDATE
        `total_orders` = VALUES(`total_orders`),
        `total_canceled_orders` = VALUES(`total_canceled_orders`),
        `revenue_total` = VALUES(`revenue_total`),
        `revenue_cash` = VALUES(`revenue_cash`),
        `revenue_wallet` = VALUES(`revenue_wallet`),
        `new_acc_created` = VALUES(`new_acc_created`),
        `total_wallet_refills` = VALUES(`total_wallet_refills`),
        `total_wallet_refills_amount` = VALUES(`total_wallet_refills_amount`),
        `average_order_price` = VALUES(`average_order_price`),
        `most_purchased_productId` = VALUES(`most_purchased_productId`),
        `lastUpdate` = CURRENT_TIMESTAMP;
END //



CREATE PROCEDURE stats_insertDailyStatsEstablishmentsCall (
    IN p_establishmentId INT,
    IN p_date DATE
)
BEGIN
    DECLARE total_orders INT;
    DECLARE total_canceled_orders INT;
    DECLARE revenue_total DECIMAL(10, 2);
    DECLARE revenue_cash DECIMAL(10, 2);
    DECLARE revenue_wallet DECIMAL(10, 2);
    DECLARE average_order_price DECIMAL(10, 2);
    DECLARE most_purchased_productId INT;
    
    SELECT
        COUNT(orderId) INTO total_orders
    FROM 
        orders
    WHERE
        orders.status != "CANCELED"
        AND orders.establishmentId = p_establishmentId
        AND DATE(orders.createdTime) = p_date;


    SELECT
        COUNT(orderId) INTO total_canceled_orders
    FROM 
        orders
    WHERE
        orders.status = "CANCELED"
        AND orders.establishmentId = p_establishmentId
        AND DATE(orders.createdTime) = p_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_total
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND orders.establishmentId = p_establishmentId
        AND DATE(orders.createdTime) = p_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_cash
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND orders.paymentType = "CASH"
        AND orders.establishmentId = p_establishmentId
        AND DATE(orders.createdTime) = p_date;


    SELECT
        SUM(ROUND(orders_products.price * orders_products.quantity, 2)) INTO revenue_wallet
    FROM
        orders
    LEFT JOIN
        orders_products ON orders.orderId = orders_products.orderId
    WHERE
        orders.status != "CANCELED"
        AND orders.paymentType = "WALLET"
        AND orders.establishmentId = p_establishmentId
        AND DATE(orders.createdTime) = p_date;


    SELECT
        orders_products.productId INTO most_purchased_productId
    FROM
        orders_products
    JOIN
        orders ON orders.orderId = orders_products.orderId
    WHERE
        DATE(orders.createdTime) = p_date
        AND orders.establishmentId = p_establishmentId
        AND orders.status != "CANCELED"
    GROUP BY
        orders_products.productId
    ORDER BY
        SUM(orders_products.quantity) DESC
    LIMIT 1;


    SET average_order_price = revenue_total / total_orders;


    INSERT INTO
        stats_daily_establishments
        (
            `statsEstablishmentId`,
            `date`,
            `establishmentId`,
            `total_orders`,
            `total_canceled_orders`,
            `revenue_total`,
            `revenue_cash`,
            `revenue_wallet`,
            `average_order_price`,
            `most_purchased_productId`,
            `lastUpdate`
        )
    VALUES 
        (
            MD5(CONCAT(p_establishmentId, "/", p_date)),
            p_date,
            p_establishmentId,
            total_orders,
            total_canceled_orders,
            revenue_total,
            revenue_cash,
            revenue_wallet,
            average_order_price,
            most_purchased_productId,
            CURRENT_TIMESTAMP
        )
    ON DUPLICATE KEY UPDATE
        `total_orders` = VALUES(`total_orders`),
        `total_canceled_orders` = VALUES(`total_canceled_orders`),
        `revenue_total` = VALUES(`revenue_total`),
        `revenue_cash` = VALUES(`revenue_cash`),
        `revenue_wallet` = VALUES(`revenue_wallet`),
        `average_order_price` = VALUES(`average_order_price`),
        `most_purchased_productId` = VALUES(`most_purchased_productId`),
        `lastUpdate` = CURRENT_TIMESTAMP;
END //



CREATE PROCEDURE stats_insertDailyStatsEstablishments (
    IN p_date DATE 
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE establishment_id INT;
    DECLARE cur CURSOR FOR SELECT establishmentId FROM establishments;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO establishment_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Call your stored procedure here for each establishment
        CALL stats_insertDailyStatsEstablishmentsCall(establishment_id, DATE(p_date));
    END LOOP;
    CLOSE cur;
END 