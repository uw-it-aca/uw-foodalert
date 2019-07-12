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
        --checkbox-size: 32px;
        --radio-size: 32px;

    }
    .custom-checkbox .custom-control-label::before, .custom-checkbox .custom-control-label::after {
        height: var(--checkbox-size) !important;
        width: var(--checkbox-size) !important;
    }
    .custom-checkbox .custom-control-label::before {
        border: 1.5px solid #AAAAAA;
        border-radius: 6.25% !important;
    }
    .custom-checkbox .custom-control-input:disabled~.custom-control-label::before {
        border: 1.5px solid #EAEAEA;
        background: initial;
    }
    .custom-checkbox .custom-control-input:checked~.custom-control-label::after {
        background: url("../../img/check.svg") no-repeat 50%/75% !important;  
    }
    .custom-checkbox .custom-control-label{
        padding-left: calc(var(--checkbox-size) - 0.5rem);
        display: flex;
        align-items: center;
        min-height: calc(var(--checkbox-size) + 0.5rem);
    }
    .custom-control.custom-checkbox {
        min-height: calc(var(--checkbox-size) + 0.5rem);
    }

    .custom-checkbox:hover .custom-control-label::before  {
        border-color: #0D95FC;
    }

    .custom-radio .custom-control-label::before, .custom-radio .custom-control-label::after {
        height: var(--radio-size) !important;
        width: var(--radio-size) !important;
    }
    .custom-radio .custom-control-label::before {
        border: 1.5px solid #AAAAAA;
    }
    .custom-radio .custom-control-input:disabled~.custom-control-label::before {
        border: 1.5px solid #EAEAEA;
        background: initial;
    }
    .custom-radio .custom-control-input:checked~.custom-control-label::before {
        background-color: initial;
    }
    .custom-radio .custom-control-input:checked~.custom-control-label::after {
        background: url("../../img/dot.svg") no-repeat center center/69% !important;  
    }
    .custom-radio .custom-control-label{
        padding-left: calc(var(--radio-size) - 0.5rem);
        display: flex;
        align-items: center;
        min-height: calc(var(--radio-size) + 0.5rem);
    }
    .custom-control.custom-radio {
        min-height: calc(var(--radio-size) + 0.5rem);
    }

    .custom-radio:hover .custom-control-label::before  {
        border-color: #0D95FC;
    }
</style>
