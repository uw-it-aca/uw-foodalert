<template>
    <div class="alert-container">
        <div class="alert-image my-auto">
            <img src="../../img/check 2.svg" alt="checkmark">
        </div>
        <div class="alert-text">
            <slot>
            </slot>
        </div>
    </div>
</template>

<style scoped>
    .alert-container {
        width: 100%;
        border: 2px solid #AAAAAA;
        /*border-radius: 0 10px 10px 0;*/
        padding: 16px;
        display: flex;
        align-items: center;
        /*border-left: 10px solid #0070c9;
        background: #f1f1f1;*/
        border-radius: 10px;
        font-size: 16px;
        font-weight: 400;
    }

    .alert-container .alert-image {
        margin-right: 16px;
        /*background-color: #0070c9;
        border-radius: 50%;*/
    }

    .alert-container .alert-image > img {
        height: 36px;
        width: 36px;
        /*background: url("../../img/check.svg") no-repeat center;
        background-size: 50%;*/
    }

    .alert-container .alert-text {

    }
</style>