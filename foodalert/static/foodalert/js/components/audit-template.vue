<template>
     <div class="audit-parent">
         <div>
            <b-dropdown text="Year" v-on:click.native="setYear($event)">
              <b-dropdown-item v-for="year in this.years" :key="year">
                {{ year }}
              </b-dropdown-item>
            </b-dropdown>
            <b-dropdown text="Month" v-on:click.native="setMonth($event)">
              <b-dropdown-item v-for="month in this.months" :key="month">
                {{ month }}
              </b-dropdown-item>
            </b-dropdown>
            <b-button style="float: right" @click="exportTable">
              Export
            </b-button>
         </div>
         <p></p>
         <b-table hover :items="items" :fields="fields"></b-table>
     </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
    },
    years: {
      type: Array,
    },
    months: {
      type: Array,
    },
  },
  methods: {
    exportTable() {
      this.$emit('export');
    },
    setMonth(event) {
      this.$emit('updateMonth', event.target.innerText);
    },
    setYear(event) {
      this.$emit('updateYear', event.target.innerText);
    },
  },
  data() {
    return {
      fields: [
        'host.netID',
        'location',
        'event',
        'time.created',
        'time.ended',
        'food.served',
        'food.amount',
        'food.allergens',
        'bringContainers',
        'host.userAgent',
        'ended',
      ],
    };
  },
};
</script>

<style>
    .audit-parent .table-update td {
        border-top : 0;
    }
</style>
