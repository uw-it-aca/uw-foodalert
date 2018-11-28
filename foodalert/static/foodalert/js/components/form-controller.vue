<template>
    <form-template
        :allergens='["milk", "eggs", "soy", "fish", "shellfish", "Peanuts", "wheat"]'
        :preview-text="'preview text'">
    </form-template>
</template>

<script type="text/javascript">
    import FormTemplate from './form-template.vue';
    export default {
        components: {
            'form-template': FormTemplate,
        }
    }
</script>
