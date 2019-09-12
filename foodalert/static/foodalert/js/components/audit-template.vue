<template>
     <div class="audit-parent">
        <b-row>
          <b-col id = "filter-bar" sm="12" md="8" lg="6">
            <b-input
              id="search-filter" type="search"
              class="mr-3 ml-2" v-model="search">
            </b-input>
            <b-dropdown text="Year"
              v-on:click.native="setYear($event)" class="mr-1">
              <b-dropdown-item v-for="year in this.years" :key="year">
                {{ year }}
              </b-dropdown-item>
            </b-dropdown>
            <b-dropdown text="Month" v-on:click.native="setMonth($event)">
              <b-dropdown-item v-for="month in this.months" :key="month">
                {{ month }}
              </b-dropdown-item>
            </b-dropdown>
          </b-col>
        </b-row>
         <p></p>
         <b-table @click="showDetails" hover :items="items" :fields="fields">
            <template v-slot:cell(food.served)="row">
              {{ row.value }}
              <b-button @click="row.toggleDetails" class="float-right" variant="link">
                Show {{row.detailsShowing ? 'Less' : 'More'}}
              </b-button>
            </template>

            <template v-slot:row-details="row">
              <b-card class="message-details">
                <b-row>
                  <b-col class="text-sm-left">
                    <strong>Event:</strong> {{row.item.event }}
                  </b-col>
                </b-row>
                <b-row>
                  <b-col class="text-sm-left">
                    <strong>Location:</strong> {{row.item.location }}
                  </b-col>
                </b-row>
                <b-row>
                  <b-col class="text-sm-left">
                    <strong>End time:</strong> {{ row.item['time.end'] }}
                  </b-col>
                </b-row>
                <b-row>
                  <b-col class="text-sm-left">
                    <strong>May Contain:</strong> {{ row.item['food.allergens'] }}
                  </b-col>
                </b-row>
                <b-row>
                  <b-col class="text-sm-left">
                    <strong>Bring Container:</strong> {{ row.item['bring_container'] }}
                  </b-col>
                </b-row>
              </b-card>
            </template>
         </b-table>
     </div>
</template>

<script type="text/javascript">
import axios from 'axios';
import flatten from 'flat';
export default {
  data() {
    return {
      items: [],
      updates: [],
      years: ['All'],
      months: ['All'],
      selectedMonth: 'All',
      selectedYear: 'All',
      search: '',
      fields: [
        {key: 'netID', label: 'netID'},
        {key: 'event', label: 'Event'},
        {key: 'location', label: 'Location'},
        {key: 'food.qualifications', label: 'Food Qualifications'},
        {key: 'time.created', label: 'Time Created'},
        {key: 'food.served', label: 'Message'},
        {key: 'ended', label: 'Event Ended'}
      ],
      req: null,
    };
  },
  watch: {
    search(newVal, oldVal) {
      if (this.req !== null) {
        clearTimeout(this.req);
      }

      this.req = setTimeout(() => {
        this.requestLogs(newVal);
      }, 500);
    },
  },
  methods: {
    showDetails(items) {
      console.log("show details");
      console.log(items);
    },
    requestLogs(search) {
      const headers = {
        'Content-Type': 'application/json',
      };

      this.items = [];

      let url = '/notification/';

      if (search) {
        url = url + '?search=' + search;
      }

      axios.get(url, {headers})
          .then((response) => {
            for (let i = 0; i < response.data.length; i++) {
            // Iterate through each detail
              axios.get('/notification/' + response.data[i].id + '/', {headers})
                  .then(this.addItems)
                  .catch((error) => this.showErrorPage(error.response,
                      'a-audit')
                  );
            }

            this.$emit('requestComplete');
          })
          .catch((error) => this.showErrorPage(error.response,
              'a-audit'));
    },
    addItems(response) {
      const log = response.data;

      // Make datetimes readable
      log.time.created = new Date(log.time.created).toDateString() +
        ' ' + new Date(log.time.created).toLocaleTimeString('en-US');
      log.time.end = new Date(log.time.end).toDateString() +
        ' ' + new Date(log.time.end).toLocaleTimeString('en-US');
      // Add the year and month to respective arrays for sorting
      const year = log.time.created.substring(11, 15);
      const month = log.time.created.substring(4, 7);

      if (!this.years.includes(year)) {
        this.years.push(year);
      }

      if (!this.months.includes(month)) {
        this.months.push(month);
      }

      // format food qualifications and allergens
      log.food.qualifications = log.food.qualifications.join(', ');
      log.food.allergens = log.food.allergens.join(', ');

      // Flatten the row and rename columns
      const flat = flatten(log);

      // Add the item to our audit logs
      this.items.push(flat);

      // Gather all updates to this corresponding item
      const itemUpdates = this.updates.filter(function(update) {
        return (update.parent_notification === log.id);
      });

      // Add each update of this item to the log
      for (let j = 0; j < itemUpdates.length; j++) {
        this.items.push(this.updateToLog(itemUpdates[j]));
      }
    },
    requestUpdates() {
      const headers = {
        'Content-Type': 'application/json',
      };

      axios.get('/updates/', {headers})
          .then((response) => {
            const data = response.data;

            for (let i = 0; i < data.length; i++) {
              this.updates.push(data[i]);
            }
          })
          .catch((error) => this.showErrorPage(error.response,
              'a-audit'));
    },
    updateToLog(update) {
      const ret = {
        'location': '',
        'event': '',
        'time.created': new Date(update.created_time).toDateString() +
          ' ' + new Date(update.created_time).toLocaleTimeString('en-US'),
        'time.ended': '',
        'food.served': '',
        'food.amount': update.text,
        'food.allergens': '',
        'bringContainers': '',
        'host.netID': '',
        'host.userAgent': '',
        'ended': '',
        '_rowVariant': 'update',
      };

      return ret;
    },
    updateMonth(value) {
      this.selectedMonth = value;
    },
    updateYear(value) {
      this.selectedYear = value;
    },
    setMonth(event) {
      this.updateMonth(event.target.innerText);
    },
    setYear(event) {
      this.updateYear(event.target.innerText);
    },
  },
  mounted() {
    this.requestUpdates();
    this.requestLogs();
  },
  computed: {
    filteredItems() {
      let logs = this.items;
      const year = this.selectedYear;
      const month = this.selectedMonth;

      if (year !== 'All') {
        logs = logs.filter(function(log) {
          return log['time.created'].includes(year);
        });
      }

      if (month !== 'All') {
        logs = logs.filter(function(log) {
          return log['time.created'].includes(month);
        });
      }

      return logs;
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

    .message-details {
      margin-left: 50%;
    }
</style>
