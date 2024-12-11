<template>
  <byjove-model-crud model-name="Customer"
                     :mode="mode"
                     @refresh="record => { customer = record }"
                     @save="save"
                     :allow-edit="false">

    <b-field grouped>
      <b-field label="Name" expanded>
        <b-input v-if="mode == 'creating' || mode == 'editing'"
                 v-model="customer.name">
        </b-input>
        <span v-if="mode == 'viewing' || mode == 'deleting'">
          {{ customer.name }}
        </span>
      </b-field>

      <b-button v-if="mode == 'viewing'"
                type="is-primary"
                tag="router-link"
                :to="`/customers/${customer.uuid}/edit`"
                icon-left="edit">
        Edit Customer
      </b-button>
    </b-field>

    <div v-if="mode == 'creating' || mode == 'editing'">
      <b-field label="Street">
        <b-input v-model="customer.address_street"></b-input>
      </b-field>

      <b-field label="Street 2">
        <b-input v-model="customer.address_street2"></b-input>
      </b-field>

      <b-field label="City">
        <b-input v-model="customer.address_city"></b-input>
      </b-field>

      <b-field grouped>
        <b-field label="State" expanded>
          <b-input v-model="customer.address_state"></b-input>
        </b-field>
        <b-field label="Zipcode" expanded>
          <b-input v-model="customer.address_zipcode"></b-input>
        </b-field>
      </b-field>
    </div>

    <b-field v-if="mode == 'viewing' || mode == 'deleting'"
             label="Physical Address">
      {{ customer.default_mailing_address }}
    </b-field>

    <b-field label="Phone Number">
      <b-input v-if="mode == 'creating' || mode == 'editing'"
               v-model="customer.phone_number">
      </b-input>
      <span v-if="mode == 'viewing' || mode == 'deleting'">
        {{ customer.phone_number }}
      </span>
    </b-field>

    <b-field label="Email Address">
      <b-input v-if="mode == 'creating' || mode == 'editing'"
               v-model="customer.email_address">
      </b-input>
      <span v-if="mode == 'viewing' || mode == 'deleting'">
        {{ customer.email_address }}
      </span>
    </b-field>

    <b-field label="Notes">
      <b-input v-if="mode == 'creating' || mode == 'editing'"
               v-model="customer.default_note"
               type="textarea" rows="2">
      </b-input>
      <span v-if="mode == 'viewing' || mode == 'deleting'">
        {{ customer.default_note }}
      </span>
    </b-field>

  </byjove-model-crud>
</template>

<script>
import {ByjoveModelCrud} from 'byjove'

export default {
    name: 'Customer',
    props: {
        mode: String,
    },
    components: {
        ByjoveModelCrud,
    },
    data: function() {
        return {
            customer: {},
        }
    },
    methods: {
        save(url) {
            let params = {
                id: this.customer.id,
                name: this.customer.name,
                address_street: this.customer.address_street,
                address_street2: this.customer.address_street2,
                address_city: this.customer.address_city,
                address_state: this.customer.address_state,
                address_zipcode: this.customer.address_zipcode,
                phone_number: this.customer.phone_number,
                email_address: this.customer.email_address,
                default_note: this.customer.default_note,
            }
            this.$http.post(url, params).then(response => {
                this.$router.push('/customers/' + response.data.data.uuid)
            })
        },
    },
}
</script>
