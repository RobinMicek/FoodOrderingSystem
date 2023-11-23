INSERT INTO accounts
(accountId, email, phone, token, hash, firstname, surname, since, dateOfBirth, active, `role`, lastInteraction)
VALUES(1, 'micek.robin@gmail.com', '+420123456789', 'Bearer 6438c0b66ecc2b9255706bc556b94d2a5cbbf563819a44345a8ff8e484037eaa', 'dfd72cdf33fe9e247969200e161b338eaae8529d16b4c3f1bce289b45d07fd5d', 'Robin', 'Míček', '2023-09-22 15:03:21', '1997-12-15', 1, 'admin', '2023-10-06 14:12:25');

INSERT INTO establishments
(establishmentId, name, imagePath, address, wifi, dineIn, yard, playground, parking, eCharger, `show`, slug, token)
VALUES(1, 'Restaurant u Gymnázia', '/files/storage/images/establishments/MmiI6ek7i4.png', 'Dvořákovy sady 22, Karlovy Vary, 360 01, Czech Republic', 0, 1, 0, 0, 1, 0, 1, 'RestaurantuGymnzia-FpB7o0hLnc', 'EST-Rest-2Y6J-gvjF-Ljv8-OHOX');
INSERT INTO establishments
(establishmentId, name, imagePath, address, wifi, dineIn, yard, playground, parking, eCharger, `show`, slug, token)
VALUES(2, 'PopUp Bistro | FoodFest Karlovy Vary 2024', '/files/storage/images/establishments/8xUGHGH1Lo.png', 'nam.dr.Horákové 9, Karlovy Vary, 360 01', 0, 1, 0, 0, 0, 0, 1, 'PopUpBistroFoodFestKarlovyVary2024-EuAc6aknVu', 'EST-PopU-ZhAr-t3ps-pOuv-Ia4M');

INSERT INTO establishments_menus
(establishmentId, menuId)
VALUES(1, 1);
INSERT INTO establishments_menus
(establishmentId, menuId)
VALUES(1, 2);
INSERT INTO establishments_menus
(establishmentId, menuId)
VALUES(2, 2);

INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 1, '08:00:00', '22:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 2, '11:00:00', '22:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 3, '11:00:00', '23:59:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 4, '11:00:00', '22:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 5, '11:00:00', '23:59:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 6, '11:00:00', '23:59:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(1, 7, '11:00:00', '23:59:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 1, '17:00:00', '18:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 2, '06:00:00', '23:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 3, '00:00:00', '00:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 4, '00:00:00', '00:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 5, '00:00:00', '00:00:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 6, '10:00:00', '23:59:00');
INSERT INTO establishments_openinghours
(establishmentId, dayOfTheWeek, openingTime, closingTime)
VALUES(2, 7, '10:00:00', '13:37:00');

INSERT INTO menus
(menuId, name, note, description, imagePath, `show`)
VALUES(1, 'Zeleninová Jídla', 'Stálá nabídka', 'Zeleninová jídla, stejně jako masová, najdeme napříč lidskou historií a jsou oblíbená i v dnešní době. ', '/files/storage/images/menus/ZKivuHGsUN.png', 1);
INSERT INTO menus
(menuId, name, note, description, imagePath, `show`)
VALUES(2, 'Měsíční Speciality', 'Září 2023', 'Speciality našich kuchařů, které si pro vás připravili pouze pro tento měsíc.', '/files/storage/images/menus/l2mIx9ly7b.png', 1);

INSERT INTO menus_products
(menuId, productId)
VALUES(1, 8);
INSERT INTO menus_products
(menuId, productId)
VALUES(1, 6);
INSERT INTO menus_products
(menuId, productId)
VALUES(1, 5);
INSERT INTO menus_products
(menuId, productId)
VALUES(2, 7);
INSERT INTO menus_products
(menuId, productId)
VALUES(2, 4);
INSERT INTO menus_products
(menuId, productId)
VALUES(2, 2);
INSERT INTO menus_products
(menuId, productId)
VALUES(2, 1);
INSERT INTO menus_products
(menuId, productId)
VALUES(2, 3);

INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(1, 'Těstoviny se špenátem a rajčaty', 'Klasické italské těstoviny podávané se špenátem, čerstvými rajčaty, olivovým olejem a parmazánem. Doba vaření je orientační a závisí na druhu těstovin.', 32.75, '00:05:00', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(2, 'Grilovaný losos s dýní', 'Grilovaný losos s medovou glazurou podávaný s dušenou dýní a čerstvými bylinkami. Skvělé jídlo plné omega-3 mastných kyselin.', 79.9, '00:06:20', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(3, 'Rýže s kořeněnými fazolemi', 'Jasmínová rýže s dochucenými fazolemi, česnekem a koriandrem. Skvělý veganský pokrm plný bílkovin a vlákniny.', 38.25, '00:03:45', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(4, 'Hovězí burger s hranolkami', 'Lahodný hovězí burger s cheddarem, karamelizovanou cibulkou a majonézou. Podáváme s křupavými hranolkami a kečupem.', 69.99, '00:07:10', '/files/storage/images/products/tu3R4jxA8i.png', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(5, 'Vegetariánská pizza s artyčoky', 'Klasická pizza s rajčatovým základem, sýrem, olivami, artyčoky a špenátem. Ideální pro milovníky zeleniny.', 45.5, '00:08:30', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(6, 'Kuřecí nudličky na hrášku', 'Kuřecí nudličky podávané s hráškem, mrkví, cibulí a sójovou omáčkou.', 54.25, '00:05:50', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(7, 'Lososový steak s bylinkovým máslem', 'Grilovaný lososový steak s bylinkovým máslem podávaný s restovanými bramborami a cherry rajčaty.', 78.9, '00:06:40', '/files/storage/images/products/placeholder.jpg', 1);
INSERT INTO products
(productId, name, description, price, preparationTime, imagePath, `show`)
VALUES(8, 'Květákové karbanátky', 'Květákové karbanátky podávané s bramborovou kaší a čerstvou zeleninovou oblohou.', 36.75, '00:07:20', '/files/storage/images/products/placeholder.jpg', 1);
