<template>
    <b-container :id="containerId"  class="form-category my-3" :aria-labelledby="'category-heading-' + id">
        <h3 v-if="sectionName" class="h5 pt-2 pb-3 pl-1" :id="'category-heading-' + id">{{ sectionName  }} </h3>
        <b-container class="ml-2 pl-4">
            <slot></slot>
        </b-container>
    </b-container>
</template>

<script>
    export default {
        props: {
            active: {
                type: Boolean,
                default: false,
            },
            sectionName: {
                type: String,
            },
        },
        data() {
            return {
                id: null,
                containerId: (this.sectionName || "form-category").toLowerCase().split(' ').join('-'),
                scrollY: null,
            }
        },
        mounted() {
            this.id = this._uid;
        },
    }
</script>
