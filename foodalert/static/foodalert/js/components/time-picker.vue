<template>
  <div class="time-picker-root">
    <b-input-group :id="timeID" :aria-labelledby="labelbyID"
      :aria-describedby="timeID + '-feedback'">
        <b-form-select v-model="hourSelected"
            aria-label="Enter hours" :state="(hourSelected == '--' && showInvalidTimeError) ? false : null"
            :options="hourOptions" size="lg"
            @change="updateTime()">
        </b-form-select>
        <b-form-select v-model="minuteSelected"
            aria-label="Enter minutes" :state="(minuteSelected == '--' && showInvalidTimeError) ? false : null"
            :options="minuteOptions" size="lg"
            @change="updateTime()">
        </b-form-select>
        <b-form-select v-model="periodSelected"
            aria-label="Enter AM/PM" :state="(periodSelected == '--' && showInvalidTimeError) ? false : null"
            :options="periodOptions"
            size="lg"
            @change="updateTime()">
        </b-form-select>
    </b-input-group>
    <b-form-invalid-feedback :id="timeID + '-feedback'" role="alert" :state="formValidity">
      <div class="text-primary" v-if="endTimeBeforeCurrent">
        <slot name="timeBeforeWarning" style="font-size: 14px; font-weight: 800;">
        </slot>
      </div>
      <slot name="invalidTimeWarning" v-else-if="invalidTime && showInvalidTimeError">
      </slot>
    </b-form-invalid-feedback>
  </div>
</template>

<script>
export default {
  props: {
    value: String,
    timeID: String,
    startWithCurrent: Boolean,
    labelbyID: String,
    showInvalidTimeError: Boolean,
  },
  data() {
    const _hourOptions = Array(13);

    _hourOptions[0] = '--';

    for (let i = 1; i < _hourOptions.length; i++) {
      _hourOptions[i] = i;
    }

    const _minuteOptions = Array(61);

    _minuteOptions[0] = '--';

    for (let i = 1; i < _minuteOptions.length; i++) {
      _minuteOptions[i] = ((((i - 1) < 10) ? '0' : '') + (i - 1));
    }

    return {
      hourOptions: _hourOptions,
      minuteOptions: _minuteOptions,
      periodOptions: ['--', 'AM', 'PM'],
      hourSelected: null,
      minuteSelected: null,
      periodSelected: null,
    };
  },
  methods: {
    updateTime() {
      if (this.selectedTimeInDateTime == null) {
        this.$emit('input', null);
      } else {
        this.$emit(
          'input',
          this.selectedTimeInDateTime.getHours() + ':' + String(this.selectedTimeInDateTime.getMinutes()).padStart(2, '0')
        );
      }
    },
  },
  beforeMount() {
    if (this.startWithCurrent) {
      const semiFormattedTime = new Date().toLocaleTimeString().split(/:| /);

      this.hourSelected = parseInt(semiFormattedTime[0]);
      this.minuteSelected = semiFormattedTime[1];
      this.periodSelected = semiFormattedTime[3];

      this.updateTime();
    } else {
      this.hourSelected = this.minuteSelected = this.periodSelected = '--';
    }
  },
  computed: {
    invalidTime: function() {
      return this.hourSelected == '--' || this.minuteSelected == '--' || this.periodSelected == '--';
    },
    selectedTimeInDateTime: function() {
      if (!this.invalidTime) {
        const datetime = new Date();
        let hour = this.hourSelected;

        if (this.periodSelected === 'AM') {
          if (this.hourSelected === 12) {
            hour = 0;
          }
        } else {
          if (this.hourSelected !== 12) {
            hour += 12;
          }
        }
        datetime.setHours(hour, this.minuteSelected);

        return datetime;
      } else {
        return null;
      }
    },
    endTimeBeforeCurrent: function() {
      if (this.selectedTimeInDateTime == null) {
        return false;
      } else {
        return this.selectedTimeInDateTime <= new Date();
      } 
    },
    formValidity: function() {
      if (this.endTimeBeforeCurrent || (this.invalidTime && this.showInvalidTimeError)) {
        return false;
      } else {
        return null;
      }
    }
  },
};
</script>

<style scoped>
    .foodalert .custom-select {
        background: unset;
    }
</style>
