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
    .custom-control-label::before {
        transform: scale(1.5);
        padding: 4px;
        vertical-align: bottom;
        margin-top: 6px;
        border-radius: 100% !important;
    }

    .custom-control-label::after {
        transform: scale(1.5);
        padding: 4px;
        vertical-align: bottom;
        margin-top: 6px;
        border-radius: 100% !important;
        /* background: 0; */
        /* This still does not do what we want for styling */
    }

    .custom-control-label {
        padding-left: 0.6rem;
        padding-bottom: 1.2rem;
        padding-top: 0.4rem;
    }
</style>
