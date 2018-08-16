<template>
    <b-container class="form-category my-3" :aria-labelledby="'category-heading-' + id">
        <h3 :id="'category-heading-' + id"><font-awesome-icon class="category-icon pt-1" :icon="iconName" />&nbsp; {{ sectionName  }} </h3>
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
