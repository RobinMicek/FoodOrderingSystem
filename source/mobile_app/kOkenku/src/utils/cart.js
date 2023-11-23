import { getObject, setObject } from "@/utils/storage.js";

export class CartObject {
    constructor(establishmentId) {
        this.establishmentId = establishmentId
    }

    async getCart() {
        const storedCart = await getObject("cart")
        const storedCartParsed = JSON.parse(storedCart)

        if (!storedCartParsed || !storedCartParsed.establishmentId || storedCartParsed.establishmentId !== this.establishmentId) {            
            // Cart doesn't exist in storage, or establishmentId doesn't match, set it to an empty cart
            this.cart = {
                establishmentId: this.establishmentId,
                products: []
            }
            await setObject("cart", JSON.stringify(this.cart))

        } else {
            // Cart exists in storage, parse and set it
            this.cart = JSON.parse(storedCart)
        }

        return this.cart
    }

    async addItem(product) {
        await this.getCart()

        const existingProduct = this.cart.products.find((existing) => existing.productId === product.productId)

        if (existingProduct) {
            existingProduct.quantity += 1
        } else {
            product.quantity = 1
            this.cart.products.push(product)
        }

        await setObject("cart", JSON.stringify(this.cart))
    
    }


    async removeItem (productId) {
        await this.getCart()

        this.cart.products = this.cart.products.filter(product => product.productId !== productId);

        await setObject("cart", JSON.stringify(this.cart))
    }

    async getStats () {
        await this.getCart()

        let price = 0
        let numberOfProducts = 0

        if (this.cart.products.length != 0){
            for (var i = 0; i < this.cart.products.length; i++) {
                price += this.cart.products[i].price * this.cart.products[i].quantity
                numberOfProducts += this.cart.products[i].quantity
            }
        }

        return {
            "price": price.toFixed(2),
            "numberOfProducts": numberOfProducts
        }
    }

    async cleanCart () {
        this.cart = {
            establishmentId: this.establishmentId,
            products: []
        }
        await setObject("cart", JSON.stringify(this.cart))
    }
}
