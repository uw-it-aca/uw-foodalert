<template>
    <audit-template
        :items="this.filteredItems"
        :years="this.years"
        :months="this.months"
        @export="this.exportTable"
        @updateValue="this.updateValue"
        >
    </audit-template>
</template>

<script type="text/javascript">
    import AuditTemplate from './audit-template.vue';
    const axios = require('axios')
    var flatten = require('flat')

    export default {
        components: {
            'audit-template': AuditTemplate,
        },
        mounted() {
            this.requestLogs();
        },
        methods: {
            requestLogs() {
                var headers = {
                    'Content-Type': 'application/json',
                }
                axios.get('http://0.0.0.0:8000/notification/', {"headers": headers})
                    .then(response => {
                        console.log(response);
                        var data = response.data
                        for (var i = 0; i < data.length; i++) {
                            //Iterate over our logs row by row
                            var log = data[i]

                            //Make datetimes readable
                            log.time.created = new Date(log.time.created).toDateString() + " " + new Date(log.time.created).toLocaleTimeString('en-US');
                            log.time.ended = new Date(log.time.ended).toDateString() + " " + new Date(log.time.ended).toLocaleTimeString('en-US');

                            //Add the year and month to respective arrays for sorting
                            var year = log.time.created.substring(11, 15);
                            var month = log.time.created.substring(4, 7);
                            if (!this.years.includes(year)) {
                                this.years.push(year);
                            }
                            if (!this.months.includes(month)) {
                                this.months.push(month);
                            }

                            //Remove unnecessary fields
                            log.location = log.location.main;
                            delete log.id;
                            delete log.location.detail;
                            delete log.location.main;
                            delete log.foodServiceInfo.safeToShareFood;

                            //Flatten the row and rename columns
                            var flat = flatten(log);
                            flat["permitNumber"] = flat["foodServiceInfo.permitNumber"];
                            flat["hostID"] = flat["host.hostID"];
                            delete flat["foodServiceInfo.permitNumber"];
                            delete flat["host.hostID"];

                            this.items.push(flat);
                        }
                        this.filteredItems = this.items;
                    })
                    .catch(function (error) {
                        alert("There was an error processing the request");
                        console.log(error);
                    })
            },
            exportTable() {
                //Write the column names as the first line in the result
                var keys = Object.keys(this.items[0]);
                var result = '';
                result += keys.join(',');
                result += '\n';

                //Iterate over each row and append them with comma seperation
                this.filteredItems.forEach(function(item) {
                    keys.forEach(function(key) {
                        if (item[key] === "") {
                            result += 'null';
                        } else {
                            result += item[key];
                        }
                        result += ',';
                    });
                    result = result.slice(0, -1);
                    result += '\n';
                });

                //Define the content of our csv & encode the URI
                var csv = 'data:text/csv;charset=utf-8,' + result
                var data = encodeURI(csv);

                //Programmatically make a link to download the csv and click it
                var link = document.createElement('a');
                link.setAttribute('href', data);
                link.setAttribute('download', 'auditlog.csv');
                document.body.appendChild(link);
                link.click();
                link.remove();
            },
            updateValue(context, value) {
                if (context === "Year") {
                    this.selectedYear = value;
                } else if (context === "Month") {
                    this.selectedMonth = value;
                }
                this.filterLogs();
            },
            filterLogs() {
                var logs = this.items;
                var year = this.selectedYear;
                var month = this.selectedMonth;
                if (year != "All") {
                    logs = logs.filter(function(log) {
                        return log["time.created"].includes(year);
                    });
                }
                if (month != "All") {
                    logs = logs.filter(function(log) {
                        return log["time.created"].includes(month);
                    });
                }
                this.filteredItems = logs;
            }
        },
        data() {
            return {
                items: [test],
                filteredItems: [],
                years: ["All", "2017", "2019"],
                months: ["All", "Jan"],
                selectedMonth: "All",
                selectedYear: "All",
            }
        },
    }   
</script>

