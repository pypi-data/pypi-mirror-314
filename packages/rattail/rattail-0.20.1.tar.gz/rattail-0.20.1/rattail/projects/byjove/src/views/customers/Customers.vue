<template>
  <byjove-model-index model-name="Customer"
                      :api-index-sort="{field: 'name', dir: 'asc'}"
                      :api-index-filters="customerFilters">

    <b-field>
      <b-input v-model="searchTerm"
               icon="search"
               icon-clickable
               @icon-click="performSearch"
               icon-right="times-circle"
               icon-right-clickable
               @icon-right-click="cancelSearch"
               @keydown.native="searchTermKeydown">
      </b-input>
    </b-field>

  </byjove-model-index>
</template>

<script>
import {ByjoveModelIndex} from 'byjove'

export default {
    name: 'Customers',
    components: {
        ByjoveModelIndex,
    },
    data() {
        return {
            searchTerm: null,
            customerFilters: [],
        }
    },
    methods: {

        searchTermKeydown(event) {
            if (event.which == 13) { // ENTER
                if (this.searchTerm && this.searchTerm.length) {
                    this.performSearch()
                } else {
                    this.customerFilters = []
                }
            }
        },

        performSearch() {
            this.customerFilters = [
                {field: 'name', op: 'ilike', value: `%${this.searchTerm}%`},
            ]
        },

        cancelSearch() {
            this.searchTerm = null
            this.customerFilters = []
        },

    },
}
</script>
