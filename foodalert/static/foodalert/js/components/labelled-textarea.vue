<template>
    <b-container fluid class="px-0">
        <b-form-group class="labelled-textarea" :label-for="'textarea-' + id">
            <template slot="label">
                <strong v-if="isOptional">Optional:</strong> {{ labelText }} <br />
                <em v-if="subLabel" class="text-muted"> {{ subLabel}} </em>
            </template>
            <b-form-textarea :rows="2" :placeholder="exampleText":id="'textarea-' + id" size="lg" v-model="text"> </b-form-textarea>
            <span>{{ this.maxChars - this.text.length }} characters left</span>
        </b-form-group>
        <b-alert v-if="warningText" show variant="primary" placement="bottom"> {{warningText}} </b-alert>
    </b-container>
</template>

<script>
    export default {
        props: {
            labelText: String,
            subLabel: String,
            isOptional: Boolean,
            exampleText: String,
            warningText: String,
            maxChars: {
                default: 100,
                type: Number,
            },
        },
        data: function () {
            return {
                id: null,
                isOptional: true,
                text: "",
            }
        },
        mounted() {
            this.id = this._uid;
        }
    }
</script>
