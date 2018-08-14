<template>
    <section class="form-category container">
        <h3 class="row"><i class="fas fa-utensils"></i> {{ section_name  }} </h3>
        <labelled-textarea></labelled-textarea>
        <labelled-textarea></labelled-textarea>
    </section>
</template>

<script>
    import LabelledTextarea from './labelled-textarea.vue';

    export default {
        data: function () {
            return {
                section_name: "test name"
            };
        },
        components: {
            LabelledTextarea,
        }
    }
</script>
