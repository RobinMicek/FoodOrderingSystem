/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


GRANT CREATE, DROP, ALTER, SUPER
ON *.*
TO 'kOkenkuBackEnd'@'%';

GRANT SELECT, INSERT, UPDATE, DELETE, INDEX, CREATE ROUTINE
ON kOkenku.*
TO 'kOkenkuBackEnd'@'%';

FLUSH PRIVILEGES;