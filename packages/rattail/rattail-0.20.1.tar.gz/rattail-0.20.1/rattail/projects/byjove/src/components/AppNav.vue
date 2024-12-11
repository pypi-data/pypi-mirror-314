<template>
  <byjove-menu :appsettings="appsettings"
               :include-about-link="$store.state.user_is_admin">

    <b-dropdown-item aria-role="menuitem" has-link>
      <router-link to="/">Home</router-link>
    </b-dropdown-item>

    <b-dropdown-item v-if="$byjoveHasPerm('customers.list')"
                     aria-role="menuitem"
                     has-link>
      <router-link to="/customers/">Customers</router-link>
    </b-dropdown-item>

    <b-dropdown-item v-if="$byjoveHasPerm('products.list')"
                     aria-role="menuitem"
                     has-link>
      <router-link to="/products/">Products</router-link>
    </b-dropdown-item>

    <!-- <b-dropdown-item v-if="$byjoveHasPerm('ordering.list')" -->
    <!--                  aria-role="menuitem" -->
    <!--                  has-link> -->
    <!--   <router-link to="/ordering/">Ordering</router-link> -->
    <!-- </b-dropdown-item> -->

    <!-- <b-dropdown-item v-if="$byjoveHasPerm('receiving.list')" -->
    <!--                  aria-role="menuitem" -->
    <!--                  has-link> -->
    <!--   <router-link to="/receiving/">Receiving</router-link> -->
    <!-- </b-dropdown-item> -->

  </byjove-menu>
</template>

<script>
import {ByjoveMenu} from 'byjove'
import appsettings from '../appsettings'

export default {
    name: 'AppNav',
    components: {
        ByjoveMenu,
    },
    data() {
        return {
            appsettings: appsettings,
        }
    },
}
</script>
