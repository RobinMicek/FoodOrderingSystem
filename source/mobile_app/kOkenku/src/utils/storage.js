/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


// These functions are for setting and getting
// information from localStorage

// USAGE:
`
<script>
import { setObject, getObject } from "@/utils/storage.js"

export default {
  data() {
    return {
    };
  },

  methods: {
    async insert() {
      try {
        await setObject(key, value);
      } catch (error) {
        console.error(error);
      }
    },

    async retrieve() {
      try {
        const value = await getObject(key);
      } catch (error) {
        console.error(error);
      }
    },

    async remove() {
      try {
        const removal = await getObject(key);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
`

import { Preferences } from '@capacitor/preferences';

export async function setObject(key, value) {
  await Preferences.set({
    key: key.toString(),
    value: value.toString(),
  });
}

export async function getObject(key) {
  const value = await Preferences.get({ key: key.toString() });
  return value.value; 
}

export async function removeObject(key) {
  const value = await Preferences.remove({ key: key.toString() });
}
