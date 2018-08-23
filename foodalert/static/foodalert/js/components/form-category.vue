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
            sectionName: String,
            iconName: String,
            scrollY: Number,
        },
        data() {
            return {
                id: null,
                containerId: this.sectionName.toLowerCase().split(' ').join('-'),
            }
        },
        watch: {
            scrollY: function() {
                var domRect = document.getElementById(this.containerId).getBoundingClientRect();
                if(this.$store.state.currentCat != this.sectionName && domRect.top < 0 && domRect.bottom > 0) {
                    this.$store.commit('setCurrentCat', this.sectionName);
                }
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>
