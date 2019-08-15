<template>
    <b-input-group :id="timeID">
        <b-form-select v-model="hourSelected" :options="hourOptions" size="lg" @change="updateTime()" :aria-labelledby="labelbyID"></b-form-select>
        <b-form-select v-model="minuteSelected" :options="minuteOptions" size="lg" @change="updateTime()" :aria-labelledby="labelbyID"></b-form-select>
        <b-form-select v-model="periodSelected" :options="periodOptions" size="lg" @change="updateTime()" :aria-labelledby="labelbyID"></b-form-select>
    </b-input-group>
</template>

<script>
export default {
    props: {
        value: String,
        timeID: String,
        startWithCurrent: Boolean,
        labelbyID: String,
    },
    data() {
        var _hourOptions = Array(12)
        for (var i = 0; i < 12; i++) {
            _hourOptions[i] = i + 1
        }
        var _minuteOptions = Array(60)
        for (var i = 0; i < 60; i++) {
            _minuteOptions[i] = i + 1
        }

        return {
            hourOptions: _hourOptions,
            minuteOptions: _minuteOptions,
            periodOptions: ['AM', 'PM'],
            hourSelected: null,
            minuteSelected: null,
            periodSelected: null,
        }
    },
    methods: {
        updateTime() {
            this.$emit('input', this.hourSelected + ":" +
                this.minuteSelected + " " + this.periodSelected)
        }
    },
    beforeMount() {
        if (this.startWithCurrent) {
            var semiFormattedTime = new Date().toLocaleTimeString().split(/\:| /)
            this.hourSelected = parseInt(semiFormattedTime[0])
            this.minuteSelected = parseInt(semiFormattedTime[1])
            this.periodSelected = semiFormattedTime[3]
        }
    },
}
</script>

<style scoped>
    .foodalert .custom-select {
        background: unset;
    }
</style>