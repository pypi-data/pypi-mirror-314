<template>
  <div id="app">
    <byjove-app :appsettings="appsettings">
      <app-nav></app-nav>
      <template v-slot:footer>
        <router-link to="/about">{{ appsettings.appTitle }} {{ appsettings.version }}</router-link>
        <div>
          <br />
          <a href="/">View Desktop Site</a>
        </div>
      </template>
    </byjove-app>
  </div>
</template>

<script>
import {ByjoveApp} from 'byjove'
import AppNav from './components/AppNav.vue'
import appsettings from './appsettings'

export default {
    name: 'app',
    components: {
        ByjoveApp,
        AppNav,
    },
    data() {
        return {
            appsettings: appsettings,
        }
    },
}
</script>

<style>

/******************************
 * main app layout
******************************/

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.main-container {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
.page-content {
    flex: 1;
    padding: 0.5rem 1rem 0.5rem 0.5rem;
}
.footer {
    text-align: center;
}

/******************************
 * general stuff
******************************/

h1 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
h2 {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

/******************************
 * root-user
******************************/

[role=menuitem].root-user {
    background-color: red;
}

/******************************
 * model-index
******************************/

.model-index .menu {
    margin-bottom: 1rem;
}

.model-index .menu-list li {
    border-bottom: 1px solid #4a4a4a;
}

.model-index .menu-list li:last-child {
    border: 0px;
}

/******************************
 * model-crud
******************************/

.model-crud .menu {
    margin-bottom: 1rem;
}

.model-crud .menu-list li {
    border-bottom: 1px solid #4a4a4a;
}

.model-crud .menu-list li:last-child {
    border: 0px;
}

</style>
