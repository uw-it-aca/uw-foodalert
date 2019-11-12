<template>
    <generic-page pageSizeClass='full-container'>
        <template #heading>Audit Log</template>
        <template #body>
            <div class="audit-parent">
                <!-- search and filter feature -->
                <b-row class="mt-1">
                <b-col id="filter-bar" sm="4" lg="4">
                    <b-input
                    id="search-filter" type="search"
                    v-model="search"
                    placeholder="Filter by sender's UW NetID or name of event"
                    aria-label="filter results by uw netid or name of event"/>
                </b-col>
                </b-row>
                <br/>

                <!-- audit log table -->
                <b-table
                :sort-by.sync="sortBy"
                :sort-desc.sync="sortDesc"
                :items="items"
                :fields="fields">
                <template  v-slot:cell(food.served)="row">
                    <div v-if="row.item['netID']!=''">
                      Food served: {{ row.value }}
                      <br/>
                      Ends at: {{ row.item['time.end'] }}
                      <div v-if="row.item['food.allergens']">
                        Food Contains: {{ row.item['food.allergens'] }}
                      </div>
                      <div v-if="row.item.bring_container">
                        Please bring a container!
                      </div>
                    </div>
                    <div v-else>
                      Update: {{row.value}}
                    </div>
                </template>
                <template  v-slot:cell(ended)="row">
                  <div v-if="row.value">
                    yes
                  </div>
                  <div v-else-if="row.value === false">
                    no
                  </div>
                </template>
                </b-table>

                <!-- pagination -->
                <nav id="pagination" role="navigation"
                  aria-label="Search results page navigation">
                  <ul id="btn-nav" class="list-unstyled">
                    <li>
                      <b-button id="prev-btn" variant="link"
                        :disabled="!prevPage" aria-label="Previous page"
                        @click="currentPage--; requestLogs()">
                            &lt;Previous
                      </b-button>
                    </li>
                    <!-- anchor first page -->
                    <li>
                      <b-button variant="link"
                        aria-label="navigate to page one"
                        @click="currentPage=1; requestLogs()"
                        v-bind:class="{'active': (1 === currentPage)}">
                        1
                      </b-button>
                    </li>
                    <li
                      v-bind:class="{'d-none':
                      (currentPage<=3 || totalPages<=3)}">
                      ...
                    </li>
                    <li v-for="page in pages" :key="page">
                      <b-button v-bind:class="{'active':(page===currentPage)}"
                        variant="link" :aria-label="'navigate to page '+page"
                        @click="currentPage=page; requestLogs()">
                        {{ page }}
                      </b-button>
                    </li>
                    <li
                      v-bind:class="{'d-none':
                      (currentPage>=totalPages-2 || totalPages<=3)}">
                        ...
                    </li>
                    <!-- anchor last page -->
                    <li>
                      <b-button variant="link"
                        :aria-label="'navigate to page ' + totalPages"
                        @click="currentPage=totalPages; requestLogs()"
                        v-bind:class="{'active': (totalPages === currentPage)}">
                        {{totalPages}}
                      </b-button>
                    </li>
                    <li>
                      <b-button id="next-btn" variant="link"
                        :disabled="!nextPage"
                        aria-label="Next page"
                        @click="currentPage++; requestLogs()">
                        Next&gt;
                      </b-button>
                    </li>
                  </ul>
                  <small id="num-results" aria-live="polite"></small>
                </nav>
            </div>
        </template>
     </generic-page>
</template>

<script type="text/javascript">
import GenericPage from '../../components/generic-page.vue';
import axios from 'axios';
import flatten from 'flat';

