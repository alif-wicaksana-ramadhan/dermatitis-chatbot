<script setup lang="ts">
const answer = ref('');
const textInput = ref('');
const isLoading = ref(false);

const submitMessage = async () => {
  const question = textInput.value;
  textInput.value = '';
  isLoading.value = true;

  // const runtimeConfig = useRuntimeConfig();
  // console.log(runtimeConfig.public.backendUrl);
  // const res = await $fetch(`${runtimeConfig.public.backendUrl}/submit`, {
  //   method: 'POST',
  //   body: {
  //     question: question
  //   },
  // })
  // answer.value = res.llm.replies[0];
  // isLoading.value = false;

  const data = await $fetch('/api/submit', {
    method: 'post',
    body: { question: question },
  })
  console.log(data)
  answer.value = data.data.answer;

  isLoading.value = false;
}

const parseTextToSpan = (text: string) => {
  return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}
</script>

<template>
  <div class="p-4 mx-auto flex flex-col h-screen items-center justify-evenly bg-gray-100">
    <div class="container flex flex-col h-screen items-center justify-evenly">
      <span class="text-7xl">Dermatitis AI</span>
      <div v-if="answer" class="flex items-center justify-center h-1/3">
        <Buble :isLoading="isLoading" :text="parseTextToSpan(answer)" />
      </div>
      <div v-else class="flex items-center justify-center overflow-auto h-1/3">
        <Icon v-if="isLoading" name="eos-icons:loading" size="300" style="color: black" />
      </div>
      <div class="flex items-center w-full justify-center">
        <textarea
            v-model="textInput"
            :disabled="isLoading"
            @keydown.enter.exact.prevent="submitMessage"
            @keydown.enter.shift.exact="newLine"
            placeholder="...."
            class="w-full p-3 border rounded-tl-lg rounded-bl-lg h-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="1"
        ></textarea>
        <button @click="submitMessage" :disabled="isLoading" class="p-2 h-full bg-blue-400 rounded-tr-lg rounded-br-lg">Send</button>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>