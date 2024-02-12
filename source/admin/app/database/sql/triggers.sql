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
-- TRIGGERS
--


CREATE TRIGGER setOrderTag
BEFORE INSERT ON orders FOR EACH ROW
BEGIN
    DECLARE prev_tag INT;

    -- Find the tag of the row before the new one
    SELECT COALESCE(tag, 0) INTO prev_tag
    FROM orders
    WHERE establishmentId = NEW.establishmentId AND createdTime <= NEW.createdTime
    ORDER BY createdTime DESC
    LIMIT 1;

    -- Set the tag for the new row based on the tag of the row before
    SET NEW.tag = (prev_tag + 1) % 1000;
    IF NEW.tag = 0 THEN
        SET NEW.tag = 1;
    END IF;
    
    IF prev_tag IS NULL THEN
        SET NEW.tag = 1;
    END IF;
END