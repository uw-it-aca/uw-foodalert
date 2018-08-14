<template>
    <section class="form-category container">
        <h3 class="row"><font-awesome-icon class="category-icon" icon="utensils" />&nbsp; {{ section_name  }} </h3>
        <labelled-textarea></labelled-textarea>
        <labelled-textarea></labelled-textarea>
    </section>
</template>

<script>
    import LabelledTextarea from './labelled-textarea.vue';

    export default {
        data: function () {
            return {
                section_name: "test name",
                icon_name: "utensils"
            };
        },
        components: {
            LabelledTextarea,
        }
    }
</script>
