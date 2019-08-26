<template>
    <b-input-group :id="timeID" :aria-labelledby="labelbyID">
        <b-form-select v-model="hourSelected"
            aria-label="Enter hours"
            :options="hourOptions" size="lg"
            @change="updateTime()">
        </b-form-select>
        <b-form-select v-model="minuteSelected"
            aria-label="Enter minutes"
            :options="minuteOptions" size="lg"
            @change="updateTime()">
        </b-form-select>
        <b-form-select v-model="periodSelected"
            aria-label="Enter AM/PM"
            :options="periodOptions"
            size="lg"
            @change="updateTime()">
        </b-form-select>
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
    const _hourOptions = Array(12);
    for (let i = 0; i < 12; i++) {
      _hourOptions[i] = i + 1;
    }
    const _minuteOptions = Array(60);
    for (let i = 0; i < 60; i++) {
      _minuteOptions[i] = (((i < 10) ? '0' : '') + i);
    }

    return {
      hourOptions: _hourOptions,
      minuteOptions: _minuteOptions,
      periodOptions: ['AM', 'PM'],
      hourSelected: null,
      minuteSelected: null,
      periodSelected: null,
    };
  },
  methods: {
    updateTime() {
      this.$emit('input',
          (this.hourSelected + (this.periodSelected == 'AM' ? 0 : 12)) + ':' +
          this.minuteSelected);
    },
  },
  beforeMount() {
    if (this.startWithCurrent) {
      const semiFormattedTime = new Date().toLocaleTimeString().split(/\:| /);
      this.hourSelected = parseInt(semiFormattedTime[0]);
      this.minuteSelected = semiFormattedTime[1];
      this.periodSelected = semiFormattedTime[3];

      this.updateTime();
    }
  },
};
</script>

<style scoped>
    .foodalert .custom-select {
        background: unset;
    }
</style>
