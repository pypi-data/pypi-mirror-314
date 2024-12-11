<template>
  <div class="about">
    <h1>About {{ appsettings.appTitle }}</h1>
    <h2>{{ appsettings.appTitle }} {{ appsettings.version }}</h2>
    <p>{{ appsettings.systemTitle }} {{ libVersions.system }}</p>
    <p v-for="name in packageNames" :key="name">
      {{ name }} {{ libVersions[name] }}
    </p>
    <br />
    <p>Please see <a href="https://rattailproject.org/" target="_blank">rattailproject.org</a> for more info.</p>
  </div>
</template>

<script>
import appsettings from '@/appsettings'

export default {
    name: 'About',
    data() {
        return {
            appsettings: appsettings,
            libVersions: {},
            packageNames: [],
            inited: false,
        }
    },
    created: function() {
        this.init()
    },
    watch: {
        '$store.state.session_established': 'init',
    },
    methods: {

        init() {
            // only need to init once
            if (this.inited) {
                return
            }

            // cannot init until session is established
            if (!this.$store.state.session_established) {
                return
            }

            // go ahead and fetch data, regardless of user level
            this.fetchData()

            // we did it!
            this.inited = true
        },

        fetchData() {
            this.$http.get('/api/about').then(response => {
                this.libVersions = response.data.packages
                this.packageNames = response.data.package_names
                this.libVersions.system = response.data.project_version
            })
        },
    },
}
</script>
