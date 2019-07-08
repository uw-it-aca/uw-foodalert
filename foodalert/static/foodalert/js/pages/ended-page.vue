<template>
    <generic-page startWithNotification>
        <template #notification>
             Your update was sent.
        </template>
        <template #heading>
            Our sincere thanks
        </template>
        <template #body>
            <p>Thank you for sharing food. Your generosity means that less people have to worry about food insecurity at UW. You've also contributed to decrease the University's food waste.</p>
        </template>
        <template #navigation>
            <div class="mt-5">
                <b-row align-h="between">
                    <b-col md="5" lg="4" order-md="2"><b-button class="mb-3" type="submit" block variant="primary" style="white-space: nowrap;" @click="$router.push({'name': 'h-welcome'})">Submit</b-button>
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
    }
</script>