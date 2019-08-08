<template>
    <generic-page>
        <template #heading>
            <p class="foodalert-error-heading">{{errorHeading}}</p>
        </template>
        <template #body>
            <p>
                {{errorMessage}}
            </p>
            <p>
                Error code: {{errorCode}}
            </p>
            <p>
                Please <a href="mailto:help@uw.edu?subject=Hungry Husky support">contact support</a> to get help.
            </p>
        </template>
        <template #navigation>
            <div style="margin-top: 32px">
               <b-row align-h="between">
                 <b-col md="4" lg="3" order-md="2">
                   <b-button class="mb-3" type="submit" block size="lg" variant="primary" @click="getNextPage()">Try Again</b-button>
                 </b-col>
                 <b-col md="5" lg="4" order-md="1"></b-col>
               </b-row>
            </div>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../components/generic-page.vue";
    export default {
        components:{
            "generic-page": GenericPage,
        },
        props: {
            errorHeading: {
                type: String,
                default: "SMS verification failed"
            },
            errorMessage: {
                type: String,
                default: "There was an error connecting to the Hungry Husky server"
            },
            errorCode: {
                type: Number,
                default: 500
            },
            tryAgainPage: {
                type: String,
                default: "s-welcome"
            }
        },
        methods: {
            getNextPage() {
                this.$router.push({ name: this.tryAgainPage });
            },
        },
        data() {
            return {
            }
        }
    }
</script>

<style>
.foodalert-error-heading {
    font-style: normal;
    font-weight: bold;
    font-size: 32px;
    line-height: 42px;
    color: #E05018;
}
</style>

