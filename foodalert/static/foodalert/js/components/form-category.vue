<template>
    <b-container class="form-category" :aria-labelledby="'category-heading-' + id">
        <h3 :id="'category-heading-' + id"><font-awesome-icon class="category-icon" :icon="iconName" />&nbsp; {{ sectionName  }} </h3>
        <slot></slot>
    </b-container>
</template>

<script>
    import LabelledTextarea from './labelled-textarea.vue';

    export default {
        props: {
            sectionName: String,
            iconName: String,
        },
        data() {
            return {
                id: null,
            }
        },
        components: {
            LabelledTextarea,
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>

<style scoped>
    section {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .category-icon {
        padding-top: 10px;
    }
</style>
