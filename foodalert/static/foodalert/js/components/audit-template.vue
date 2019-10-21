<template>
     <div class="audit-parent">
       <b-navbar class="mx-auto" style="height: 64px;">
          <b-navbar-brand class="pl-2 pb-2">
            <img :src="require('../../img/food-alert-logo.svg')"
                  alt="UW Food Alert Logo" height="22"
                  >
          </b-navbar-brand>
        </b-navbar>
        <!-- search and filter feature -->
        <b-row class="ml-1">
          <b-col id="filter-bar" sm="4" lg="4">
            <b-input
              id="search-filter" type="search"
              class="mr-3" v-model="search"
              placeholder="Search by netID, event name">
            </b-input> 
          </b-col>
          <b-col id="time-filter" sm="3" lg="4">
            <label for="from">
              From
            </label>
            <b-input id="from" type="date" class="mr-2"> </b-input>
            <label for="to"> 
              to
            </label>
            <b-input id="to" type="date"></b-input>
            <button class="ml-2">
              Filter
            </button>
          </b-col>
        </b-row>
        <p></p>
        <!-- audit log table -->
        <b-table hover
          :sort-by.sync="sortBy"
          :items="items" 
          :fields="fields">
          <template v-slot:cell(food.served)="row">
            Food served: {{ row.value }}
            <br/>
            Ends at: {{ row.item['time.end'] }}
            <br/>
            Food Contains: {{ row.item['food.allergens']}}
            <br/>
            <div v-if="row.item.bring_container">
                Please bring a container!
            </div>
            <br/>
            <b-button @click="getUpdates(row.item)" class="toggle-button float-right" 
              variant="link">
              {{row.detailsShowing ? 'Hide' : 'Show'}} Updates
            </b-button>
          </template>

          <template v-if="items.length > 0" v-slot:head(food.served)="data">
            <span>{{data.label}}</span>
            <b-button
              id="show-all"
              @click="items.forEach(function(el, arr){getUpdates(el, showAll)});
              showAll = !showAll" class="toggle-button" variant="link">
              {{showAll ? 'Expand' : 'Collapse'}} All Updates
            </b-button>
          </template>

          <template v-slot:row-details="row">
            <b-card v-if="row.item.updates && row.item.updates.length > 0" class="message-details">
                <b-row>
                    <b-col class="col-5">
                      <strong>Time created</strong>
                    </b-col>
                    <b-col>
                      <strong>Update</strong>
                    </b-col>
                </b-row>
                <div v-for="(update, index) in row.item.updates" :key="index">
                  <b-row>
                    <b-col class="col-5">
                      {{ row.item.updates[index].created_time }}
                    </b-col>
                    <b-col>
                      {{ row.item.updates[index].update_text }}
                    </b-col>
                  </b-row>
                </div>
            </b-card>
          </template>
        </b-table>
        <nav role="navigation" aria-label="Search results pages">
          <b-button @click="requestLogs">See More</b-button>
        </nav>
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
      sortBy: 'unformatted_time_created',
      showAll: true,
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
      url: "/notification/?page=1"
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
    getUpdates(item, showAll) {
      const id = item.id;
      // make axios request to get updates and display accordingly
      if(!item.updates){
        axios.get('/updates/?parent_notification=' + id)
          .then((response) => {
            let context = [];
            let length = response.data.length;
            if (length === 0){
              if(showAll !== undefined) {
                item._showDetails = showAll;
              } else {
                item._showDetails = !item._showDetails;
              }
            } else {
              for(let i = 0; i < length; i++){
                let updateID = response.data[i].id;
                axios.get('/updates/' + updateID + '/')
                  .then((response) => {
                    let updateText = response.data.text;
                    let createdTime = new Date(response.data.created_time).toDateString() +
                      ' ' + new Date(response.data.created_time).toLocaleTimeString('en-US');
                    
                    let innerContext = {
                      'created_time': createdTime,
                      'update_text': updateText,
                    }
                    context.push(innerContext);
                    item['updates'] = context;

                    //toggle only when all updates have been retrieved
                    if(i === length - 1) {
                      setTimeout(() => {
                        if(showAll !== undefined) {
                          item._showDetails = showAll;
                        } else {
                          item._showDetails = !item._showDetails;
                        }
                      }, 100);
                    }
                  })
                  .catch(console.log);
              }
            }
          })
          .catch(console.log);
      } else {
        if(showAll !== undefined) {
          item._showDetails = showAll;
        } else {
          item._showDetails = !item._showDetails;
        }
      }
    },
    requestLogs(search) {
      const headers = {
        'Content-Type': 'application/json',
      };

      this.items = [];
      
      let url = this.url

      if (search) {
        this.url = url + '?search=' + search;
      }

      axios.get(url, {headers})
          .then((response) => {
            this.url = response.data.next
            
            for (let i = 0; i < response.data.results.length; i++) {
            // Iterate through each detail
              axios.get('/notification/' + response.data.results[i].id + '/', {headers})
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

      // store unformatted time for sorting
      log['unformatted_time_created'] = log.time.created;

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

      // add _showDetails to each item to use to toggle details
      log['_showDetails'] = false;

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
    #filter-bar, #time-filter {
      display: flex;
      align-items: center;
      margin-left: 5px;
    }

    .message-details {
      margin-left: 38%;
      margin-right: 10%;
    }

    .audit-parent .toggle-button {
      font-size: 11pt;
      padding: 1px;
      float: right;
    }                                                                                           
</style>
