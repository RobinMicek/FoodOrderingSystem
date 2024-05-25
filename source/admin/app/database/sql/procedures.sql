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
-- PROCEDURES 
--


-- Procedure for inserting data into the accounts table
CREATE PROCEDURE InsertAccount(
      IN p_email VARCHAR(255),
      IN p_phone VARCHAR(255),
      IN p_token VARCHAR(255),
      IN p_hash VARCHAR(255),
      IN p_firstname VARCHAR(255),
      IN p_surname VARCHAR(255),
      IN p_dateOfBirth DATE,
      IN p_role VARCHAR(255)
    )
    BEGIN
        INSERT INTO accounts (`email`, `cardNumber`, `phone`, `token`, `hash`, `firstname`, `surname`, `dateOfBirth`, `role`)
        VALUES (p_email, CONCAT("Karta-", UUID()), p_phone, p_token, p_hash, p_firstname, p_surname, p_dateOfBirth, p_role);
    END //


CREATE PROCEDURE RefillWalletBalance(
      IN p_id INTEGER,
      IN p_amount INTEGER,
      IN p_establishmentId INTEGER
    )
    BEGIN
        DECLARE current_balance DECIMAL(10, 2);
    
        -- Select current wallet balance into a variable
        SELECT `walletBalance` INTO current_balance
        FROM accounts
        WHERE `accountId` = p_id;
    
        -- Insert into accounts_wallet_refills
        INSERT INTO accounts_wallet_refills (`accountId`, `amount`, `establishmentId`)
        VALUES (p_id, ROUND(p_amount, 0), p_establishmentId);
        
        -- Update the wallet balance using the variable
        UPDATE accounts
        SET `walletBalance` = current_balance + ROUND(p_amount, 0)
        WHERE `accountId` = p_id;
      
    END //


CREATE PROCEDURE RefundMoneyFromCanceledOrder(
      IN p_id INTEGER,
      IN p_amount INTEGER
    )
    BEGIN
        DECLARE current_balance DECIMAL(10, 2);
    
        -- Select current wallet balance into a variable
        SELECT `walletBalance` INTO current_balance
        FROM accounts
        WHERE `accountId` = p_id;
        
        -- Update the wallet balance using the variable
        UPDATE accounts
        SET `walletBalance` = current_balance + ROUND(p_amount, 0)
        WHERE `accountId` = p_id;
      
    END //



-- Procedure for checking if user with specified email exists
CREATE PROCEDURE CheckUserExists(
    IN p_email VARCHAR(255),
    OUT p_exists BOOLEAN
    )
    BEGIN
        SET p_exists = EXISTS(SELECT 1 FROM `accounts` WHERE `email` = p_email);
    END //



-- Procedure for authenticating user with specified email and password
CREATE PROCEDURE AuthUserPassword(
    IN p_email VARCHAR(255),
    IN p_hash VARCHAR(255),
    OUT p_auth BOOLEAN
    )
    BEGIN
        SET p_auth = EXISTS(SELECT 1 FROM `accounts` WHERE `email` = p_email and `hash` = p_hash);
    END //



-- Procedure for authenticating user with specified token
CREATE PROCEDURE AuthUserToken(
    IN p_token VARCHAR(255),
    OUT p_email VARCHAR(255)
    )
    BEGIN
        SET p_email = (SELECT email FROM `accounts` WHERE `token` = p_token);

        UPDATE `accounts`
        SET `lastTokenRefresh` = CURRENT_TIMESTAMP
        WHERE `token` = p_token;
    END //


-- Procedure that toggles menus's visibility
CREATE PROCEDURE ToggleAccountActive(
    IN p_id INTEGER
)
BEGIN
    UPDATE `accounts`
    SET `active` = CASE WHEN `active` = 0 THEN 1 ELSE 0 END
    WHERE `accountId` = p_id;
END //


-- Procedure for inserting new establishment
CREATE PROCEDURE InsertEstablishment(
    IN p_name VARCHAR(255),
    IN p_imagePath VARCHAR(255),
    IN p_address VARCHAR(255),
    IN p_wifi TINYINT,
    IN p_dineIn TINYINT,
    IN p_yard TINYINT,
    IN p_playground TINYINT,
    IN p_parking TINYINT,
    IN p_eCharger TINYINT,
    IN p_slug VARCHAR(255),
    IN p_token VARCHAR(255),
    OUT p_insertedID INTEGER
    )
    BEGIN
        INSERT INTO `establishments` (`name`, `imagePath`, `address`, `wifi`, `dineIn`, `yard`, `playground`, `parking`, `eCharger`, `slug`, `token`) 
        VALUES (p_name, p_imagePath, p_address, p_wifi, p_dineIn, p_yard, p_playground, p_parking, p_eCharger, p_slug, p_token);

        SET p_insertedID = (LAST_INSERT_ID());
    END //


