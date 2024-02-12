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
-- Triggers
--

-- Trigger that deletes all DONE orders when new order is inserted

CREATE TRIGGER deleteOrders
AFTER INSERT ON orders
BEGIN
    DELETE FROM orders WHERE status IN ('DONE', 'CANCELED') 
    AND (SELECT COUNT(*) FROM orders WHERE status IN ('DONE', 'CANCELED')) > 100;
END //
