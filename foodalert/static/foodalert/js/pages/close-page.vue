<template>
    <generic-page>
        <template #heading>
            Your food cannot be shared with Hungry Husky
        </template>
        <template #body>
            <p>You indicated that your food is homemade which is ineligible to be shared with the public via Hungry Husky.</p>
          <p>You are still able to share it with your colleagues in your office. If you have questions about how to share food with Hungry Husky, please email <a href="mailto:hungryhusky@uw.edu">hungryhusky@uw.edu</a>.</p>
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