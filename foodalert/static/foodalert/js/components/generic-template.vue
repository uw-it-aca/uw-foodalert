<template>
    <router-view :subId="this.subId">

    </router-view>
</template>

<script>
export default {
    props: {
        subId: Number,
    },
}
</script>

<style>
    :root{
        --checbox-size: 32px;
        --checbox-check-size: 22px;
    }
    .custom-checkbox .custom-control-label::before, .custom-checkbox .custom-control-label::after {
        height: var(--checbox-size) !important;
        width: var(--checbox-size) !important;
    }

</style>
