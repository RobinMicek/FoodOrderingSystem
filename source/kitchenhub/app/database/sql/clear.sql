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
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `orders_products`;
DROP TABLE IF EXISTS `app_configuration`;


-- Drop triggers if they exist
DROP TRIGGER IF EXISTS `deleteDoneOrders`;