<template>
    <b-container class="custom-checkbox-main-container">
        <b-row class="justify-content-md-center">
            <b-col class="custom-checkbox-container">
                <div class="custom-checkbox-box align-middle" @click="toggleCheckBox()">
                    <div class="custom-checkbox-box-on" v-if="v_model_local.includes(c_value)">
                        <img src="../../img/check.svg" class="checkbox-check-img"/>
                    </div>
                </div>
            </b-col>
            <b-col style="margin: auto">
                <b-form-checkbox class="custom-checkbox"
                    v-model="v_model_local"
                    :key="c_value"
                    :value="c_value">
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
        c_value: String,
    },
    data() {
        return {
            v_model_local: [],
        }
    },
    methods: {
        toggleCheckBox() {
            var index = this.v_model_local.indexOf(this.c_value);
            if (index > -1) {
                this.v_model_local.splice(index, 1)
            } else {
                this.v_model_local.push(this.c_value)
            }
        }
    },
    watch: {
        v_model(newState, oldState) {
            this.v_model_local = this.v_model;
        },
        v_model_local(newState, oldState) {
            this.$emit("update:v_model", this.v_model_local)
        },
        disabled(newState, oldState) {
            var index = this.v_model_local.indexOf(this.c_value);
            if (index > -1) {
                this.v_model_local.splice(index, 1)
            }
        },
    }
}
</script>

<style>
:root {
    --checkbox-size: 32px;
    --checkbox-check-size: 22px;
}

.custom-checkbox-main-container .custom-control-label::before, .custom-checkbox-main-container .custom-control-label::after{
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
    border-radius: 2px;
    background-color: white;
    border: 1px solid #6B6C72;
}
.custom-checkbox-box:hover{
    border: 1px solid #0D95FC;
}
.custom-checkbox-main-container .custom-checkbox{
    margin-left: calc(var(--checkbox-size) - 75px) !important;
} 
.custom-checkbox-main-container{
    padding-bottom: 20px;
}
.custom-checkbox-box-on {
    background-color: #0D95FC;
    width: var(--checkbox-size);
    height: var(--checkbox-size);
    border-radius: 2px;
}
.custom-checkbox-box-disabled {
    height: var(--checkbox-size);
    width: var(--checkbox-size);
    border-radius: 2px;
    background-color: #f1f1f1;
    border: 1px solid #9F9F9F;
}
.checkbox-check-img{
    height: calc(var(--checkbox-check-size));
    width: calc(var(--checkbox-check-size));
    margin: calc((var(--checkbox-size) - var(--checkbox-check-size)) * 0.5);
    filter: invert(100%);
}
</style>
