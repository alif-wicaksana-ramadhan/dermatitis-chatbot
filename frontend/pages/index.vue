<script setup lang="ts">
const response = ref('');
const textInput = ref('');

const submitMessage = async () => {
  const data = await $fetch('/api/submit', {
    method: 'post',
    body: { text: textInput.value },
  })
  textInput.value = '';
  console.log(data)
}
</script>

<template>
  <div class="container p-4 mx-auto flex flex-col h-screen items-center justify-evenly bg-yellow-100">
    <span class="text-7xl">Dermatitis AI</span>
    <div v-if="response" class="flex items-center justify-center h-1/3 bg-green-100">
      <Buble :text="response" />
    </div>
    <div class="flex items-center justify-center bg-green-100">
      <textarea
          v-model="textInput"
          @keydown.enter.exact.prevent="submitMessage"
          @keydown.enter.shift.exact="newLine"
          placeholder="...."
          class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="1"
      ></textarea>
      <button @click="submitMessage" class="p-2">Send</button>
    </div>
  </div>
</template>

<style scoped>

</style>