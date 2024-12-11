<template>
  <byjove-login :appsettings="appsettings"></byjove-login>
</template>

<script>
import appsettings from '@/appsettings'
import {ByjoveLogin} from 'byjove'

export default {
    name: 'Login',
    components: {
        ByjoveLogin,
    },
    data() {
        return {
            appsettings: appsettings,
        }
    },
}
</script>
