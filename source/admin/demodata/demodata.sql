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


-- Products 
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(1, 'Hamburger Classic', 'Šťavnatý hovězí burger s čerstvou zeleninou, sýrem a klasickou omáčkou.', 99.9, '00:10:00', '/files/storage/images/products/k2RgTKgQ0l.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(2, 'Kuřecí Wrap Tex-Mex', 'Grilované kuřecí kousky, zelenina, sýr a pikantní omáčka zabalené v tortille.', 89.9, '00:12:00', '/files/storage/images/products/oouMZ6Ahtb.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(3, 'Ryba & Hranolky', 'Křupavá ryba s domácími hranolkami, podávaná s citronovým dipem.', 119.9, '00:15:00', '/files/storage/images/products/2g27t4mXk7.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(4, 'Smažený Sýr v Housce', 'Křupavý smažený sýr podávaný s tatarskou omáčkou.', 79.0, '00:08:00', '/files/storage/images/products/AAAOVS6w4x.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(5, 'Řízek v Housce', 'Klasický řízek v housce s čerstvou zeleninou a majonézou.', 109.9, '00:12:00', '/files/storage/images/products/WALf6nlMpQ.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(6, 'Coca Cola 0,5L', 'Osvěžující klasická cola.', 45.9, '00:00:30', '/files/storage/images/products/iPOgyrUHFd.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(7, 'Pilsner Urquell 0,5L', 'Lahodná, studená, česká klasika.', 59.9, '00:00:30', '/files/storage/images/products/NofegypAUO.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(8, 'Natura Neperlivá 0,33L', 'Čistá voda z horského pramene.', 35.9, '00:00:30', '/files/storage/images/products/eD1egvynKL.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(9, 'Natura Neperlivá 0,5L', 'Čistá voda z horského pramene.', 55.9, '00:00:30', '/files/storage/images/products/VRlBNdSjnh.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(10, 'Citronový Čaj Lipton', 'Čerstvě uvařený čaj s citronem a medem.', 39.9, '00:03:30', '/files/storage/images/products/jSZLvCNo9L.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(11, 'Jahodový Cheesecake', 'Lahodný cheesecake s vrstvou čerstvých jahodových plátků.', 79.9, '00:08:00', '/files/storage/images/products/3x2X6QLMOD.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(12, 'Belgický Waffle s Čokoládou', 'Křehké belgické waffle s horkou tekutou čokoládou a šlehačkou.', 89.9, '00:10:00', '/files/storage/images/products/pyBjC8C9a5.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(13, 'Cappuccino', 'Italský nápoj z espressa, horkého mléka a mléčné pěny, spojených do harmonického blendu s bohatou kávovou chutí a jemnou texturou.', 45.9, '00:03:00', '/files/storage/images/products/dt77fA60Qb.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(14, 'Smažené Cibulové Kroužky', 'Křupavé smažené kroužky cibule, podávané s pikantní omáčkou.', 49.9, '00:08:00', '/files/storage/images/products/U8Ggyvi5dB.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(15, 'Domácí Hranolky', 'Křupavé domácí hranolky s kečupem.', 49.9, '00:06:00', '/files/storage/images/products/LLfeIWxrOZ.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(16, 'Kečup', 'Porce kečupu navíc.', 15.9, '00:00:30', '/files/storage/images/products/dKr8IrTSMh.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(17, 'BBQ Omáčka', 'Porce BBQ omáčky navíc', 15.9, '00:00:30', '/files/storage/images/products/V0YVOJyO15.png', 1);
INSERT INTO kOkenku.products (productId, name, description, price, preparationTime, imagePath, `show`) VALUES(18, 'Česneková Omáčka', 'Porce česnekové omáčky navíc.', 15.9, '00:00:30', '/files/storage/images/products/jXFSXRWixn.png', 1);


-- Menus Products
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(1, 5);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(1, 4);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(1, 3);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(1, 2);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(1, 1);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(2, 9);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(2, 8);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(2, 7);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(2, 6);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(3, 13);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(3, 10);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(4, 12);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(4, 11);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(5, 15);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(5, 14);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(6, 18);
INSERT INTO kOkenku.menus_products (menuId, productId) VALUES(6, 17);


-- Menus
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(1, 'Hlavní Pokrmy', '[Demodata] Všechna hlavní jídla', 'Rozmanitá nabídka oblíbených fastfoodových specialit, včetně chutných hamburgerů a dalších hlavních pochoutek.', '/files/storage/images/menus/EOLQwwmtFe.png', 1);
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(2, 'Studené Nápoje', '[Demodata] Všechny studené nápoje', 'Osvěžující nápoje, ideální pro zahnání žízně a osvěžení.', '/files/storage/images/menus/s88sGLSBsb.png', 1);
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(3, 'Teplé Nápoje', '[Demodata] Všechny teplé nápoje', 'Lahodné horké nápoje, které dodají energii a potěší chuťové buňky.', '/files/storage/images/menus/8jL4CteSEl.png', 1);
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(4, 'Dezerty', '[Demodata] Všechna sladká jídla', 'Sladké pochoutky, včetně šťavnatých dortů, chutných wafflí a dalších lahodných dobrot.', '/files/storage/images/menus/mrl6FTvjow.png', 1);
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(5, 'Přílohy', '[Demodata] Všechny přílohy', 'Skvělé doplňky k hlavním jídlům, nebo jen tak na chuť.', '/files/storage/images/menus/3gjD6rCqqI.png', 1);
INSERT INTO kOkenku.menus (menuId, name, note, description, imagePath, `show`) VALUES(6, 'Omáčky', '[Demodata] Všechny omáčky', 'Rozmanité omáčky, které doplní každý pokrm, aby každé sousto získalo perfektní chuťový doplněk.', '/files/storage/images/menus/80AHbAh4JQ.png', 1);

-- Menus Establishments
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 1);
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 2);
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 3);
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 4);
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 5);
INSERT INTO kOkenku.establishments_menus (establishmentId, menuId) VALUES(1, 6);

-- Establishments
INSERT INTO kOkenku.establishments (establishmentId, name, imagePath, address, wifi, dineIn, yard, playground, parking, eCharger, `show`, slug, token) VALUES(1, 'Gymnázium Sokolov', '/files/storage/images/establishments/4WbK0x8FyT.png', 'Husitská 2053, Sokolov', 1, 1, 1, 0, 0, 0, 1, 'GymnziumSokolov-3luYyu4nqL', 'EST-Gymn-scre-tEGm-mfOX-ETAk');

-- Establishments Opening Hours
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 1, '09:00:00', '22:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 2, '09:00:00', '16:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 3, '09:00:00', '16:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 4, '09:00:00', '16:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 5, '09:00:00', '16:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 6, '09:00:00', '16:00:00');
INSERT INTO kOkenku.establishments_openinghours (establishmentId, dayOfTheWeek, openingTime, closingTime) VALUES(1, 7, '09:00:00', '16:00:00');
