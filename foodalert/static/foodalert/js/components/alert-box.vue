<template>
    <div class="alert-container">
        <div class="alert-text">
            <slot>
            </slot>
        </div>
    </div>
</template>

<style scoped>
    .alert-container {
        width: 100%;
        padding: 16px;
        display: flex;
        align-items: center;
        background-color: #0070c9;
        color: white;
        font-size: 18px;
        font-weight: 400;
    }

    .alert-container .alert-image {
        margin-right: 16px;
    }

    .alert-container .alert-image > img {
        height: 36px;
        width: 36px;
        /*background: url("../../img/check.svg") no-repeat center;
        background-size: 50%;*/
    }

    .alert-container .alert-text {
        margin: 0 auto;
    }
</style>
