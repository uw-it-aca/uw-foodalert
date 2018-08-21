<template>
    <b-container :id="containerId"  class="form-category my-3" :aria-labelledby="'category-heading-' + id">
        <h3 class="h5 pt-2 pb-3" :id="'category-heading-' + id"><font-awesome-icon class="category-icon" :icon="iconName" />&nbsp; {{ sectionName  }} </h3>
        <slot></slot>
    </b-container>
</template>

<script>
    export default {
        props: {
            sectionName: String,
            iconName: String,
        },
        computed: {
            containerId: function() {
                return this.sectionName.toLowerCase().split(' ').join('-');
            }
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
