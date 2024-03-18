/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


async function loadDatabase() {
  const db = await idb.openDB("kOkenkuPOSDB", 1, {
    upgrade(db, oldVersion, newVersion, transaction) {
      db.createObjectStore("products", {
        keyPath: "productId",
      })
    },
  })

  return {
    db,
    deleteAll: async () => (await db.getAll("products")).map(product => db.delete("products", product.productId)),
    getProducts: async () => await db.getAll("products"),
    addProduct: async (product) => await db.add("products", product),
    editProduct: async (product) => await db.put("products", product),
    deleteProduct: async (product) => await db.delete("products", product.productId),
  };
}

function initApp() {
  const app = {
    db: null,
    time: null,
    firstTime: localStorage.getItem("first_time") === null,
    activeMenu: 'pos',
    loadingSampleData: false,
    moneys: [1, 2, 5, 10, 20, 50, 100, 200, 500, 500, 1000, 2000, 5000],
    products: [],
    keyword: "",
    cart: [],
    cash: 0,
    change: 0,
    isShowModalReceipt: false,
    receiptNo: null,
    receiptDate: null,
    orderTag: null,
    allEstablishments: [],
    establishmentId: parseInt(localStorage.getItem("establishmentId")),
    establishmentName: localStorage.getItem("establishmentName"),
    receiptPrefix: localStorage.getItem("receiptPrefix"),
    companyName: localStorage.getItem("companyName"),


    async factoryReset() {
      localStorage.clear();
      await this.db.deleteAll()
      location.reload()
    },


    async firstTimeSetup() {
      this.allEstablishments = await new serverRequests().getAllEstablishments()
    },


    async updateVariables(establishmentId, establishmentName, establishmentSlug) {
      this.establishmentId = parseInt(establishmentId)
      localStorage.setItem("establishmentId", this.establishmentId)

      this.establishmentName = establishmentName
      localStorage.setItem("establishmentName", this.establishmentName)
      
      this.receiptPrefix = (`${(establishmentSlug.split('-')[0]).slice(0, 2)}${(establishmentSlug.split('-')[0]).slice(-2)}`).toUpperCase()
      localStorage.setItem("receiptPrefix", this.receiptPrefix)

      this.companyName = (await getConfiguration()).companyInfo.companyName
      localStorage.setItem("companyName", this.companyName)
      
    },


    async initDatabase() {
      this.db = await loadDatabase()
      this.loadProducts()
    },


    async loadProducts() {
      this.products = await this.db.getProducts()
    },


    async storeDataFromApi() {
      try {
        await this.db.deleteAll()

        const serverRequest = new serverRequests()
        this.products = await serverRequest.getAllProducts(this.establishmentId)
        
        for (let product of this.products) {
          product = JSON.parse(JSON.stringify(product))
          await this.db.addProduct(product)
        }

        this.setFirstTime(false)
      } catch (error) {
        console.log(error)
        alert("Něco se pokazilo! Zkuste to prosím znovu.")
      }
      
    },


    setFirstTime(firstTime) {
      this.firstTime = firstTime
      if (firstTime) {
        localStorage.removeItem("first_time")
      } else {
        localStorage.setItem("first_time", new Date().getTime())
      }
    },
    

    filteredProducts() {
      const rg = this.keyword ? new RegExp(this.keyword, "gi") : null
      return this.products.filter((p) => !rg || p.name.match(rg))
    },


    addToCart(product) {
      const index = this.findCartIndex(product)
      if (index === -1) {
        this.cart.push({
          productId: product.productId,
          image: product.imagePath,
          name: product.name,
          price: product.price,
          preparationTime: product.preparationTime,
          qty: 1,
        });
      } else {
        this.cart[index].qty += 1
      }
      this.beep()
      this.updateChange()
    },


    findCartIndex(product) {
      return this.cart.findIndex((p) => p.productId === product.productId)
    },
    

    addQty(item, qty) {
      const index = this.cart.findIndex((i) => i.productId === item.productId)
      if (index === -1) {
        return;
      }
      const afterAdd = item.qty + qty
      if (afterAdd === 0) {
        this.cart.splice(index, 1)
        this.clearSound();
      } else {
        this.cart[index].qty = afterAdd
        this.beep();
      }
      this.updateChange()
    },


    addCash(amount) {      
      this.cash = (this.cash || 0) + amount
      this.updateChange()
      this.beep()
    },
    
    
    getItemsCount() {
      return this.cart.reduce((count, item) => count + item.qty, 0)
    },
    
    
    updateChange() {
      this.change = this.cash - this.getTotalPrice()
    },
    
    
    updateCash(value) {
      this.cash = parseFloat(value.replace(/[^0-9]+/g, ""))
      this.updateChange()
    },
    
    
    getTotalPrice() {
      return this.cart.reduce(
        (total, item) => total + item.qty * item.price,
        0
      );
    },
    
    
    submitable() {
      return this.change >= 0 && this.cart.length > 0
    },
    
    
    async submit() {
      const serverRequest = new serverRequests()
      const order = await serverRequest.completeOrder(this.cart, this.establishmentId)

      if (order != false) {
        this.orderTag = `#${order.tag}`
        const time = new Date()
        this.isShowModalReceipt = true
        this.receiptNo = `${this.receiptPrefix}-${order.orderId}`
        this.receiptDate = this.dateFormat(time)
      }
      else {
        alert("Něco se pokazilo! Zkuste to prosím znovu...")
      }     
      
    },
    
    
    closeModalReceipt() {
      this.isShowModalReceipt = false
    },
    
    
    dateFormat(date) {
      const formatter = new Intl.DateTimeFormat('id', { dateStyle: 'short', timeStyle: 'short'})
      return formatter.format(date)
    },
    
    
    numberFormat(number, round = false) {
      if (isNaN(number) || number === null) {
        return "";
      }
    
      const roundedNumber = round ? parseFloat(number).toFixed(0) : parseFloat(number).toFixed(2)
    
      const [integerPart, decimalPart] = roundedNumber.split(".")
    
      const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",")
      const result = decimalPart ? `${formattedIntegerPart}.${decimalPart}` : formattedIntegerPart
    
      return result
    },
        
    
    priceFormat(number, round = false) {
      return number ? `${this.numberFormat(number, round)} Kč` : `0 Kč`
    },
    
    
    clear() {
      this.cash = 0
      this.cart = []
      this.orderTag = null
      this.receiptNo = null
      this.receiptDate = null
      this.updateChange()
      this.clearSound()
    },
    
    
    beep() {
      this.playSound("sound/beep-29.mp3")
    },
    
    
    clearSound() {
      this.playSound("sound/button-21.mp3")
    },
    
    
    playSound(src) {
      const sound = new Audio()
      sound.src = src
      sound.play()
      sound.onended = () => delete(sound)
    },
    
    
    printAndProceed() {    
      const receiptContent = document.getElementById('receipt-content')
      
      const titleBefore = document.title
      const printArea = document.getElementById('print-area')

      printArea.innerHTML = receiptContent.innerHTML
      document.title = this.receiptNo

      window.print()
      this.isShowModalReceipt = false

      printArea.innerHTML = ''
      document.title = titleBefore

      this.clear()
    }
  };

  return app
}
