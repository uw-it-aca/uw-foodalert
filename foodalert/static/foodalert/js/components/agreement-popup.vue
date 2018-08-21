<template>
    <b-modal
        :id="'modal-' + this.id"
        title=""
        v-model="modalShow"
        no-close-on-backdrop
        no-close-on-esc
        hide-header-close
        footer-class="d-flex justify-content-center"
        header-border-variant="none"
        footer-border-variant="none">
        <template slot="modal-header">
            <a v-if="canBack" ><font-awesome-icon icon="chevron-left"></font-awesome-icon> Back </a>
        </template>

        <div class="text-center">
            <p v-if="introText" class="h5 text-center"> {{ introText }} </p>
            <br>
            <p class="h5 text-center"> {{ mainText }} </p>
            <br>
        </div>

        <template slot="modal-footer">
            <div>
                <div class="d-flex justify-content-center">
                    <b-button v-if="secondaryText" class="px-5" size="lg" variant="secondary">{{ secondaryText }}</b-button>
                    <b-button v-if="primaryText" class="px-5 ml-2" size="lg" variant="primary" @click="modalShow = false">{{ primaryText }}</b-button>
                </div>
                <br>
                <p v-if="infoText" class="d-block text-center w-100"> {{ infoText }} </p>
                <a v-if="linkText" :href="linkLocation" class="d-block text-center"> {{ linkText }} </a>
            </div>
        </template>
    </b-modal>
</template>


<script>
    export default {
        props: {
            mainText: String,
            introText: String,
            infoText: String,
            linkText: String,
            linkLocation: String,
            primaryText: String,
            secondaryText: String,
            canBack: Boolean,
        },
        data() {
            return {
                modalShow: true,
                id: null,
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>

<style>

</style>
