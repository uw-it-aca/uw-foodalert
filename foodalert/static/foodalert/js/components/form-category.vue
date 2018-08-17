<template>
    <b-container class="form-category my-3" :aria-labelledby="'category-heading-' + id">
        <h2 class="h5 pt-1 pb-5" :id="'category-heading-' + id"><font-awesome-icon class="category-icon" :icon="iconName" />&nbsp; {{ sectionName  }} </h2>
        <slot></slot>
    </b-container>
</template>

<script>
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
        mounted() {
            this.id = this._uid;
        }
    }
</script>
