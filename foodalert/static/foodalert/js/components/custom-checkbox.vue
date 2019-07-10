<template>
    <b-container class="custom-checkbox-main-container">
        <b-row class="justify-content-md-center">
            <b-col class="custom-checkbox-container">
                <div class="custom-checkbox-box align-middle" @click="toggleCheckBox()" v-if="!disabled">
                    <div class="custom-checkbox-box-on" v-if="v_model_local.includes(value)">
                        
                    </div>
                </div>
                <div class="custom-checkbox-box-disabled align-middle" v-else>
                </div>
            </b-col>
            <b-col style="margin: auto">
                <b-form-checkbox class="custom-checkbox"
                    v-model="v_model_local"
                    :key="value"
                    :value="value"
                    :disabled="disabled">

                    <slot>
                    </slot>
                </b-form-checkbox>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    props: {
        v_model: Array,
        value: String,
        disabled: Boolean,
    },
    data() {
        return {
            v_model_local: [],
        }
    },
    methods: {
        toggleCheckBox() {
            var index = this.v_model_local.indexOf(this.value);
            if (index > -1) {
                this.v_model_local.splice(index, 1)
            } else {
                this.v_model_local.push(this.value)
            }
        }
    },
    watch: {
        v_model(newState, oldState) {
            this.v_model_local = this.v_model;
        },
        v_model_local(newState, oldState) {
            this.$emit("update:v_model", this.v_model_local)
        }
    }
}
</script>

<style>
:root {
    --checkbox-size: 32px;
    --checkbox-check-size: 22px;
}
.custom-control-label::before, .custom-control-label::after{
    display: none !important;
}
.custom-checkbox-container{
    -ms-flex: 0 0 var(--checkbox-size) !important;
    flex: 0 0 var(--checkbox-size) !important;
    padding-left: 0 !important;
    z-index: 10;
}
.custom-checkbox-box {
    height: var(--checkbox-size);
    width: var(--checkbox-size);
    border-radius: 15%;
    background-color: white;
    border: 1.5px solid #6B6C72;
}
.custom-checkbox{
    margin-left: calc(var(--checkbox-size) - 75px) !important;
}
.custom-checkbox-main-container{
    padding-bottom: 20px;
}
.custom-checkbox-box-on {
    background-color: #6B6C72;
    width: var(--checkbox-check-size);
    height: var(--checkbox-check-size);
    margin: calc((var(--checkbox-size) - var(--checkbox-check-size) - 3px) * 0.5);
    border-radius: 15%;
}
.custom-checkbox-box-disabled {
    height: var(--checkbox-size);
    width: var(--checkbox-size);
    border-radius: 15%;
    background-color: #A9A9A9;
    border: 1.5px solid #808080;
}
</style>
