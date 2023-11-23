<template>
    <div class="mt-8 relative w-full">
      <input :type="type" :id="id" :value="inputValue" @input="$emit('update:modelValue', $event.target.value)" required 
        class="w-full h-12 py-4vh px-5 rounded-lg">

      <label :for="id" class="absolute px-2 py-0.5 left-3 -top-3 bg-white text-text primary text-sm rounded-md font-medium">
        {{ name }}
      </label>
    </div>
</template>

<script>
export default {
    props: {
        type: String,
        id: String,
        name: String,
        modelValue: String,
    },
    data() {
        return {
        inputValue: this.modelValue,
        };
    },
    watch: {
        modelValue(newValue) {
            this.inputValue = newValue;
        },

        inputValue(newValue) {
            this.$emit('update:modelValue', newValue);
        },
},
};
</script>
  