<template>
  <byjove-home :appsettings="appsettings"
               :force-login="true">
  </byjove-home>
</template>

<script>
import appsettings from '../appsettings'
import {ByjoveHome} from 'byjove'

export default {
    name: 'home',
    components: {
        ByjoveHome,
    },
    data() {
        return {
            appsettings: appsettings,
        }
    },
}
</script>