export default {
  components: {
    'generic-page': GenericPage,
  },
  data() {
    return {
      items: [],
      search: '',
      sortBy: 'id',
      sortDesc: true,
      fields: [
        {key: 'netID', label: 'UW NetID'},
        {key: 'event', label: 'Event'},
        {key: 'location', label: 'Location'},
        {key: 'food.qualifications', label: 'Food Qualifications'},
        {key: 'time.created', label: 'Time Created'},
        {key: 'food.served', label: 'Message'},
        {key: 'ended', label: 'Host ended event'},
      ],
      req: null,
      baseURL: '/notification/',
      currentPage: null,
      totalPages: null,
      nextPage: null,
      prevPage: null,
      pages: [],
    };
  },
  watch: {
    search(newVal, oldVal) {
      if (this.req !== null) {
        clearTimeout(this.req);
      }

      this.req = setTimeout(() => {
        let url = this.baseURL;

        if (newVal !== '') {
          url += '?search=' + newVal;
        } else {
          // navigte back to first page
          this.currentPage = 1;
          url += '?page=1';
        }

        this.requestLogs(url);
      }, 500);
    },
  },
  methods: {
    updatePagination(response) {
      if (!response.data.previous.page && !response.data.next.page) {
        // if only one page do not display buttons
        document.getElementById('btn-nav').classList.add('d-none');
      } else {
        document.getElementById('pagination').classList.remove('d-none');
        this.prevPage = response.data.previous.page;
        this.nextPage = response.data.next.page;
        // add specific page buttons
        this.totalPages = Math.ceil(
            response.data.count / response.data.pagesize);
        this.pages = [];

        if (this.prevPage && this.prevPage !== 1) {
          this.pages.push(this.prevPage);
        }

        if (this.currentPage !== 1 && this.currentPage !== this.totalPages) {
          this.pages.push(this.currentPage);
        }

        if (this.nextPage && this.nextPage !== this.totalPages) {
          this.pages.push(this.nextPage);
        }
      }

      // Fill in result text
      const results = document.getElementById('num-results');
      const x = response.data.pagesize * (this.currentPage - 1) + 1;
      const y = x + response.data.results.length - 1;


      results.innerText = x + '-' + y + ' of ' +
        response.data.count + ' results';
    },
    requestLogs(url) {
      const headers = {
        'Content-Type': 'application/json',
      };

      this.items = [];

      // default to load page 1 if not url passed
      if (!url) {
        url = this.baseURL + '?page=' + this.currentPage;
      }

      axios.get(url, {headers})
          .then((response) => {
            let resp;

            if (url.includes('?page=')) {
              resp = response.data.results;

              this.updatePagination(response);
            } else {
              document.getElementById('pagination').classList.add('d-none');
              resp = response.data;
            }

            for (let i = 0; i < resp.length; i++) {
            // Iterate through each notification detail
              axios.get('/notification/' + resp[i].id + '/', {headers})
                  .then(this.addItems)
                  .catch((error) => this.showErrorPage(error.response,
                      'a-audit'),
                  );
            }
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

      // format food qualifications and allergens
      log.food.qualifications = log.food.qualifications.join(', ');
      log.food.allergens = log.food.allergens.join(', ');

      // Flatten the row and rename columns
      const flat = flatten(log);

      // Add the item to our audit logs
      this.items.push(flat);

      this.requestUpdates(log.id);
    },
    requestUpdates(id) {
      const headers = {
        'Content-Type': 'application/json',
      };

      axios.get('/updates/?parent_notification=' + id, {headers})
          .then((response) => {
            const data = response.data;

            for (let i = 0; i < data.length; i++) {
              axios.get('/updates/' + data[i].id + '/', {headers})
                  .then((response) => {
                    const update = response.data;
                    const calc = id - (i+1)/(data.length +1);
                    let ret = {
                      'id': calc,
                      'netID': '',
                      'location': '',
                      'event': '',
                      'time.created':
                          new Date(update.created_time).toDateString() + ' ' +
                          new Date(update.created_time)
                              .toLocaleTimeString('en-US'),
                      'time.ended': '',
                      'food.served': update.text,
                      'food.allergens': '',
                      'bringContainers': '',
                      'host.netID': '',
                      'host.userAgent': '',
                      'ended': '',
                      '_rowVariant': 'update',
                      '_showDetails': false,
                    };

                    ret = flatten(ret);
                    this.items.push(ret);
                  });
            }
          })
          .catch((error) => this.showErrorPage(error.response,
              'a-audit'));
    },
  },
  beforeMount() {
    this.currentPage = 1;
    this.requestLogs(this.baseURL + '?page=1');
  },
};
</script>

<style>
    .audit-parent #pagination {
      text-align: center;
      margin-top: 30px;
    }
    .audit-parent tr.table-update td[aria-colindex="1"],
    .audit-parent tr.table-update td[aria-colindex="2"],
    .audit-parent tr.table-update td[aria-colindex="3"],
    .audit-parent tr.table-update td[aria-colindex="4"]{
      border-top: none;
    }
    .audit-parent tbody tr:not(.table-update){
      border-top: solid 2px gray;
    }
    #btn-nav {
      display: flex;
      justify-content: center;
    }

    #btn-nav .active {
      border: solid 1px black;
    }
</style>
