<template>
    <audit-template
        :items="this.filteredItems"
        :years="this.years"
        :months="this.months"
        @export="this.exportTable"
        @updateMonth="this.updateMonth"
        @updateYear="this.updateYear"
        >
    </audit-template>
</template>

<script type="text/javascript">
import AuditTemplate from './audit-template.vue';
import axios from 'axios';
import flatten from 'flat';

export default {
  components: {
    'audit-template': AuditTemplate,
  },
  mounted() {
    this.requestUpdates();
    this.requestLogs();
  },
  data() {
    return {
      items: [],
      updates: [],
      years: ['All'],
      months: ['All'],
      selectedMonth: 'All',
      selectedYear: 'All',
    };
  },
  methods: {
    addItems(response){
      const log = response.data;

      console.log(log)

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
      
      //format food qualifications text
      log.food.qualifications = log.food.qualifications.join(' / ');

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
    requestLogs() {
      const headers = {
        'Content-Type': 'application/json',
      };

      axios.get('/notification/', {headers})
        .then((response) => {
          for (let i = 0; i < response.data.length; i++) {
            // Iterate through each detail
            axios.get('/notification/' + response.data[i].id + '/', {headers})
              .then(this.addItems)
              .catch(console.log);
          }
          this.$emit('requestComplete');
        })
        .catch((error) => this.showErrorPage(error.response,
            'a-audit'));
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
    exportTable() {
      // Write the column names as the first line in the result
      const keys = Object.keys(this.items[0]);
      let result = '';

      result += keys.join(',');
      result += '\n';

      // Iterate over each row and append them with comma seperation
      this.filteredItems.forEach(function(item) {
        keys.forEach(function(key) {
          if (item[key] === '') {
            result += 'null';
          } else {
            result += item[key];
          }

          result += ',';
        });
        result = result.slice(0, -1);
        result += '\n';
      });

      // Define the content of our csv & encode the URI
      const csv = 'data:text/csv;charset=utf-8,' + result;
      const data = encodeURI(csv);

      // Programmatically make a link to download the csv and click it
      const link = document.createElement('a');

      link.setAttribute('href', data);
      link.setAttribute('download', 'auditlog.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    },
    updateMonth(value) {
      this.selectedMonth = value;
    },
    updateYear(value) {
      this.selectedYear = value;
    },
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
