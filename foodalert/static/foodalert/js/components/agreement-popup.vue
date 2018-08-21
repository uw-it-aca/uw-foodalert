<template>
    <b-modal id="modal1" title="Bootstrap-Vue" v-model="modalShow">
        <template slot="modal-header">
            &#8203;
        </template>

        <div class="text-center">

            <h4 class="text-center">Thanks for sharing leftover food!</h4>
            <br>
            <h4 class="text-center">Do you have a Food Distribution Permit?</h4>
            <br>

            <!-- <b-container class="border py-4">
                <p class="text-center"> I have a food permit </p>
                <b-form-input id="input-large" size="lg" type="text" placeholder="Enter number" aria-label="Permit Number" class="text-center border-0"></b-form-input>
                <b-button size="lg" class="mx-auto" variant="success">Create Notification</b-button>
            </b-container>
            <a class="text-center"> How to get permit </a> -->

            <div
                v-if="primaryText">
                <b-button class="px-5" size="lg" variant="secondary">No</b-button>
                <b-button class="px-5 ml-2" size="lg" variant="primary">Yes</b-button>
            </div>
            <div
            <!-- <a class="text-center"> View list </a> -->
        </div>

        <template slot="modal-footer">
            &#8203;
        </template>
    </b-modal>
</template>


<script>
    export default {
        props: {
            primaryText: String,
            secondaryText: String,
        },
        data() {
            return {
                modalShow: true,
            }
        }
    }
</script>

<style>

</style>
