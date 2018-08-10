<template>
    <p> This is a hello world component. {{ dynamic_content }}</p>
</template>

<script>
    export default {
        data() {
            return {
                dynamic_content: "This is dynamic content"
            }
        }
    }
</script>
