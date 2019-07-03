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
    .custom-control-label::before, .custom-control-label::after {
        transform: scale(1.5);
        padding: 10px;
        vertical-align: bottom;
        margin-top: 6px;
    }

    .custom-control-label {
        padding-left: 1rem;
        padding-bottom: 1.5rem;
        padding-top: 0.3rem;
    }
</style>
