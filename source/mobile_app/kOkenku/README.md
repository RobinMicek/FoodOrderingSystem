# Jak sestavit mobilní aplikaci

1. Nainstalujte Node.js a npm

   ```bash
   sudo apt install nodejs npm
   ```

2. Nainstalujte potřebné knihovny projektu

    ```bash
    npm install
    ```

3. Spusťte vývojový server - Pouze pro vývoj
    ```bash
    npm run dev
    ```

4. Upravte proměnné v _./src/variables.js_

5. Vybuilděte Vue.JS projekt
    ```bash
    npm run build
    ```

6. Přidejte iOS / Android

    ```bash
    npx cap add android ios
    ```

7. Vygenerujte grafiku

    ```
    npx capacitor-assets generate
    ```

8. Synchronizujte projekt s Capacitorem

    ```bash
    npx cap sync
    ```

9. Spusťte xCode / Android Studio

    ```bash
    npx cap open android/ios
    ```
    
# xCode - Změna zobrazovaného názvu aplikace
Pro změnu zobrazeného názvu aplikace na iOS (v XCode) upravte vlastnost __Bundle Display Name__ v _App/App/info_.

# Whitelabelling 
Projekt __K Okénku__ byl vytvářen s úmyslem, že ten, kdo ho chce využívat si ho graficky upraví podle své značky.

- Pro whitelabelling mobilní aplikace je potřeba nahradit tuto grafiku:
    - _./src/assets/favicon.png_
    - _./src/assets/images/favicon.png_
    - _./resources/icon-only.png_ (1024x1024px)
    - _./resouces/icon-foreground.png_
    - _./resouces/icon-background.png_
    - _./resouces/splash.png_ (2732x2732px)
    - _./resouces/splash-dark.png_ 
- Barvy se upravují v _./tailwind.config.js_
- Název se upraví v _./src/variables.js_

Tyto úpravy je nutné udělat před tím, než začnete sestavovat aplikaci!