<template>
  <div id="app">
    <v-app style="min-height: 100vh">
      <v-navigation-drawer permanent expand-on-hover clipped mini-variant app v-if='$store.state.isAuthenticated'>
        <v-list nav dense active-class="deep-purple--text text--accent-4">
          <v-list-item link to="/flat">
            <v-list-item-icon>
              <v-icon>home</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Квартира</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item link to="/car">
            <v-list-item-icon>
              <v-icon>directions_car_filled</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Автомобиль</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item link to="/settings">
            <v-list-item-icon>
              <v-icon>settings</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Настройки</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-group prepend-icon="person">
            <template v-slot:activator>
              <v-list-item-title>Пользователь</v-list-item-title>
            </template>
            <v-list-item @click="$store.dispatch('logout')"
              ><v-list-item-icon>
                <v-icon>logout</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Выйти</v-list-item-title>
              </v-list-item-content></v-list-item
            >
          </v-list-group>
        </v-list>
      </v-navigation-drawer>

      <v-app-bar app clipped-left>
        <v-app-bar-title>Parrotdocx</v-app-bar-title>
      </v-app-bar>
      <v-main class="m-2">
        <router-view></router-view>
      </v-main>
      <v-dialog v-model="showErrorModal" max-width="300">
        <v-card>
          <v-card-title class="text-h5"> Ошибка </v-card-title>

          <v-card-text>
            {{ modalContent }}
          </v-card-text>

          <v-card-actions>
            <v-btn color="green darken-1" text @click="showErrorModal = false">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import ErrorModal from "./plugins/ErrorModal";

export default {
  name: "app",
  data() {
    return {
      showErrorModal: false,
      modalContent: null,
    };
  },
  async beforeMount() {
    await this.$store.dispatch('getSettings');
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
  },
};
</script>
<style>
#app {
}
a {
  text-decoration: none !important;
}
</style>
