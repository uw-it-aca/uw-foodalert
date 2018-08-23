<template>
    <b-container fluid class="px-0 py-1">
        <b-form-group class="labelled-textarea mb-0" :label-for="'textarea-' + id">
            <template slot="label">
                <strong v-if="isOptional" class="text-secondary font-italic" >Optional:</strong> {{ labelText }} <br />
                <em v-if="subLabel" class="text-muted"> {{ subLabel}} </em>
            </template>
            <b-form-textarea
                v-if="inputType=='textarea'"
                :rows="rows"
                :placeholder="exampleText"
                :id="'textarea-' + id"
                size="md"
                v-model="text">
            </b-form-textarea>
            <b-form-checkbox-group
                v-else-if="inputType=='checkbox'"
                v-model="checked"
                :id="'checkbox-' + id">
                <b-row
                    v-for="box in boxes"
                    class="mx-0">
                    <b-form-checkbox :value="box"> {{ box }} </b-form-checkbox><br>
                </b-row>
            </b-form-checkbox-group>
            <span
                v-if="(inputType == 'textarea') && !noCharCount"
                class="text-right w-100">
                <span
                    v-if="this.text.length > 0">
                    {{ this.maxChars - this.text.length }} characters left
                </span>
                <span v-else> &nbsp; </span>
            </span>
            <span v-else-if="!noPadding"> &nbsp; </span>
        </b-form-group>
        <b-alert v-if="warningText" show variant="primary" placement="bottom" class="mt-1"> {{warningText}} </b-alert>
    </b-container>
</template>

<script>
    export default {
        props: {
            inputType: {
                type: String,
                default: "textarea",
                validator: function (value) {
                    return [
                        'textarea',
                        'checkbox',
                    ].indexOf(value) !== -1;
                }
            },
            labelText: String,
            subLabel: String,
            isOptional: Boolean,
            exampleText: String,
            warningText: String,
            boxes: Array,
            maxChars: {
                default: 100,
                type: Number,
            },
            rows: {
                type: Number,
                default: 1
            },
            noPadding: {
                type: Boolean,
                default: false,
            },
            noCharCount: {
                type: Boolean,
                default: false,
            }
        },
        data: function () {
            return {
                id: null,
                text: "",
                checked: "",
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>
