<template>
    <b-modal
        :id="'modal-' + this.id"
        title=""
        :visible="modalShow"
        no-close-on-backdrop
        no-close-on-esc
        hide-header
        hide-footer
        footer-class="d-flex justify-content-center"
        header-border-variant="none"
        footer-border-variant="none">
        <slot :name="mode"></slot>
    </b-modal>
</template>

<script>
    export default {
        props: {
            modalShow: Boolean,
            mode: String,
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
