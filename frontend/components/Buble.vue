<script setup lang="ts">
const { text } = defineProps({
  text: {
    type: String,
    required: true
  },
  isLoading: {
    type: Boolean,
    required: true
  }
})
</script>

<template>
<div class="bg-white shadow rounded-xl p-4">
  <span v-if="!isLoading" style="white-space: pre-line;" class="">{{text}}</span>
  <Icon v-else name="eos-icons:loading" size="300" style="color: black" />
</div>
</template>

<style scoped>

</style>