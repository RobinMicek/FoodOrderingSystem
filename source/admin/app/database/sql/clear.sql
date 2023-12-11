/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

    Jakákoliv úprava a distribuce tohoto kódu 
    bez povolení autora je zakázána!

    © Robin Míček 2023 - 2024

********************************************************
*/


-- Drop tables if they exist
DROP TABLE IF EXISTS `establishments_openinghours`;
DROP TABLE IF EXISTS `establishments_menus`;
DROP TABLE IF EXISTS `establishments`;
DROP TABLE IF EXISTS `menus`;
DROP TABLE IF EXISTS `menus_products`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `orders_products`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `accounts`;


-- Delete statements for procedures
DROP PROCEDURE IF EXISTS InsertAccount;
DROP PROCEDURE IF EXISTS CheckUserExists;
DROP PROCEDURE IF EXISTS AuthUserPassword;
DROP PROCEDURE IF EXISTS AuthUserToken;
DROP PROCEDURE IF EXISTS ToggleAccountActive;
DROP PROCEDURE IF EXISTS InsertEstablishment;
DROP PROCEDURE IF EXISTS UpdateEstablishmentWithImage;
DROP PROCEDURE IF EXISTS UpdateEstablishmentWithoutImage;
DROP PROCEDURE IF EXISTS ToggleEstablishmentShow;
DROP PROCEDURE IF EXISTS AuthEstablishmentToken;
DROP PROCEDURE IF EXISTS InsertProduct;
DROP PROCEDURE IF EXISTS UpdateProductWithImage;
DROP PROCEDURE IF EXISTS UpdateProductWithoutImage;
DROP PROCEDURE IF EXISTS ToggleProductShow;
DROP PROCEDURE IF EXISTS InsertMenu;
DROP PROCEDURE IF EXISTS UpdateMenuWithImage;
DROP PROCEDURE IF EXISTS UpdateMenuWithoutImage;
DROP PROCEDURE IF EXISTS ToggleMenuShow;
DROP PROCEDURE IF EXISTS InsertOrder;
DROP PROCEDURE IF EXISTS InsertOrderProduct;
DROP PROCEDURE IF EXISTS ToggleOrderStatus;
DROP PROCEDURE IF EXISTS UpdateOrderStatus;
DROP PROCEDURE IF EXISTS CancelOrder;
DROP PROCEDURE IF EXISTS SocketSentOrder
