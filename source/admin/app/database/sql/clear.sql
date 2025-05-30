/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

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
DROP TABLE IF EXISTS `accounts_wallet_refills`;
DROP TABLE IF EXISTS `stats_daily_overall`;
DROP TABLE IF EXISTS `stats_daily_establishments`;


-- Delete statements for procedures
DROP PROCEDURE IF EXISTS InsertAccount;
DROP PROCEDURE IF EXISTS RefillWalletBalance;
DROP PROCEDURE IF EXISTS RefundMoneyFromCanceledOrder;
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
DROP PROCEDURE IF EXISTS SocketSentOrder;

DROP PROCEDURE IF EXISTS stats_insertDailyStatsOverall;
DROP PROCEDURE IF EXISTS stats_insertDailyStatsEstablishmentsCall;
DROP PROCEDURE IF EXISTS stats_insertDailyStatsEstablishments;

DROP EVENT IF EXISTS event_insertDailyStatsOverall_today;
DROP EVENT IF EXISTS event_insertDailyStatsEstablishments_today;
DROP EVENT IF EXISTS event_insertDailyStatsOverall_previousDay;
DROP EVENT IF EXISTS event_insertDailyStatsEstablishments_previousDay