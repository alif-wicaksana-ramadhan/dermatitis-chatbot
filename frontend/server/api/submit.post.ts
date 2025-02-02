export default defineEventHandler(async (event) => {
    const runtimeConfig = useRuntimeConfig();
    const body = await readBody(event);
    console.log(runtimeConfig.backendUrl);
    const res = await $fetch(`${runtimeConfig.backendUrl}/submit`, {
        method: 'POST',
        body: body,
    })
    return {
        data: { answer: res.llm.replies[0]}
    }
})