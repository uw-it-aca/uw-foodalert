<template>
    <div class="foodalert">
        <router-view ref="foodalertAppRouter">
        </router-view>
        <!-- To load the images before they need to be displayed
            without this we can still use the default bootstrap checkmark and
            but they look worse and dont match the color that we need.
        !-->
        <img src="../../img/check.svg" style="display: none">
        <img src="../../img/dot.svg" style="display: none">
    </div>
</template>

<script>
export default {

};
</script>

<style>
    :root{
        --checkbox-size: 32px;
        --radio-size: 32px;
        --switch-width: 50px;
        --switch-height: 32px;
        --switch-circle: 26px;
    }
    .foodalert .custom-checkbox .custom-control-label::before,
    .custom-checkbox .custom-control-label::after {
        height: var(--checkbox-size);
        width: var(--checkbox-size);
    }
    .foodalert .custom-checkbox .custom-control-label::before {
        border: 1.5px solid #AAAAAA;
        border-radius: 6.25%;
    }
    .foodalert .custom-checkbox
    .custom-control-input:disabled~.custom-control-label::before {
        border: 1.5px solid #EAEAEA;
        background: initial;
    }
    .foodalert .custom-checkbox
    .custom-control-input:checked~.custom-control-label::before {
        border-color: var(--primary);
    }
    .foodalert .custom-checkbox
    .custom-control-input:checked~.custom-control-label::after {
        background: url("../../img/check.svg") no-repeat 50%/75%;
    }
    .foodalert .custom-checkbox .custom-control-label{
        padding-left: calc(var(--checkbox-size) - 0.5rem);
        display: flex;
        align-items: center;
        min-height: calc(var(--checkbox-size) + 0.5rem);
    }
    .foodalert .custom-control.custom-checkbox {
        min-height: calc(var(--checkbox-size) + 0.5rem);
    }

    .foodalert .custom-checkbox:hover .custom-control-label::before  {
        border-color: var(--primary);
    }

    .foodalert .custom-radio .custom-control-label::before,
    .custom-radio .custom-control-label::after {
        height: var(--radio-size);
        width: var(--radio-size);
    }
    .foodalert .custom-radio .custom-control-label::before {
        border: 1.5px solid #AAAAAA;
    }
    .foodalert .custom-radio
    .custom-control-input:disabled~.custom-control-label::before {
        border: 1.5px solid #EAEAEA;
        background: initial;
    }
    .foodalert .custom-radio
    .custom-control-input:checked~.custom-control-label::before {
        border-color: var(--primary);
        background-color: initial;
    }
    .foodalert .custom-radio
    .custom-control-input:checked~.custom-control-label::after {
        background: url("../../img/dot.svg") no-repeat center center/69%;
    }
    .foodalert .custom-radio .custom-control-label{
        padding-left: calc(var(--radio-size) - 0.5rem);
        display: flex;
        align-items: center;
        min-height: calc(var(--radio-size) + 0.5rem);
    }
    .foodalert .custom-control.custom-radio {
        min-height: calc(var(--radio-size) + 0.5rem);
    }

    .foodalert .custom-radio:hover .custom-control-label::before  {
        border-color: var(--primary);
    }

    .foodalert .custom-switch .custom-control-label::before {
        width: var(--switch-width);
        height: var(--switch-height);
        border-radius: calc(var(--switch-width) / 2);
        top: 0px;
    }

    .foodalert .custom-switch .custom-control-label:after {
        width: var(--switch-circle);
        height: var(--switch-circle);
        border-radius: 50%;
            left: calc(-2.25rem + 3px);
        top: calc((var(--switch-height) - var(--switch-circle)) / 2);
    }

    .foodalert .custom-switch
    .custom-control-input:checked~.custom-control-label::after {
        transform: translateX(calc(var(--switch-width) -
            var(--switch-circle) - 5.5px));
    }

    .foodalert .custom-control.custom-switch {
        height: var(--switch-height);
    }

    .foodalert .h2 {
        font-size: 24px;
        font-weight: 600;
        line-height: 1.375;
        color: #484848;
        -moz-osx-font-smoothing: grayscale;
        padding-top: 32px;
        padding-bottom: 2px;
        margin-top: 0px !important;
    }

    .foodalert .h3 {
      font-size: 18px;
      font-weight: 600;
      line-height: 1.375;
      color: #484848;
      -moz-osx-font-smoothing: grayscale;
      padding-top: 24px;
      padding-bottom: 16px;
      margin-bottom: 0px;
    }

    .foodalert .standard-placeholder::placeholder {
        font-size: 16px;
        font-weight: 400;
        color: #767676;
        -moz-osx-font-smoothing: grayscale;
    }

    .foodalert .standard-label {
        font-size: 16px;
        font-weight: 600;
        line-height: 1.375;
        color: #484848;
        -moz-osx-font-smoothing: grayscale;
        margin-top: 24px;
    }

    .foodalert .form-control.is-invalid {
        background: unset;
    }

    .foodalert .invalid-feedback {
        font-size: 14px;
        font-weight: 400;
        line-height: 1.375;
        -moz-osx-font-smoothing: grayscale;
    }

    .foodalert .custom-control-input.is-invalid~.custom-control-label {
        color: initial;
    }

    .foodalert .super-show {
        display: block !important;
    }

    .foodalert .super-hide {
        display: none !important;
    }

</style>
