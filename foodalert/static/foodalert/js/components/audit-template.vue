<template>
     <div class="audit-parent">
         <div id="filter-bar">
           <div class="d-flex">
              <b-input
                id="search-filter" type="search"
                class="mr-3" v-model="search">
              </b-input>
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
            </div>
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
    requestLogs: Function,
  },
  data() {
    return {
      search: '',
      fields: [
        {key: 'netID', label: 'netID'},
        {key: 'event', label: 'Event'},
        {key: 'location', label: 'Location'},
        {key: 'food.qualifications', label: 'Food Qualifications'},
        {key: 'time.created', label: 'Time Created'},
        {key: 'food.served', label: 'Message'},
      ],
      req: null,
    };
  },
  watch: {
    search(newVal, oldVal) {
      if(this.req != null){
        clearTimeout(this.req);
      }
      this.req = setTimeout(() => {
        this.requestLogs(newVal)
      }, 1000);
    },
  },
  methods: {
    setMonth(event) {
      this.$emit('updateMonth', event.target.innerText);
    },
    setYear(event) {
      this.$emit('updateYear', event.target.innerText);
    },
  },
};
</script>

<style>
    .audit-parent .table-update td {
        border-top : 0;
    }

    #filter-bar {
      display: flex;
      justify-content: space-between;
    }
</style>
