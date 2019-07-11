<template>
    <b-container class="custom-radio-main-container">
        <b-row class="justify-content-md-center">
            <b-col class="custom-radio-container">
                <div class="custom-radio-box align-middle" @click="toggleradiov2()" v-if="!disabled">
                    <div class="custom-radio-box-on" v-if="local_checked">

                    </div>
                </div>
                <div class="custom-radio-box-disabled align-middle" v-else>
                </div>
            </b-col>
            <b-col style="margin: auto">
                <b-form-radio class="custom-radio"
                    :value="c_value"
                    :disabled="disabled" ref="curRadio">
                    <slot>
                    </slot>
                </b-form-radio>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    props: {
        c_value: [Boolean, String],
        disabled: Boolean,
    },
    data() {
        return {
            componentLoaded: false,
        }
    },
    methods: {
        toggleradiov2() {
            this.$refs.curRadio.$el.children[1].click();
        },
    },
    computed: {
        local_checked() {
            if (this.componentLoaded)
                return this.$refs.curRadio.isChecked;
        }
    },
    watch: {
    },
    mounted() {
        this.componentLoaded = true;
    }
}
</script>

<style>
:root {
    --radio-size: 32px;
    --radio-check-size: 22px;
}
.custom-radio-main-container .custom-control-label::before, .custom-radio-main-container .custom-control-label::after{
    display: none !important;
}
.custom-radio-container{
    -ms-flex: 0 0 var(--radio-size) !important;
    flex: 0 0 var(--radio-size) !important;
    padding-left: 0 !important;
    z-index: 10;
}
.custom-radio-box {
    height: var(--radio-size);
    width: var(--radio-size);
    border-radius: 50%;
    background-color: white;
    border: 1.5px solid #6B6C72;
}
.custom-radio{
    margin-left: calc(var(--radio-size) - 75px) !important;
}
.custom-radio-main-container{
    padding-bottom: 20px;
}
.custom-radio-box-on {
    background-color: #0D95FC;
    width: var(--radio-check-size);
    height: var(--radio-check-size);
    margin: calc((var(--radio-size) - var(--radio-check-size) - 3px) * 0.5);
    border-radius: 50%;
}
.custom-radio-box-disabled {
    height: var(--radio-size);
    width: var(--radio-size);
    border-radius: 50%;
    background-color: #f1f1f1;
    border: 1.5px solid #9F9F9F;
}
</style>