-- Procedure for updating establisment and its image
CREATE PROCEDURE UpdateEstablishmentWithImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_imagePath VARCHAR(255),
    IN p_address VARCHAR(255),
    IN p_wifi TINYINT,
    IN p_dineIn TINYINT,
    IN p_yard TINYINT,
    IN p_playground TINYINT,
    IN p_parking TINYINT,
    IN p_eCharger TINYINT
    )
    BEGIN
        UPDATE `establishments`
        SET `name` = p_name, `imagePath` = p_imagePath, `address` = p_address, `wifi` = p_wifi, `dineIn` = p_dineIn, `yard` = p_yard, `playground` = p_playground, `parking` = p_parking, `eCharger` = p_eCharger 
        WHERE `establishmentId` = p_id;
    END //


-- Procedure for updating establisment without new image
CREATE PROCEDURE UpdateEstablishmentWithoutImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_address VARCHAR(255),
    IN p_wifi TINYINT,
    IN p_dineIn TINYINT,
    IN p_yard TINYINT,
    IN p_playground TINYINT,
    IN p_parking TINYINT,
    IN p_eCharger TINYINT
    )
    BEGIN
        UPDATE `establishments`
        SET `name` = p_name, `address` = p_address, `wifi` = p_wifi, `dineIn` = p_dineIn, `yard` = p_yard, `playground` = p_playground, `parking` = p_parking, `eCharger` = p_eCharger 
        WHERE `establishmentId` = p_id;
    END //


-- Procedure that toggles establishment's visibility
CREATE PROCEDURE ToggleEstablishmentShow(
    IN p_id INTEGER
    )
    BEGIN
        UPDATE `establishments`
        SET `show` = CASE WHEN `show` = 0 THEN 1 ELSE 0 END
        WHERE `establishmentId` = p_id;
    END //


-- Procedure for authentization the KitchenHub server
CREATE PROCEDURE AuthEstablishmentToken(
    IN p_slug VARCHAR(255),
    IN p_token VARCHAR(255),
    OUT p_establishmentId INTEGER
    )
    BEGIN
        SET p_establishmentId = (SELECT establishmentId FROM `establishments` WHERE `token` = p_token and `slug` = p_slug);
    END //


-- Procedure for inserting new product
CREATE PROCEDURE InsertProduct(
    IN p_name VARCHAR(255),
    IN p_description text,
    IN p_price FLOAT,
    IN p_preparationTime TIME,
    IN p_imagePath VARCHAR(255),
    OUT p_insertedID INTEGER
)
BEGIN
    INSERT INTO `products` (`name`, `description`, `price`, `preparationTime`, `imagePath`)
    VALUES (p_name, p_description, p_price, p_preparationTime, p_imagePath);

    SET p_insertedID = (LAST_INSERT_ID());
END //


-- Procedure for updating product and its image
CREATE PROCEDURE UpdateProductWithImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_description TEXT,
    IN p_price FLOAT,
    IN p_preparationTime TIME,
    IN p_imagePath VARCHAR(255)
)
BEGIN
    UPDATE `products`
    SET `name` = p_name, `description` = p_description, `price` = p_price, `preparationTime` = p_preparationTime, `imagePath` = p_imagePath
    WHERE `productId` = p_id;
END //


-- Procedure for updating product without an image
CREATE PROCEDURE UpdateProductWithoutImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_description TEXT,
    IN p_price FLOAT,
    IN p_preparationTime TIME
)
BEGIN
    UPDATE `products`
    SET `name` = p_name, `description` = p_description, `price` = p_price, `preparationTime` = p_preparationTime
    WHERE `productId` = p_id;
END //


-- Procedure that toggles product's visibility
CREATE PROCEDURE ToggleProductShow(
    IN p_id INTEGER
)
BEGIN
    UPDATE `products`
    SET `show` = CASE WHEN `show` = 0 THEN 1 ELSE 0 END
    WHERE `productId` = p_id;
END //


