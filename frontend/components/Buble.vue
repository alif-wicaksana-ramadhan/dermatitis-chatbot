<script setup lang="ts">
const { text } = defineProps({
  text: {
    type: String,
    required: true
  }
})
</script>

<template>
<div class="bg-white shadow rounded-xl p-4">
  <span class="">{{text}}</span>
</div>
</template>

<style scoped>

</style>