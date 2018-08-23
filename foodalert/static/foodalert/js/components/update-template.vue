<template>
    <b-container class="px-4 pt-3">
        <p><strong>Thanks for Sharing! Here's what's next:</strong></p>

        <p class="mt-4"> Let people know when food runs out </p>
        <b-btn class="w-100 mb-3 py-2" variant="primary" @click="modalShowing = true"> No Food Left </b-btn>

        <labelled-input
            label-text="Notify people if plans change"
            is-optional
            :rows="2"
            example-text="e.g. We moved to HUB 230! Still 4 more sandwiches"
            class="mt-3">
        </labelled-input>
        <b-btn class="w-100 mb-3 py-2"> Send Update </b-btn>

        <b-modal
            v-model="modalShowing"
            header-border-variant="0"
            footer-border-variant="0"
            class="text-center"
            footer-class="d-flex flex-column">
            <p class="h5 pb-3"> Are you sure you'd like to notify student's there's <strong> no food left</strong>? </p>

            <blockquote class="border rounded mb-0 mx-3 p-3 text-left bg-light">Update: No Food left! “Hot Indian buffet food leftover
            from from FIUTs weekly meeting” is all gone.</blockquote>


            <template slot="modal-footer">
                <b-link class="btn btn-lg btn-primary mx-auto mb-2" href="/ended"> Send 'No Food Left' </b-link>
                <a href="#" @click="modalShowing = false" class="mx-auto"> Cancel </a>
            </template>
        </b-modal>
    </b-container>
</template>


<script>
    import LabelledInput from './labelled-input.vue'

    export default {
        components: {
            'labelled-input': LabelledInput,
        },
        data() {
            return {
                id: null,
                modalShowing: false,
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>
