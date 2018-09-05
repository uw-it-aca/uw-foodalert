<template>
    <b-container :id="containerId"  class="form-category my-3" :aria-labelledby="'category-heading-' + id">
        <h3 class="h5 pt-2 pb-3 pl-1" :id="'category-heading-' + id"><font-awesome-icon class="category-icon" :icon="iconName" />&nbsp;&nbsp; {{ sectionName  }} </h3>
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
                required: true
            },
            iconName: String,
        },
        data() {
            return {
                id: null,
                containerId: this.sectionName.toLowerCase().split(' ').join('-'),
                scrollY: null,
            }
        },
        watch: {
            scrollY: function() {
                var domRect = document.getElementById(this.containerId).getBoundingClientRect();
                if (domRect.top < 0 && domRect.bottom > 0) {
                    if (!this.active){
                        this.$emit('update:active', true);
                    }
                } else {
                    if (this.active) {
                        this.$emit('update:active', false);
                    }
                }
            }
        },
        mounted() {
            this.id = this._uid;
        },
        methods: {
            handleScroll() {
                this.scrollY = window.scrollY;
            },
        },
        created() {
            window.addEventListener('scroll', this.handleScroll);
        },
        destroyed() {
            window.removeEventListener('scroll', this.handleScroll);
        },
    }
</script>
