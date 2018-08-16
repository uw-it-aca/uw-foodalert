<template>
    <b-modal id="modal1" title="Bootstrap-Vue" v-model="modalShow">
        <template slot="modal-header">
            &#8203;
        </template>

        <div class="text-center">
            <p class="text-center">Before you create a notification, you must do some stuff that we'll add into this popup later</p>

            <b-container class="border py-4">
                <p class="text-center"> I have a food permit </p>
                <b-form-input id="input-large" size="lg" type="text" placeholder="Enter number" aria-label="Permit Number" class="text-center border-0"></b-form-input>
                <b-button size="lg" class="mx-auto" variant="success">Create Notification</b-button>
            </b-container>
            <a class="text-center"> How to get permit </a>

            <b-container class="mt-4">
                <b-button size="lg" variant="success">My food is on the safe to share list</b-button>
            </b-container>
            <a class="text-center"> View list </a>
        </div>

        <template slot="modal-footer">
            &#8203;
        </template>
    </b-modal>
</template>

<script>
    export default {
        data() {
            return {
                modalShow: true,
            }
        }
    }
</script>
