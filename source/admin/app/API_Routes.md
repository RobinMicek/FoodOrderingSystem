# /api/login

Returns the account API Bearer token.  

```
POST /api/login HTTP/1.1
Host: [host]
Content-Type: application/json
User-Agent: [user-agent]
Content-Length: [length]

{
    "email": "[email value]",
    "password": "[password value]"
}
```

## Responses

### 200:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "token": "[user token]"
}
```

### 401
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "message": "Login denied!"
}
```




# /api/register

Creates new account.

```
POST /api/register HTTP/1.1
Host: [host]
Content-Type: application/json
User-Agent: [user-agent]
Content-Length: [length]

{
    "email": "[email value]",
    "phone": "[phone value]",
    "password": "[password value]",
    "firstname": "[firstname value]",
    "surname": "[surname value]",
    "dateOfBirth": "[dateOfBirth value]"
}
```

## Responses

### 200:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": true
}
```

### 400
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "status": false
}

------------------------------

HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "status": 0 (Email already exists)
}
```




# /api/get-all-establishments

Returns info about all establishments.

```
GET /get-all-establishments HTTP/1.1
Host: [host]
User-Agent: [user-agent]
Authorization: Bearer [token]
```

## Responses

### 200:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": [
    {
      "address": "Dvořákovy sady 22, Karlovy Vary, 360 01, Czech Republic",
      "dineIn": 1,
      "eCharger": 0,
      "establishmentId": 1,
      "imagePath": "/files/storage/images/establishments/iaxAIfwtSb.png",
      "isOpen": {
        "closingTime": "00:00",
        "isOpen": false,
        "openingTime": "00:00"
      },
      "name": "PopUp Bistro | FoodFest Karlovy Vary 2024",
      "parking": 1,
      "playground": 0,
      "show": 1,
      "wifi": 1,
      "yard": 1
    }
  ]
}
```

### 401
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "status": 401,
    "message": "Valid user token required!"
}
```




# /api/get-establishment?establishmentId=[establishmentId]

Returns info about a specified establishment.

```
GET /get-establishment?establishmentId=[establishmentId] HTTP/1.1
Host: [host]
User-Agent: [user-agent]
Authorization: Bearer [token]
```

## Responses

### 200:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "address": "Dvořákovy sady 22, Karlovy Vary, 360 01, Czech Republic",
    "dineIn": 1,
    "eCharger": 0,
    "establishmentId": 1,
    "imagePath": "/files/storage/images/establishments/iaxAIfwtSb.png",
    "isOpen": {
      "closingTime": "00:00",
      "isOpen": false,
      "openingTime": "00:00"
    },
    "menus": [
      {
        "description": " ",
        "establishmentId": 1,
        "imagePath": "/files/storage/images/menus/cXqrXGhTEi.png",
        "menuId": 1,
        "name": "Teplá Jídla",
        "note": "Stálá nabídka",
        "show": 1
      }
    ],
    "name": "PopUp Bistro | FoodFest Karlovy Vary 2024",
    "parking": 1,
    "playground": 0,
    "show": 1,
    "wifi": 1,
    "yard": 1
  }
}
```

### 404
```
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "message": "Could not find the establishment!"
}
```

### 401
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "status": 401,
    "message": "Valid user token required!"
}
```




# /api/get-menu?menuId=[menuId]

Returns info about a specified menu.

```
GET /get-menu?menuId=[menuId] HTTP/1.1
Host: [host]
User-Agent: [user-agent]
Authorization: Bearer [token]
```

## Responses

### 200:
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": {
    "description": " ",
    "imagePath": "/files/storage/images/menus/cXqrXGhTEi.png",
    "menuId": 1,
    "name": "Teplá Jídla",
    "note": "Stálá nabídka",
    "products": [
      {
        "description": "Gulášová polévka z hovězího masa s cibulí, paprikou a kořením je krémová a pikantní. Podáváme ji s čerstvým chlebem.",
        "imagePath": "/files/storage/images/products/LjK7RsNEle.png",
        "menuId": 1,
        "name": "Gulášová polévka",
        "preparationTime": "00:03:30",
        "price": 45.99,
        "productId": 1,
        "show": 1
      }
    ],
    "show": 1
  }
}
```

### 404
```
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "message": "Could not find the menu!"
}
```

### 401
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "status": 401,
    "message": "Valid user token required!"
}
```
```




# /api/create-order

Creates new order.

```
POST /create-order HTTP/1.1
Host: [host]
Content-Type: application/json
User-Agent: [user-agent]
Authorization: Bearer [token]
Content-Length: [length]

{
    "establishmentId": [establishmentId],
    "pickupTime": "[pickupTime]",
    "products": [
        {
            "productId": [productId1],
            "quantity": [quantity1]
        },
        {
            "productId": [productId2],
            "quantity": [quantity2]
        },
        ...
    ]
}
```

## Responses

### 200:
```HTTP/1.1 200 OK
Content-Type: application/json

{
    "data": {
        "orderId": "[orderId]"
    }
}
```

### 400
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "message": "Could not create new order!"
}
```

### 401
```
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
    "status": 401,
    "message": "Valid user token required!"
}
```