-- Procedure that creates new menu
CREATE PROCEDURE InsertMenu(
    IN p_name VARCHAR(255),
    IN p_note TEXT,
    IN p_description TEXT,
    IN p_imagePath VARCHAR(255),
    OUT p_insertedID INTEGER
)
BEGIN
    INSERT INTO `menus` (`name`, `note`, `description`, `imagePath`)
    VALUES (p_name, p_note, p_description, p_imagePath);

    SET p_insertedID = (LAST_INSERT_ID());
END //


-- Procedure for updating menu and its image
CREATE PROCEDURE UpdateMenuWithImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_note TEXT,
    IN p_description TEXT,
    IN p_imagePath VARCHAR(255)
)
BEGIN
    UPDATE `menus`
    SET `name` = p_name, `note` = p_note, `description` = p_description, `imagePath` = p_imagePath
    WHERE `menuId` = p_id;
END //


-- Procedure for updating menu without an image
CREATE PROCEDURE UpdateMenuWithoutImage(
    IN p_id INTEGER,
    IN p_name VARCHAR(255),
    IN p_note TEXT,
    IN p_description TEXT
)
BEGIN
    UPDATE `menus`
    SET `name` = p_name, `note` = p_note, `description` = p_description
    WHERE `menuId` = p_id;
END //


-- Procedure that toggles menus's visibility
CREATE PROCEDURE ToggleMenuShow(
    IN p_id INTEGER
)
BEGIN
    UPDATE `menus`
    SET `show` = CASE WHEN `show` = 0 THEN 1 ELSE 0 END
    WHERE `menuId` = p_id;
END //


-- Procedure that creates a new order
CREATE PROCEDURE InsertOrder(
    IN p_accountId INTEGER,
    IN p_establishmentId INTEGER,
    IN p_paymentType VARCHAR(255),
    IN p_pickupTime TIMESTAMP,
    OUT p_insertedID INTEGER
)
BEGIN
    INSERT INTO `orders` (`accountId`, `establishmentId`, `paymentType`, `pickupTime`)
    VALUES (p_accountId, p_establishmentId, p_paymentType, p_pickupTime);

    SET p_insertedID = (LAST_INSERT_ID());
END //


-- Procedure that adds product to an order
CREATE PROCEDURE InsertOrderProduct(
    IN p_orderId INTEGER,
    IN p_productId INTEGER,
    IN p_quantity INTEGER,
    IN p_price FLOAT
)
BEGIN
    INSERT INTO `orders_products` (`orderId`, `productId`, `quantity`, `price`)
    VALUES (p_orderId, p_productId, p_quantity, p_price);
END //


-- Procedure that toggles order's status
CREATE PROCEDURE ToggleOrderStatus(
    IN p_id INTEGER
)
BEGIN
    UPDATE `orders`
    SET `status` = CASE 
        WHEN `status` = "CREATED" THEN "PROCESSING"
        WHEN `status` = "PROCESSING" THEN "READY"
        WHEN `status` = "READY" THEN "DONE"
        WHEN `status` = "DONE" THEN "DONE"
        ELSE "UNKNOWN" END,
        `lastUpdate` =  CURRENT_TIMESTAMP
    WHERE `orderId` = p_id;
END //


-- Procedure that updates order's status
CREATE PROCEDURE UpdateOrderStatus(
    IN p_id INTEGER,
    IN p_status VARCHAR(255)
)
BEGIN
    IF p_status = 'DONE' or p_status = "CANCELED" THEN
        UPDATE `orders`
        SET `status` = p_status,
            `tag` = NULL,
            `lastUpdate` = CURRENT_TIMESTAMP
        WHERE `orderId` = p_id;
    ELSE
        UPDATE `orders`
        SET `status` = p_status,
            `lastUpdate` = CURRENT_TIMESTAMP
        WHERE `orderId` = p_id;
    END IF;
END //


-- Procedure that cancels an order
CREATE PROCEDURE CancelOrder(
    IN p_id INTEGER
)
BEGIN
    UPDATE `orders`
    SET `status` = 'CANCELED',
    `lastUpdate` =  CURRENT_TIMESTAMP
    WHERE `orderId` = p_id;
END //


-- Procedure that updates the column when the order is sent to KitchenHub
CREATE PROCEDURE SocketSentOrder(
    IN p_id INTEGER
)
BEGIN
    UPDATE `orders`
    SET `socketSent` = '1'
    WHERE `orderId` = p_id;
END