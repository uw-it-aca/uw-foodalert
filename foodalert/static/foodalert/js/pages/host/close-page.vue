<template>
    <generic-page>
        <template #heading>
            Your food cannot be shared with Hungry Husky
        </template>
        <template #body>
            <p>You indicated that your food is homemade, which makes it ineligible to be shared with the public via Hungry Husky.</p>
          <p>You are still able to share it with your colleagues in your office. If you have questions about how to share food with Hungry Husky, please email <a href="mailto:hungryhusky@uw.edu">hungryhusky@uw.edu</a>. And thanks for thinking of Hungry Husky!</p>
        </template>
    </generic-page>
</template>

<script type="text/javascript">
    import GenericPage from "../../components/generic-page.vue";
    export default {
        components:{
            "generic-page": GenericPage,
        },
        beforeMount() {
            axios.get("/notification/?host_netid=" + this.netID).then((result) => {
                result.data = result.data.filter((d)=>!d.ended)
                if(result.data.length)
                    this.$router.push({ name: 'h-update', params: {notificationText: "You already have an event running."}});
            }).catch((error) => this.showErrorPage(error.response, "h-welcome"));
        },
    }
</script>
