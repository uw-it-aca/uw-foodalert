<template>
    <b-container>
        <p><strong>Thanks for Sharing! Here's what's next:</strong></p>

        <p class="mt-4"> Let people know when food runs out </p>
        <b-btn class="w-100 mb-3" variant="primary" @click="modalShowing = true"> No Food Left </b-btn>

        <labelled-input
            label-text="Notify people if plans Change"
            is-optional
            :rows="2"
            example-text="e.g. We moved to HUB 230! Still 4 more sandwiches"
            class="mt-3">
        </labelled-input>
        <b-btn class="w-100 mb-3"> Send Update </b-btn>

        <b-modal
            v-model="modalShowing"
            header-border-variant="0"
            footer-border-variant="0"
            class="text-center"
            footer-class="d-flex flex-column">
            <p> Are you sure you'd like to notify student's there's <strong> no food left </strong> </p>

            <blockquote class="border rounded mb-0">What do blockquotes look like?</blockquote>


            <template slot="modal-footer">
                <b-link class=" btn btn-primary mx-auto mb-2" href="/ended"> Send 'No Food Left' </b-link>
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
